"""
Configuración de la aplicación usando Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Application
    APP_NAME: str = "ERP Ferretería"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Data Storage (CSV files)
    DATA_DIR: Path = Path("data")
    
    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # AWS (opcional para producción)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = "erp-ferreteria-docs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()

# Crear directorio de datos si no existe
settings.DATA_DIR.mkdir(exist_ok=True)
