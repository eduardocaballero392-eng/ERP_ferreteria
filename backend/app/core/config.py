"""
Configuración de la aplicación usando Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path
from pydantic import field_validator
import shutil


BACKEND_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = BACKEND_DIR / "data"


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Application
    APP_NAME: str = "ERP Ferretería"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CSV files are the single source of truth for application data.
    DATA_DIR: Path = DEFAULT_DATA_DIR
    
    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = ",".join([
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:3002",
        "http://localhost:5173"
    ])
    
    # AWS (opcional para producción)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = "erp-ferreteria-docs"
    
    @field_validator("DATA_DIR", mode="before")
    @classmethod
    def resolve_data_dir(cls, value):
        path = Path(value)
        return path if path.is_absolute() else BACKEND_DIR / path

    class Config:
        env_file = BACKEND_DIR / ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()

if not settings.DEBUG and settings.SECRET_KEY == "change-this-secret-key-in-production":
    raise RuntimeError("Define SECRET_KEY before running with DEBUG=false")


def get_allowed_origins() -> List[str]:
    origins = [origin.strip().rstrip("/") for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]
    # Keep local Vite origins available even when .env customizes production origins.
    if settings.DEBUG:
        origins.extend(["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"])
    return list(dict.fromkeys(origins))

# Crear directorio de datos si no existe
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
if settings.DATA_DIR != DEFAULT_DATA_DIR:
    for source in DEFAULT_DATA_DIR.glob("*.csv"):
        destination = settings.DATA_DIR / source.name
        if not destination.exists():
            shutil.copy2(source, destination)
