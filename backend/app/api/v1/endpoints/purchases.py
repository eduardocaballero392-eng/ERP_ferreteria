"""
Endpoints de Compras
"""
from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.purchase import (
    PurchaseCreate, PurchaseUpdate, PurchaseResponse,
    PurchaseWithDetails, PurchaseStats
)
from app.schemas.auth import UserResponse
from app.services.purchase_service import purchase_service
from app.security.dependencies import get_current_active_user, require_role

router = APIRouter()


@router.get("/", response_model=List[PurchaseResponse], summary="Listar compras")
async def list_purchases(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene todas las compras
    
    **Requiere:** Autenticación
    """
    return purchase_service.get_all_purchases()


@router.get("/stats", response_model=PurchaseStats, summary="Estadísticas de compras")
async def get_purchase_stats(
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Obtiene estadísticas generales de compras:
    - Total de compras realizadas
    - Total gastado
    - Compra promedio
    - Proveedor principal
    
    **Requiere rol:** admin o almacenero
    """
    return purchase_service.get_purchase_stats()


@router.get("/{purchase_id}", response_model=PurchaseWithDetails, summary="Obtener compra")
async def get_purchase(
    purchase_id: int,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene una compra por ID con todos los detalles (items)
    
    **Requiere:** Autenticación
    """
    return purchase_service.get_purchase_by_id(purchase_id)


@router.post(
    "/",
    response_model=PurchaseWithDetails,
    status_code=status.HTTP_201_CREATED,
    summary="Crear compra"
)
async def create_purchase(
    purchase_data: PurchaseCreate,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Crea una nueva orden de compra
    
    **Requiere rol:** admin o almacenero
    
    **Importante:**
    - Se genera automáticamente el número de orden (OC-YYYY-###)
    - Se calcula automáticamente el IGV (18%)
    - **Se actualiza el stock automáticamente** (suma las cantidades)
    - Requiere al menos 1 item en el detalle
    
    **Ejemplo:**
    ```json
    {
      "proveedor_id": 1,
      "fecha": "2026-10-31 10:00:00",
      "observaciones": "Compra de cemento y agregados",
      "detalles": [
        {
          "producto_id": 1,
          "cantidad": 50,
          "costo_unitario": 22.50
        },
        {
          "producto_id": 6,
          "cantidad": 500,
          "costo_unitario": 0.85
        }
      ]
    }
    ```
    """
    return purchase_service.create_purchase(purchase_data)


@router.put("/{purchase_id}", response_model=PurchaseResponse, summary="Actualizar compra")
async def update_purchase(
    purchase_id: int,
    purchase_data: PurchaseUpdate,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Actualiza una compra existente
    
    **Requiere rol:** admin o almacenero
    
    **Nota:** Solo se pueden actualizar observaciones y estado.
    No se pueden modificar los items después de creada la compra.
    """
    return purchase_service.update_purchase(purchase_id, purchase_data)


@router.delete("/{purchase_id}", summary="Anular compra")
async def delete_purchase(
    purchase_id: int,
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Anula una compra (cambia estado a ANULADA)
    
    **Requiere rol:** admin
    
    **⚠️ IMPORTANTE:** El stock NO se revierte automáticamente.
    Si se necesita ajustar el stock, debe hacerse manualmente.
    """
    return purchase_service.delete_purchase(purchase_id)
