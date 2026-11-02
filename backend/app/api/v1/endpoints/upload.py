"""
Endpoints para carga de archivos CSV
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
import csv
import io
from app.core.csv_handler import get_csv_handler
from app.security.dependencies import get_current_active_user, require_role
from app.schemas.auth import UserResponse

router = APIRouter()


@router.post("/csv", summary="Cargar archivo CSV")
async def upload_csv(
    entity: str = Form(..., description="Entidad: productos, categorias, clientes, proveedores, ventas, compras"),
    file: UploadFile = File(..., description="Archivo CSV")
):
    """
    Carga datos masivos desde un archivo CSV
    
    **Requiere rol:** admin
    
    **Entidades soportadas:**
    - productos
    - categorias
    - clientes
    - proveedores
    - ventas
    - compras
    
    **Formato CSV:**
    - Primera fila debe contener nombres de columnas
    - Separador: coma (,)
    - Codificación: UTF-8
    """
    
    # Validar extensión
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser CSV"
        )
    
    # Mapeo de entidades a archivos CSV
    entity_files = {
        'productos': 'productos.csv',
        'categorias': 'categorias.csv',
        'clientes': 'clientes.csv',
        'proveedores': 'proveedores.csv',
        'ventas': 'ventas.csv',
        'compras': 'compras.csv',
    }
    
    if entity not in entity_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entidad '{entity}' no soportada. Use: {', '.join(entity_files.keys())}"
        )
    
    try:
        # Leer contenido del archivo
        contents = await file.read()
        decoded = contents.decode('utf-8')
        
        # Parsear CSV
        csv_reader = csv.DictReader(io.StringIO(decoded))
        rows = list(csv_reader)
        
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo CSV está vacío"
            )
        
        # Obtener handler de CSV
        csv_handler = get_csv_handler(entity_files[entity])
        
        # Contador de registros procesados
        created = 0
        updated = 0
        errors = []
        
        for idx, row in enumerate(rows, start=2):  # start=2 porque la fila 1 es el header
            try:
                # Verificar si el registro ya existe (por ID si está presente)
                record_id = row.get('id')
                
                if record_id and csv_handler.read_by_id(int(record_id)):
                    # Actualizar registro existente
                    csv_handler.update(int(record_id), row)
                    updated += 1
                else:
                    # Crear nuevo registro
                    csv_handler.append(row)
                    created += 1
                    
            except Exception as e:
                errors.append(f"Fila {idx}: {str(e)}")
        
        return {
            "message": f"Archivo procesado exitosamente",
            "entity": entity,
            "filename": file.filename,
            "total_rows": len(rows),
            "created": created,
            "updated": updated,
            "errors": errors[:10] if errors else []  # Limitar errores a 10
        }
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de codificación. Asegúrate de usar UTF-8"
        )
    except csv.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al parsear CSV: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar archivo: {str(e)}"
        )
