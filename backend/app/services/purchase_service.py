"""
Servicio de Compras - Lógica de negocio
"""
from typing import List
from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from app.schemas.purchase import (
    PurchaseCreate, PurchaseUpdate, PurchaseResponse,
    PurchaseWithDetails, PurchaseDetailResponse, PurchaseStats
)
from app.repositories.purchase_repository import purchase_repository
from app.repositories.supplier_repository import supplier_repository
from app.repositories.product_repository import product_repository
from app.core.utils import calcular_igv, calcular_total_con_igv


class PurchaseService:
    """Servicio de gestión de compras"""
    
    def __init__(self):
        self.purchase_repo = purchase_repository
        self.supplier_repo = supplier_repository
        self.product_repo = product_repository
    
    def get_all_purchases(self) -> List[PurchaseResponse]:
        """Obtiene todas las compras"""
        purchases = self.purchase_repo.find_all()
        result = []
        
        for purchase in purchases:
            # Obtener proveedor
            supplier = self.supplier_repo.find_by_id(purchase['proveedor_id'])
            
            purchase_with_supplier = {
                **purchase,
                'proveedor_nombre': supplier.get('razon_social') if supplier else None,
                'proveedor_ruc': supplier.get('ruc') if supplier else None
            }
            result.append(PurchaseResponse(**purchase_with_supplier))
        
        return result
    
    def get_purchase_by_id(self, purchase_id: int) -> PurchaseWithDetails:
        """Obtiene una compra por ID con detalles"""
        purchase = self.purchase_repo.find_by_id(purchase_id)
        
        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra con ID {purchase_id} no encontrada"
            )
        
        # Obtener proveedor
        supplier = self.supplier_repo.find_by_id(purchase['proveedor_id'])
        
        # Obtener detalles
        details = self.purchase_repo.get_details(purchase_id)
        detail_responses = []
        
        for detail in details:
            # Obtener producto
            product = self.product_repo.find_by_id(detail['producto_id'])
            
            detail_with_product = {
                **detail,
                'producto_nombre': product.get('nombre') if product else None,
                'producto_sku': product.get('sku') if product else None
            }
            detail_responses.append(PurchaseDetailResponse(**detail_with_product))
        
        purchase_with_details = {
            **purchase,
            'proveedor_nombre': supplier.get('razon_social') if supplier else None,
            'proveedor_ruc': supplier.get('ruc') if supplier else None,
            'detalles': detail_responses
        }
        
        return PurchaseWithDetails(**purchase_with_details)
    
    def create_purchase(self, purchase_data: PurchaseCreate) -> PurchaseWithDetails:
        """
        Crea una nueva compra y actualiza el stock automáticamente
        """
        # Verificar que el proveedor existe
        supplier = self.supplier_repo.find_by_id(purchase_data.proveedor_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Proveedor con ID {purchase_data.proveedor_id} no encontrado"
            )
        
        # Verificar que todos los productos existen y calcular totales
        subtotal = Decimal('0')
        validated_details = []
        
        for detail in purchase_data.detalles:
            product = self.product_repo.find_by_id(detail.producto_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Producto con ID {detail.producto_id} no encontrado"
                )
            
            detail_subtotal = Decimal(str(detail.cantidad)) * Decimal(str(detail.costo_unitario))
            subtotal += detail_subtotal
            
            validated_details.append({
                'producto_id': detail.producto_id,
                'cantidad': detail.cantidad,
                'costo_unitario': detail.costo_unitario,
                'subtotal': detail_subtotal,
                'product': product
            })
        
        # Calcular IGV y total
        igv = Decimal(str(calcular_igv(float(subtotal))))
        total = Decimal(str(calcular_total_con_igv(float(subtotal))))
        
        # Generar número de orden
        numero_orden = self.purchase_repo.get_next_numero_orden()
        
        # Crear compra
        fecha = purchase_data.fecha or datetime.now()
        new_purchase_data = {
            "numero_orden": numero_orden,
            "proveedor_id": purchase_data.proveedor_id,
            "fecha": fecha.isoformat() if isinstance(fecha, datetime) else fecha,
            "subtotal": float(subtotal),
            "igv": float(igv),
            "total": float(total),
            "observaciones": purchase_data.observaciones,
            "estado": "COMPLETADA",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            created_purchase = self.purchase_repo.create(new_purchase_data)
            purchase_id = created_purchase['id']
            
            # Crear detalles y actualizar stock
            for detail_data in validated_details:
                # Crear detalle
                detail = {
                    "compra_id": purchase_id,
                    "producto_id": detail_data['producto_id'],
                    "cantidad": detail_data['cantidad'],
                    "costo_unitario": float(detail_data['costo_unitario']),
                    "subtotal": float(detail_data['subtotal']),
                    "created_at": datetime.now().isoformat()
                }
                self.purchase_repo.create_detail(detail)
                
                # Actualizar stock del producto (SUMA)
                product = detail_data['product']
                stock_actual = int(product.get('stock_actual', 0))
                nuevo_stock = stock_actual + detail_data['cantidad']
                
                self.product_repo.update_stock(detail_data['producto_id'], nuevo_stock)
                
                # TODO: Registrar en movimientos_inventario
            
            # Retornar compra creada con detalles
            return self.get_purchase_by_id(purchase_id)
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear compra: {str(e)}"
            )
    
    def update_purchase(self, purchase_id: int, purchase_data: PurchaseUpdate) -> PurchaseResponse:
        """Actualiza una compra (solo observaciones y estado)"""
        # Verificar que existe
        existing = self.purchase_repo.find_by_id(purchase_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra con ID {purchase_id} no encontrada"
            )
        
        # Preparar datos a actualizar
        update_data = purchase_data.model_dump(exclude_unset=True)
        if update_data:
            update_data['updated_at'] = datetime.now().isoformat()
            
            success = self.purchase_repo.update(purchase_id, update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar compra"
                )
        
        # Retornar compra actualizada
        updated_purchase = self.purchase_repo.find_by_id(purchase_id)
        supplier = self.supplier_repo.find_by_id(updated_purchase['proveedor_id'])
        
        purchase_with_supplier = {
            **updated_purchase,
            'proveedor_nombre': supplier.get('razon_social') if supplier else None,
            'proveedor_ruc': supplier.get('ruc') if supplier else None
        }
        
        return PurchaseResponse(**purchase_with_supplier)
    
    def delete_purchase(self, purchase_id: int) -> dict:
        """Anula una compra (NO revierte el stock)"""
        # Verificar que existe
        existing = self.purchase_repo.find_by_id(purchase_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra con ID {purchase_id} no encontrada"
            )
        
        # Verificar que no esté ya anulada
        if existing.get('estado') == 'ANULADA':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La compra ya está anulada"
            )
        
        # Anular (no se revierte el stock automáticamente por seguridad)
        success = self.purchase_repo.delete(purchase_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al anular compra"
            )
        
        return {
            "message": f"Compra {purchase_id} anulada exitosamente",
            "nota": "El stock NO se ha revertido automáticamente. Debe ajustarse manualmente si es necesario."
        }
    
    def get_purchase_stats(self) -> PurchaseStats:
        """Obtiene estadísticas de compras"""
        purchases = self.purchase_repo.find_all()
        purchases_completadas = [p for p in purchases if p.get('estado') == 'COMPLETADA']
        
        total_compras = len(purchases_completadas)
        total_gastado = sum(float(p.get('total', 0)) for p in purchases_completadas)
        compra_promedio = total_gastado / total_compras if total_compras > 0 else 0
        
        # Proveedor principal (con más compras)
        if purchases_completadas:
            from collections import Counter
            proveedor_counts = Counter(p.get('proveedor_id') for p in purchases_completadas)
            main_supplier_id = proveedor_counts.most_common(1)[0][0]
            main_supplier = self.supplier_repo.find_by_id(main_supplier_id)
            proveedor_principal = main_supplier.get('razon_social') if main_supplier else None
        else:
            proveedor_principal = None
        
        return PurchaseStats(
            total_compras=total_compras,
            total_gastado=round(Decimal(str(total_gastado)), 2),
            compra_promedio=round(Decimal(str(compra_promedio)), 2),
            proveedor_principal=proveedor_principal
        )


# Singleton
purchase_service = PurchaseService()
