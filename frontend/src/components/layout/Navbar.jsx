/**
 * Navbar principal
 */

import { useState } from 'react'
import { useLocation } from 'react-router-dom'
import { Menu, LogOut, User, Key } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '@/context/useAuth'
import { ROLE_NAMES } from '@/constants/roles'
import { getInitials } from '@/utils'
import { authService } from '@/api'
import { Button, Modal } from '@/components/common'

export const Navbar = ({ onMenuClick }) => {
  const { user, logout } = useAuth()
  const location = useLocation()
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

  const currentPage = [
    ['/inventory/categories', 'Categorías'], ['/inventory/movements', 'Movimientos'],
    ['/inventory/adjustments', 'Ajustes de stock'], ['/inventory', 'Inventario'],
    ['/sales/new', 'Nueva venta'], ['/sales/quotes', 'Cotizaciones'],
    ['/sales/receivables', 'Ventas a crédito'], ['/sales', 'Ventas'],
    ['/purchases/new', 'Nueva compra'], ['/purchases/suppliers', 'Proveedores'],
    ['/purchases/payables', 'Cuentas por pagar'], ['/purchases', 'Compras'],
    ['/customers', 'Clientes'], ['/employees/sellers', 'Vendedores'],
    ['/employees/warehouse', 'Almaceneros'], ['/employees', 'Empleados'],
    ['/reports/sales', 'Ventas por período'], ['/reports/inventory', 'Inventario valorizado'],
    ['/reports/profitability', 'Rentabilidad'], ['/reports', 'Reportes'],
    ['/dashboard', 'Resumen ejecutivo'],
  ].find(([path]) => location.pathname.startsWith(path))?.[1] || 'Panel'

  return (
    <nav className="fixed top-0 z-30 w-full border-b border-slate-800 bg-[#0b1220] text-white shadow-[0_8px_24px_rgba(2,6,23,0.18)]">
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo y menú hamburguesa */}
          <div className="flex items-center">
            <button
              onClick={onMenuClick}
              className="rounded-lg p-2 text-slate-300 transition hover:bg-white/10 hover:text-white lg:hidden"
              aria-label="Abrir menú de navegación"
            >
              <Menu className="h-6 w-6" />
            </button>
            <div className="flex items-center ml-4">
              <div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-sm font-extrabold tracking-tight text-white shadow-lg shadow-blue-950/40">EF</div><div><h1 className="text-[15px] font-extrabold leading-tight tracking-tight text-white">ERP Ferretería</h1><p className="mt-0.5 text-[10px] font-bold uppercase tracking-[.16em] text-slate-400">Gestión integrada</p></div></div>
            </div>
          </div>

          <div className="hidden items-center gap-2 text-sm xl:flex"><span className="text-slate-500">Espacio de trabajo</span><span className="text-slate-600">/</span><span className="font-semibold text-slate-100">{currentPage}</span></div>

          {/* Usuario */}
          <div className="flex items-center gap-4">
            <div className="hidden md:block text-right">
              <p className="max-w-48 truncate text-sm font-semibold text-slate-100">
                {user?.nombre_completo || [user?.nombre, user?.apellido].filter(Boolean).join(' ')}
              </p>
              <p className="text-[11px] font-semibold uppercase tracking-wide text-slate-400">
                {ROLE_NAMES[user?.role ?? user?.rol] || user?.role || user?.rol}
              </p>
            </div>

            <div className="relative">
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary-600 to-indigo-700 font-bold text-white shadow-md shadow-primary-900/15 transition hover:-translate-y-0.5"
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
