"""
Manejador de archivos CSV para almacenamiento de datos
"""
import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.config import settings


class CSVHandler:
    """Clase para manejar operaciones CRUD con archivos CSV"""
    
    def __init__(self, filename: str):
        """
        Inicializa el manejador de CSV
        
        Args:
            filename: Nombre del archivo CSV (ej: 'productos.csv')
        """
        self.filepath = settings.DATA_DIR / filename
        self.filename = filename
        
    def read_all(self) -> List[Dict[str, Any]]:
        """
        Lee todos los registros del CSV
        
        Returns:
            Lista de diccionarios con los datos
        """
        if not self.filepath.exists():
            return []
        
        try:
            df = pd.read_csv(self.filepath)
            # Reemplazar NaN con None
            df = df.where(pd.notna(df), None)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error leyendo {self.filename}: {str(e)}")
            return []
    
    def read_by_id(self, record_id: int, id_column: str = 'id') -> Optional[Dict[str, Any]]:
        """
        Lee un registro por ID
        
        Args:
            record_id: ID del registro
            id_column: Nombre de la columna de ID
        
        Returns:
            Diccionario con los datos o None si no existe
        """
        records = self.read_all()
        for record in records:
            if str(record.get(id_column)) == str(record_id):
                return record
        return None
    
    def find_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """
        Busca registros por un campo específico
        
        Args:
            field: Nombre del campo
            value: Valor a buscar
        
        Returns:
            Lista de registros que coinciden
        """
        records = self.read_all()
        return [r for r in records if str(r.get(field)) == str(value)]
    
    def write_all(self, records: List[Dict[str, Any]]) -> bool:
        """
        Escribe todos los registros al CSV (sobrescribe)
        
        Args:
            records: Lista de diccionarios con los datos
        
        Returns:
            True si fue exitoso
        """
        try:
            if not records:
                # Si no hay registros, crear archivo vacío con headers si existe uno previo
                if self.filepath.exists():
                    df = pd.read_csv(self.filepath, nrows=0)
                    df.to_csv(self.filepath, index=False)
                return True
            
            df = pd.DataFrame(records)
            df.to_csv(self.filepath, index=False)
            return True
        except Exception as e:
            print(f"Error escribiendo {self.filename}: {str(e)}")
            return False
    
    def append(self, record: Dict[str, Any]) -> bool:
        """
        Agrega un nuevo registro al CSV
        
        Args:
            record: Diccionario con los datos del nuevo registro
        
        Returns:
            True si fue exitoso
        """
        records = self.read_all()
        
        # Generar ID automático si no existe
        if 'id' not in record or not record['id']:
            max_id = max([int(r.get('id', 0)) for r in records] + [0])
            record['id'] = max_id + 1
        
        # Agregar timestamps si no existen
        if 'created_at' not in record:
            record['created_at'] = datetime.now().isoformat()
        
        records.append(record)
        return self.write_all(records)
    
    def update(self, record_id: int, updated_data: Dict[str, Any], id_column: str = 'id') -> bool:
        """
        Actualiza un registro existente
        
        Args:
            record_id: ID del registro a actualizar
            updated_data: Diccionario con los datos a actualizar
            id_column: Nombre de la columna de ID
        
        Returns:
            True si fue exitoso
        """
        records = self.read_all()
        found = False
        
        for i, record in enumerate(records):
            if str(record.get(id_column)) == str(record_id):
                # Actualizar solo los campos proporcionados
                records[i].update(updated_data)
                # Actualizar timestamp
                records[i]['updated_at'] = datetime.now().isoformat()
                found = True
                break
        
        if found:
            return self.write_all(records)
        return False
    
    def delete(self, record_id: int, id_column: str = 'id') -> bool:
        """
        Elimina un registro (marca como inactivo)
        
        Args:
            record_id: ID del registro a eliminar
            id_column: Nombre de la columna de ID
        
        Returns:
            True si fue exitoso
        """
        return self.update(record_id, {'activo': False}, id_column)
    
    def filter(self, conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filtra registros por múltiples condiciones
        
        Args:
            conditions: Diccionario con campo: valor
        
        Returns:
            Lista de registros que cumplen todas las condiciones
        """
        records = self.read_all()
        filtered = records
        
        for field, value in conditions.items():
            filtered = [r for r in filtered if str(r.get(field)) == str(value)]
        
        return filtered
    
    def exists(self) -> bool:
        """Verifica si el archivo CSV existe"""
        return self.filepath.exists()
    
    def get_max_id(self, id_column: str = 'id') -> int:
        """
        Obtiene el ID máximo del archivo
        
        Args:
            id_column: Nombre de la columna de ID
        
        Returns:
            ID máximo o 0 si no hay registros
        """
        records = self.read_all()
        if not records:
            return 0
        return max([int(r.get(id_column, 0)) for r in records])


def get_csv_handler(filename: str) -> CSVHandler:
    """
    Factory function para obtener un manejador de CSV
    
    Args:
        filename: Nombre del archivo CSV
    
    Returns:
        Instancia de CSVHandler
    """
    return CSVHandler(filename)
