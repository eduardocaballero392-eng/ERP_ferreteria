/**
 * Context de autenticación
 * Maneja el estado de autenticación del usuario
 */

import { useState, useEffect, useCallback } from 'react'
import { authService } from '@/api'
import { AuthContext } from './auth-context'

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Verificar si hay sesión al cargar
  const logout = useCallback(() => {
    authService.logout()
    setUser(null)
    setIsAuthenticated(false)
  }, [])

  const checkAuth = useCallback(async () => {
    try {
      const token = localStorage.getItem('token')
      if (token) {
        const userData = await authService.getCurrentUser()
        setUser(userData)
        setIsAuthenticated(true)
      }
    } catch (error) {
      console.error('Error al verificar autenticación:', error)
      logout()
    } finally {
      setLoading(false)
    }
  }, [logout])

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  const login = async (username, password) => {
    try {
      const data = await authService.login(username, password)
      
      // Guardar token
      localStorage.setItem('token', data.access_token)
      
      // Obtener datos del usuario
      const userData = await authService.getCurrentUser()
      setUser(userData)
      setIsAuthenticated(true)
      
      return { success: true }
    } catch (error) {
      console.error('Error en login:', error)
      return {
        success: false,
        error: error.message || 'Error al iniciar sesión',
      }
    }
  }

  const hasPermission = (permission) => {
    if (!user) return false
    const role = user.role ?? user.rol
    
    // Admin tiene todos los permisos
    if (role === 'admin') return true
    
    // Verificar permisos específicos por rol
    const permissions = {
      vendedor: ['sales', 'customers', 'reports'],
      almacenero: ['inventory', 'purchases', 'suppliers', 'reports'],
    }
    
    return permissions[role]?.includes(permission) || false
  }

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    hasPermission,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
