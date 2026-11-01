"""
Schemas para autenticación y autorización
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema para datos decodificados del token"""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema para solicitud de login"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "admin@ferreteria.com",
                    "password": "admin123"
                }
            ]
        }
    }


class UserCreate(BaseModel):
    """Schema para crear un nuevo usuario"""
    email: EmailStr
    nombre: str = Field(..., min_length=2, max_length=200)
    apellido: str = Field(..., min_length=2, max_length=200)
    password: str = Field(..., min_length=6)
    role: str = Field(..., description="admin, vendedor, o almacenero")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "nuevo@ferreteria.com",
                    "nombre": "Juan",
                    "apellido": "Pérez",
                    "password": "mipassword123",
                    "role": "vendedor"
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """Schema para respuesta de usuario"""
    id: int
    email: str
    nombre: str
    apellido: str
    role: str
    activo: bool
    created_at: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "email": "admin@ferreteria.com",
                    "nombre": "Carlos",
                    "apellido": "Mendoza",
                    "role": "admin",
                    "activo": True,
                    "created_at": "2026-10-01 08:00:00"
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=200)
    apellido: Optional[str] = Field(None, min_length=2, max_length=200)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[str] = None
    activo: Optional[bool] = None


class ChangePasswordRequest(BaseModel):
    """Schema para cambio de contraseña"""
    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "current_password": "oldpass123",
                    "new_password": "newpass456"
                }
            ]
        }
    }
