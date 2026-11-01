/**
 * Servicios de clientes
 */

import apiClient from './client'
import { API_ENDPOINTS } from '@/config/api'

export const customerService = {
  /**
   * Listar clientes
   */
  async getCustomers(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.CUSTOMERS.LIST, { params })
    return response.data
  },

  /**
   * Obtener clientes con estadísticas
   */
  async getCustomersWithStats() {
    const response = await apiClient.get(API_ENDPOINTS.CUSTOMERS.WITH_STATS)
    return response.data
  },

  /**
   * Buscar clientes
   */
  async searchCustomers(query) {
    const response = await apiClient.get(API_ENDPOINTS.CUSTOMERS.SEARCH, {
      params: { q: query },
    })
    return response.data
  },

  /**
   * Obtener cliente por ID
   */
  async getCustomer(id) {
    const response = await apiClient.get(API_ENDPOINTS.CUSTOMERS.DETAIL(id))
    return response.data
  },

  /**
   * Crear cliente
   */
  async createCustomer(data) {
    const response = await apiClient.post(API_ENDPOINTS.CUSTOMERS.CREATE, data)
    return response.data
  },

  /**
   * Actualizar cliente
   */
  async updateCustomer(id, data) {
    const response = await apiClient.put(API_ENDPOINTS.CUSTOMERS.UPDATE(id), data)
    return response.data
  },

  /**
   * Eliminar cliente
   */
  async deleteCustomer(id) {
    const response = await apiClient.delete(API_ENDPOINTS.CUSTOMERS.DELETE(id))
    return response.data
  },
}
