/**
 * Servicios de proveedores
 */

import apiClient from './client'
import { API_ENDPOINTS } from '@/config/api'

export const supplierService = {
  /**
   * Listar proveedores
   */
  async getSuppliers(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.SUPPLIERS.LIST, { params })
    return response.data
  },

  /**
   * Obtener proveedores con estadísticas
   */
  async getSuppliersWithStats() {
    const response = await apiClient.get(API_ENDPOINTS.SUPPLIERS.WITH_STATS)
    return response.data
  },

  /**
   * Buscar proveedores
   */
  async searchSuppliers(query) {
    const response = await apiClient.get(API_ENDPOINTS.SUPPLIERS.SEARCH, {
      params: { q: query },
    })
    return response.data
  },

  /**
   * Obtener proveedor por ID
   */
  async getSupplier(id) {
    const response = await apiClient.get(API_ENDPOINTS.SUPPLIERS.DETAIL(id))
    return response.data
  },

  /**
   * Crear proveedor
   */
  async createSupplier(data) {
    const response = await apiClient.post(API_ENDPOINTS.SUPPLIERS.CREATE, data)
    return response.data
  },

  /**
   * Actualizar proveedor
   */
  async updateSupplier(id, data) {
    const response = await apiClient.put(API_ENDPOINTS.SUPPLIERS.UPDATE(id), data)
    return response.data
  },

  /**
   * Eliminar proveedor
   */
  async deleteSupplier(id) {
    const response = await apiClient.delete(API_ENDPOINTS.SUPPLIERS.DELETE(id))
    return response.data
  },
}
