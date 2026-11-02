/**
 * Servicios de reportes
 */

import apiClient from './client'
import { API_ENDPOINTS } from '@/config/api'

export const reportService = {
  /**
   * Obtener dashboard
   */
  async getDashboard(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.REPORTS.DASHBOARD, { params })
    
    // Obtener actividad reciente
    try {
      const activityResponse = await apiClient.get('/reports/recent-activity')
      response.data.recent_activity = activityResponse.data
    } catch (error) {
      console.error('Error loading recent activity:', error)
      response.data.recent_activity = []
    }
    
    return response.data
  },

  /**
   * Reporte de inventario
   */
  async getInventoryReport(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.REPORTS.INVENTORY, { params })
    return response.data
  },

  /**
   * Reporte de ventas
   */
  async getSalesReport(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.REPORTS.SALES, { params })
    return response.data
  },

  /**
   * Reporte de compras
   */
  async getPurchasesReport(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.REPORTS.PURCHASES, { params })
    return response.data
  },

  /**
   * Movimientos de producto
   */
  async getProductMovements(productId, params = {}) {
    const response = await apiClient.get(
      API_ENDPOINTS.REPORTS.MOVEMENTS(productId),
      { params }
    )
    return response.data
  },

  /**
   * Log de auditoría
   */
  async getAuditLog(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.REPORTS.AUDIT, { params })
    return response.data
  },
}
