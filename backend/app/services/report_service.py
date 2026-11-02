"""
Servicio de Reportes - Lógica de negocio
"""
from typing import List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from collections import Counter, defaultdict
from app.schemas.report import (
    InventoryReport, InventoryReportItem,
    SalesReport, SalesReportItem,
    PurchasesReport, PurchasesReportItem,
    MovementReport, ProductMovement,
    DashboardStats, TopProduct, TopCustomer, TopSupplier,
    AuditLog
)
from app.repositories.product_repository import product_repository
from app.repositories.category_repository import category_repository
from app.repositories.sale_repository import sale_repository
from app.repositories.purchase_repository import purchase_repository
from app.repositories.customer_repository import customer_repository
from app.repositories.supplier_repository import supplier_repository
from app.core.csv_handler import get_csv_handler


class ReportService:
    """Servicio de generación de reportes"""
    
    def __init__(self):
        self.product_repo = product_repository
        self.category_repo = category_repository
        self.sale_repo = sale_repository
        self.purchase_repo = purchase_repository
        self.customer_repo = customer_repository
        self.supplier_repo = supplier_repository
        self.audit_handler = get_csv_handler("auditoria.csv")
    
    def get_inventory_report(self) -> InventoryReport:
        """Genera reporte de inventario"""
        products = self.product_repo.find_all()
        
        items = []
        valor_total = Decimal('0')
        productos_ok = 0
        productos_reponer = 0
        productos_agotados = 0
        
        for product in products:
            # Obtener categoría
            category = self.category_repo.find_by_id(product.get('categoria_id'))
            categoria_nombre = category.get('nombre') if category else 'Sin categoría'
            
            # Calcular valores
            stock_actual = int(product.get('stock_actual', 0))
            costo = Decimal(str(product.get('costo_unitario', 0)))
            precio = Decimal(str(product.get('precio_venta', 0)))
            valor_inv = Decimal(str(stock_actual)) * costo
            margen_unit = precio - costo
            margen_pct = (margen_unit / precio * 100) if precio > 0 else Decimal('0')
            
            valor_total += valor_inv
            
            # Contar por estado
            estado = product.get('estado_stock', 'OK')
            if estado == 'OK':
                productos_ok += 1
            elif estado == 'REPONER':
                productos_reponer += 1
            elif estado == 'AGOTADO':
                productos_agotados += 1
            
            items.append(InventoryReportItem(
                producto_id=product['id'],
                sku=product.get('sku', ''),
                nombre=product.get('nombre', ''),
                categoria=categoria_nombre,
                stock_actual=stock_actual,
                stock_minimo=int(product.get('stock_minimo', 0)),
                estado_stock=estado,
                costo_unitario=costo,
                precio_venta=precio,
                valor_inventario=valor_inv,
                margen_unitario=margen_unit,
                margen_porcentaje=margen_pct
            ))
        
        return InventoryReport(
            total_productos=len(products),
            valor_total_inventario=valor_total,
            productos_ok=productos_ok,
            productos_reponer=productos_reponer,
            productos_agotados=productos_agotados,
            items=sorted(items, key=lambda x: x.valor_inventario, reverse=True)
        )
    
    def get_sales_report(
        self,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> SalesReport:
        """Genera reporte de ventas con utilidad bruta"""
        # Fechas por defecto: mes actual
        if not fecha_inicio:
            fecha_inicio = date.today().replace(day=1)
        if not fecha_fin:
            fecha_fin = date.today()
        
        sales = self.sale_repo.find_all()
        sales_completadas = [s for s in sales if s.get('estado') == 'COMPLETADA']
        
        # Filtrar por rango de fechas
        sales_filtered = []
        for sale in sales_completadas:
            fecha_venta = datetime.fromisoformat(sale.get('fecha')).date()
            if fecha_inicio <= fecha_venta <= fecha_fin:
                sales_filtered.append(sale)
        
        items = []
        total_vendido = Decimal('0')
        total_costo = Decimal('0')
        ventas_contado = 0
        ventas_credito = 0
        monto_contado = Decimal('0')
        monto_credito = Decimal('0')
        
        for sale in sales_filtered:
            # Obtener cliente
            customer = self.customer_repo.find_by_id(sale.get('cliente_id'))
            if customer:
                if customer.get('razon_social'):
                    cliente_nombre = customer.get('razon_social')
                else:
                    cliente_nombre = f"{customer.get('nombres', '')} {customer.get('apellidos', '')}".strip()
            else:
                cliente_nombre = 'Cliente desconocido'
            
            # Obtener detalles para calcular costo
            details = self.sale_repo.get_details(sale['id'])
            costo_venta = Decimal('0')
            
            for detail in details:
                product = self.product_repo.find_by_id(detail.get('producto_id'))
                if product:
                    costo_unit = Decimal(str(product.get('costo_unitario', 0)))
                    cantidad = int(detail.get('cantidad', 0))
                    costo_venta += costo_unit * Decimal(str(cantidad))
            
            total = Decimal(str(sale.get('total', 0)))
            utilidad = total - (costo_venta * Decimal('1.18'))  # Ajustar por IGV
            margen = (utilidad / total * 100) if total > 0 else Decimal('0')
            
            total_vendido += total
            total_costo += costo_venta
            
            # Contar por condición de pago
            if sale.get('condicion_pago') == 'CONTADO':
                ventas_contado += 1
                monto_contado += total
            else:
                ventas_credito += 1
                monto_credito += total
            
            items.append(SalesReportItem(
                venta_id=sale['id'],
                numero_comprobante=sale.get('numero_comprobante', ''),
                fecha=sale.get('fecha', ''),
                cliente_nombre=cliente_nombre,
                tipo_comprobante=sale.get('tipo_comprobante', ''),
                condicion_pago=sale.get('condicion_pago', ''),
                subtotal=Decimal(str(sale.get('subtotal', 0))),
                igv=Decimal(str(sale.get('igv', 0))),
                total=total,
                utilidad_bruta=utilidad,
                margen_porcentaje=margen
            ))
        
        utilidad_total = total_vendido - (total_costo * Decimal('1.18'))
        margen_promedio = (utilidad_total / total_vendido * 100) if total_vendido > 0 else Decimal('0')
        
        return SalesReport(
            fecha_inicio=fecha_inicio.isoformat(),
            fecha_fin=fecha_fin.isoformat(),
            total_ventas=len(sales_filtered),
            total_vendido=total_vendido,
            total_costo=total_costo * Decimal('1.18'),
            utilidad_bruta=utilidad_total,
            margen_promedio=margen_promedio,
            ventas_contado=ventas_contado,
            ventas_credito=ventas_credito,
            monto_contado=monto_contado,
            monto_credito=monto_credito,
            items=sorted(items, key=lambda x: x.fecha, reverse=True)
        )
    
    def get_purchases_report(
        self,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> PurchasesReport:
        """Genera reporte de compras"""
        # Fechas por defecto: mes actual
        if not fecha_inicio:
            fecha_inicio = date.today().replace(day=1)
        if not fecha_fin:
            fecha_fin = date.today()
        
        purchases = self.purchase_repo.find_all()
        purchases_completadas = [p for p in purchases if p.get('estado') == 'COMPLETADA']
        
        # Filtrar por rango de fechas
        purchases_filtered = []
        for purchase in purchases_completadas:
            fecha_compra = datetime.fromisoformat(purchase.get('fecha')).date()
            if fecha_inicio <= fecha_compra <= fecha_fin:
                purchases_filtered.append(purchase)
        
        items = []
        total_gastado = Decimal('0')
        
        for purchase in purchases_filtered:
            # Obtener proveedor
            supplier = self.supplier_repo.find_by_id(purchase.get('proveedor_id'))
            proveedor_nombre = supplier.get('razon_social') if supplier else 'Proveedor desconocido'
            
            total = Decimal(str(purchase.get('total', 0)))
            total_gastado += total
            
            items.append(PurchasesReportItem(
                compra_id=purchase['id'],
                numero_orden=purchase.get('numero_orden', ''),
                fecha=purchase.get('fecha', ''),
                proveedor_nombre=proveedor_nombre,
                subtotal=Decimal(str(purchase.get('subtotal', 0))),
                igv=Decimal(str(purchase.get('igv', 0))),
                total=total
            ))
        
        compra_promedio = total_gastado / len(purchases_filtered) if purchases_filtered else Decimal('0')
        
        return PurchasesReport(
            fecha_inicio=fecha_inicio.isoformat(),
            fecha_fin=fecha_fin.isoformat(),
            total_compras=len(purchases_filtered),
            total_gastado=total_gastado,
            compra_promedio=compra_promedio,
            items=sorted(items, key=lambda x: x.fecha, reverse=True)
        )
    
    def get_movement_report(
        self,
        producto_id: int,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> MovementReport:
        """Genera reporte de movimientos de un producto"""
        # Verificar que el producto existe
        product = self.product_repo.find_by_id(producto_id)
        if not product:
            raise ValueError(f"Producto con ID {producto_id} no encontrado")
        
        # Fechas por defecto: mes actual
        if not fecha_inicio:
            fecha_inicio = date.today().replace(day=1)
        if not fecha_fin:
            fecha_fin = date.today()
        
        movimientos = []
        
        # Obtener compras del producto
        purchases = self.purchase_repo.find_all()
        for purchase in purchases:
            if purchase.get('estado') != 'COMPLETADA':
                continue
            
            fecha_compra = datetime.fromisoformat(purchase.get('fecha')).date()
            if not (fecha_inicio <= fecha_compra <= fecha_fin):
                continue
            
            details = self.purchase_repo.get_details(purchase['id'])
            for detail in details:
                if detail.get('producto_id') == producto_id:
                    movimientos.append({
                        'fecha': purchase.get('fecha'),
                        'tipo': 'COMPRA',
                        'referencia': purchase.get('numero_orden'),
                        'cantidad': int(detail.get('cantidad', 0)),
                        'tipo_movimiento': 'ENTRADA',
                        'motivo': None
                    })
        
        # Obtener ventas del producto
        sales = self.sale_repo.find_all()
        for sale in sales:
            if sale.get('estado') != 'COMPLETADA':
                continue
            
            fecha_venta = datetime.fromisoformat(sale.get('fecha')).date()
            if not (fecha_inicio <= fecha_venta <= fecha_fin):
                continue
            
            details = self.sale_repo.get_details(sale['id'])
            for detail in details:
                if detail.get('producto_id') == producto_id:
                    movimientos.append({
                        'fecha': sale.get('fecha'),
                        'tipo': 'VENTA',
                        'referencia': sale.get('numero_comprobante'),
                        'cantidad': int(detail.get('cantidad', 0)),
                        'tipo_movimiento': 'SALIDA',
                        'motivo': None
                    })
        
        # Ordenar por fecha
        movimientos.sort(key=lambda x: x['fecha'])
        
        # Calcular stock en cada movimiento
        stock_actual = int(product.get('stock_actual', 0))
        
        # Calcular stock inicial (restar movimientos hacia atrás)
        total_entradas = sum(m['cantidad'] for m in movimientos if m['tipo_movimiento'] == 'ENTRADA')
        total_salidas = sum(m['cantidad'] for m in movimientos if m['tipo_movimiento'] == 'SALIDA')
        stock_inicial = stock_actual - total_entradas + total_salidas
        
        # Construir movimientos con stock
        stock_temp = stock_inicial
        movements_list = []
        
        for mov in movimientos:
            stock_anterior = stock_temp
            if mov['tipo_movimiento'] == 'ENTRADA':
                stock_temp += mov['cantidad']
            else:
                stock_temp -= mov['cantidad']
            
            movements_list.append(ProductMovement(
                fecha=mov['fecha'],
                tipo=mov['tipo'],
                referencia=mov['referencia'],
                cantidad=mov['cantidad'],
                tipo_movimiento=mov['tipo_movimiento'],
                stock_anterior=stock_anterior,
                stock_nuevo=stock_temp,
                motivo=mov.get('motivo')
            ))
        
        return MovementReport(
            producto_id=producto_id,
            producto_nombre=product.get('nombre', ''),
            sku=product.get('sku', ''),
            fecha_inicio=fecha_inicio.isoformat(),
            fecha_fin=fecha_fin.isoformat(),
            stock_inicial=stock_inicial,
            total_entradas=total_entradas,
            total_salidas=total_salidas,
            stock_final=stock_actual,
            movimientos=movements_list
        )
    
    def get_dashboard_stats(self) -> DashboardStats:
        """Genera estadísticas para el dashboard"""
        hoy = date.today()
        inicio_mes = hoy.replace(day=1)
        
        # Ventas del día
        sales = self.sale_repo.find_all()
        sales_hoy = [
            s for s in sales
            if s.get('estado') == 'COMPLETADA'
            and datetime.fromisoformat(s.get('fecha')).date() == hoy
        ]
        
        # Ventas del mes
        sales_mes = [
            s for s in sales
            if s.get('estado') == 'COMPLETADA'
            and datetime.fromisoformat(s.get('fecha')).date() >= inicio_mes
        ]
        
        total_vendido_mes = sum(float(s.get('total', 0)) for s in sales_mes)
        
        # Compras del mes
        purchases = self.purchase_repo.find_all()
        purchases_mes = [
            p for p in purchases
            if p.get('estado') == 'COMPLETADA'
            and datetime.fromisoformat(p.get('fecha')).date() >= inicio_mes
        ]
        
        total_gastado_mes = sum(float(p.get('total', 0)) for p in purchases_mes)
        
        # Inventario
        products = self.product_repo.find_all()
        productos_stock_bajo = [
            p for p in products
            if p.get('estado_stock') in ['REPONER', 'AGOTADO']
        ]
        
        valor_inventario = sum(
            int(p.get('stock_actual', 0)) * float(p.get('costo_unitario', 0))
            for p in products
        )
        
        # Utilidad bruta del mes
        sales_report = self.get_sales_report(inicio_mes, hoy)
        
        # Top 5 productos más vendidos
        product_sales = defaultdict(lambda: {'cantidad': 0, 'monto': Decimal('0')})
        for sale in sales_mes:
            details = self.sale_repo.get_details(sale['id'])
            for detail in details:
                pid = detail.get('producto_id')
                cantidad = int(detail.get('cantidad', 0))
                subtotal = Decimal(str(detail.get('subtotal', 0)))
                product_sales[pid]['cantidad'] += cantidad
                product_sales[pid]['monto'] += subtotal
        
        top_products = []
        for pid, data in sorted(product_sales.items(), key=lambda x: x[1]['cantidad'], reverse=True)[:5]:
            product = self.product_repo.find_by_id(pid)
            if product:
                top_products.append(TopProduct(
                    producto_id=pid,
                    nombre=product.get('nombre', ''),
                    sku=product.get('sku', ''),
                    cantidad_vendida=data['cantidad'],
                    monto_total=data['monto']
                ))
        
        # Top 5 clientes
        customer_sales = defaultdict(lambda: {'compras': 0, 'monto': Decimal('0')})
        for sale in sales_mes:
            cid = sale.get('cliente_id')
            total = Decimal(str(sale.get('total', 0)))
            customer_sales[cid]['compras'] += 1
            customer_sales[cid]['monto'] += total
        
        top_customers = []
        for cid, data in sorted(customer_sales.items(), key=lambda x: x[1]['monto'], reverse=True)[:5]:
            customer = self.customer_repo.find_by_id(cid)
            if customer:
                if customer.get('razon_social'):
                    nombre = customer.get('razon_social')
                else:
                    nombre = f"{customer.get('nombres', '')} {customer.get('apellidos', '')}".strip()
                
                top_customers.append(TopCustomer(
                    cliente_id=cid,
                    nombre=nombre,
                    documento=customer.get('numero_documento', ''),
                    total_compras=data['compras'],
                    monto_total=data['monto']
                ))
        
        # Top 5 proveedores
        supplier_purchases = defaultdict(lambda: {'compras': 0, 'monto': Decimal('0')})
        for purchase in purchases_mes:
            sid = purchase.get('proveedor_id')
            total = Decimal(str(purchase.get('total', 0)))
            supplier_purchases[sid]['compras'] += 1
            supplier_purchases[sid]['monto'] += total
        
        top_suppliers = []
        for sid, data in sorted(supplier_purchases.items(), key=lambda x: x[1]['monto'], reverse=True)[:5]:
            supplier = self.supplier_repo.find_by_id(sid)
            if supplier:
                top_suppliers.append(TopSupplier(
                    proveedor_id=sid,
                    razon_social=supplier.get('razon_social', ''),
                    ruc=supplier.get('ruc', ''),
                    total_compras=data['compras'],
                    monto_total=data['monto']
                ))
        
        return DashboardStats(
            ventas_hoy=len(sales_hoy),
            ventas_mes=len(sales_mes),
            total_vendido_mes=Decimal(str(total_vendido_mes)),
            compras_mes=len(purchases_mes),
            total_gastado_mes=Decimal(str(total_gastado_mes)),
            productos_total=len(products),
            productos_stock_bajo=len(productos_stock_bajo),
            valor_inventario=Decimal(str(valor_inventario)),
            utilidad_bruta_mes=sales_report.utilidad_bruta,
            margen_promedio_mes=sales_report.margen_promedio,
            top_productos=top_products,
            top_clientes=top_customers,
            top_proveedores=top_suppliers
        )
    
    def get_audit_logs(
        self,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        usuario: Optional[str] = None,
        modulo: Optional[str] = None
    ) -> List[AuditLog]:
        """Obtiene logs de auditoría"""
        logs = self.audit_handler.read_all()
        
        # Filtros
        if fecha_inicio:
            logs = [
                log for log in logs
                if datetime.fromisoformat(log.get('fecha')).date() >= fecha_inicio
            ]
        
        if fecha_fin:
            logs = [
                log for log in logs
                if datetime.fromisoformat(log.get('fecha')).date() <= fecha_fin
            ]
        
        if usuario:
            logs = [log for log in logs if log.get('usuario') == usuario]
        
        if modulo:
            logs = [log for log in logs if log.get('modulo') == modulo]
        
        # Ordenar por fecha descendente
        logs.sort(key=lambda x: x.get('fecha', ''), reverse=True)
        
        return [AuditLog(**log) for log in logs[:100]]  # Últimos 100
    
    def create_audit_log(
        self,
        usuario: str,
        accion: str,
        modulo: str,
        registro_id: Optional[int] = None,
        detalles: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> bool:
        """Crea un log de auditoría"""
        log_data = {
            "fecha": datetime.now().isoformat(),
            "usuario": usuario,
            "accion": accion,
            "modulo": modulo,
            "registro_id": registro_id,
            "detalles": detalles,
            "ip_address": ip_address
        }
        
        return self.audit_handler.append(log_data)
    
    def get_recent_activity(self, limit: int = 10):
        """Obtiene actividad reciente del sistema"""
        import math
        
        activities = []
        
        # Obtener últimas ventas
        sales = self.sale_repo.find_all()
        for sale in sorted(sales, key=lambda x: x.get('created_at', ''), reverse=True)[:limit]:
            customer = self.customer_repo.find_by_id(sale.get('cliente_id'))
            
            # Nombre del cliente
            if customer:
                razon_social = customer.get('razon_social')
                nombre = customer.get('nombre')
                apellido = customer.get('apellido')
                
                # Manejar NaN
                if razon_social and not (isinstance(razon_social, float) and math.isnan(razon_social)):
                    cliente_nombre = str(razon_social)
                elif nombre or apellido:
                    nombre_str = str(nombre) if nombre and not (isinstance(nombre, float) and math.isnan(nombre)) else ''
                    apellido_str = str(apellido) if apellido and not (isinstance(apellido, float) and math.isnan(apellido)) else ''
                    cliente_nombre = f"{nombre_str} {apellido_str}".strip() or "Cliente"
                else:
                    cliente_nombre = "Cliente"
            else:
                cliente_nombre = "Cliente"
            
            # Calcular tiempo relativo
            created_at = sale.get('created_at')
            time_ago = self._get_time_ago(created_at)
            
            activities.append({
                'id': f"sale_{sale['id']}",
                'type': 'sale',
                'icon': 'ShoppingBag',
                'title': f"{cliente_nombre} realizó una compra",
                'description': f"Venta {sale.get('numero_comprobante')} por S/ {sale.get('total', 0):.2f}",
                'time': time_ago,
                'timestamp': created_at,
                'color': 'emerald'
            })
        
        # Obtener últimas compras
        purchases = self.purchase_repo.find_all()
        for purchase in sorted(purchases, key=lambda x: x.get('created_at', ''), reverse=True)[:5]:
            supplier = self.supplier_repo.find_by_id(purchase.get('proveedor_id'))
            supplier_name = supplier.get('razon_social') if supplier else 'Proveedor'
            
            created_at = purchase.get('created_at')
            time_ago = self._get_time_ago(created_at)
            
            activities.append({
                'id': f"purchase_{purchase['id']}",
                'type': 'purchase',
                'icon': 'ShoppingCart',
                'title': f"Compra recibida de {supplier_name}",
                'description': f"Orden {purchase.get('numero_orden')} por S/ {purchase.get('total', 0):.2f}",
                'time': time_ago,
                'timestamp': created_at,
                'color': 'blue'
            })
        
        # Ordenar por timestamp y limitar
        activities.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return activities[:limit]
    
    def _get_time_ago(self, timestamp_str: str) -> str:
        """Calcula tiempo relativo (hace X minutos/horas/días)"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            now = datetime.now()
            diff = now - timestamp
            
            seconds = diff.total_seconds()
            
            if seconds < 60:
                return "hace unos segundos"
            elif seconds < 3600:
                minutes = int(seconds / 60)
                return f"hace {minutes} min" if minutes == 1 else f"hace {minutes} min"
            elif seconds < 86400:
                hours = int(seconds / 3600)
                return f"hace {hours} hora" if hours == 1 else f"hace {hours} horas"
            else:
                days = int(seconds / 86400)
                return f"hace {days} día" if days == 1 else f"hace {days} días"
        except:
            return "recientemente"


# Singleton
report_service = ReportService()
