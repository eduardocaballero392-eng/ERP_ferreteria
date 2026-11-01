/**
 * Página de Ventas
 */

import { useState, useEffect } from 'react'
import {
  Card,
  Button,
  Badge,
  Modal,
  SearchBar,
  Loading,
  EmptyState,
  Input,
  Select,
} from '@/components/common'
import {
  saleService,
  customerService,
  productService,
} from '@/api'
import { formatCurrency, formatDate } from '@/utils'
import {
  Plus,
  ShoppingBag,
  Eye,
  XCircle,
  Trash2,
} from 'lucide-react'
import toast from 'react-hot-toast'

export const SalesPage = () => {
  const [sales, setSales] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [showDetailModal, setShowDetailModal] = useState(false)
  const [selectedSale, setSelectedSale] = useState(null)

  // Form state
  const [formData, setFormData] = useState({
    cliente_id: '',
    tipo_comprobante: 'BOLETA',
    condicion_pago: 'CONTADO',
    observaciones: '',
  })
  const [items, setItems] = useState([])
  const [customers, setCustomers] = useState([])
  const [products, setProducts] = useState([])

  useEffect(() => {
    loadSales()
    loadCustomers()
    loadProducts()
  }, [])

  const loadSales = async () => {
    try {
      const data = await saleService.getSales()
      setSales(data)
    } catch (error) {
      toast.error('Error al cargar ventas')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const loadCustomers = async () => {
    try {
      const data = await customerService.getCustomers()
      setCustomers(data)
    } catch (error) {
      console.error('Error al cargar clientes:', error)
    }
  }

  const loadProducts = async () => {
    try {
      const data = await productService.getProducts()
      setProducts(data.filter((p) => p.stock_actual > 0))
    } catch (error) {
      console.error('Error al cargar productos:', error)
    }
  }

  const handleAddItem = () => {
    setItems([
      ...items,
      { producto_id: '', cantidad: 1, precio_unitario: 0 },
    ])
  }

  const handleRemoveItem = (index) => {
    setItems(items.filter((_, i) => i !== index))
  }

  const handleItemChange = (index, field, value) => {
    const newItems = [...items]
    newItems[index][field] = value

    // Si cambia el producto, actualizar el precio
    if (field === 'producto_id') {
      const product = products.find((p) => p.id === parseInt(value))
      if (product) {
        newItems[index].precio_unitario = product.precio_venta
      }
    }

    setItems(newItems)
  }

  const calculateTotal = () => {
    const subtotal = items.reduce(
      (sum, item) => sum + item.cantidad * item.precio_unitario,
      0
    )
    const igv = subtotal * 0.18
    return {
      subtotal,
      igv,
      total: subtotal + igv,
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.cliente_id) {
      toast.error('Selecciona un cliente')
      return
    }

    if (items.length === 0) {
      toast.error('Agrega al menos un producto')
      return
    }

    try {
      await saleService.createSale({
        ...formData,
        cliente_id: parseInt(formData.cliente_id),
        detalle: items.map((item) => ({
          producto_id: parseInt(item.producto_id),
          cantidad: parseFloat(item.cantidad),
          precio_unitario: parseFloat(item.precio_unitario),
        })),
      })

      toast.success('Venta registrada exitosamente')
      setShowModal(false)
      resetForm()
      loadSales()
    } catch (error) {
      toast.error(error.message || 'Error al registrar venta')
    }
  }

  const resetForm = () => {
    setFormData({
      cliente_id: '',
      tipo_comprobante: 'BOLETA',
      condicion_pago: 'CONTADO',
      observaciones: '',
    })
    setItems([])
  }

  const handleViewDetail = async (sale) => {
    try {
      const detail = await saleService.getSale(sale.id)
      setSelectedSale(detail)
      setShowDetailModal(true)
    } catch (error) {
      toast.error('Error al cargar detalle')
    }
  }

  const handleCancel = async (id) => {
    if (!window.confirm('¿Estás seguro de anular esta venta?')) return

    try {
      await saleService.cancelSale(id)
      toast.success('Venta anulada')
      loadSales()
    } catch (error) {
      toast.error(error.message || 'Error al anular venta')
    }
  }

  const getStatusBadge = (status) => {
    return status === 'COMPLETADA' ? (
      <Badge variant="success">Completada</Badge>
    ) : (
      <Badge variant="danger">Anulada</Badge>
    )
  }

  const filteredSales = sales.filter(
    (sale) =>
      sale.numero_comprobante.toLowerCase().includes(searchTerm.toLowerCase()) ||
      sale.cliente_nombre?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const totals = calculateTotal()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loading />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Ventas</h1>
          <p className="text-gray-500 mt-1">{sales.length} ventas registradas</p>
        </div>
        <Button onClick={() => setShowModal(true)}>
          <Plus className="h-4 w-4" />
          Nueva Venta
        </Button>
      </div>

      <Card>
        <div className="mb-4">
          <SearchBar
            value={searchTerm}
            onChange={setSearchTerm}
            placeholder="Buscar por número de comprobante o cliente..."
          />
        </div>

        {filteredSales.length === 0 ? (
          <EmptyState
            icon={ShoppingBag}
            title="No hay ventas"
            description="Comienza registrando tu primera venta"
            action={
              <Button onClick={() => setShowModal(true)}>
                <Plus className="h-4 w-4" />
                Nueva Venta
              </Button>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Comprobante</th>
                  <th>Fecha</th>
                  <th>Cliente</th>
                  <th>Tipo</th>
                  <th>Condición</th>
                  <th>Total</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredSales.map((sale) => (
                  <tr key={sale.id}>
                    <td className="font-mono text-sm">{sale.numero_comprobante}</td>
                    <td>{formatDate(sale.fecha)}</td>
                    <td>{sale.cliente_nombre}</td>
                    <td>
                      <Badge variant="info">{sale.tipo_comprobante}</Badge>
                    </td>
                    <td>{sale.condicion_pago}</td>
                    <td className="font-medium">{formatCurrency(sale.total)}</td>
                    <td>{getStatusBadge(sale.estado)}</td>
                    <td>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleViewDetail(sale)}
                          className="p-1 hover:bg-gray-100 rounded"
                          title="Ver detalle"
                        >
                          <Eye className="h-4 w-4 text-gray-600" />
                        </button>
                        {sale.estado === 'COMPLETADA' && (
                          <button
                            onClick={() => handleCancel(sale.id)}
                            className="p-1 hover:bg-red-50 rounded"
                            title="Anular"
                          >
                            <XCircle className="h-4 w-4 text-red-600" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {/* Modal Nueva Venta */}
      <Modal
        isOpen={showModal}
        onClose={() => {
          setShowModal(false)
          resetForm()
        }}
        title="Nueva Venta"
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              label="Cliente"
              value={formData.cliente_id}
              onChange={(e) =>
                setFormData({ ...formData, cliente_id: e.target.value })
              }
              options={customers.map((c) => ({
                value: c.id,
                label: `${c.nombres} ${c.apellidos || ''} - ${c.tipo_documento}: ${c.numero_documento}`,
              }))}
              required
            />

            <Select
              label="Tipo de Comprobante"
              value={formData.tipo_comprobante}
              onChange={(e) =>
                setFormData({ ...formData, tipo_comprobante: e.target.value })
              }
              options={[
                { value: 'BOLETA', label: 'Boleta' },
                { value: 'FACTURA', label: 'Factura' },
              ]}
              required
            />

            <Select
              label="Condición de Pago"
              value={formData.condicion_pago}
              onChange={(e) =>
                setFormData({ ...formData, condicion_pago: e.target.value })
              }
              options={[
                { value: 'CONTADO', label: 'Contado' },
                { value: 'CREDITO', label: 'Crédito' },
              ]}
              required
            />
          </div>

          {/* Productos */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="label">Productos</label>
              <Button
                type="button"
                variant="secondary"
                size="sm"
                onClick={handleAddItem}
              >
                <Plus className="h-4 w-4" />
                Agregar Producto
              </Button>
            </div>

            <div className="space-y-2">
              {items.map((item, index) => (
                <div
                  key={index}
                  className="flex items-end gap-2 p-3 bg-gray-50 rounded-lg"
                >
                  <div className="flex-1">
                    <Select
                      label="Producto"
                      value={item.producto_id}
                      onChange={(e) =>
                        handleItemChange(index, 'producto_id', e.target.value)
                      }
                      options={products.map((p) => ({
                        value: p.id,
                        label: `${p.nombre} - Stock: ${p.stock_actual}`,
                      }))}
                      required
                    />
                  </div>
                  <div className="w-24">
                    <Input
                      label="Cantidad"
                      type="number"
                      min="1"
                      value={item.cantidad}
                      onChange={(e) =>
                        handleItemChange(index, 'cantidad', e.target.value)
                      }
                      required
                    />
                  </div>
                  <div className="w-32">
                    <Input
                      label="Precio"
                      type="number"
                      step="0.01"
                      min="0"
                      value={item.precio_unitario}
                      onChange={(e) =>
                        handleItemChange(
                          index,
                          'precio_unitario',
                          e.target.value
                        )
                      }
                      required
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveItem(index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Totales */}
          {items.length > 0 && (
            <div className="border-t pt-4">
              <div className="flex justify-end">
                <div className="w-64 space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Subtotal:</span>
                    <span className="font-medium">
                      {formatCurrency(totals.subtotal)}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">IGV (18%):</span>
                    <span className="font-medium">
                      {formatCurrency(totals.igv)}
                    </span>
                  </div>
                  <div className="flex justify-between text-lg font-bold border-t pt-2">
                    <span>Total:</span>
                    <span>{formatCurrency(totals.total)}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          <Input
            label="Observaciones (opcional)"
            value={formData.observaciones}
            onChange={(e) =>
              setFormData({ ...formData, observaciones: e.target.value })
            }
          />

          <div className="flex items-center justify-end gap-2 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setShowModal(false)
                resetForm()
              }}
            >
              Cancelar
            </Button>
            <Button type="submit">Registrar Venta</Button>
          </div>
        </form>
      </Modal>

      {/* Modal Detalle */}
      <Modal
        isOpen={showDetailModal}
        onClose={() => setShowDetailModal(false)}
        title="Detalle de Venta"
        size="lg"
      >
        {selectedSale && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Comprobante</p>
                <p className="font-medium">{selectedSale.numero_comprobante}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Fecha</p>
                <p className="font-medium">{formatDate(selectedSale.fecha)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Cliente</p>
                <p className="font-medium">{selectedSale.cliente_nombre}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Estado</p>
                {getStatusBadge(selectedSale.estado)}
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-2">Productos</h4>
              <table className="w-full text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left p-2">Producto</th>
                    <th className="text-right p-2">Cantidad</th>
                    <th className="text-right p-2">Precio</th>
                    <th className="text-right p-2">Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedSale.detalle?.map((item, index) => (
                    <tr key={index} className="border-b">
                      <td className="p-2">{item.producto_nombre}</td>
                      <td className="text-right p-2">{item.cantidad}</td>
                      <td className="text-right p-2">
                        {formatCurrency(item.precio_unitario)}
                      </td>
                      <td className="text-right p-2">
                        {formatCurrency(item.subtotal)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="border-t pt-4">
              <div className="flex justify-end">
                <div className="w-64 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Subtotal:</span>
                    <span className="font-medium">
                      {formatCurrency(selectedSale.subtotal)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">IGV:</span>
                    <span className="font-medium">
                      {formatCurrency(selectedSale.igv)}
                    </span>
                  </div>
                  <div className="flex justify-between text-lg font-bold border-t pt-2">
                    <span>Total:</span>
                    <span>{formatCurrency(selectedSale.total)}</span>
                  </div>
                </div>
              </div>
            </div>

            {selectedSale.observaciones && (
              <div>
                <p className="text-sm text-gray-500">Observaciones</p>
                <p className="text-sm">{selectedSale.observaciones}</p>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  )
}
