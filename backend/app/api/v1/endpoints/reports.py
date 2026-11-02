"""
Endpoints de Reportes y Auditoría
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date
from app.schemas.report import (
    InventoryReport, SalesReport, PurchasesReport,
    MovementReport, DashboardStats, AuditLog
)
from app.schemas.auth import UserResponse
from app.services.report_service import report_service
from app.security.dependencies import get_current_active_user, require_role

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats, summary="Dashboard principal")
async def get_dashboard():
    """
    Obtiene estadísticas generales para el dashboard:
    - Ventas del día y del mes
    - Compras del mes
    - Estado del inventario
    - Utilidad bruta y margen promedio
    - Top 5 productos, clientes y proveedores
    
    **Requiere rol:** admin
    """
    return report_service.get_dashboard_stats()


@router.get("/recent-activity", summary="Actividad reciente")
async def get_recent_activity():
    """
    Obtiene las últimas acciones realizadas en el sistema
    para mostrar actividad en tiempo real
    """
    return report_service.get_recent_activity()


@router.get("/inventory", response_model=InventoryReport, summary="Reporte de inventario")
async def get_inventory_report(
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Genera reporte completo de inventario con:
    - Valor total del inventario
    - Productos por estado (OK/REPONER/AGOTADO)
    - Detalle de cada producto con márgenes
    
    **Requiere rol:** admin o almacenero
    """
    return report_service.get_inventory_report()


@router.get("/sales", response_model=SalesReport, summary="Reporte de ventas")
async def get_sales_report(
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    """
    Genera reporte de ventas con utilidad bruta:
    - Total vendido y costo
    - Utilidad bruta y margen promedio
    - Desglose por condición de pago (contado/crédito)
    - Detalle de cada venta con utilidad
    
    **Requiere rol:** admin o vendedor
    
    **Por defecto:** Mes actual si no se especifican fechas
    """
    return report_service.get_sales_report(fecha_inicio, fecha_fin)


@router.get("/purchases", response_model=PurchasesReport, summary="Reporte de compras")
async def get_purchases_report(
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Genera reporte de compras:
    - Total gastado y compra promedio
    - Detalle de cada compra
    
    **Requiere rol:** admin o almacenero
    
    **Por defecto:** Mes actual si no se especifican fechas
    """
    return report_service.get_purchases_report(fecha_inicio, fecha_fin)


@router.get("/movements/{producto_id}", response_model=MovementReport, summary="Movimientos de producto")
async def get_movement_report(
    producto_id: int,
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Genera reporte de movimientos de un producto específico:
    - Stock inicial y final
    - Total de entradas (compras) y salidas (ventas)
    - Detalle de cada movimiento con stock resultante
    
    **Requiere rol:** admin o almacenero
    
    **Por defecto:** Mes actual si no se especifican fechas
    """
    try:
        return report_service.get_movement_report(producto_id, fecha_inicio, fecha_fin)
    except ValueError as e:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/audit", response_model=List[AuditLog], summary="Logs de auditoría")
async def get_audit_logs(
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    usuario: Optional[str] = Query(None, description="Filtrar por usuario"),
    modulo: Optional[str] = Query(None, description="Filtrar por módulo"),
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Obtiene logs de auditoría del sistema:
    - Acciones realizadas por usuarios
    - Módulo afectado
    - Fecha y hora
    - Detalles de la acción
    
    **Requiere rol:** admin
    
    **Nota:** Retorna los últimos 100 registros
    """
    return report_service.get_audit_logs(fecha_inicio, fecha_fin, usuario, modulo)
