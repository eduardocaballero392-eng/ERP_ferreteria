/**
 * Navbar principal
 */

import { useState } from 'react'
import { Menu, LogOut, User, Key } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { ROLE_NAMES } from '@/constants/roles'
import { getInitials } from '@/utils'

export const Navbar = ({ onMenuClick }) => {
  const { user, logout } = useAuth()
  const [showDropdown, setShowDropdown] = useState(false)

  const handleLogout = () => {
    if (window.confirm('¿Estás seguro que deseas cerrar sesión?')) {
      logout()
    }
  }

  return (
    <nav className="bg-white border-b border-gray-200 fixed w-full z-30 top-0">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo y menú hamburguesa */}
          <div className="flex items-center">
            <button
              onClick={onMenuClick}
              className="p-2 rounded-lg hover:bg-gray-100 lg:hidden"
            >
              <Menu className="h-6 w-6" />
            </button>
            <div className="flex items-center ml-4">
              <h1 className="text-xl font-bold text-primary-600">
                ERP Ferretería
              </h1>
            </div>
          </div>

          {/* Usuario */}
          <div className="flex items-center gap-4">
            <div className="hidden md:block text-right">
              <p className="text-sm font-medium text-gray-900">
                {user?.nombre_completo}
              </p>
              <p className="text-xs text-gray-500">
                {ROLE_NAMES[user?.rol] || user?.rol}
              </p>
            </div>

            <div className="relative">
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="flex items-center justify-center w-10 h-10 rounded-full bg-primary-600 text-white font-medium hover:bg-primary-700"
              >
                {getInitials(user?.nombre_completo || 'Usuario')}
              </button>

              {/* Dropdown */}
              {showDropdown && (
                <>
                  <div
                    className="fixed inset-0 z-10"
                    onClick={() => setShowDropdown(false)}
                  />
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-20">
                    <div className="px-4 py-3 border-b border-gray-200">
                      <p className="text-sm font-medium text-gray-900">
                        {user?.nombre_completo}
                      </p>
                      <p className="text-xs text-gray-500">{user?.username}</p>
                    </div>
                    
                    <button
                      className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                      onClick={() => {
                        setShowDropdown(false)
                        // TODO: Abrir modal de perfil
                      }}
                    >
                      <User className="h-4 w-4" />
                      Mi perfil
                    </button>
                    
                    <button
                      className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                      onClick={() => {
                        setShowDropdown(false)
                        // TODO: Abrir modal de cambiar contraseña
                      }}
                    >
                      <Key className="h-4 w-4" />
                      Cambiar contraseña
                    </button>
                    
                    <div className="border-t border-gray-200 mt-1 pt-1">
                      <button
                        className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                        onClick={() => {
                          setShowDropdown(false)
                          handleLogout()
                        }}
                      >
                        <LogOut className="h-4 w-4" />
                        Cerrar sesión
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}
