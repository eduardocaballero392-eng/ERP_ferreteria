/**
 * Servicios de ventas
 */

import apiClient from './client'
import { API_ENDPOINTS } from '@/config/api'

export const saleService = {
  /**
   * Listar ventas
   */
  async getSales(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.SALES.LIST, { params })
    return response.data
  },

  /**
   * Obtener estadísticas de ventas
   */
  async getStats() {
    const response = await apiClient.get(API_ENDPOINTS.SALES.STATS)
    return response.data
  },

  /**
   * Obtener venta por ID
   */
  async getSale(id) {
    const response = await apiClient.get(API_ENDPOINTS.SALES.DETAIL(id))
    return response.data
  },

  /**
   * Crear venta
   */
  async createSale(data) {
    const response = await apiClient.post(API_ENDPOINTS.SALES.CREATE, data)
    return response.data
  },

  /**
   * Anular venta
   */
  async cancelSale(id) {
    const response = await apiClient.delete(API_ENDPOINTS.SALES.DELETE(id))
    return response.data
  },
}
