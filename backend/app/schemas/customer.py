"""
Schemas para Clientes
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from decimal import Decimal


class CustomerBase(BaseModel):
    """Schema base de cliente"""
    tipo_documento: str = Field(..., description="DNI o RUC")
    numero_documento: str = Field(..., min_length=8, max_length=11, description="DNI (8) o RUC (11)")
    nombres: Optional[str] = Field(None, max_length=200, description="Nombres (para persona natural)")
    apellidos: Optional[str] = Field(None, max_length=200, description="Apellidos (para persona natural)")
    razon_social: Optional[str] = Field(None, max_length=200, description="Razón social (para empresa)")
    nombre_comercial: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    limite_credito: Decimal = Field(default=Decimal('0'), ge=0, description="Límite de crédito en soles")


class CustomerCreate(CustomerBase):
    """Schema para crear un cliente"""
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tipo_documento": "DNI",
                    "numero_documento": "45678912",
                    "nombres": "Carlos",
                    "apellidos": "Mendoza García",
                    "telefono": "987654321",
                    "email": "carlos.mendoza@email.com",
                    "direccion": "Av. Los Pinos 456, San Miguel",
                    "limite_credito": 5000.00
                }
            ]
        }
    }


class CustomerUpdate(BaseModel):
    """Schema para actualizar un cliente"""
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = Field(None, min_length=8, max_length=11)
    nombres: Optional[str] = Field(None, max_length=200)
    apellidos: Optional[str] = Field(None, max_length=200)
    razon_social: Optional[str] = Field(None, max_length=200)
    nombre_comercial: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    limite_credito: Optional[Decimal] = Field(None, ge=0)
    activo: Optional[bool] = None


class CustomerResponse(CustomerBase):
    """Schema de respuesta de cliente"""
    id: int
    activo: bool
    created_at: str
    updated_at: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "tipo_documento": "DNI",
                    "numero_documento": "45678912",
                    "nombres": "Carlos",
                    "apellidos": "Mendoza García",
                    "razon_social": None,
                    "nombre_comercial": None,
                    "telefono": "987654321",
                    "email": "carlos.mendoza@email.com",
                    "direccion": "Av. Los Pinos 456, San Miguel",
                    "limite_credito": 5000.00,
                    "activo": True,
                    "created_at": "2026-08-10 09:00:00",
                    "updated_at": "2026-08-10 09:00:00"
                }
            ]
        }
    }


class CustomerWithStats(CustomerResponse):
    """Schema de cliente con estadísticas"""
    total_compras: int = Field(..., description="Total de compras realizadas")
    monto_total_compras: Decimal = Field(..., description="Monto total de compras")
    saldo_pendiente: Decimal = Field(..., description="Saldo por cobrar")
    disponible_credito: Decimal = Field(..., description="Crédito disponible")
