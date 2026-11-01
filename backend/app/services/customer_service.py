"""
Servicio de Clientes - Lógica de negocio
"""
from typing import List
from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerWithStats
from app.repositories.customer_repository import customer_repository
from app.repositories.sale_repository import sale_repository
from app.core.utils import validar_dni, validar_ruc


class CustomerService:
    """Servicio de gestión de clientes"""
    
    def __init__(self):
        self.customer_repo = customer_repository
        self.sale_repo = sale_repository
    
    def get_all_customers(self, include_inactive: bool = False) -> List[CustomerResponse]:
        """Obtiene todos los clientes"""
        customers = self.customer_repo.find_all(include_inactive)
        return [CustomerResponse(**cust) for cust in customers]
    
    def get_customers_with_stats(self) -> List[CustomerWithStats]:
        """Obtiene clientes con estadísticas de compras"""
        customers = self.customer_repo.find_all()
        result = []
        
        for cust in customers:
            # Obtener ventas del cliente
            sales = self.sale_repo.find_by_customer(cust['id'])
            sales_completadas = [s for s in sales if s.get('estado') == 'COMPLETADA']
            
            # Calcular totales
            total_compras = len(sales_completadas)
            monto_total = sum(float(s.get('total', 0)) for s in sales_completadas)
            
            # Calcular saldo pendiente (ventas a crédito no pagadas completamente)
            sales_credito = [s for s in sales_completadas if s.get('condicion_pago') == 'CREDITO']
            # TODO: Restar pagos cuando se implemente el módulo de pagos
            saldo_pendiente = sum(float(s.get('total', 0)) for s in sales_credito)
            
            # Crédito disponible
            limite_credito = float(cust.get('limite_credito', 0))
            disponible = limite_credito - saldo_pendiente
            
            cust_with_stats = {
                **cust,
                'total_compras': total_compras,
                'monto_total_compras': round(Decimal(str(monto_total)), 2),
                'saldo_pendiente': round(Decimal(str(saldo_pendiente)), 2),
                'disponible_credito': round(Decimal(str(disponible)), 2)
            }
            result.append(CustomerWithStats(**cust_with_stats))
        
        return result
    
    def get_customer_by_id(self, customer_id: int) -> CustomerResponse:
        """Obtiene un cliente por ID"""
        customer = self.customer_repo.find_by_id(customer_id)
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {customer_id} no encontrado"
            )
        
        return CustomerResponse(**customer)
    
    def search_customers(self, query: str) -> List[CustomerResponse]:
        """Busca clientes"""
        customers = self.customer_repo.search(query)
        return [CustomerResponse(**cust) for cust in customers]
    
    def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        """Crea un nuevo cliente"""
        # Validar documento
        if customer_data.tipo_documento == "DNI":
            if len(customer_data.numero_documento) != 8:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El DNI debe tener 8 dígitos"
                )
            if not validar_dni(customer_data.numero_documento):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"DNI '{customer_data.numero_documento}' no es válido"
                )
        elif customer_data.tipo_documento == "RUC":
            if len(customer_data.numero_documento) != 11:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El RUC debe tener 11 dígitos"
                )
            if not validar_ruc(customer_data.numero_documento):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"RUC '{customer_data.numero_documento}' no es válido"
                )
        
        new_customer_data = {
            **customer_data.model_dump(),
            "limite_credito": float(customer_data.limite_credito),
            "activo": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            created_customer = self.customer_repo.create(new_customer_data)
            return CustomerResponse(**created_customer)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear cliente"
            )
    
    def update_customer(self, customer_id: int, customer_data: CustomerUpdate) -> CustomerResponse:
        """Actualiza un cliente"""
        # Verificar que existe
        existing = self.customer_repo.find_by_id(customer_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {customer_id} no encontrado"
            )
        
        # Validar documento si se proporciona
        if customer_data.numero_documento:
            if customer_data.tipo_documento == "DNI":
                if len(customer_data.numero_documento) != 8 or not validar_dni(customer_data.numero_documento):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"DNI '{customer_data.numero_documento}' no es válido"
                    )
            elif customer_data.tipo_documento == "RUC":
                if len(customer_data.numero_documento) != 11 or not validar_ruc(customer_data.numero_documento):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"RUC '{customer_data.numero_documento}' no es válido"
                    )
        
        # Preparar datos a actualizar
        update_data = customer_data.model_dump(exclude_unset=True)
        if update_data:
            if 'limite_credito' in update_data:
                update_data['limite_credito'] = float(update_data['limite_credito'])
            update_data['updated_at'] = datetime.now().isoformat()
            
            success = self.customer_repo.update(customer_id, update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar cliente"
                )
        
        # Retornar cliente actualizado
        updated_customer = self.customer_repo.find_by_id(customer_id)
        return CustomerResponse(**updated_customer)
    
    def delete_customer(self, customer_id: int) -> dict:
        """Elimina (desactiva) un cliente"""
        # Verificar que existe
        existing = self.customer_repo.find_by_id(customer_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {customer_id} no encontrado"
            )
        
        # Verificar si tiene ventas
        sales = self.sale_repo.find_by_customer(customer_id)
        if sales:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar el cliente porque tiene {len(sales)} venta(s) registrada(s)"
            )
        
        # Eliminar
        success = self.customer_repo.delete(customer_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cliente"
            )
        
        return {"message": f"Cliente {customer_id} eliminado exitosamente"}


# Singleton
customer_service = CustomerService()
