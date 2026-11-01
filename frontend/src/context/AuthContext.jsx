/**
 * Context de autenticación
 * Maneja el estado de autenticación del usuario
 */

import { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '@/api'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Verificar si hay sesión al cargar
  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
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
  }

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

  const logout = () => {
    authService.logout()
    setUser(null)
    setIsAuthenticated(false)
  }

  const hasPermission = (permission) => {
    if (!user) return false
    
    // Admin tiene todos los permisos
    if (user.rol === 'admin') return true
    
    // Verificar permisos específicos por rol
    const permissions = {
      vendedor: ['sales', 'customers', 'reports'],
      almacenero: ['inventory', 'purchases', 'suppliers', 'reports'],
    }
    
    return permissions[user.rol]?.includes(permission) || false
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
