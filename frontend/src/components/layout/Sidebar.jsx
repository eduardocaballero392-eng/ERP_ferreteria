/**
 * Sidebar con navegación y submenús desplegables
 */

import { useEffect, useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { clsx } from 'clsx'
import {
  LayoutDashboard,
  Package,
  ShoppingCart,
  ShoppingBag,
  Users,
  TrendingUp,
  X,
  ChevronDown,
  ChevronRight,
  Box,
  Tag,
  Layers,
  TrendingUp as ArrowUpCircle,
  FileText,
  DollarSign,
  Truck,
  UserCog,
  BarChart3,
  PieChart,
  Activity,
} from 'lucide-react'

export const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation()
  const [openMenus, setOpenMenus] = useState({})

  useEffect(() => {
    setOpenMenus((current) => ({
      ...current,
      Inventario: location.pathname.startsWith('/inventory'),
      Ventas: location.pathname.startsWith('/sales'),
      Compras: location.pathname.startsWith('/purchases'),
      Empleados: location.pathname.startsWith('/employees'),
      Reportes: location.pathname.startsWith('/reports'),
    }))
  }, [location.pathname])

  const toggleMenu = (menuName) => {
    setOpenMenus(prev => ({
      ...prev,
      [menuName]: !prev[menuName]
    }))
  }

  // Navegación con submenús
  const navigation = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: LayoutDashboard,
    },
    {
      name: 'Inventario',
      icon: Package,
      subItems: [
        {
          name: 'Productos',
          href: '/inventory',
          icon: Box,
          description: 'Gestión de productos'
        },
        {
          name: 'Categorías',
          href: '/inventory/categories',
          icon: Tag,
          description: 'Organizar por categorías'
        },
        {
          name: 'Movimientos',
          href: '/inventory/movements',
          icon: ArrowUpCircle,
          description: 'Historial de stock'
        },
        {
          name: 'Ajustes de Stock',
          href: '/inventory/adjustments',
          icon: Layers,
          description: 'Corrección de inventario'
        },
      ]
    },
    {
      name: 'Ventas',
      icon: ShoppingBag,
      subItems: [
        {
          name: 'Nueva Venta',
          href: '/sales/new',
          icon: FileText,
          description: 'Registrar venta'
        },
        {
          name: 'Listado de Ventas',
          href: '/sales',
          icon: ShoppingBag,
          description: 'Ver todas las ventas'
        },
        {
          name: 'Cotizaciones',
          href: '/sales/quotes',
          icon: FileText,
          description: 'Gestionar cotizaciones'
        },
        {
          name: 'Ventas a Crédito',
          href: '/sales/receivables',
          icon: DollarSign,
          description: 'Ventas registradas a crédito'
        },
      ]
    },
    {
      name: 'Compras',
      icon: ShoppingCart,
      subItems: [
        {
          name: 'Nueva Compra',
          href: '/purchases/new',
          icon: FileText,
          description: 'Registrar compra'
        },
        {
          name: 'Listado de Compras',
          href: '/purchases',
          icon: ShoppingCart,
          description: 'Ver todas las compras'
        },
        {
          name: 'Proveedores',
          href: '/purchases/suppliers',
          icon: Truck,
          description: 'Gestionar proveedores'
        },
        {
          name: 'Cuentas por Pagar',
          href: '/purchases/payables',
          icon: DollarSign,
          description: 'Deudas pendientes'
        },
      ]
    },
    {
      name: 'Clientes',
      href: '/customers',
      icon: Users,
    },
    {
      name: 'Empleados',
      icon: UserCog,
      subItems: [
        {
          name: 'Listado',
          href: '/employees',
          icon: Users,
          description: 'Ver empleados'
        },
        {
          name: 'Vendedores',
          href: '/employees/sellers',
          icon: ShoppingBag,
          description: 'Estadísticas de ventas'
        },
        {
          name: 'Almaceneros',
          href: '/employees/warehouse',
          icon: Package,
          description: 'Actividad de almacén'
        },
      ]
    },
    {
      name: 'Reportes',
      icon: TrendingUp,
      subItems: [
        {
          name: 'Dashboard Ejecutivo',
          href: '/reports',
          icon: BarChart3,
          description: 'Vista general'
        },
        {
          name: 'Ventas por Período',
          href: '/reports/sales',
          icon: PieChart,
          description: 'Análisis de ventas'
        },
        {
          name: 'Inventario Valorizado',
          href: '/reports/inventory',
          icon: Package,
          description: 'Valor del stock'
        },
        {
          name: 'Rentabilidad',
          href: '/reports/profitability',
          icon: Activity,
          description: 'Utilidad bruta'
        },
      ]
    },
  ]

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
          'fixed top-0 left-0 z-30 h-full w-64 bg-white border-r border-gray-200 transition-transform duration-300 ease-in-out overflow-y-auto',
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
          {navigation.map((item) => (
            <div key={item.name}>
              {/* Item sin submenú */}
              {!item.subItems ? (
                <NavLink
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
              ) : (
                /* Item con submenú (acordeón) */
                <div>
                  <button
                    onClick={() => toggleMenu(item.name)}
                    className={clsx(
                      'flex items-center justify-between w-full gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors',
                      openMenus[item.name]
                        ? 'bg-gray-100 text-gray-900'
                        : 'text-gray-700 hover:bg-gray-50'
                    )}
                  >
                    <div className="flex items-center gap-3">
                      <item.icon className="h-5 w-5" />
                      {item.name}
                    </div>
                    {openMenus[item.name] ? (
                      <ChevronDown className="h-4 w-4" />
                    ) : (
                      <ChevronRight className="h-4 w-4" />
                    )}
                  </button>

                  {/* Submenú desplegable */}
                  <div
                    className={clsx(
                      'overflow-hidden transition-all duration-200',
                      openMenus[item.name] ? 'max-h-[36rem] mt-1' : 'max-h-0'
                    )}
                  >
                    <div className="ml-4 space-y-1 border-l-2 border-gray-200 pl-2">
                      {item.subItems.map((subItem) => (
                        <NavLink
                          key={subItem.name}
                          to={subItem.href}
                          onClick={onClose}
                          className={({ isActive }) =>
                            clsx(
                              'flex items-start gap-3 px-3 py-2 rounded-lg text-sm transition-colors group',
                              isActive
                                ? 'bg-primary-50 text-primary-700'
                                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                            )
                          }
                        >
                          <subItem.icon className="h-4 w-4 mt-0.5 flex-shrink-0" />
                          <div className="flex-1 min-w-0">
                            <div className="font-medium">{subItem.name}</div>
                            {subItem.description && (
                              <div className="text-xs text-gray-500 mt-0.5">
                                {subItem.description}
                              </div>
                            )}
                          </div>
                        </NavLink>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </nav>
      </aside>
    </>
  )
}
