/**
 * Página de Clientes
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
import { customerService } from '@/api'
import { formatCurrency, formatDocument } from '@/utils'
import { Plus, Users, Edit, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'

export const CustomersPage = () => {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingCustomer, setEditingCustomer] = useState(null)
  
  const [formData, setFormData] = useState({
    tipo_documento: 'DNI',
    numero_documento: '',
    nombres: '',
    apellidos: '',
    telefono: '',
    email: '',
    direccion: '',
    limite_credito: 0,
  })

  useEffect(() => {
    loadCustomers()
  }, [])

  const loadCustomers = async () => {
    try {
      const data = await customerService.getCustomersWithStats()
      setCustomers(data)
    } catch (error) {
      toast.error('Error al cargar clientes')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      if (editingCustomer) {
        await customerService.updateCustomer(editingCustomer.id, formData)
        toast.success('Cliente actualizado exitosamente')
      } else {
        await customerService.createCustomer(formData)
        toast.success('Cliente registrado exitosamente')
      }

      setShowModal(false)
      resetForm()
      loadCustomers()
    } catch (error) {
      toast.error(error.message || 'Error al guardar cliente')
    }
  }

  const handleEdit = (customer) => {
    setEditingCustomer(customer)
    setFormData({
      tipo_documento: customer.tipo_documento ?? 'DNI',
      numero_documento: customer.numero_documento ?? '',
      nombres: customer.nombres ?? customer.razon_social ?? '',
      apellidos: customer.apellidos ?? '',
      telefono: customer.telefono ?? '',
      email: customer.email ?? '',
      direccion: customer.direccion ?? '',
      limite_credito: customer.limite_credito ?? 0,
    })
    setShowModal(true)
  }

  const handleDelete = async (id) => {
    if (!window.confirm('¿Estás seguro de eliminar este cliente?')) return

    try {
      await customerService.deleteCustomer(id)
      toast.success('Cliente eliminado')
      loadCustomers()
    } catch (error) {
      toast.error(error.message || 'Error al eliminar cliente')
    }
  }

  const resetForm = () => {
    setFormData({
      tipo_documento: 'DNI',
      numero_documento: '',
      nombres: '',
      apellidos: '',
      telefono: '',
      email: '',
      direccion: '',
      limite_credito: 0,
    })
    setEditingCustomer(null)
  }

  const filteredCustomers = customers.filter(
    (customer) => {
      const query = searchTerm.trim().toLowerCase()
      return [customer.nombres, customer.apellidos, customer.numero_documento]
        .some((value) => String(value ?? '').toLowerCase().includes(query))
    }
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loading />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-[.16em] text-primary-600">Relaciones comerciales</p>
          <h1 className="mt-1 text-3xl font-extrabold tracking-tight text-slate-900">Clientes</h1>
          <p className="mt-1 text-sm text-slate-500">{customers.length} clientes registrados · historial y capacidad de crédito</p>
        </div>
        <Button onClick={() => setShowModal(true)} className="shrink-0">
          <Plus className="h-4 w-4" />
          Nuevo cliente
        </Button>
      </header>

      <Card className="overflow-hidden p-0">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 bg-slate-50/60 px-5 py-4">
          <div><h2 className="text-sm font-bold text-slate-800">Directorio de clientes</h2><p className="mt-0.5 text-xs text-slate-500">Consulta documentos, contacto y crédito disponible.</p></div>
          <SearchBar
            value={searchTerm}
            onChange={setSearchTerm}
            placeholder="Buscar por nombre o documento..."
            className="w-full sm:max-w-xs"
          />
        </div>

        {filteredCustomers.length === 0 ? (
          <EmptyState
            icon={Users}
            title="No hay clientes"
            description="Comienza registrando tu primer cliente"
            action={
              <Button onClick={() => setShowModal(true)}>
                <Plus className="h-4 w-4" />
                Nuevo Cliente
              </Button>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Documento</th>
                  <th>Cliente</th>
                  <th>Contacto</th>
                  <th>Límite Crédito</th>
                  <th>Crédito Disponible</th>
                  <th>Total Compras</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredCustomers.map((customer) => (
                  <tr key={customer.id}>
                    <td>
                      <div className="text-sm">
                        <div className="font-medium">
                          {customer.tipo_documento}
                        </div>
                        <div className="text-gray-500">
                      {formatDocument(customer.tipo_documento, customer.numero_documento)}
                        </div>
                      </div>
                    </td>
                    <td>
                      <div className="font-medium">
                          {[customer.nombres, customer.apellidos].filter(Boolean).join(' ') || customer.razon_social || customer.nombre_comercial || '—'}
                      </div>
                    </td>
                    <td>
                      <div className="text-sm">
                        {customer.telefono && (
                          <div>{customer.telefono}</div>
                        )}
                        {customer.email && (
                          <div className="text-gray-500">{customer.email}</div>
                        )}
                      </div>
                    </td>
                    <td className="font-medium">
                      {formatCurrency(customer.limite_credito)}
                    </td>
                    <td>
                      <Badge
                        variant={
                          customer.disponible_credito > 0
                            ? 'success'
                            : 'warning'
                        }
                      >
                        {formatCurrency(customer.disponible_credito)}
                      </Badge>
                    </td>
                    <td className="font-medium">
                      {formatCurrency(customer.total_compras || 0)}
                    </td>
                    <td>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleEdit(customer)}
                          className="p-1 hover:bg-gray-100 rounded"
                          title="Editar"
                        >
                          <Edit className="h-4 w-4 text-gray-600" />
                        </button>
                        <button
                          onClick={() => handleDelete(customer.id)}
                          className="p-1 hover:bg-red-50 rounded"
                          title="Eliminar"
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {/* Modal Formulario */}
      <Modal
        isOpen={showModal}
        onClose={() => {
          setShowModal(false)
          resetForm()
        }}
        title={editingCustomer ? 'Editar Cliente' : 'Nuevo Cliente'}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              label="Tipo de Documento"
              value={formData.tipo_documento}
              onChange={(e) =>
                setFormData({ ...formData, tipo_documento: e.target.value })
              }
              options={[
                { value: 'DNI', label: 'DNI' },
                { value: 'RUC', label: 'RUC' },
              ]}
              required
            />

            <Input
              label={`Número de ${formData.tipo_documento}`}
              type="text"
              value={formData.numero_documento}
              onChange={(e) =>
                setFormData({ ...formData, numero_documento: e.target.value })
              }
              maxLength={formData.tipo_documento === 'DNI' ? 8 : 11}
              required
            />

            <Input
              label="Nombres"
              value={formData.nombres}
              onChange={(e) =>
                setFormData({ ...formData, nombres: e.target.value })
              }
              required
            />

            <Input
              label="Apellidos"
              value={formData.apellidos}
              onChange={(e) =>
                setFormData({ ...formData, apellidos: e.target.value })
              }
            />

            <Input
              label="Teléfono"
              type="tel"
              value={formData.telefono}
              onChange={(e) =>
                setFormData({ ...formData, telefono: e.target.value })
              }
            />

            <Input
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
            />

            <Input
              label="Límite de Crédito"
              type="number"
              step="0.01"
              min="0"
              value={formData.limite_credito}
              onChange={(e) =>
                setFormData({ ...formData, limite_credito: e.target.value })
              }
            />
          </div>

          <Input
            label="Dirección"
            value={formData.direccion}
            onChange={(e) =>
              setFormData({ ...formData, direccion: e.target.value })
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
            <Button type="submit">
              {editingCustomer ? 'Actualizar' : 'Registrar'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
