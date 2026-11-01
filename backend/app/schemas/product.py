"""
Schemas para Productos
"""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProductBase(BaseModel):
    """Schema base de producto"""
    sku: str = Field(..., min_length=2, max_length=50, description="Código SKU único")
    nombre: str = Field(..., min_length=2, max_length=200, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    categoria_id: int = Field(..., description="ID de la categoría")
    unidad_medida: str = Field(..., max_length=20, description="UND, MT, KG, LT, etc.")
    stock_minimo: int = Field(..., ge=0, description="Stock mínimo para alerta")
    costo_unitario: Decimal = Field(..., gt=0, decimal_places=2, description="Costo sin IGV")
    precio_venta: Decimal = Field(..., gt=0, decimal_places=2, description="Precio sin IGV")


class ProductCreate(ProductBase):
    """Schema para crear un producto"""
    stock_actual: int = Field(0, ge=0, description="Stock inicial")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sku": "CEM-001",
                    "nombre": "Cemento Andino Tipo I x 42.5 kg",
                    "descripcion": "Cemento portland tipo I para construcción general",
                    "categoria_id": 1,
                    "stock_actual": 100,
                    "stock_minimo": 50,
                    "unidad_medida": "UND",
                    "costo_unitario": 22.50,
                    "precio_venta": 28.00
                }
            ]
        }
    }


class ProductUpdate(BaseModel):
    """Schema para actualizar un producto"""
    sku: Optional[str] = Field(None, min_length=2, max_length=50)
    nombre: Optional[str] = Field(None, min_length=2, max_length=200)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    stock_actual: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    unidad_medida: Optional[str] = Field(None, max_length=20)
    costo_unitario: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    precio_venta: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    activo: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema de respuesta de producto"""
    id: int
    stock_actual: int
    activo: bool
    created_at: str
    updated_at: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "sku": "CEM-001",
                    "nombre": "Cemento Andino Tipo I x 42.5 kg",
                    "descripcion": "Cemento portland tipo I",
                    "categoria_id": 1,
                    "stock_actual": 245,
                    "stock_minimo": 50,
                    "unidad_medida": "UND",
                    "costo_unitario": 22.50,
                    "precio_venta": 28.00,
                    "activo": True,
                    "created_at": "2026-10-01 08:00:00",
                    "updated_at": "2026-10-31 14:30:00"
                }
            ]
        }
    }


class ProductWithDetails(ProductResponse):
    """Schema de producto con detalles adicionales"""
    estado_stock: str = Field(..., description="OK, REPONER, AGOTADO")
    valor_inventario: Decimal = Field(..., description="stock_actual * costo_unitario")
    margen_utilidad: Decimal = Field(..., description="Porcentaje de utilidad")
    categoria_nombre: Optional[str] = Field(None, description="Nombre de la categoría")


class ProductStockAdjust(BaseModel):
    """Schema para ajustar stock manualmente"""
    cantidad: int = Field(..., description="Cantidad a ajustar (positivo o negativo)")
    motivo: str = Field(..., min_length=5, description="Motivo del ajuste")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cantidad": -5,
                    "motivo": "Productos dañados en almacén"
                }
            ]
        }
    }


class ProductSearchFilters(BaseModel):
    """Schema para filtros de búsqueda"""
    categoria_id: Optional[int] = None
    estado_stock: Optional[str] = Field(None, description="OK, REPONER, AGOTADO")
    activo: Optional[bool] = None
    buscar: Optional[str] = Field(None, description="Buscar en nombre, SKU o descripción")
