"""
Servicio de Productos - Lógica de negocio
"""
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductWithDetails, ProductStockAdjust, ProductSearchFilters
)
from app.repositories.product_repository import product_repository
from app.repositories.category_repository import category_repository
from app.core.utils import obtener_estado_stock


class ProductService:
    """Servicio de gestión de productos"""
    
    def __init__(self):
        self.product_repo = product_repository
        self.category_repo = category_repository
    
    def get_all_products(self, include_inactive: bool = False) -> List[ProductResponse]:
        """Obtiene todos los productos"""
        products = self.product_repo.find_all(include_inactive)
        return [ProductResponse(**prod) for prod in products]
    
    def get_products_with_details(self) -> List[ProductWithDetails]:
        """Obtiene productos con detalles adicionales"""
        products = self.product_repo.find_all()
        result = []
        
        for prod in products:
            # Obtener categoría
            category = self.category_repo.find_by_id(prod['categoria_id'])
            
            # Calcular detalles
            stock_actual = int(prod.get('stock_actual', 0))
            stock_minimo = int(prod.get('stock_minimo', 0))
            costo = float(prod.get('costo_unitario', 0))
            precio = float(prod.get('precio_venta', 0))
            
            estado_stock = obtener_estado_stock(stock_actual, stock_minimo)
            valor_inventario = stock_actual * costo
            margen_utilidad = ((precio - costo) / precio * 100) if precio > 0 else 0
            
            prod_with_details = {
                **prod,
                'estado_stock': estado_stock,
                'valor_inventario': round(valor_inventario, 2),
                'margen_utilidad': round(margen_utilidad, 2),
                'categoria_nombre': category.get('nombre') if category else None
            }
            result.append(ProductWithDetails(**prod_with_details))
        
        return result
    
    def get_product_by_id(self, product_id: int) -> ProductWithDetails:
        """Obtiene un producto por ID con detalles"""
        product = self.product_repo.find_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        
        # Obtener categoría
        category = self.category_repo.find_by_id(product['categoria_id'])
        
        # Calcular detalles
        stock_actual = int(product.get('stock_actual', 0))
        stock_minimo = int(product.get('stock_minimo', 0))
        costo = float(product.get('costo_unitario', 0))
        precio = float(product.get('precio_venta', 0))
        
        product_with_details = {
            **product,
            'estado_stock': obtener_estado_stock(stock_actual, stock_minimo),
            'valor_inventario': round(stock_actual * costo, 2),
            'margen_utilidad': round(((precio - costo) / precio * 100) if precio > 0 else 0, 2),
            'categoria_nombre': category.get('nombre') if category else None
        }
        
        return ProductWithDetails(**product_with_details)
    
    def search_products(self, filters: ProductSearchFilters) -> List[ProductWithDetails]:
        """Busca y filtra productos"""
        filter_dict = filters.model_dump(exclude_unset=True)
        products = self.product_repo.filter_products(filter_dict)
        
        # Agregar detalles
        result = []
        for prod in products:
            category = self.category_repo.find_by_id(prod['categoria_id'])
            
            stock_actual = int(prod.get('stock_actual', 0))
            stock_minimo = int(prod.get('stock_minimo', 0))
            costo = float(prod.get('costo_unitario', 0))
            precio = float(prod.get('precio_venta', 0))
            
            prod_with_details = {
                **prod,
                'estado_stock': obtener_estado_stock(stock_actual, stock_minimo),
                'valor_inventario': round(stock_actual * costo, 2),
                'margen_utilidad': round(((precio - costo) / precio * 100) if precio > 0 else 0, 2),
                'categoria_nombre': category.get('nombre') if category else None
            }
            result.append(ProductWithDetails(**prod_with_details))
        
        return result
    
    def get_low_stock_products(self) -> List[ProductWithDetails]:
        """Obtiene productos con stock bajo o agotado"""
        products = self.product_repo.find_low_stock()
        
        result = []
        for prod in products:
            category = self.category_repo.find_by_id(prod['categoria_id'])
            
            stock_actual = int(prod.get('stock_actual', 0))
            stock_minimo = int(prod.get('stock_minimo', 0))
            costo = float(prod.get('costo_unitario', 0))
            precio = float(prod.get('precio_venta', 0))
            
            prod_with_details = {
                **prod,
                'estado_stock': obtener_estado_stock(stock_actual, stock_minimo),
                'valor_inventario': round(stock_actual * costo, 2),
                'margen_utilidad': round(((precio - costo) / precio * 100) if precio > 0 else 0, 2),
                'categoria_nombre': category.get('nombre') if category else None
            }
            result.append(ProductWithDetails(**prod_with_details))
        
        return result
    
    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Crea un nuevo producto"""
        # Verificar que la categoría existe
        category = self.category_repo.find_by_id(product_data.categoria_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoría con ID {product_data.categoria_id} no encontrada"
            )
        
        new_product_data = {
            **product_data.model_dump(),
            "activo": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            created_product = self.product_repo.create(new_product_data)
            return ProductResponse(**created_product)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear producto"
            )
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> ProductResponse:
        """Actualiza un producto"""
        # Verificar que existe
        existing = self.product_repo.find_by_id(product_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        
        # Si se actualiza la categoría, verificar que existe
        if product_data.categoria_id:
            category = self.category_repo.find_by_id(product_data.categoria_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Categoría con ID {product_data.categoria_id} no encontrada"
                )
        
        # Preparar datos a actualizar
        update_data = product_data.model_dump(exclude_unset=True)
        if update_data:
            update_data['updated_at'] = datetime.now().isoformat()
            
            success = self.product_repo.update(product_id, update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar producto"
                )
        
        # Retornar producto actualizado
        updated_product = self.product_repo.find_by_id(product_id)
        return ProductResponse(**updated_product)
    
    def adjust_stock(self, product_id: int, adjustment: ProductStockAdjust) -> ProductWithDetails:
        """Ajusta el stock de un producto manualmente"""
        # Obtener producto
        product = self.product_repo.find_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        
        # Calcular nuevo stock
        stock_actual = int(product.get('stock_actual', 0))
        new_stock = stock_actual + adjustment.cantidad
        
        if new_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El ajuste resultaría en stock negativo ({new_stock})"
            )
        
        # Actualizar stock
        success = self.product_repo.update_stock(product_id, new_stock)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al ajustar stock"
            )
        
        # TODO: Registrar en movimientos_inventario con tipo AJUSTE
        
        return self.get_product_by_id(product_id)

    def clear_all_stock(self) -> dict:
        """Vacía las existencias sin eliminar los productos del catálogo."""
        try:
            result = self.product_repo.clear_all_stock()
        except OSError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo guardar el inventario vacío",
            ) from error

        return {
            "message": "El stock de todos los productos quedó en cero",
            **result,
        }
    
    def delete_product(self, product_id: int) -> dict:
        """Elimina (desactiva) un producto"""
        # Verificar que existe
        existing = self.product_repo.find_by_id(product_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        
        # Eliminar
        success = self.product_repo.delete(product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar producto"
            )
        
        return {"message": f"Producto {product_id} eliminado exitosamente"}


# Singleton
product_service = ProductService()
