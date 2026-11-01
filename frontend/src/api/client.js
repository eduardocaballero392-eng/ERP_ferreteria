/**
 * Cliente HTTP con Axios
 * Maneja autenticación, interceptores y manejo de errores
 */

import axios from 'axios'
import { API_CONFIG } from '@/config/api'

// Crear instancia de axios
const apiClient = axios.create({
  baseURL: `${API_CONFIG.BASE_URL}${API_CONFIG.API_VERSION}`,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor de request - Agregar token JWT
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor de response - Manejo de errores
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      // Error de respuesta del servidor
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // Token inválido o expirado
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
          break
          
        case 403:
          // Sin permisos
          error.message = 'No tienes permisos para realizar esta acción'
          break
          
        case 404:
          error.message = data?.detail || 'Recurso no encontrado'
          break
          
        case 422:
          // Errores de validación
          error.message = data?.detail || 'Error de validación'
          break
          
        case 500:
          error.message = 'Error interno del servidor'
          break
          
        default:
          error.message = data?.detail || 'Error desconocido'
      }
    } else if (error.request) {
      // Error de red
      error.message = 'Error de conexión. Verifica tu conexión a internet.'
    } else {
      error.message = 'Error al procesar la solicitud'
    }
    
    return Promise.reject(error)
  }
)

export default apiClient
