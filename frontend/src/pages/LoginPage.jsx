/**
 * Página de Login
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'
import { Button, Input } from '@/components/common'
import { LogIn } from 'lucide-react'
import toast from 'react-hot-toast'

export const LoginPage = () => {
  const navigate = useNavigate()
  const { login } = useAuth()
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.username || !formData.password) {
      toast.error('Por favor completa todos los campos')
      return
    }

    setLoading(true)
    
    try {
      const result = await login(formData.username, formData.password)
      
      if (result.success) {
        toast.success('Inicio de sesión exitoso')
        navigate('/dashboard')
      } else {
        toast.error(result.error || 'Error al iniciar sesión')
      }
    } catch (error) {
      toast.error('Error al iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          {/* Logo y título */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
              <LogIn className="h-8 w-8 text-primary-600" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900">
              ERP Ferretería
            </h1>
            <p className="text-gray-500 mt-2">
              Sistema de gestión empresarial
            </p>
          </div>

          {/* Formulario */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Usuario"
              name="username"
              type="text"
              value={formData.username}
              onChange={handleChange}
              placeholder="Ingresa tu usuario"
              required
              autoFocus
            />

            <Input
              label="Contraseña"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Ingresa tu contraseña"
              required
            />

            <Button
              type="submit"
              loading={loading}
              className="w-full"
              size="lg"
            >
              Iniciar Sesión
            </Button>
          </form>

          {/* Credenciales de prueba */}
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <p className="text-xs font-semibold text-gray-700 mb-2">
              Credenciales de prueba:
            </p>
            <div className="space-y-1 text-xs text-gray-600">
              <p><strong>Admin:</strong> admin / admin123</p>
              <p><strong>Vendedor:</strong> vendedor / vendedor123</p>
              <p><strong>Almacenero:</strong> almacenero / almacenero123</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-white text-sm mt-6">
          © 2026 ERP Ferretería. Todos los derechos reservados.
        </p>
      </div>
    </div>
  )
}
