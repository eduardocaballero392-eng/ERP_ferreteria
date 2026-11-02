/**
 * Navbar principal
 */

import { useState } from 'react'
import { Menu, LogOut, User, Key } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '@/context/useAuth'
import { ROLE_NAMES } from '@/constants/roles'
import { getInitials } from '@/utils'
import { authService } from '@/api'
import { Button, Modal } from '@/components/common'

export const Navbar = ({ onMenuClick }) => {
  const { user, logout } = useAuth()
  const [showDropdown, setShowDropdown] = useState(false)
  const [profileOpen, setProfileOpen] = useState(false)
  const [passwordOpen, setPasswordOpen] = useState(false)
  const [password, setPassword] = useState({ current: '', next: '', confirm: '' })
  const [savingPassword, setSavingPassword] = useState(false)

  const changePassword = async (event) => {
    event.preventDefault()
    if (password.next !== password.confirm) return toast.error('Las contraseñas nuevas no coinciden')
    if (password.next.length < 6) return toast.error('La contraseña debe tener al menos 6 caracteres')
    setSavingPassword(true)
    try {
      await authService.changePassword(password.current, password.next)
      toast.success('Contraseña actualizada')
      setPasswordOpen(false)
      setPassword({ current: '', next: '', confirm: '' })
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'No se pudo cambiar la contraseña')
    } finally { setSavingPassword(false) }
  }

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
                {user?.nombre_completo || [user?.nombre, user?.apellido].filter(Boolean).join(' ')}
              </p>
              <p className="text-xs text-gray-500">
                {ROLE_NAMES[user?.role ?? user?.rol] || user?.role || user?.rol}
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
                        setProfileOpen(true)
                      }}
                    >
                      <User className="h-4 w-4" />
                      Mi perfil
                    </button>
                    
                    <button
                      className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                      onClick={() => {
                        setShowDropdown(false)
                        setPasswordOpen(true)
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
      <Modal isOpen={profileOpen} onClose={() => setProfileOpen(false)} title="Mi perfil" size="sm">
        <dl className="space-y-3 text-sm">
          <div><dt className="text-gray-500">Nombre</dt><dd className="font-medium">{user?.nombre_completo || [user?.nombre, user?.apellido].filter(Boolean).join(' ') || '—'}</dd></div>
          <div><dt className="text-gray-500">Usuario</dt><dd className="font-medium">{user?.username || user?.email || '—'}</dd></div>
          <div><dt className="text-gray-500">Rol</dt><dd className="font-medium">{ROLE_NAMES[user?.rol || user?.role] || user?.rol || user?.role || '—'}</dd></div>
        </dl>
      </Modal>
      <Modal isOpen={passwordOpen} onClose={() => setPasswordOpen(false)} title="Cambiar contraseña" size="sm">
        <form onSubmit={changePassword} className="space-y-4">
          <label className="label">Contraseña actual<input className="input mt-1" type="password" autoComplete="current-password" required value={password.current} onChange={(event) => setPassword({ ...password, current: event.target.value })} /></label>
          <label className="label">Nueva contraseña<input className="input mt-1" type="password" autoComplete="new-password" minLength="6" required value={password.next} onChange={(event) => setPassword({ ...password, next: event.target.value })} /></label>
          <label className="label">Confirmar nueva contraseña<input className="input mt-1" type="password" autoComplete="new-password" minLength="6" required value={password.confirm} onChange={(event) => setPassword({ ...password, confirm: event.target.value })} /></label>
          <Button type="submit" loading={savingPassword}>Guardar contraseña</Button>
        </form>
      </Modal>
    </nav>
  )
}
