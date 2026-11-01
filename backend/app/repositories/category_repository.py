"""
Repositorio de Categorías - Capa de acceso a datos CSV
"""
from typing import Optional, List, Dict, Any
from app.core.csv_handler import get_csv_handler


class CategoryRepository:
    """Repositorio para operaciones CRUD de categorías"""
    
    def __init__(self):
        self.csv_handler = get_csv_handler("categorias.csv")
    
    def find_all(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtiene todas las categorías"""
        categories = self.csv_handler.read_all()
        if not include_inactive:
            return [c for c in categories if c.get('activo') in [True, 'True', '1', 1]]
        return categories
    
    def find_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Busca una categoría por ID"""
        return self.csv_handler.read_by_id(category_id)
    
    def find_by_name(self, nombre: str) -> Optional[Dict[str, Any]]:
        """Busca una categoría por nombre"""
        categories = self.csv_handler.find_by_field("nombre", nombre)
        return categories[0] if categories else None
    
    def create(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva categoría"""
        # Verificar si el nombre ya existe
        existing = self.find_by_name(category_data.get("nombre"))
        if existing:
            raise ValueError(f"La categoría '{category_data.get('nombre')}' ya existe")
        
        # Crear categoría
        success = self.csv_handler.append(category_data)
        if not success:
            raise Exception("Error al crear categoría")
        
        # Retornar la categoría creada
        return self.find_by_name(category_data.get("nombre"))
    
    def update(self, category_id: int, category_data: Dict[str, Any]) -> bool:
        """Actualiza una categoría existente"""
        return self.csv_handler.update(category_id, category_data)
    
    def delete(self, category_id: int) -> bool:
        """Elimina (desactiva) una categoría"""
        return self.csv_handler.delete(category_id)


# Singleton
category_repository = CategoryRepository()
