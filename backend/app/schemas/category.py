"""
Schemas para Categorías
"""
from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    """Schema base de categoría"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")


class CategoryCreate(CategoryBase):
    """Schema para crear una categoría"""
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Cemento y Agregados",
                    "descripcion": "Cemento, arena, piedra, ladrillos"
                }
            ]
        }
    }


class CategoryUpdate(BaseModel):
    """Schema para actualizar una categoría"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Schema de respuesta de categoría"""
    id: int
    activo: bool
    created_at: str
    updated_at: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "nombre": "Cemento y Agregados",
                    "descripcion": "Cemento, arena, piedra, ladrillos",
                    "activo": True,
                    "created_at": "2026-10-01 08:00:00",
                    "updated_at": "2026-10-01 08:00:00"
                }
            ]
        }
    }


class CategoryWithProductCount(CategoryResponse):
    """Schema de categoría con conteo de productos"""
    total_productos: int = Field(..., description="Total de productos en esta categoría")
