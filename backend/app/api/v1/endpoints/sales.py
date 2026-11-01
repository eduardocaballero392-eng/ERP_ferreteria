"""
Endpoints de Ventas
"""
from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.sale import (
    SaleCreate, SaleUpdate, SaleResponse,
    SaleWithDetails, SaleStats
)
from app.schemas.auth import UserResponse
from app.services.sale_service import sale_service
from app.security.dependencies import get_current_active_user, require_role

router = APIRouter()


@router.get("/", response_model=List[SaleResponse], summary="Listar ventas")
async def list_sales(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene todas las ventas
    
    **Requiere:** Autenticación
    """
    return sale_service.get_all_sales()


@router.get("/stats", response_model=SaleStats, summary="Estadísticas de ventas")
async def get_sale_stats(
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    """
    Obtiene estadísticas generales de ventas:
    - Total de ventas realizadas
    - Total vendido
    - Venta promedio
    - Cliente principal
    - Ventas al contado vs crédito
    
    **Requiere rol:** admin o vendedor
    """
    return sale_service.get_sale_stats()


@router.get("/{sale_id}", response_model=SaleWithDetails, summary="Obtener venta")
async def get_sale(
    sale_id: int,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene una venta por ID con todos los detalles (items)
    
    **Requiere:** Autenticación
    """
    return sale_service.get_sale_by_id(sale_id)


@router.post(
    "/",
    response_model=SaleWithDetails,
    status_code=status.HTTP_201_CREATED,
    summary="Crear venta"
)
async def create_sale(
    sale_data: SaleCreate,
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    """
    Crea una nueva venta
    
    **Requiere rol:** admin o vendedor
    
    **Importante:**
    - Se genera automáticamente el número de comprobante (B/FYYYY-######)
    - Se calcula automáticamente el IGV (18%)
    - **Se actualiza el stock automáticamente** (resta las cantidades)
    - Valida stock disponible antes de crear la venta
    - Valida límite de crédito si es venta a crédito
    - Requiere al menos 1 item en el detalle
    
    **Tipos de comprobante:**
    - BOLETA: Para ventas a personas naturales
    - FACTURA: Para ventas a empresas (RUC)
    
    **Condiciones de pago:**
    - CONTADO: Pago inmediato
    - CREDITO: Pago diferido (valida límite de crédito)
    
    **Ejemplo:**
    ```json
    {
      "cliente_id": 1,
      "tipo_comprobante": "BOLETA",
      "condicion_pago": "CONTADO",
      "fecha": "2026-10-31 15:00:00",
      "observaciones": "Venta de materiales",
      "detalles": [
        {
          "producto_id": 1,
          "cantidad": 10,
          "precio_unitario": 28.00
        }
      ]
    }
    ```
    """
    return sale_service.create_sale(sale_data)


@router.put("/{sale_id}", response_model=SaleResponse, summary="Actualizar venta")
async def update_sale(
    sale_id: int,
    sale_data: SaleUpdate,
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    """
    Actualiza una venta existente
    
    **Requiere rol:** admin o vendedor
    
    **Nota:** Solo se pueden actualizar observaciones y estado.
    No se pueden modificar los items después de creada la venta.
    """
    return sale_service.update_sale(sale_id, sale_data)


@router.delete("/{sale_id}", summary="Anular venta")
async def delete_sale(
    sale_id: int,
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Anula una venta (cambia estado a ANULADA)
    
    **Requiere rol:** admin
    
    **⚠️ IMPORTANTE:** El stock NO se revierte automáticamente.
    Si se necesita ajustar el stock, debe hacerse manualmente.
    """
    return sale_service.delete_sale(sale_id)
