"""
Repositorio de Compras - Capa de acceso a datos CSV
"""
from typing import Optional, List, Dict, Any
from app.core.csv_handler import get_csv_handler


class PurchaseRepository:
    """Repositorio para operaciones CRUD de compras"""
    
    def __init__(self):
        self.csv_handler = get_csv_handler("compras.csv")
        self.detail_handler = get_csv_handler("detalle_compras.csv")
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Obtiene todas las compras"""
        return self.csv_handler.read_all()
    
    def find_by_id(self, purchase_id: int) -> Optional[Dict[str, Any]]:
        """Busca una compra por ID"""
        return self.csv_handler.read_by_id(purchase_id)
    
    def find_by_supplier(self, supplier_id: int) -> List[Dict[str, Any]]:
        """Busca compras por proveedor"""
        return self.csv_handler.filter({"proveedor_id": supplier_id})
    
    def find_by_numero_orden(self, numero_orden: str) -> Optional[Dict[str, Any]]:
        """Busca una compra por número de orden"""
        purchases = self.csv_handler.find_by_field("numero_orden", numero_orden)
        return purchases[0] if purchases else None
    
    def get_details(self, purchase_id: int) -> List[Dict[str, Any]]:
        """Obtiene los detalles de una compra"""
        return self.detail_handler.filter({"compra_id": purchase_id})

    def get_replenished_product_ids(self) -> set[int]:
        """Obtiene los productos incluidos en compras completadas."""
        completed_purchase_ids = {
            str(purchase.get("id"))
            for purchase in self.find_all()
            if purchase.get("estado") == "COMPLETADA"
        }
        return {
            int(float(detail["producto_id"]))
            for detail in self.detail_handler.read_all()
            if str(detail.get("compra_id")) in completed_purchase_ids
            and int(float(detail.get("cantidad") or 0)) > 0
        }
    
    def create(self, purchase_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva compra"""
        # Verificar si el número de orden ya existe
        existing = self.find_by_numero_orden(purchase_data.get("numero_orden"))
        if existing:
            raise ValueError(f"El número de orden '{purchase_data.get('numero_orden')}' ya existe")
        
        # Crear compra
        success = self.csv_handler.append(purchase_data)
        if not success:
            raise Exception("Error al crear compra")
        
        # Retornar la compra creada
        return self.find_by_numero_orden(purchase_data.get("numero_orden"))
    
    def create_detail(self, detail_data: Dict[str, Any]) -> bool:
        """Crea un detalle de compra"""
        return self.detail_handler.append(detail_data)
    
    def update(self, purchase_id: int, purchase_data: Dict[str, Any]) -> bool:
        """Actualiza una compra existente"""
        return self.csv_handler.update(purchase_id, purchase_data)
    
    def delete(self, purchase_id: int) -> bool:
        """Marca una compra como anulada"""
        from datetime import datetime
        return self.csv_handler.update(purchase_id, {
            "estado": "ANULADA",
            "updated_at": datetime.now().isoformat()
        })
    
    def get_next_numero_orden(self) -> str:
        """Genera el siguiente número de orden"""
        from datetime import datetime
        purchases = self.find_all()
        
        # Obtener el año actual
        year = datetime.now().year
        
        # Contar compras del año actual
        year_purchases = [
            p for p in purchases
            if p.get('numero_orden', '').startswith(f"OC-{year}")
        ]
        
        next_number = len(year_purchases) + 1
        return f"OC-{year}-{next_number:03d}"


# Singleton
purchase_repository = PurchaseRepository()
