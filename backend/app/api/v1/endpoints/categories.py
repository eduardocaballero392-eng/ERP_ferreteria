"""
Endpoints de Categorías
"""
from fastapi import APIRouter, Depends, Query, status
from typing import List
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithProductCount
from app.schemas.auth import UserResponse
from app.services.category_service import category_service
from app.security.dependencies import get_current_active_user, require_role

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse], summary="Listar categorías")
async def list_categories(
    include_inactive: bool = Query(False, description="Incluir categorías inactivas"),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene todas las categorías
    
    **Requiere:** Autenticación
    """
    return category_service.get_all_categories(include_inactive)


@router.get("/with-count", response_model=List[CategoryWithProductCount], summary="Categorías con conteo")
async def list_categories_with_count(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene categorías con el conteo de productos en cada una
    
    **Requiere:** Autenticación
    """
    return category_service.get_categories_with_count()


@router.get("/{category_id}", response_model=CategoryResponse, summary="Obtener categoría")
async def get_category(
    category_id: int,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene una categoría por ID
    
    **Requiere:** Autenticación
    """
    return category_service.get_category_by_id(category_id)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría"
)
async def create_category(
    category_data: CategoryCreate,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Crea una nueva categoría
    
    **Requiere rol:** admin o almacenero
    """
    return category_service.create_category(category_data)


@router.put("/{category_id}", response_model=CategoryResponse, summary="Actualizar categoría")
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Actualiza una categoría existente
    
    **Requiere rol:** admin o almacenero
    """
    return category_service.update_category(category_id, category_data)


@router.delete("/{category_id}", summary="Eliminar categoría")
async def delete_category(
    category_id: int,
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Elimina (desactiva) una categoría
    
    **Requiere rol:** admin
    
    **Nota:** No se puede eliminar si tiene productos asociados
    """
    return category_service.delete_category(category_id)
