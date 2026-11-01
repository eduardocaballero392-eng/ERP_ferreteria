"""
Schemas para Reportes
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import date


class InventoryReportItem(BaseModel):
    """Item del reporte de inventario"""
    producto_id: int
    sku: str
    nombre: str
    categoria: str
    stock_actual: int
    stock_minimo: int
    estado_stock: str
    costo_unitario: Decimal
    precio_venta: Decimal
    valor_inventario: Decimal
    margen_unitario: Decimal
    margen_porcentaje: Decimal


class InventoryReport(BaseModel):
    """Reporte de inventario"""
    total_productos: int
    valor_total_inventario: Decimal
    productos_ok: int
    productos_reponer: int
    productos_agotados: int
    items: List[InventoryReportItem]


class SalesReportItem(BaseModel):
    """Item del reporte de ventas"""
    venta_id: int
    numero_comprobante: str
    fecha: str
    cliente_nombre: str
    tipo_comprobante: str
    condicion_pago: str
    subtotal: Decimal
    igv: Decimal
    total: Decimal
    utilidad_bruta: Decimal
    margen_porcentaje: Decimal


class SalesReport(BaseModel):
    """Reporte de ventas"""
    fecha_inicio: str
    fecha_fin: str
    total_ventas: int
    total_vendido: Decimal
    total_costo: Decimal
    utilidad_bruta: Decimal
    margen_promedio: Decimal
    ventas_contado: int
    ventas_credito: int
    monto_contado: Decimal
    monto_credito: Decimal
    items: List[SalesReportItem]


class PurchasesReportItem(BaseModel):
    """Item del reporte de compras"""
    compra_id: int
    numero_orden: str
    fecha: str
    proveedor_nombre: str
    subtotal: Decimal
    igv: Decimal
    total: Decimal


class PurchasesReport(BaseModel):
    """Reporte de compras"""
    fecha_inicio: str
    fecha_fin: str
    total_compras: int
    total_gastado: Decimal
    compra_promedio: Decimal
    items: List[PurchasesReportItem]


class ProductMovement(BaseModel):
    """Movimiento de un producto"""
    fecha: str
    tipo: str  # COMPRA, VENTA, AJUSTE
    referencia: str
    cantidad: int
    tipo_movimiento: str  # ENTRADA, SALIDA
    stock_anterior: int
    stock_nuevo: int
    motivo: Optional[str] = None


class MovementReport(BaseModel):
    """Reporte de movimientos de inventario"""
    producto_id: int
    producto_nombre: str
    sku: str
    fecha_inicio: str
    fecha_fin: str
    stock_inicial: int
    total_entradas: int
    total_salidas: int
    stock_final: int
    movimientos: List[ProductMovement]


class TopProduct(BaseModel):
    """Producto más vendido"""
    producto_id: int
    nombre: str
    sku: str
    cantidad_vendida: int
    monto_total: Decimal


class TopCustomer(BaseModel):
    """Cliente que más compra"""
    cliente_id: int
    nombre: str
    documento: str
    total_compras: int
    monto_total: Decimal


class TopSupplier(BaseModel):
    """Proveedor principal"""
    proveedor_id: int
    razon_social: str
    ruc: str
    total_compras: int
    monto_total: Decimal


class DashboardStats(BaseModel):
    """Estadísticas del dashboard"""
    # Ventas
    ventas_hoy: int
    ventas_mes: int
    total_vendido_mes: Decimal
    
    # Compras
    compras_mes: int
    total_gastado_mes: Decimal
    
    # Inventario
    productos_total: int
    productos_stock_bajo: int
    valor_inventario: Decimal
    
    # Utilidad
    utilidad_bruta_mes: Decimal
    margen_promedio_mes: Decimal
    
    # Top 5
    top_productos: List[TopProduct]
    top_clientes: List[TopCustomer]
    top_proveedores: List[TopSupplier]


class AuditLog(BaseModel):
    """Log de auditoría"""
    id: int
    fecha: str
    usuario: str
    accion: str
    modulo: str
    registro_id: Optional[int] = None
    detalles: Optional[str] = None
    ip_address: Optional[str] = None
