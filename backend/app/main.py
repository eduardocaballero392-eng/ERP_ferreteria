"""
FastAPI Application - Main Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_allowed_origins, settings

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema ERP para gestión de ferretería en Perú",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configurar CORS - Permitir todos los orígenes en desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Importar y registrar routers de la API
from app.api.v1.router import api_router
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def provision_default_admin():
    """Asegura la cuenta inicial en cada entorno con almacenamiento persistente."""
    from app.services.auth_service import auth_service
    auth_service.ensure_default_admin()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
