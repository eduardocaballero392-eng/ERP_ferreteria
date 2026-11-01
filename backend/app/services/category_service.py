"""
Servicio de Categorías - Lógica de negocio
"""
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithProductCount
from app.repositories.category_repository import category_repository
from app.repositories.product_repository import product_repository


class CategoryService:
    """Servicio de gestión de categorías"""
    
    def __init__(self):
        self.category_repo = category_repository
        self.product_repo = product_repository
    
    def get_all_categories(self, include_inactive: bool = False) -> List[CategoryResponse]:
        """Obtiene todas las categorías"""
        categories = self.category_repo.find_all(include_inactive)
        return [CategoryResponse(**cat) for cat in categories]
    
    def get_categories_with_count(self) -> List[CategoryWithProductCount]:
        """Obtiene categorías con conteo de productos"""
        categories = self.category_repo.find_all()
        result = []
        
        for cat in categories:
            products = self.product_repo.find_by_category(cat['id'])
            cat_with_count = {
                **cat,
                'total_productos': len(products)
            }
            result.append(CategoryWithProductCount(**cat_with_count))
        
        return result
    
    def get_category_by_id(self, category_id: int) -> CategoryResponse:
        """Obtiene una categoría por ID"""
        category = self.category_repo.find_by_id(category_id)
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )
        
        return CategoryResponse(**category)
    
    def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        """Crea una nueva categoría"""
        new_category_data = {
            "nombre": category_data.nombre,
            "descripcion": category_data.descripcion,
            "activo": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            created_category = self.category_repo.create(new_category_data)
            return CategoryResponse(**created_category)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear categoría"
            )
    
    def update_category(self, category_id: int, category_data: CategoryUpdate) -> CategoryResponse:
        """Actualiza una categoría"""
        # Verificar que existe
        existing = self.category_repo.find_by_id(category_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )
        
        # Preparar datos a actualizar
        update_data = category_data.model_dump(exclude_unset=True)
        if update_data:
            update_data['updated_at'] = datetime.now().isoformat()
            
            success = self.category_repo.update(category_id, update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar categoría"
                )
        
        # Retornar categoría actualizada
        updated_category = self.category_repo.find_by_id(category_id)
        return CategoryResponse(**updated_category)
    
    def delete_category(self, category_id: int) -> dict:
        """Elimina (desactiva) una categoría"""
        # Verificar que existe
        existing = self.category_repo.find_by_id(category_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID {category_id} no encontrada"
            )
        
        # Verificar si tiene productos
        products = self.product_repo.find_by_category(category_id)
        if products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar la categoría porque tiene {len(products)} producto(s) asociado(s)"
            )
        
        # Eliminar
        success = self.category_repo.delete(category_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar categoría"
            )
        
        return {"message": f"Categoría {category_id} eliminada exitosamente"}


# Singleton
category_service = CategoryService()
