/**
 * Servicios de productos
 */

import apiClient from './client'
import { API_ENDPOINTS } from '@/config/api'

export const productService = {
  /**
   * Listar productos
   */
  async getProducts(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.PRODUCTS.LIST, { params })
    return response.data
  },

  /**
   * Obtener productos con detalles
   */
  async getProductsDetails() {
    const response = await apiClient.get(API_ENDPOINTS.PRODUCTS.DETAILS)
    return response.data
  },

  /**
   * Obtener productos con stock bajo
   */
  async getLowStockProducts() {
    const response = await apiClient.get(API_ENDPOINTS.PRODUCTS.LOW_STOCK)
    return response.data
  },

  /**
   * Buscar productos
   */
  async searchProducts(query) {
    const response = await apiClient.get(API_ENDPOINTS.PRODUCTS.SEARCH, {
      params: { q: query },
    })
    return response.data
  },

  /**
   * Obtener producto por ID
   */
  async getProduct(id) {
    const response = await apiClient.get(API_ENDPOINTS.PRODUCTS.DETAIL(id))
    return response.data
  },

  /**
   * Crear producto
   */
  async createProduct(data) {
    const response = await apiClient.post(API_ENDPOINTS.PRODUCTS.CREATE, data)
    return response.data
  },

  /**
   * Actualizar producto
   */
  async updateProduct(id, data) {
    const response = await apiClient.put(API_ENDPOINTS.PRODUCTS.UPDATE(id), data)
    return response.data
  },

  /**
   * Ajustar stock
   */
  async adjustStock(id, quantity, reason) {
    const response = await apiClient.post(API_ENDPOINTS.PRODUCTS.ADJUST_STOCK(id), {
      cantidad: quantity,
      motivo: reason,
    })
    return response.data
  },

  /**
   * Eliminar producto
   */
  async deleteProduct(id) {
    const response = await apiClient.delete(API_ENDPOINTS.PRODUCTS.DELETE(id))
    return response.data
  },
}
