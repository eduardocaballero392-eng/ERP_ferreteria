"""Carga del inventario inicial o del stock actualizado del día."""
import csv
import io
import re
import unicodedata

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.repositories.product_repository import product_repository

router = APIRouter()


def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.strip().lower())
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


@router.post("/stock", summary="Actualizar existencias desde el CSV maestro")
async def upload_stock(file: UploadFile = File(...)):
    """Actualiza el stock de productos existentes usando SKU, código o nombre.

    Acepta encabezados comunes en español o inglés y detecta coma, punto y coma
    o tabulador. Las demás áreas consultan el mismo catálogo actualizado.
    """
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Selecciona un archivo .csv")

    contents = await file.read(10 * 1024 * 1024 + 1)
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="El CSV supera el límite de 10 MB")
    if not contents.strip():
        raise HTTPException(status_code=400, detail="El archivo CSV está vacío")

    decoded = None
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            decoded = contents.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    try:
        dialect = csv.Sniffer().sniff(decoded[:4096], delimiters=",;\t| ")
    except csv.Error:
        dialect = csv.excel

    reader = csv.DictReader(io.StringIO(decoded), dialect=dialect)
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="El CSV debe incluir encabezados")

    columns = {_normalize(name): name for name in reader.fieldnames if name}

    def find_column(aliases):
        return next((columns[name] for name in aliases if name in columns), None)

    stock_column = find_column({"stock", "stock_actual", "existencia", "existencias", "cantidad", "inventario", "saldo", "quantity", "current_stock", "units"})
    key_column = find_column({"sku", "codigo", "codigo_producto", "cod_producto", "product_code", "code", "id"})
    name_column = find_column({"nombre", "producto", "nombre_producto", "product", "product_name", "description"})

    if not stock_column:
        raise HTTPException(status_code=400, detail="No encuentro la columna de stock (stock, existencia o cantidad)")
    if not key_column and not name_column:
        raise HTTPException(status_code=400, detail="Incluye una columna SKU/código o nombre del producto para relacionar el stock")

    products = product_repository.find_all(include_inactive=True)
    by_sku = {str(p.get("sku", "")).strip().casefold(): p for p in products}
    by_id = {str(p.get("id", "")).strip(): p for p in products}
    by_name = {str(p.get("nombre", "")).strip().casefold(): p for p in products}

    updated = 0
    unchanged = 0
    errors = []
    seen = set()
    for line, row in enumerate(reader, start=2):
        key = str(row.get(key_column, "")).strip() if key_column else ""
        name = str(row.get(name_column, "")).strip() if name_column else ""
        product = by_sku.get(key.casefold()) or by_id.get(key) or by_name.get(name.casefold())
        if not product:
            errors.append(f"Fila {line}: no se encontró el producto '{key or name}'")
            continue
        product_id = str(product["id"])
        if product_id in seen:
            errors.append(f"Fila {line}: producto repetido ({product.get('sku') or product.get('nombre')})")
            continue
        raw_stock = str(row.get(stock_column, "")).strip().replace(" ", "").replace(",", ".")
        try:
            stock = int(float(raw_stock))
            if stock < 0:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"Fila {line}: stock inválido '{raw_stock}'")
            continue
        seen.add(product_id)
        if int(product.get("stock_actual", 0)) == stock:
            unchanged += 1
        elif product_repository.update_stock(int(product_id), stock):
            updated += 1
        else:
            errors.append(f"Fila {line}: no se pudo guardar el stock")

    if updated + unchanged == 0:
        raise HTTPException(status_code=400, detail="No se actualizó ningún producto. Revisa los encabezados y los SKU.")

    return {
        "message": "Inventario sincronizado",
        "filename": file.filename,
        "total_rows": updated + unchanged + len(errors),
        "updated": updated,
        "unchanged": unchanged,
        "errors": errors[:20],
    }
