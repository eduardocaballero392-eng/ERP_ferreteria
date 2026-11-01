/**
 * Página de Inventario
 */

import { useState, useEffect } from 'react'
import { Card, Button, Badge } from '@/components/common'
import { productService } from '@/api'
import { formatCurrency } from '@/utils'
import { Package, Plus, AlertTriangle } from 'lucide-react'
import toast from 'react-hot-toast'

export const InventoryPage = () => {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      const data = await productService.getProductsDetails()
      setProducts(data)
    } catch (error) {
      toast.error('Error al cargar productos')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const getStockBadge = (status) => {
    const variants = {
      OK: 'success',
      REPONER: 'warning',
      AGOTADO: 'danger',
    }
    return <Badge variant={variants[status]}>{status}</Badge>
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Inventario</h1>
          <p className="text-gray-500 mt-1">
            {products.length} productos registrados
          </p>
        </div>
        <Button>
          <Plus className="h-4 w-4" />
          Nuevo Producto
        </Button>
      </div>

      {/* Alertas de stock bajo */}
      {products.some((p) => p.estado_stock !== 'OK') && (
        <Card>
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5" />
            <div>
              <p className="font-medium text-gray-900">
                Productos con stock bajo
              </p>
              <p className="text-sm text-gray-500 mt-1">
                {products.filter((p) => p.estado_stock !== 'OK').length}{' '}
                productos necesitan reposición
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* Tabla de productos */}
      <Card>
        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Producto</th>
                <th>Categoría</th>
                <th>Stock</th>
                <th>Estado</th>
                <th>Precio Venta</th>
                <th>Valor Stock</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id}>
                  <td className="font-mono text-xs">{product.codigo}</td>
                  <td>
                    <div>
                      <p className="font-medium">{product.nombre}</p>
                      <p className="text-xs text-gray-500">{product.marca}</p>
                    </div>
                  </td>
                  <td className="text-gray-600">
                    {product.categoria_nombre}
                  </td>
                  <td>
                    <div>
                      <p className="font-medium">{product.stock_actual}</p>
                      <p className="text-xs text-gray-500">
                        Min: {product.stock_minimo}
                      </p>
                    </div>
                  </td>
                  <td>{getStockBadge(product.estado_stock)}</td>
                  <td className="font-medium">
                    {formatCurrency(product.precio_venta)}
                  </td>
                  <td className="font-medium">
                    {formatCurrency(product.valor_stock)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
