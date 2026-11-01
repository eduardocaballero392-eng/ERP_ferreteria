"""
Repositorio de Ventas - Capa de acceso a datos CSV
"""
from typing import Optional, List, Dict, Any
from app.core.csv_handler import get_csv_handler


class SaleRepository:
    """Repositorio para operaciones CRUD de ventas"""
    
    def __init__(self):
        self.csv_handler = get_csv_handler("ventas.csv")
        self.detail_handler = get_csv_handler("detalle_ventas.csv")
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Obtiene todas las ventas"""
        return self.csv_handler.read_all()
    
    def find_by_id(self, sale_id: int) -> Optional[Dict[str, Any]]:
        """Busca una venta por ID"""
        return self.csv_handler.read_by_id(sale_id)
    
    def find_by_customer(self, customer_id: int) -> List[Dict[str, Any]]:
        """Busca ventas por cliente"""
        return self.csv_handler.filter({"cliente_id": customer_id})
    
    def find_by_numero_comprobante(self, numero_comprobante: str) -> Optional[Dict[str, Any]]:
        """Busca una venta por número de comprobante"""
        sales = self.csv_handler.find_by_field("numero_comprobante", numero_comprobante)
        return sales[0] if sales else None
    
    def get_details(self, sale_id: int) -> List[Dict[str, Any]]:
        """Obtiene los detalles de una venta"""
        return self.detail_handler.filter({"venta_id": sale_id})
    
    def create(self, sale_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva venta"""
        # Verificar si el número de comprobante ya existe
        existing = self.find_by_numero_comprobante(sale_data.get("numero_comprobante"))
        if existing:
            raise ValueError(f"El número de comprobante '{sale_data.get('numero_comprobante')}' ya existe")
        
        # Crear venta
        success = self.csv_handler.append(sale_data)
        if not success:
            raise Exception("Error al crear venta")
        
        # Retornar la venta creada
        return self.find_by_numero_comprobante(sale_data.get("numero_comprobante"))
    
    def create_detail(self, detail_data: Dict[str, Any]) -> bool:
        """Crea un detalle de venta"""
        return self.detail_handler.append(detail_data)
    
    def update(self, sale_id: int, sale_data: Dict[str, Any]) -> bool:
        """Actualiza una venta existente"""
        return self.csv_handler.update(sale_id, sale_data)
    
    def delete(self, sale_id: int) -> bool:
        """Marca una venta como anulada"""
        from datetime import datetime
        return self.csv_handler.update(sale_id, {
            "estado": "ANULADA",
            "updated_at": datetime.now().isoformat()
        })
    
    def get_next_numero_comprobante(self, tipo: str) -> str:
        """Genera el siguiente número de comprobante"""
        from datetime import datetime
        sales = self.find_all()
        
        # Obtener el año actual
        year = datetime.now().year
        
        # Prefijo según tipo
        prefix = "B" if tipo == "BOLETA" else "F"
        
        # Contar comprobantes del año y tipo actual
        year_sales = [
            s for s in sales
            if s.get('numero_comprobante', '').startswith(f"{prefix}{year}")
        ]
        
        next_number = len(year_sales) + 1
        return f"{prefix}{year}-{next_number:06d}"


# Singleton
sale_repository = SaleRepository()
