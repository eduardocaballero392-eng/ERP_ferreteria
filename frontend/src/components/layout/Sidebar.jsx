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
          'fixed top-0 left-0 z-30 h-full w-64 overflow-y-auto border-r border-slate-800 bg-[#111b2e] text-slate-200 transition-transform duration-300 ease-in-out',
          'lg:translate-x-0 lg:top-16 lg:h-[calc(100vh-4rem)]',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex items-center justify-between border-b border-white/10 p-4 lg:hidden">
          <div><p className="text-sm font-bold text-white">ERP Ferretería</p><p className="mt-0.5 text-[10px] font-semibold uppercase tracking-[.14em] text-slate-500">Navegación</p></div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-300 transition hover:bg-white/10 hover:text-white"
            aria-label="Cerrar menú de navegación"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav aria-label="Navegación principal" className="space-y-1 px-3 py-5">
          <p className="mb-3 px-3.5 text-[10px] font-bold uppercase tracking-[.18em] text-slate-600">Menú principal</p>
          {navigation.map((item) => (
            <div key={item.name}>
              {/* Item sin submenú */}
              {!item.subItems ? (
                <NavLink
                  to={item.href}
                  onClick={onClose}
                  className={({ isActive }) =>
                    clsx(
                      'flex items-center gap-3 rounded-xl px-3.5 py-3 text-sm font-semibold transition-all',
                      isActive
                        ? 'bg-blue-500/15 text-blue-200 ring-1 ring-inset ring-blue-400/10'
                        : 'text-slate-400 hover:bg-white/[.06] hover:text-white'
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
                      'flex w-full items-center justify-between gap-3 rounded-xl px-3.5 py-3 text-sm font-semibold transition-all',
                      openMenus[item.name]
                        ? 'bg-white/[.07] text-white'
                        : 'text-slate-400 hover:bg-white/[.05] hover:text-white'
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
                    <div className="ml-4 space-y-1 border-l border-white/10 pl-2">
                      {item.subItems.map((subItem) => (
                        <NavLink
                          key={subItem.name}
                          to={subItem.href}
                          end
                          onClick={onClose}
                          className={({ isActive }) =>
                            clsx(
                              'group flex items-start gap-3 rounded-lg px-3 py-2.5 text-[13px] transition-all',
                              isActive
                                ? 'bg-blue-500/15 font-semibold text-blue-200'
                                : 'text-slate-500 hover:bg-white/[.05] hover:text-slate-100'
                            )
                          }
                        >
                          <subItem.icon className="h-4 w-4 mt-0.5 flex-shrink-0" />
                          <div className="flex-1 min-w-0">
                            <div className="font-medium">{subItem.name}</div>
                            {subItem.description && (
                              <div className="mt-0.5 text-[11px] leading-4 text-slate-500 group-hover:text-slate-400">
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
