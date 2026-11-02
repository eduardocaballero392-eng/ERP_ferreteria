"""CSV storage shared by all ERP modules."""
import csv
import os
import re
import tempfile
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.config import settings


_LOCKS: Dict[Path, threading.RLock] = {}
_LOCKS_GUARD = threading.Lock()
_IDENTIFIER_FIELDS = ("ruc", "documento", "telefono", "sku", "codigo", "clave", "numero_")


def _lock_for(path: Path) -> threading.RLock:
    with _LOCKS_GUARD:
        return _LOCKS.setdefault(path, threading.RLock())


def _convert_value(field: str, value: Optional[str]) -> Any:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    if field == "activo":
        return value.lower() in {"true", "1", "yes", "si", "sí"}
    is_phone = "telefono" in field.lower() or "phone" in field.lower()
    if not is_phone and field not in _IDENTIFIER_FIELDS and not field.startswith(_IDENTIFIER_FIELDS):
        if re.fullmatch(r"-?\d+", value):
            return int(value)
        if re.fullmatch(r"-?\d+\.\d+", value):
            return float(value)
    return value


def _normalize_legacy_fields(filename: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Expose the current API field names for older CSV column names."""
    if filename == "clientes.csv":
        record["nombres"] = record.get("nombres") or record.get("nombre")
        record["apellidos"] = record.get("apellidos") or record.get("apellido")
    elif filename == "ventas.csv":
        record["condicion_pago"] = record.get("condicion_pago") or record.get("condicion") or "CONTADO"
    return record


class CSVHandler:
    """CRUD adapter for a CSV file in the configured data directory."""

    def __init__(self, filename: str):
        self.filename = Path(filename).name
        if not self.filename.lower().endswith(".csv"):
            self.filename += ".csv"
        self.filepath = settings.DATA_DIR / self.filename
        self._lock = _lock_for(self.filepath)

    def read_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            if not self.filepath.exists():
                return []
            try:
                with self.filepath.open("r", encoding="utf-8-sig", newline="") as stream:
                    sample = stream.read(4096)
                    stream.seek(0)
                    try:
                        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
                    except csv.Error:
                        dialect = csv.excel
                    reader = csv.DictReader(stream, dialect=dialect)
                    if not reader.fieldnames:
                        return []
                    records = []
                    for row in reader:
                        record = {
                            field: _convert_value(field, value)
                            for field, value in row.items()
                            if field is not None
                        }
                        records.append(_normalize_legacy_fields(self.filename, record))
                    return records
            except (OSError, csv.Error) as error:
                raise RuntimeError(f"No se pudo leer {self.filename}: {error}") from error

    def read_by_id(self, record_id: int, id_column: str = "id") -> Optional[Dict[str, Any]]:
        return next((record for record in self.read_all() if str(record.get(id_column)) == str(record_id)), None)

    def find_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        return [record for record in self.read_all() if str(record.get(field)) == str(value)]

    def write_all(self, records: List[Dict[str, Any]]) -> bool:
        with self._lock:
            try:
                self.filepath.parent.mkdir(parents=True, exist_ok=True)
                fields: List[str] = []
                if self.filepath.exists():
                    with self.filepath.open("r", encoding="utf-8-sig", newline="") as source:
                        fields = next(csv.reader(source), [])
                for record in records:
                    for field in record:
                        if field not in fields:
                            fields.append(field)
                if not fields:
                    return True

                temp_path: Optional[str] = None
                try:
                    with tempfile.NamedTemporaryFile(
                        mode="w", encoding="utf-8-sig", newline="", dir=self.filepath.parent,
                        prefix=f".{self.filepath.name}.", suffix=".tmp", delete=False,
                    ) as temp_file:
                        temp_path = temp_file.name
                        writer = csv.DictWriter(temp_file, fieldnames=fields, extrasaction="ignore")
                        writer.writeheader()
                        writer.writerows(records)
                    os.replace(temp_path, self.filepath)
                finally:
                    if temp_path and os.path.exists(temp_path):
                        os.unlink(temp_path)
                return True
            except (OSError, csv.Error, TypeError, ValueError) as error:
                print(f"Error escribiendo {self.filename}: {error}")
                return False

    def append(self, record: Dict[str, Any]) -> bool:
        with self._lock:
            records = self.read_all()
            saved = dict(record)
            if not saved.get("id"):
                saved["id"] = max((int(float(item.get("id") or 0)) for item in records), default=0) + 1
            if not saved.get("created_at"):
                saved["created_at"] = datetime.now().isoformat()
            records.append(saved)
            return self.write_all(records)

    def update(self, record_id: int, updated_data: Dict[str, Any], id_column: str = "id") -> bool:
        with self._lock:
            records = self.read_all()
            for record in records:
                if str(record.get(id_column)) == str(record_id):
                    record.update(updated_data)
                    record["updated_at"] = datetime.now().isoformat()
                    return self.write_all(records)
            return False

    def delete(self, record_id: int, id_column: str = "id") -> bool:
        return self.update(record_id, {"activo": False}, id_column)

    def filter(self, conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            record for record in self.read_all()
            if all(str(record.get(key)) == str(value) for key, value in conditions.items())
        ]

    def exists(self) -> bool:
        return self.filepath.exists()

    def get_max_id(self, id_column: str = "id") -> int:
        return max((int(float(record.get(id_column) or 0)) for record in self.read_all()), default=0)


def get_csv_handler(filename: str) -> CSVHandler:
    return CSVHandler(filename)
