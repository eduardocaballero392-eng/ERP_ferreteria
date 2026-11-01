/**
 * Servicios de categorías
 */

import apiClient from './client'
import { API_ENDPOINTS } from '@/config/api'

export const categoryService = {
  /**
   * Listar categorías
   */
  async getCategories() {
    const response = await apiClient.get(API_ENDPOINTS.CATEGORIES.LIST)
    return response.data
  },

  /**
   * Listar categorías con conteo de productos
   */
  async getCategoriesWithCount() {
    const response = await apiClient.get(API_ENDPOINTS.CATEGORIES.WITH_COUNT)
    return response.data
  },

  /**
   * Obtener categoría por ID
   */
  async getCategory(id) {
    const response = await apiClient.get(API_ENDPOINTS.CATEGORIES.DETAIL(id))
    return response.data
  },

  /**
   * Crear categoría
   */
  async createCategory(data) {
    const response = await apiClient.post(API_ENDPOINTS.CATEGORIES.CREATE, data)
    return response.data
  },

  /**
   * Actualizar categoría
   */
  async updateCategory(id, data) {
    const response = await apiClient.put(API_ENDPOINTS.CATEGORIES.UPDATE(id), data)
    return response.data
  },

  /**
   * Eliminar categoría
   */
  async deleteCategory(id) {
    const response = await apiClient.delete(API_ENDPOINTS.CATEGORIES.DELETE(id))
    return response.data
  },
}
