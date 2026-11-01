"""
Schemas para Proveedores
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SupplierBase(BaseModel):
    """Schema base de proveedor"""
    ruc: str = Field(..., min_length=11, max_length=11, description="RUC del proveedor (11 dígitos)")
    razon_social: str = Field(..., min_length=2, max_length=200, description="Razón social")
    nombre_comercial: Optional[str] = Field(None, max_length=200, description="Nombre comercial")
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    contacto_nombre: Optional[str] = Field(None, max_length=200, description="Nombre del contacto")
    contacto_telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del contacto")


class SupplierCreate(SupplierBase):
    """Schema para crear un proveedor"""
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ruc": "20518520442",
                    "razon_social": "Distribuidora Andina SAC",
                    "nombre_comercial": "Dist. Andina",
                    "telefono": "015551234",
                    "email": "ventas@andina.com.pe",
                    "direccion": "Av. Argentina 2850, Callao",
                    "contacto_nombre": "Roberto Paredes",
                    "contacto_telefono": "987654321"
                }
            ]
        }
    }


class SupplierUpdate(BaseModel):
    """Schema para actualizar un proveedor"""
    ruc: Optional[str] = Field(None, min_length=11, max_length=11)
    razon_social: Optional[str] = Field(None, min_length=2, max_length=200)
    nombre_comercial: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    contacto_nombre: Optional[str] = Field(None, max_length=200)
    contacto_telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None


class SupplierResponse(SupplierBase):
    """Schema de respuesta de proveedor"""
    id: int
    activo: bool
    created_at: str
    updated_at: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "ruc": "20518520442",
                    "razon_social": "Distribuidora Andina SAC",
                    "nombre_comercial": "Dist. Andina",
                    "telefono": "015551234",
                    "email": "ventas@andina.com.pe",
                    "direccion": "Av. Argentina 2850, Callao",
                    "contacto_nombre": "Roberto Paredes",
                    "contacto_telefono": "987654321",
                    "activo": True,
                    "created_at": "2026-09-15 09:00:00",
                    "updated_at": "2026-09-15 09:00:00"
                }
            ]
        }
    }


class SupplierWithStats(SupplierResponse):
    """Schema de proveedor con estadísticas"""
    total_compras: int = Field(..., description="Total de compras realizadas")
    monto_total_compras: float = Field(..., description="Monto total de compras")
