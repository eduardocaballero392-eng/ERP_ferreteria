"""
Servicio de Ventas - Lógica de negocio
"""
from typing import List
from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from app.schemas.sale import (
    SaleCreate, SaleUpdate, SaleResponse,
    SaleWithDetails, SaleDetailResponse, SaleStats
)
from app.repositories.sale_repository import sale_repository
from app.repositories.customer_repository import customer_repository
from app.repositories.product_repository import product_repository
from app.core.utils import calcular_igv, calcular_total_con_igv


class SaleService:
    """Servicio de gestión de ventas"""
    
    def __init__(self):
        self.sale_repo = sale_repository
        self.customer_repo = customer_repository
        self.product_repo = product_repository
    
    def get_all_sales(self) -> List[SaleResponse]:
        """Obtiene todas las ventas"""
        sales = self.sale_repo.find_all()
        result = []
        
        for sale in sales:
            # Obtener cliente
            customer = self.customer_repo.find_by_id(sale['cliente_id'])
            
            # Nombre del cliente
            cliente_nombre = "Cliente Desconocido"
            cliente_documento = None
            
            if customer:
                # Manejar pandas NaN - convertir a None
                razon_social = customer.get('razon_social')
                nombre = customer.get('nombre')
                apellido = customer.get('apellido')
                
                # pandas NaN es float, verificar tipo
                import math
                if razon_social and not (isinstance(razon_social, float) and math.isnan(razon_social)):
                    cliente_nombre = str(razon_social)
                elif nombre or apellido:
                    nombre_str = str(nombre) if nombre and not (isinstance(nombre, float) and math.isnan(nombre)) else ''
                    apellido_str = str(apellido) if apellido and not (isinstance(apellido, float) and math.isnan(apellido)) else ''
                    cliente_nombre = f"{nombre_str} {apellido_str}".strip() or "Cliente Sin Nombre"
                
                if customer.get('numero_documento'):
                    cliente_documento = str(customer.get('numero_documento'))
            
            # Mapear condicion -> condicion_pago para compatibilidad
            sale_with_customer = {
                **sale,
                'condicion_pago': sale.get('condicion') or sale.get('condicion_pago', 'CONTADO'),
                'cliente_nombre': cliente_nombre,
                'cliente_documento': cliente_documento
            }
            result.append(SaleResponse(**sale_with_customer))
        
        return result
    
    def get_sale_by_id(self, sale_id: int) -> SaleWithDetails:
        """Obtiene una venta por ID con detalles"""
        sale = self.sale_repo.find_by_id(sale_id)
        
        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta con ID {sale_id} no encontrada"
            )
        
        # Obtener cliente
        customer = self.customer_repo.find_by_id(sale['cliente_id'])
        
        # Nombre del cliente
        if customer:
            if customer.get('razon_social'):
                cliente_nombre = customer.get('razon_social')
            else:
                cliente_nombre = f"{customer.get('nombres', '')} {customer.get('apellidos', '')}".strip()
        else:
            cliente_nombre = None
        
        # Obtener detalles
        details = self.sale_repo.get_details(sale_id)
        detail_responses = []
        
        for detail in details:
            # Obtener producto
            product = self.product_repo.find_by_id(detail['producto_id'])
            
            detail_with_product = {
                **detail,
                'producto_nombre': product.get('nombre') if product else None,
                'producto_sku': product.get('sku') if product else None
            }
            detail_responses.append(SaleDetailResponse(**detail_with_product))
        
        sale_with_details = {
            **sale,
            # Legacy sales rows store this as "condicion"; the API schema
            # exposes it consistently as "condicion_pago".
            'condicion_pago': sale.get('condicion_pago') or sale.get('condicion') or 'CONTADO',
            'cliente_nombre': cliente_nombre,
            'cliente_documento': customer.get('numero_documento') if customer else None,
            'detalles': detail_responses
        }
        
        return SaleWithDetails(**sale_with_details)
    
    def create_sale(self, sale_data: SaleCreate) -> SaleWithDetails:
        """
        Crea una nueva venta y actualiza el stock automáticamente
        """
        # Verificar que el cliente existe
        customer = self.customer_repo.find_by_id(sale_data.cliente_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cliente con ID {sale_data.cliente_id} no encontrado"
            )
        
        # Validar tipo de comprobante
        if sale_data.tipo_comprobante not in ["BOLETA", "FACTURA"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El tipo de comprobante debe ser BOLETA o FACTURA"
            )
        
        # Validar condición de pago
        if sale_data.condicion_pago not in ["CONTADO", "CREDITO"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La condición de pago debe ser CONTADO o CREDITO"
            )
        
        # Si es a crédito, verificar límite de crédito
        if sale_data.condicion_pago == "CREDITO":
            # Calcular saldo pendiente del cliente
            customer_sales = self.sale_repo.find_by_customer(sale_data.cliente_id)
            sales_credito = [
                s for s in customer_sales 
                if s.get('condicion_pago') == 'CREDITO' and s.get('estado') == 'COMPLETADA'
            ]
            saldo_pendiente = sum(float(s.get('total', 0)) for s in sales_credito)
            
            # Calcular total de esta venta
            subtotal_temp = sum(
                float(d.cantidad) * float(d.precio_unitario)
                for d in sale_data.detalles
            )
            total_temp = subtotal_temp * 1.18  # Con IGV
            
            limite_credito = float(customer.get('limite_credito', 0))
            disponible = limite_credito - saldo_pendiente
            
            if total_temp > disponible:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Crédito insuficiente. Disponible: S/ {disponible:.2f}, Requerido: S/ {total_temp:.2f}"
                )
        
        # Verificar que todos los productos existen y hay stock suficiente
        subtotal = Decimal('0')
        validated_details = []
        
        for detail in sale_data.detalles:
            product = self.product_repo.find_by_id(detail.producto_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Producto con ID {detail.producto_id} no encontrado"
                )
            
            # Verificar stock disponible
            stock_actual = int(product.get('stock_actual', 0))
            if stock_actual < detail.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para '{product.get('nombre')}'. Disponible: {stock_actual}, Solicitado: {detail.cantidad}"
                )
            
            detail_subtotal = Decimal(str(detail.cantidad)) * Decimal(str(detail.precio_unitario))
            subtotal += detail_subtotal
            
            validated_details.append({
                'producto_id': detail.producto_id,
                'cantidad': detail.cantidad,
                'precio_unitario': detail.precio_unitario,
                'subtotal': detail_subtotal,
                'product': product
            })
        
        # Calcular IGV y total
        igv = Decimal(str(calcular_igv(float(subtotal))))
        total = Decimal(str(calcular_total_con_igv(float(subtotal))))
        
        # Generar número de comprobante
        numero_comprobante = self.sale_repo.get_next_numero_comprobante(sale_data.tipo_comprobante)
        
        # Crear venta
        fecha = sale_data.fecha or datetime.now()
        new_sale_data = {
            "numero_comprobante": numero_comprobante,
            "cliente_id": sale_data.cliente_id,
            "tipo_comprobante": sale_data.tipo_comprobante,
            "condicion_pago": sale_data.condicion_pago,
            "fecha": fecha.isoformat() if isinstance(fecha, datetime) else fecha,
            "subtotal": float(subtotal),
            "igv": float(igv),
            "total": float(total),
            "observaciones": sale_data.observaciones,
            "estado": "COMPLETADA",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            created_sale = self.sale_repo.create(new_sale_data)
            sale_id = created_sale['id']
            
            # Crear detalles y actualizar stock
            for detail_data in validated_details:
                # Crear detalle
                detail = {
                    "venta_id": sale_id,
                    "producto_id": detail_data['producto_id'],
                    "cantidad": detail_data['cantidad'],
                    "precio_unitario": float(detail_data['precio_unitario']),
                    "subtotal": float(detail_data['subtotal']),
                    "created_at": datetime.now().isoformat()
                }
                self.sale_repo.create_detail(detail)
                
                # Actualizar stock del producto (RESTA)
                product = detail_data['product']
                stock_actual = int(product.get('stock_actual', 0))
                nuevo_stock = stock_actual - detail_data['cantidad']
                
                self.product_repo.update_stock(detail_data['producto_id'], nuevo_stock)
                
                # TODO: Registrar en movimientos_inventario
            
            # Retornar venta creada con detalles
            return self.get_sale_by_id(sale_id)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear venta: {str(e)}"
            )
    
    def update_sale(self, sale_id: int, sale_data: SaleUpdate) -> SaleResponse:
        """Actualiza una venta (solo observaciones y estado)"""
        # Verificar que existe
        existing = self.sale_repo.find_by_id(sale_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta con ID {sale_id} no encontrada"
            )
        
        # Preparar datos a actualizar
        update_data = sale_data.model_dump(exclude_unset=True)
        if update_data:
            update_data['updated_at'] = datetime.now().isoformat()
            
            success = self.sale_repo.update(sale_id, update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar venta"
                )
        
        # Retornar venta actualizada
        updated_sale = self.sale_repo.find_by_id(sale_id)
        customer = self.customer_repo.find_by_id(updated_sale['cliente_id'])
        
        # Nombre del cliente
        if customer:
            if customer.get('razon_social'):
                cliente_nombre = customer.get('razon_social')
            else:
                cliente_nombre = f"{customer.get('nombres', '')} {customer.get('apellidos', '')}".strip()
        else:
            cliente_nombre = None
        
        sale_with_customer = {
            **updated_sale,
            'cliente_nombre': cliente_nombre,
            'cliente_documento': customer.get('numero_documento') if customer else None
        }
        
        return SaleResponse(**sale_with_customer)
    
    def delete_sale(self, sale_id: int) -> dict:
        """Anula una venta (NO revierte el stock)"""
        # Verificar que existe
        existing = self.sale_repo.find_by_id(sale_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta con ID {sale_id} no encontrada"
            )
        
        # Verificar que no esté ya anulada
        if existing.get('estado') == 'ANULADA':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La venta ya está anulada"
            )
        
        # Anular (no se revierte el stock automáticamente por seguridad)
        success = self.sale_repo.delete(sale_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al anular venta"
            )
        
        return {
            "message": f"Venta {sale_id} anulada exitosamente",
            "nota": "El stock NO se ha revertido automáticamente. Debe ajustarse manualmente si es necesario."
        }
    
    def get_sale_stats(self) -> SaleStats:
        """Obtiene estadísticas de ventas"""
        sales = self.sale_repo.find_all()
        sales_completadas = [s for s in sales if s.get('estado') == 'COMPLETADA']
        
        total_ventas = len(sales_completadas)
        total_vendido = sum(float(s.get('total', 0)) for s in sales_completadas)
        venta_promedio = total_vendido / total_ventas if total_ventas > 0 else 0
        
        # Cliente principal (con más compras)
        if sales_completadas:
            from collections import Counter
            customer_counts = Counter(s.get('cliente_id') for s in sales_completadas)
            main_customer_id = customer_counts.most_common(1)[0][0]
            main_customer = self.customer_repo.find_by_id(main_customer_id)
            if main_customer:
                if main_customer.get('razon_social'):
                    cliente_principal = main_customer.get('razon_social')
                else:
                    cliente_principal = f"{main_customer.get('nombres', '')} {main_customer.get('apellidos', '')}".strip()
            else:
                cliente_principal = None
        else:
            cliente_principal = None
        
        # Estadísticas por condición de pago
        ventas_contado = [s for s in sales_completadas if s.get('condicion_pago') == 'CONTADO']
        ventas_credito = [s for s in sales_completadas if s.get('condicion_pago') == 'CREDITO']
        
        monto_contado = sum(float(s.get('total', 0)) for s in ventas_contado)
        monto_credito = sum(float(s.get('total', 0)) for s in ventas_credito)
        
        return SaleStats(
            total_ventas=total_ventas,
            total_vendido=round(Decimal(str(total_vendido)), 2),
            venta_promedio=round(Decimal(str(venta_promedio)), 2),
            cliente_principal=cliente_principal,
            ventas_contado=len(ventas_contado),
            ventas_credito=len(ventas_credito),
            monto_contado=round(Decimal(str(monto_contado)), 2),
            monto_credito=round(Decimal(str(monto_credito)), 2)
        )


# Singleton
sale_service = SaleService()
