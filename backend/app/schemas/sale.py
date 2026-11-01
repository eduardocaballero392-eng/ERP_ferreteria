"""
Schemas para Ventas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime


class SaleDetailBase(BaseModel):
    """Schema base de detalle de venta"""
    producto_id: int = Field(..., description="ID del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad vendida")
    precio_unitario: Decimal = Field(..., gt=0, decimal_places=2, description="Precio unitario sin IGV")


class SaleDetailCreate(SaleDetailBase):
    """Schema para crear un detalle de venta"""
    pass


class SaleDetailResponse(SaleDetailBase):
    """Schema de respuesta de detalle de venta"""
    id: int
    venta_id: int
    subtotal: Decimal
    created_at: str
    
    # Información adicional del producto
    producto_nombre: Optional[str] = None
    producto_sku: Optional[str] = None


class SaleBase(BaseModel):
    """Schema base de venta"""
    cliente_id: int = Field(..., description="ID del cliente")
    tipo_comprobante: str = Field(..., description="BOLETA o FACTURA")
    condicion_pago: str = Field(..., description="CONTADO o CREDITO")
    observaciones: Optional[str] = Field(None, description="Observaciones de la venta")


class SaleCreate(SaleBase):
    """Schema para crear una venta"""
    fecha: Optional[datetime] = Field(None, description="Fecha de la venta (por defecto: ahora)")
    detalles: List[SaleDetailCreate] = Field(..., min_length=1, description="Items de la venta")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cliente_id": 1,
                    "tipo_comprobante": "BOLETA",
                    "condicion_pago": "CONTADO",
                    "fecha": "2026-10-31 15:00:00",
                    "observaciones": "Venta de materiales de construcción",
                    "detalles": [
                        {
                            "producto_id": 1,
                            "cantidad": 10,
                            "precio_unitario": 28.00
                        },
                        {
                            "producto_id": 2,
                            "cantidad": 20,
                            "precio_unitario": 45.00
                        }
                    ]
                }
            ]
        }
    }


class SaleUpdate(BaseModel):
    """Schema para actualizar una venta"""
    observaciones: Optional[str] = None
    estado: Optional[str] = Field(None, description="COMPLETADA o ANULADA")


class SaleResponse(SaleBase):
    """Schema de respuesta de venta"""
    id: int
    numero_comprobante: str
    fecha: str
    subtotal: Decimal
    igv: Decimal
    total: Decimal
    estado: str
    created_at: str
    updated_at: Optional[str] = None
    
    # Información adicional del cliente
    cliente_nombre: Optional[str] = None
    cliente_documento: Optional[str] = None


class SaleWithDetails(SaleResponse):
    """Schema de venta con detalles"""
    detalles: List[SaleDetailResponse] = Field(..., description="Items de la venta")


class SaleStats(BaseModel):
    """Schema de estadísticas de ventas"""
    total_ventas: int
    total_vendido: Decimal
    venta_promedio: Decimal
    cliente_principal: Optional[str] = None
    ventas_contado: int
    ventas_credito: int
    monto_contado: Decimal
    monto_credito: Decimal
