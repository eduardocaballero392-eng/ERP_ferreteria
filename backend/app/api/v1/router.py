"""
Router principal de API v1
Aquí se registran todos los endpoints de los módulos
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, categories, products, suppliers, purchases, customers, sales, reports, upload

# Crear router principal
api_router = APIRouter()

# Registrar routers de cada módulo
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categorías"])
api_router.include_router(products.router, prefix="/products", tags=["Productos"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Proveedores"])
api_router.include_router(purchases.router, prefix="/purchases", tags=["Compras"])
api_router.include_router(customers.router, prefix="/customers", tags=["Clientes"])
api_router.include_router(sales.router, prefix="/sales", tags=["Ventas"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reportes y Auditoría"])
api_router.include_router(upload.router, prefix="/upload", tags=["Carga de Datos"])

# TODO: Importar y registrar otros routers
# from app.api.v1.endpoints import payments

# api_router.include_router(payments.router, prefix="/payments", tags=["Pagos"])


@api_router.get("/")
async def api_root():
    """Endpoint raíz de la API"""
    return {
        "message": "API v1 - ERP Ferretería",
        "version": "1.0.0",
        "status": "active",
        "authentication": "JWT Bearer Token",
        "endpoints": {
            "auth": "/api/v1/auth",
            "docs": "/api/docs",
            "users": "/api/v1/users",
            "categories": "/api/v1/categories",
            "products": "/api/v1/products",
            "suppliers": "/api/v1/suppliers",
            "customers": "/api/v1/customers",
            "purchases": "/api/v1/purchases",
            "sales": "/api/v1/sales",
            "payments": "/api/v1/payments",
            "reports": "/api/v1/reports"
        }
    }
