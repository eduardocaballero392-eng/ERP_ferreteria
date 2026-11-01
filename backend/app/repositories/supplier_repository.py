"""
Repositorio de Proveedores - Capa de acceso a datos CSV
"""
from typing import Optional, List, Dict, Any
from app.core.csv_handler import get_csv_handler


class SupplierRepository:
    """Repositorio para operaciones CRUD de proveedores"""
    
    def __init__(self):
        self.csv_handler = get_csv_handler("proveedores.csv")
    
    def find_all(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtiene todos los proveedores"""
        suppliers = self.csv_handler.read_all()
        if not include_inactive:
            return [s for s in suppliers if s.get('activo') in [True, 'True', '1', 1]]
        return suppliers
    
    def find_by_id(self, supplier_id: int) -> Optional[Dict[str, Any]]:
        """Busca un proveedor por ID"""
        return self.csv_handler.read_by_id(supplier_id)
    
    def find_by_ruc(self, ruc: str) -> Optional[Dict[str, Any]]:
        """Busca un proveedor por RUC"""
        suppliers = self.csv_handler.find_by_field("ruc", ruc)
        return suppliers[0] if suppliers else None
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Busca proveedores por razón social, nombre comercial o RUC"""
        suppliers = self.find_all()
        query_lower = query.lower()
        
        return [
            s for s in suppliers
            if query_lower in str(s.get('razon_social', '')).lower()
            or query_lower in str(s.get('nombre_comercial', '')).lower()
            or query_lower in str(s.get('ruc', '')).lower()
        ]
    
    def create(self, supplier_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo proveedor"""
        # Verificar si el RUC ya existe
        existing = self.find_by_ruc(supplier_data.get("ruc"))
        if existing:
            raise ValueError(f"El RUC '{supplier_data.get('ruc')}' ya está registrado")
        
        # Crear proveedor
        success = self.csv_handler.append(supplier_data)
        if not success:
            raise Exception("Error al crear proveedor")
        
        # Retornar el proveedor creado
        return self.find_by_ruc(supplier_data.get("ruc"))
    
    def update(self, supplier_id: int, supplier_data: Dict[str, Any]) -> bool:
        """Actualiza un proveedor existente"""
        return self.csv_handler.update(supplier_id, supplier_data)
    
    def delete(self, supplier_id: int) -> bool:
        """Elimina (desactiva) un proveedor"""
        return self.csv_handler.delete(supplier_id)


# Singleton
supplier_repository = SupplierRepository()
