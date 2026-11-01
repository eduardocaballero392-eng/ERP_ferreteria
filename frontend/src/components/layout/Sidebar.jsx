/**
 * Sidebar con navegación
 */

import { NavLink } from 'react-router-dom'
import { clsx } from 'clsx'
import {
  LayoutDashboard,
  Package,
  ShoppingCart,
  ShoppingBag,
  Users,
  TrendingUp,
  X,
} from 'lucide-react'
import { useAuth } from '@/context/AuthContext'

const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
    permission: null, // Todos pueden ver
  },
  {
    name: 'Inventario',
    href: '/inventory',
    icon: Package,
    permission: 'inventory',
  },
  {
    name: 'Ventas',
    href: '/sales',
    icon: ShoppingBag,
    permission: 'sales',
  },
  {
    name: 'Compras',
    href: '/purchases',
    icon: ShoppingCart,
    permission: 'purchases',
  },
  {
    name: 'Clientes',
    href: '/customers',
    icon: Users,
    permission: 'customers',
  },
  {
    name: 'Reportes',
    href: '/reports',
    icon: TrendingUp,
    permission: 'reports',
  },
]

export const Sidebar = ({ isOpen, onClose }) => {
  const { hasPermission } = useAuth()

  const filteredNavigation = navigation.filter(
    (item) => !item.permission || hasPermission(item.permission)
  )

  return (
    <>
      {/* Overlay móvil */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={clsx(
          'fixed top-0 left-0 z-30 h-full w-64 bg-white border-r border-gray-200 transition-transform duration-300 ease-in-out',
          'lg:translate-x-0 lg:top-16',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex items-center justify-between p-4 border-b border-gray-200 lg:hidden">
          <h2 className="text-lg font-semibold text-gray-900">Menú</h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="p-4 space-y-1">
          {filteredNavigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              onClick={onClose}
              className={({ isActive }) =>
                clsx(
                  'flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-700 hover:bg-gray-100'
                )
              }
            >
              <item.icon className="h-5 w-5" />
              {item.name}
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  )
}
