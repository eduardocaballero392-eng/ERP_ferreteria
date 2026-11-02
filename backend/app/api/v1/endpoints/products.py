"""
Endpoints de Productos
"""
from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductWithDetails, ProductStockAdjust, ProductSearchFilters
)
from app.schemas.auth import UserResponse
from app.services.product_service import product_service
from app.security.dependencies import get_current_active_user, require_role

router = APIRouter()


@router.get("/", response_model=List[ProductResponse], summary="Listar productos")
async def list_products(
    include_inactive: bool = Query(False, description="Incluir productos inactivos"),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene todos los productos
    
    **Requiere:** Autenticación
    """
    return product_service.get_all_products(include_inactive)


@router.get("/details", response_model=List[ProductWithDetails], summary="Productos con detalles")
async def list_products_with_details(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene productos con detalles adicionales:
    - Estado de stock (OK/REPONER/AGOTADO)
    - Valor del inventario
    - Margen de utilidad
    - Nombre de la categoría
    
    **Requiere:** Autenticación
    """
    return product_service.get_products_with_details()


@router.get("/low-stock", response_model=List[ProductWithDetails], summary="Productos con stock bajo")
async def list_low_stock_products(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene productos con stock bajo o agotado
    
    **Útil para:** Alertas de reposición
    
    **Requiere:** Autenticación
    """
    return product_service.get_low_stock_products()


@router.post("/search", response_model=List[ProductWithDetails], summary="Buscar productos")
async def search_products(
    filters: ProductSearchFilters,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Busca y filtra productos por múltiples criterios:
    - Por categoría
    - Por estado de stock (OK/REPONER/AGOTADO)
    - Por texto (nombre, SKU, descripción)
    - Por estado activo/inactivo
    
    **Requiere:** Autenticación
    """
    return product_service.search_products(filters)


@router.get("/{product_id}", response_model=ProductWithDetails, summary="Obtener producto")
async def get_product(
    product_id: int,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene un producto por ID con todos los detalles
    
    **Requiere:** Autenticación
    """
    return product_service.get_product_by_id(product_id)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto"
)
async def create_product(
    product_data: ProductCreate,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Crea un nuevo producto
    
    **Requiere rol:** admin o almacenero
    
    **Nota:** El SKU debe ser único
    """
    return product_service.create_product(product_data)


@router.post("/clear-stock", summary="Poner todo el stock en cero")
async def clear_all_stock(
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """Pone las existencias de todos los productos en cero. Solo para administradores."""
    return product_service.clear_all_stock()


@router.put("/{product_id}", response_model=ProductResponse, summary="Actualizar producto")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Actualiza un producto existente
    
    **Requiere rol:** admin o almacenero
    """
    return product_service.update_product(product_id, product_data)


@router.post("/{product_id}/adjust-stock", response_model=ProductWithDetails, summary="Ajustar stock")
async def adjust_stock(
    product_id: int,
    adjustment: ProductStockAdjust,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Ajusta el stock de un producto manualmente
    
    **Requiere rol:** admin o almacenero
    
    **Casos de uso:**
    - Productos dañados (cantidad negativa)
    - Inventario físico (ajuste positivo o negativo)
    - Corrección de errores
    
    **Ejemplo:**
    ```json
    {
      "cantidad": -5,
      "motivo": "Productos dañados en almacén"
    }
    ```
    """
    return product_service.adjust_stock(product_id, adjustment)


@router.delete("/{product_id}", summary="Eliminar producto")
async def delete_product(
    product_id: int,
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Elimina (desactiva) un producto
    
    **Requiere rol:** admin
    
    **Nota:** El producto se desactiva pero no se elimina físicamente
    """
    return product_service.delete_product(product_id)
