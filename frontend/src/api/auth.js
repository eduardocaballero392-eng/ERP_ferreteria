/**
 * Servicios de autenticación
 */

import apiClient from './client'
import { API_ENDPOINTS } from '@/config/api'

export const authService = {
  /**
   * Login con credenciales
   */
  async login(username, password) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    
    return response.data
  },

  /**
   * Obtener usuario actual
   */
  async getCurrentUser() {
    const response = await apiClient.get(API_ENDPOINTS.AUTH.ME)
    return response.data
  },

  /**
   * Cambiar contraseña
   */
  async changePassword(currentPassword, newPassword) {
    const response = await apiClient.post(API_ENDPOINTS.AUTH.CHANGE_PASSWORD, {
      current_password: currentPassword,
      new_password: newPassword,
    })
    return response.data
  },

  /**
   * Logout
   */
  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
}
