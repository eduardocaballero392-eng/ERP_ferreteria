/**
 * Servicios de compras
 */

import apiClient from './client'
import { API_ENDPOINTS } from '@/config/api'

export const purchaseService = {
  /**
   * Listar compras
   */
  async getPurchases(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.PURCHASES.LIST, { params })
    return response.data
  },

  /**
   * Obtener estadísticas de compras
   */
  async getStats() {
    const response = await apiClient.get(API_ENDPOINTS.PURCHASES.STATS)
    return response.data
  },

  /**
   * Obtener compra por ID
   */
  async getPurchase(id) {
    const response = await apiClient.get(API_ENDPOINTS.PURCHASES.DETAIL(id))
    return response.data
  },

  /**
   * Crear compra
   */
  async createPurchase(data) {
    const response = await apiClient.post(API_ENDPOINTS.PURCHASES.CREATE, data)
    return response.data
  },

  /**
   * Anular compra
   */
  async cancelPurchase(id) {
    const response = await apiClient.delete(API_ENDPOINTS.PURCHASES.DELETE(id))
    return response.data
  },
}
