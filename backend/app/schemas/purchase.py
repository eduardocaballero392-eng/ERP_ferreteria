"""
Schemas para Compras
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime


class PurchaseDetailBase(BaseModel):
    """Schema base de detalle de compra"""
    producto_id: int = Field(..., description="ID del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad comprada")
    costo_unitario: Decimal = Field(..., gt=0, decimal_places=2, description="Costo unitario sin IGV")


class PurchaseDetailCreate(PurchaseDetailBase):
    """Schema para crear un detalle de compra"""
    pass


class PurchaseDetailResponse(PurchaseDetailBase):
    """Schema de respuesta de detalle de compra"""
    id: int
    compra_id: int
    subtotal: Decimal
    created_at: str
    
    # Información adicional del producto
    producto_nombre: Optional[str] = None
    producto_sku: Optional[str] = None


class PurchaseBase(BaseModel):
    """Schema base de compra"""
    proveedor_id: int = Field(..., description="ID del proveedor")
    observaciones: Optional[str] = Field(None, description="Observaciones de la compra")


class PurchaseCreate(PurchaseBase):
    """Schema para crear una compra"""
    fecha: Optional[datetime] = Field(None, description="Fecha de la compra (por defecto: ahora)")
    detalles: List[PurchaseDetailCreate] = Field(..., min_length=1, description="Items de la compra")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "proveedor_id": 1,
                    "fecha": "2026-10-31 10:00:00",
                    "observaciones": "Compra de cemento y agregados",
                    "detalles": [
                        {
                            "producto_id": 1,
                            "cantidad": 50,
                            "costo_unitario": 22.50
                        },
                        {
                            "producto_id": 6,
                            "cantidad": 500,
                            "costo_unitario": 0.85
                        }
                    ]
                }
            ]
        }
    }


class PurchaseUpdate(BaseModel):
    """Schema para actualizar una compra"""
    observaciones: Optional[str] = None
    estado: Optional[str] = Field(None, description="COMPLETADA o ANULADA")


class PurchaseResponse(PurchaseBase):
    """Schema de respuesta de compra"""
    id: int
    numero_orden: str
    fecha: str
    subtotal: Decimal
    igv: Decimal
    total: Decimal
    estado: str
    created_at: str
    updated_at: Optional[str] = None
    
    # Información adicional del proveedor
    proveedor_nombre: Optional[str] = None
    proveedor_ruc: Optional[str] = None


class PurchaseWithDetails(PurchaseResponse):
    """Schema de compra con detalles"""
    detalles: List[PurchaseDetailResponse] = Field(..., description="Items de la compra")


class PurchaseStats(BaseModel):
    """Schema de estadísticas de compras"""
    total_compras: int
    total_gastado: Decimal
    compra_promedio: Decimal
    proveedor_principal: Optional[str] = None
