"""
Endpoints de Clientes
"""
from fastapi import APIRouter, Depends, Query, status
from typing import List
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerWithStats
from app.schemas.auth import UserResponse
from app.services.customer_service import customer_service
from app.security.dependencies import get_current_active_user, require_role

router = APIRouter()


@router.get("/", response_model=List[CustomerResponse], summary="Listar clientes")
async def list_customers(
    include_inactive: bool = Query(False, description="Incluir clientes inactivos"),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene todos los clientes
    
    **Requiere:** Autenticación
    """
    return customer_service.get_all_customers(include_inactive)


@router.get("/with-stats", response_model=List[CustomerWithStats], summary="Clientes con estadísticas")
async def list_customers_with_stats(
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    """
    Obtiene clientes con estadísticas de compras:
    - Total de compras realizadas
    - Monto total de compras
    - Saldo pendiente por cobrar
    - Crédito disponible
    
    **Requiere rol:** admin o vendedor
    """
    return customer_service.get_customers_with_stats()


@router.get("/search", response_model=List[CustomerResponse], summary="Buscar clientes")
async def search_customers(
    query: str = Query(..., min_length=2, description="Buscar por nombres, apellidos, razón social o documento"),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Busca clientes por nombres, apellidos, razón social o número de documento
    
    **Requiere:** Autenticación
    """
    return customer_service.search_customers(query)


@router.get("/{customer_id}", response_model=CustomerResponse, summary="Obtener cliente")
async def get_customer(
    customer_id: int,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene un cliente por ID
    
    **Requiere:** Autenticación
    """
    return customer_service.get_customer_by_id(customer_id)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear cliente"
)
async def create_customer(
    customer_data: CustomerCreate,
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    """
    Crea un nuevo cliente
    
    **Requiere rol:** admin o vendedor
    
    **Nota:** 
    - El DNI debe tener 8 dígitos
    - El RUC debe tener 11 dígitos
    - El documento debe ser único
    """
    return customer_service.create_customer(customer_data)


@router.put("/{customer_id}", response_model=CustomerResponse, summary="Actualizar cliente")
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    """
    Actualiza un cliente existente
    
    **Requiere rol:** admin o vendedor
    """
    return customer_service.update_customer(customer_id, customer_data)


@router.delete("/{customer_id}", summary="Eliminar cliente")
async def delete_customer(
    customer_id: int,
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Elimina (desactiva) un cliente
    
    **Requiere rol:** admin
    
    **Nota:** No se puede eliminar si tiene ventas registradas
    """
    return customer_service.delete_customer(customer_id)
