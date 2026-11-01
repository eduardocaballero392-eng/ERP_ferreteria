"""
Endpoints de Proveedores
"""
from fastapi import APIRouter, Depends, Query, status
from typing import List
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse, SupplierWithStats
from app.schemas.auth import UserResponse
from app.services.supplier_service import supplier_service
from app.security.dependencies import get_current_active_user, require_role

router = APIRouter()


@router.get("/", response_model=List[SupplierResponse], summary="Listar proveedores")
async def list_suppliers(
    include_inactive: bool = Query(False, description="Incluir proveedores inactivos"),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene todos los proveedores
    
    **Requiere:** Autenticación
    """
    return supplier_service.get_all_suppliers(include_inactive)


@router.get("/with-stats", response_model=List[SupplierWithStats], summary="Proveedores con estadísticas")
async def list_suppliers_with_stats(
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Obtiene proveedores con estadísticas de compras:
    - Total de compras realizadas
    - Monto total de compras
    
    **Requiere rol:** admin o almacenero
    """
    return supplier_service.get_suppliers_with_stats()


@router.get("/search", response_model=List[SupplierResponse], summary="Buscar proveedores")
async def search_suppliers(
    query: str = Query(..., min_length=2, description="Buscar por razón social, nombre comercial o RUC"),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Busca proveedores por razón social, nombre comercial o RUC
    
    **Requiere:** Autenticación
    """
    return supplier_service.search_suppliers(query)


@router.get("/{supplier_id}", response_model=SupplierResponse, summary="Obtener proveedor")
async def get_supplier(
    supplier_id: int,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene un proveedor por ID
    
    **Requiere:** Autenticación
    """
    return supplier_service.get_supplier_by_id(supplier_id)


@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear proveedor"
)
async def create_supplier(
    supplier_data: SupplierCreate,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Crea un nuevo proveedor
    
    **Requiere rol:** admin o almacenero
    
    **Nota:** El RUC debe ser único y válido (11 dígitos)
    """
    return supplier_service.create_supplier(supplier_data)


@router.put("/{supplier_id}", response_model=SupplierResponse, summary="Actualizar proveedor")
async def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Actualiza un proveedor existente
    
    **Requiere rol:** admin o almacenero
    """
    return supplier_service.update_supplier(supplier_id, supplier_data)


@router.delete("/{supplier_id}", summary="Eliminar proveedor")
async def delete_supplier(
    supplier_id: int,
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Elimina (desactiva) un proveedor
    
    **Requiere rol:** admin
    
    **Nota:** No se puede eliminar si tiene compras registradas
    """
    return supplier_service.delete_supplier(supplier_id)
