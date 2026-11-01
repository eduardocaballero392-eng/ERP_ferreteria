"""
Repositorio de Productos - Capa de acceso a datos CSV
"""
from typing import Optional, List, Dict, Any
from app.core.csv_handler import get_csv_handler


class ProductRepository:
    """Repositorio para operaciones CRUD de productos"""
    
    def __init__(self):
        self.csv_handler = get_csv_handler("productos.csv")
    
    def find_all(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtiene todos los productos"""
        products = self.csv_handler.read_all()
        if not include_inactive:
            return [p for p in products if p.get('activo') in [True, 'True', '1', 1]]
        return products
    
    def find_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Busca un producto por ID"""
        return self.csv_handler.read_by_id(product_id)
    
    def find_by_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        """Busca un producto por SKU"""
        products = self.csv_handler.find_by_field("sku", sku)
        return products[0] if products else None
    
    def find_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """Busca productos por categoría"""
        return self.csv_handler.filter({"categoria_id": category_id, "activo": True})
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Busca productos por nombre, SKU o descripción
        """
        products = self.find_all()
        query_lower = query.lower()
        
        return [
            p for p in products
            if query_lower in str(p.get('nombre', '')).lower()
            or query_lower in str(p.get('sku', '')).lower()
            or query_lower in str(p.get('descripcion', '')).lower()
        ]
    
    def find_low_stock(self) -> List[Dict[str, Any]]:
        """Obtiene productos con stock bajo o agotado"""
        products = self.find_all()
        return [
            p for p in products
            if int(p.get('stock_actual', 0)) <= int(p.get('stock_minimo', 0))
        ]
    
    def filter_products(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filtra productos según múltiples criterios
        """
        products = self.find_all()
        
        # Filtrar por categoría
        if filters.get('categoria_id'):
            products = [p for p in products if str(p.get('categoria_id')) == str(filters['categoria_id'])]
        
        # Filtrar por estado de stock
        if filters.get('estado_stock'):
            estado = filters['estado_stock']
            filtered = []
            for p in products:
                stock_actual = int(p.get('stock_actual', 0))
                stock_minimo = int(p.get('stock_minimo', 0))
                
                if estado == "AGOTADO" and stock_actual <= 0:
                    filtered.append(p)
                elif estado == "REPONER" and 0 < stock_actual <= stock_minimo:
                    filtered.append(p)
                elif estado == "OK" and stock_actual > stock_minimo:
                    filtered.append(p)
            
            products = filtered
        
        # Filtrar por búsqueda de texto
        if filters.get('buscar'):
            query_lower = filters['buscar'].lower()
            products = [
                p for p in products
                if query_lower in str(p.get('nombre', '')).lower()
                or query_lower in str(p.get('sku', '')).lower()
                or query_lower in str(p.get('descripcion', '')).lower()
            ]
        
        return products
    
    def create(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo producto"""
        # Verificar si el SKU ya existe
        existing = self.find_by_sku(product_data.get("sku"))
        if existing:
            raise ValueError(f"El SKU '{product_data.get('sku')}' ya existe")
        
        # Crear producto
        success = self.csv_handler.append(product_data)
        if not success:
            raise Exception("Error al crear producto")
        
        # Retornar el producto creado
        return self.find_by_sku(product_data.get("sku"))
    
    def update(self, product_id: int, product_data: Dict[str, Any]) -> bool:
        """Actualiza un producto existente"""
        return self.csv_handler.update(product_id, product_data)
    
    def delete(self, product_id: int) -> bool:
        """Elimina (desactiva) un producto"""
        return self.csv_handler.delete(product_id)
    
    def update_stock(self, product_id: int, new_stock: int) -> bool:
        """Actualiza el stock de un producto"""
        from datetime import datetime
        return self.csv_handler.update(product_id, {
            "stock_actual": new_stock,
            "updated_at": datetime.now().isoformat()
        })


# Singleton
product_repository = ProductRepository()
