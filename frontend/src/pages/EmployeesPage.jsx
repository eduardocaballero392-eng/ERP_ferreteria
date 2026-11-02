/**
 * Página de Empleados - Ver vendedores y almaceneros
 */

import { useState, useEffect } from 'react'
import {
  Card,
  Button,
  Badge,
  SearchBar,
  Loading,
  EmptyState,
} from '@/components/common'
import { Users, UserPlus, TrendingUp, Package, ShoppingBag } from 'lucide-react'
import { formatCurrency } from '@/utils'
import { Modal } from '@/components/common'
import { authService } from '@/api'
import toast from 'react-hot-toast'

export const EmployeesPage = () => {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filter, setFilter] = useState('todos') // todos, vendedor, almacenero
  const [createOpen, setCreateOpen] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({ nombre: '', apellido: '', email: '', password: '', role: 'vendedor' })

  useEffect(() => {
    loadEmployees()
  }, [])

  const loadEmployees = async () => {
    try {
      // El backend permite registrar usuarios, pero aún no ofrece un endpoint de listado.
      setEmployees([])
    } catch (error) {
      console.error('Error al cargar empleados:', error)
    } finally {
      setLoading(false)
    }
  }

  const createEmployee = async (event) => {
    event.preventDefault()
    setSaving(true)
    try {
      const created = await authService.register(form)
      const role = created.role || form.role
      setEmployees((current) => [{
        ...created,
        nombre_completo: created.nombre_completo || `${created.nombre} ${created.apellido}`,
        role,
        activo: created.activo ?? true,
        estadisticas: role === 'vendedor'
          ? { ventas_mes: 0, monto_vendido: 0, clientes_atendidos: 0 }
          : { compras_mes: 0, monto_compras: 0, productos_gestionados: 0 },
      }, ...current])
      setForm({ nombre: '', apellido: '', email: '', password: '', role: 'vendedor' })
      setCreateOpen(false)
      toast.success('Usuario creado correctamente')
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'No se pudo crear el usuario')
    } finally { setSaving(false) }
  }

  const getRoleBadge = (role) => {
    const variants = {
      vendedor: { color: 'info', label: 'Vendedor' },
      almacenero: { color: 'warning', label: 'Almacenero' },
    }
    const config = variants[role] || { color: 'info', label: role }
    return <Badge variant={config.color}>{config.label}</Badge>
  }

  const filteredEmployees = employees.filter((emp) => {
    const matchesSearch =
      emp.nombre_completo.toLowerCase().includes(searchTerm.toLowerCase()) ||
      emp.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filter === 'todos' || emp.role === filter
    return matchesSearch && matchesFilter
  })

  // Estadísticas generales
  const stats = {
    total: employees.length,
    vendedores: employees.filter((e) => e.role === 'vendedor').length,
    almaceneros: employees.filter((e) => e.role === 'almacenero').length,
    activos: employees.filter((e) => e.activo).length,
  }

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
          <p className="text-xs font-bold uppercase tracking-[.16em] text-primary-600">Administración de acceso</p>
          <h1 className="mt-1 text-3xl font-extrabold tracking-tight text-slate-900">Equipo de trabajo</h1>
          <p className="mt-1 text-sm text-slate-500">Crea usuarios y asigna el perfil de acceso adecuado.</p>
        </div>
        <Button onClick={() => setCreateOpen(true)} className="shrink-0">
          <UserPlus className="h-4 w-4" />
          Nuevo empleado
        </Button>
      </header>

      {/* Estadísticas */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Empleados</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {stats.total}
              </p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Vendedores</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {stats.vendedores}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <ShoppingBag className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Almaceneros</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {stats.almaceneros}
              </p>
            </div>
            <div className="p-3 bg-orange-100 rounded-lg">
              <Package className="h-6 w-6 text-orange-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Activos</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {stats.activos}
              </p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </Card>
      </div>

      <Card className="overflow-hidden p-0">
        <div className="flex flex-wrap items-center gap-4 border-b border-slate-100 bg-slate-50/60 px-5 py-4">
          <SearchBar
            value={searchTerm}
            onChange={setSearchTerm}
            placeholder="Buscar por nombre o email..."
            className="flex-1"
          />

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setFilter('todos')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'todos'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Todos
            </button>
            <button
              onClick={() => setFilter('vendedor')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'vendedor'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Vendedores
            </button>
            <button
              onClick={() => setFilter('almacenero')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'almacenero'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Almaceneros
            </button>
          </div>
        </div>

        {filteredEmployees.length === 0 ? (
          <EmptyState
            icon={Users}
            title="No hay empleados"
            description="Comienza agregando empleados a tu equipo"
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {filteredEmployees.map((employee) => (
              <div
                key={employee.id}
                className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                      <Users className="h-6 w-6 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">
                        {employee.nombre_completo}
                      </h3>
                      <p className="text-sm text-gray-500">{employee.email}</p>
                    </div>
                  </div>
                  {getRoleBadge(employee.role)}
                </div>

                {/* Información */}
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Teléfono:</span>
                    <span className="font-medium">{employee.telefono}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Estado:</span>
                    <Badge variant={employee.activo ? 'success' : 'danger'}>
                      {employee.activo ? 'Activo' : 'Inactivo'}
                    </Badge>
                  </div>
                </div>

                {/* Estadísticas del mes */}
                <div className="border-t pt-4">
                  <h4 className="text-sm font-semibold text-gray-700 mb-3">
                    Actividad del Mes
                  </h4>
                  {employee.role === 'vendedor' ? (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Ventas:</span>
                        <span className="font-medium">
                          {employee.estadisticas.ventas_mes}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Monto vendido:</span>
                        <span className="font-medium text-green-600">
                          {formatCurrency(employee.estadisticas.monto_vendido)}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Clientes:</span>
                        <span className="font-medium">
                          {employee.estadisticas.clientes_atendidos}
                        </span>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Compras:</span>
                        <span className="font-medium">
                          {employee.estadisticas.compras_mes}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Monto compras:</span>
                        <span className="font-medium text-blue-600">
                          {formatCurrency(employee.estadisticas.monto_compras)}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Productos:</span>
                        <span className="font-medium">
                          {employee.estadisticas.productos_gestionados}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
      <Modal isOpen={createOpen} onClose={() => setCreateOpen(false)} title="Nuevo empleado" size="md">
        <form onSubmit={createEmployee} className="grid gap-4 sm:grid-cols-2">
          <label className="label">Nombre<input className="input mt-1" required minLength="2" value={form.nombre} onChange={(event) => setForm({ ...form, nombre: event.target.value })} /></label>
          <label className="label">Apellido<input className="input mt-1" required minLength="2" value={form.apellido} onChange={(event) => setForm({ ...form, apellido: event.target.value })} /></label>
          <label className="label sm:col-span-2">Correo electrónico<input className="input mt-1" type="email" required value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} /></label>
          <label className="label sm:col-span-2">Contraseña inicial<input className="input mt-1" type="password" minLength="6" required value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} /></label>
          <label className="label sm:col-span-2">Rol<select className="input mt-1" value={form.role} onChange={(event) => setForm({ ...form, role: event.target.value })}><option value="vendedor">Vendedor</option><option value="almacenero">Almacenero</option></select></label>
          <div className="sm:col-span-2"><Button type="submit" loading={saving}>Crear usuario</Button></div>
        </form>
      </Modal>
    </div>
  )
}
