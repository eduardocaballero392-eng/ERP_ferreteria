/**
 * Página de Dashboard
 */

import { useState, useEffect } from 'react'
import { Card } from '@/components/common'
import { reportService } from '@/api'
import { formatCurrency, formatPercentage } from '@/utils'
import {
  TrendingUp,
  TrendingDown,
  Package,
  ShoppingBag,
  ShoppingCart,
  AlertTriangle,
} from 'lucide-react'
import toast from 'react-hot-toast'

export const DashboardPage = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const result = await reportService.getDashboard()
      setData(result)
    } catch (error) {
      toast.error('Error al cargar dashboard')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">
          Resumen general del negocio
        </p>
      </div>

      {/* Estadísticas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Ventas del día */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Ventas Hoy</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formatCurrency(data?.ventas_hoy || 0)}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <ShoppingBag className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </Card>

        {/* Ventas del mes */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Ventas del Mes</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formatCurrency(data?.ventas_mes || 0)}
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </Card>

        {/* Compras del mes */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Compras del Mes</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formatCurrency(data?.compras_mes || 0)}
              </p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <ShoppingCart className="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </Card>

        {/* Productos en stock */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Productos en Stock</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {data?.inventario?.total_productos || 0}
              </p>
              {data?.inventario?.productos_stock_bajo > 0 && (
                <p className="text-xs text-red-600 mt-1 flex items-center gap-1">
                  <AlertTriangle className="h-3 w-3" />
                  {data.inventario.productos_stock_bajo} bajo stock
                </p>
              )}
            </div>
            <div className="p-3 bg-orange-100 rounded-lg">
              <Package className="h-6 w-6 text-orange-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Utilidad y Margen */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Utilidad Bruta del Mes">
          <div className="text-3xl font-bold text-green-600">
            {formatCurrency(data?.utilidad_bruta || 0)}
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Ganancia después de costos
          </p>
        </Card>

        <Card title="Margen Promedio">
          <div className="text-3xl font-bold text-blue-600">
            {formatPercentage(data?.margen_promedio || 0)}
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Sobre ventas totales
          </p>
        </Card>
      </div>

      {/* Top productos, clientes, proveedores */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top productos */}
        <Card title="Top 5 Productos">
          <div className="space-y-3">
            {data?.top_productos?.map((producto, index) => (
              <div
                key={producto.producto_id}
                className="flex items-center justify-between"
              >
                <div className="flex items-center gap-2">
                  <span className="flex items-center justify-center w-6 h-6 rounded-full bg-primary-100 text-primary-600 text-xs font-medium">
                    {index + 1}
                  </span>
                  <span className="text-sm text-gray-900">
                    {producto.nombre}
                  </span>
                </div>
                <span className="text-sm font-medium text-gray-900">
                  {producto.cantidad_vendida}
                </span>
              </div>
            ))}
          </div>
        </Card>

        {/* Top clientes */}
        <Card title="Top 5 Clientes">
          <div className="space-y-3">
            {data?.top_clientes?.map((cliente, index) => (
              <div
                key={cliente.cliente_id}
                className="flex items-center justify-between"
              >
                <div className="flex items-center gap-2">
                  <span className="flex items-center justify-center w-6 h-6 rounded-full bg-green-100 text-green-600 text-xs font-medium">
                    {index + 1}
                  </span>
                  <span className="text-sm text-gray-900">
                    {cliente.nombre}
                  </span>
                </div>
                <span className="text-sm font-medium text-gray-900">
                  {formatCurrency(cliente.total_compras)}
                </span>
              </div>
            ))}
          </div>
        </Card>

        {/* Top proveedores */}
        <Card title="Top 5 Proveedores">
          <div className="space-y-3">
            {data?.top_proveedores?.map((proveedor, index) => (
              <div
                key={proveedor.proveedor_id}
                className="flex items-center justify-between"
              >
                <div className="flex items-center gap-2">
                  <span className="flex items-center justify-center w-6 h-6 rounded-full bg-purple-100 text-purple-600 text-xs font-medium">
                    {index + 1}
                  </span>
                  <span className="text-sm text-gray-900">
                    {proveedor.razon_social}
                  </span>
                </div>
                <span className="text-sm font-medium text-gray-900">
                  {formatCurrency(proveedor.total_compras)}
                </span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}
