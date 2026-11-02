/**
 * Componente para proteger rutas que requieren autenticación
 */

import { Navigate } from 'react-router-dom'
import { useAuth } from '@/context/useAuth'

export const ProtectedRoute = ({ children, permission }) => {
  const { isAuthenticated, loading, hasPermission } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (permission && !hasPermission(permission)) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900">403</h1>
          <p className="text-gray-500 mt-2">
            No tienes permisos para acceder a esta página
          </p>
        </div>
      </div>
    )
  }

  return children
}
