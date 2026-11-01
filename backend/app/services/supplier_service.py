"""
Servicio de Proveedores - Lógica de negocio
"""
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse, SupplierWithStats
from app.repositories.supplier_repository import supplier_repository
from app.repositories.purchase_repository import purchase_repository
from app.core.utils import validar_ruc


class SupplierService:
    """Servicio de gestión de proveedores"""
    
    def __init__(self):
        self.supplier_repo = supplier_repository
        self.purchase_repo = purchase_repository
    
    def get_all_suppliers(self, include_inactive: bool = False) -> List[SupplierResponse]:
        """Obtiene todos los proveedores"""
        suppliers = self.supplier_repo.find_all(include_inactive)
        return [SupplierResponse(**supp) for supp in suppliers]
    
    def get_suppliers_with_stats(self) -> List[SupplierWithStats]:
        """Obtiene proveedores con estadísticas de compras"""
        suppliers = self.supplier_repo.find_all()
        result = []
        
        for supp in suppliers:
            # Obtener compras del proveedor
            purchases = self.purchase_repo.find_by_supplier(supp['id'])
            purchases_completadas = [p for p in purchases if p.get('estado') == 'COMPLETADA']
            
            # Calcular totales
            total_compras = len(purchases_completadas)
            monto_total = sum(float(p.get('total', 0)) for p in purchases_completadas)
            
            supp_with_stats = {
                **supp,
                'total_compras': total_compras,
                'monto_total_compras': round(monto_total, 2)
            }
            result.append(SupplierWithStats(**supp_with_stats))
        
        return result
    
    def get_supplier_by_id(self, supplier_id: int) -> SupplierResponse:
        """Obtiene un proveedor por ID"""
        supplier = self.supplier_repo.find_by_id(supplier_id)
        
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID {supplier_id} no encontrado"
            )
        
        return SupplierResponse(**supplier)
    
    def search_suppliers(self, query: str) -> List[SupplierResponse]:
        """Busca proveedores"""
        suppliers = self.supplier_repo.search(query)
        return [SupplierResponse(**supp) for supp in suppliers]
    
    def create_supplier(self, supplier_data: SupplierCreate) -> SupplierResponse:
        """Crea un nuevo proveedor"""
        # Validar RUC
        if not validar_ruc(supplier_data.ruc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"RUC '{supplier_data.ruc}' no es válido"
            )
        
        new_supplier_data = {
            **supplier_data.model_dump(),
            "activo": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            created_supplier = self.supplier_repo.create(new_supplier_data)
            return SupplierResponse(**created_supplier)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear proveedor"
            )
    
    def update_supplier(self, supplier_id: int, supplier_data: SupplierUpdate) -> SupplierResponse:
        """Actualiza un proveedor"""
        # Verificar que existe
        existing = self.supplier_repo.find_by_id(supplier_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID {supplier_id} no encontrado"
            )
        
        # Validar RUC si se proporciona
        if supplier_data.ruc and not validar_ruc(supplier_data.ruc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"RUC '{supplier_data.ruc}' no es válido"
            )
        
        # Preparar datos a actualizar
        update_data = supplier_data.model_dump(exclude_unset=True)
        if update_data:
            update_data['updated_at'] = datetime.now().isoformat()
            
            success = self.supplier_repo.update(supplier_id, update_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al actualizar proveedor"
                )
        
        # Retornar proveedor actualizado
        updated_supplier = self.supplier_repo.find_by_id(supplier_id)
        return SupplierResponse(**updated_supplier)
    
    def delete_supplier(self, supplier_id: int) -> dict:
        """Elimina (desactiva) un proveedor"""
        # Verificar que existe
        existing = self.supplier_repo.find_by_id(supplier_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID {supplier_id} no encontrado"
            )
        
        # Verificar si tiene compras
        purchases = self.purchase_repo.find_by_supplier(supplier_id)
        if purchases:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar el proveedor porque tiene {len(purchases)} compra(s) registrada(s)"
            )
        
        # Eliminar
        success = self.supplier_repo.delete(supplier_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar proveedor"
            )
        
        return {"message": f"Proveedor {supplier_id} eliminado exitosamente"}


# Singleton
supplier_service = SupplierService()
