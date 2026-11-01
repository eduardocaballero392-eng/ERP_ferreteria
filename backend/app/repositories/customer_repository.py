"""
Repositorio de Clientes - Capa de acceso a datos CSV
"""
from typing import Optional, List, Dict, Any
from app.core.csv_handler import get_csv_handler


class CustomerRepository:
    """Repositorio para operaciones CRUD de clientes"""
    
    def __init__(self):
        self.csv_handler = get_csv_handler("clientes.csv")
    
    def find_all(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtiene todos los clientes"""
        customers = self.csv_handler.read_all()
        if not include_inactive:
            return [c for c in customers if c.get('activo') in [True, 'True', '1', 1]]
        return customers
    
    def find_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """Busca un cliente por ID"""
        return self.csv_handler.read_by_id(customer_id)
    
    def find_by_documento(self, numero_documento: str) -> Optional[Dict[str, Any]]:
        """Busca un cliente por número de documento"""
        customers = self.csv_handler.find_by_field("numero_documento", numero_documento)
        return customers[0] if customers else None
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Busca clientes por nombres, apellidos, razón social o documento"""
        customers = self.find_all()
        query_lower = query.lower()
        
        return [
            c for c in customers
            if query_lower in str(c.get('nombres', '')).lower()
            or query_lower in str(c.get('apellidos', '')).lower()
            or query_lower in str(c.get('razon_social', '')).lower()
            or query_lower in str(c.get('numero_documento', '')).lower()
        ]
    
    def create(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo cliente"""
        # Verificar si el documento ya existe
        existing = self.find_by_documento(customer_data.get("numero_documento"))
        if existing:
            raise ValueError(f"El documento '{customer_data.get('numero_documento')}' ya está registrado")
        
        # Crear cliente
        success = self.csv_handler.append(customer_data)
        if not success:
            raise Exception("Error al crear cliente")
        
        # Retornar el cliente creado
        return self.find_by_documento(customer_data.get("numero_documento"))
    
    def update(self, customer_id: int, customer_data: Dict[str, Any]) -> bool:
        """Actualiza un cliente existente"""
        return self.csv_handler.update(customer_id, customer_data)
    
    def delete(self, customer_id: int) -> bool:
        """Elimina (desactiva) un cliente"""
        return self.csv_handler.delete(customer_id)


# Singleton
customer_repository = CustomerRepository()
