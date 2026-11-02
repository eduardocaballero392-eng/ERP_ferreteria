/**
 * Página de Dashboard - Rediseño de Arquitectura UI
 */

import { useState, useEffect, useRef } from 'react'
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
  LayoutDashboard,
  Loader2,
  ArrowUpRight,
  Upload,
  FileText,
  X,
  CheckCircle2,
  AlertCircle,
  Activity
} from 'lucide-react'
import toast from 'react-hot-toast'

// Sub-componente para subir CSV
const CSVUploader = ({ onUploadComplete }) => {
  const [selectedEntity, setSelectedEntity] = useState('')
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)

  const entities = [
    { value: 'productos', label: 'Productos', icon: Package },
    { value: 'categorias', label: 'Categorías', icon: FileText },
    { value: 'clientes', label: 'Clientes', icon: ShoppingBag },
    { value: 'proveedores', label: 'Proveedores', icon: ShoppingCart },
    { value: 'ventas', label: 'Ventas', icon: TrendingUp },
    { value: 'compras', label: 'Compras', icon: ShoppingCart },
  ]

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && droppedFile.name.endsWith('.csv')) {
      setFile(droppedFile)
    } else {
      toast.error('Por favor selecciona un archivo CSV')
    }
  }

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.name.endsWith('.csv')) {
      setFile(selectedFile)
    } else {
      toast.error('Por favor selecciona un archivo CSV')
    }
  }

  const handleUpload = async () => {
    if (!selectedEntity) {
      toast.error('Selecciona una entidad')
      return
    }
    if (!file) {
      toast.error('Selecciona un archivo CSV')
      return
    }

    setUploading(true)
    
    try {
      // Importar el servicio dinámicamente
      const { uploadService } = await import('@/api')
      
      const result = await uploadService.uploadCSV(file, selectedEntity)
      
      toast.success(
        `✅ ${result.created} registros creados, ${result.updated} actualizados`,
        { duration: 4000 }
      )
      
      if (result.errors && result.errors.length > 0) {
        toast.error(`⚠️ ${result.errors.length} errores encontrados`)
      }
      
      // Reset
      setFile(null)
      setSelectedEntity('')
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      
      // Callback para recargar datos
      if (onUploadComplete) {
        onUploadComplete()
      }
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Error al cargar el archivo'
      toast.error(errorMsg)
      console.error(error)
    } finally {
      setUploading(false)
    }
  }

  return (
    <Card className="border-0 shadow-sm bg-white">
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-50 rounded-lg">
            <Upload className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-slate-900">Cargar Datos desde CSV</h3>
            <p className="text-sm text-slate-500">Importa datos masivos a tu sistema</p>
          </div>
        </div>

        {/* Selector de entidad */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Selecciona la entidad
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {entities.map((entity) => {
              const Icon = entity.icon
              return (
                <button
                  key={entity.value}
                  onClick={() => setSelectedEntity(entity.value)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg border-2 transition-all ${
                    selectedEntity === entity.value
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300 text-slate-600'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span className="text-sm font-medium">{entity.label}</span>
                </button>
              )
            })}
          </div>
        </div>

        {/* Zona de drop */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`relative border-2 border-dashed rounded-xl p-8 transition-all cursor-pointer ${
            isDragging
              ? 'border-blue-500 bg-blue-50'
              : file
              ? 'border-emerald-500 bg-emerald-50'
              : 'border-gray-300 hover:border-gray-400 bg-gray-50'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            className="hidden"
          />
          
          <div className="text-center">
            {file ? (
              <div className="flex flex-col items-center">
                <CheckCircle2 className="h-12 w-12 text-emerald-600 mb-3" />
                <p className="text-sm font-medium text-slate-900">{file.name}</p>
                <p className="text-xs text-slate-500 mt-1">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    setFile(null)
                    if (fileInputRef.current) {
                      fileInputRef.current.value = ''
                    }
                  }}
                  className="mt-3 text-sm text-red-600 hover:text-red-700 font-medium"
                >
                  Eliminar archivo
                </button>
              </div>
            ) : (
              <>
                <Upload className="h-12 w-12 text-gray-400 mx-auto mb-3" />
                <p className="text-sm font-medium text-slate-900">
                  Arrastra tu archivo CSV aquí
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  o haz clic para seleccionar
                </p>
              </>
            )}
          </div>
        </div>

        {/* Botón de carga */}
        <button
          onClick={handleUpload}
          disabled={!file || !selectedEntity || uploading}
          className={`w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg font-medium transition-all ${
            !file || !selectedEntity || uploading
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700 shadow-sm hover:shadow-md'
          }`}
        >
          {uploading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Cargando...
            </>
          ) : (
            <>
              <Upload className="h-5 w-5" />
              Cargar Archivo
            </>
          )}
        </button>

        {/* Información */}
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
          <div className="flex gap-2">
            <AlertCircle className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div className="text-xs text-amber-800">
              <p className="font-medium mb-1">Formato CSV requerido:</p>
              <ul className="list-disc list-inside space-y-0.5 text-amber-700">
                <li>Primera fila debe contener los nombres de columnas</li>
                <li>Usa comas (,) como separador</li>
                <li>Codificación UTF-8 recomendada</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </Card>
  )
}

// Sub-componente para las tarjetas de estadísticas (KPI)
const StatCard = ({ title, value, icon: Icon, color = 'blue', trend, subtitle }) => {
  // Mapeo de colores suaves para fondos e iconos
  const colorMap = {
    emerald: { bg: 'bg-emerald-50', text: 'text-emerald-600', iconBg: 'bg-emerald-100' },
    blue: { bg: 'bg-blue-50', text: 'text-blue-600', iconBg: 'bg-blue-100' },
    purple: { bg: 'bg-purple-50', text: 'text-purple-600', iconBg: 'bg-purple-100' },
    amber: { bg: 'bg-amber-50', text: 'text-amber-600', iconBg: 'bg-amber-100' },
  }
  const styles = colorMap[color] || colorMap.blue

  return (
    <Card className="relative overflow-hidden group hover:shadow-lg transition-all duration-300 border-0 shadow-sm bg-white">
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="text-3xl font-bold text-slate-900 tracking-tight">{value}</p>
          {subtitle && (
            <div className="flex items-center gap-1 mt-1">
              {trend === 'up' && <ArrowUpRight className="h-3 w-3 text-emerald-500" />}
              {trend === 'down' && <TrendingDown className="h-3 w-3 text-red-500" />}
              <p className={`text-xs font-medium ${trend === 'up' ? 'text-emerald-600' : trend === 'down' ? 'text-red-600' : 'text-slate-500'}`}>
                {subtitle}
              </p>
            </div>
          )}
        </div>
        <div className={`p-3 rounded-xl ${styles.iconBg} ${styles.text} transition-colors group-hover:bg-opacity-80`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      {/* Barra decorativa inferior */}
      <div className={`absolute bottom-0 left-0 right-0 h-1 ${styles.bg}`} />
    </Card>
  )
}

// Sub-componente para rankings (Top 5)
const RankingList = ({ title, data, formatValue, avatarColor = 'primary' }) => {
  const badgeColors = {
    primary: 'bg-primary-50 text-primary-600',
    green: 'bg-emerald-50 text-emerald-600',
    purple: 'bg-purple-50 text-purple-600',
  }

  if (!data || data.length === 0) {
    return (
      <Card title={title} className="h-full border-0 shadow-sm">
        <div className="flex flex-col items-center justify-center h-40 text-slate-400 text-sm">
          <Package className="h-8 w-8 mb-2 opacity-50" />
          <p>Sin datos registrados</p>
        </div>
      </Card>
    )
  }

  return (
    <Card title={title} className="h-full border-0 shadow-sm">
      <div className="space-y-1">
        {data.map((item, index) => (
          <div
            key={index}
            className="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50 transition-colors duration-200"
          >
            <div className="flex items-center gap-3">
              <span className={`flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${index === 0 ? 'bg-amber-100 text-amber-700' : badgeColors[avatarColor]}`}>
                {index + 1}
              </span>
              <span className="text-sm font-medium text-slate-700 truncate max-w-[150px]">
                {item.name}
              </span>
            </div>
            <span className="text-sm font-bold text-slate-900">
              {formatValue(item.value)}
            </span>
          </div>
        ))}
      </div>
    </Card>
  )
}

export const DashboardPage = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showUploader, setShowUploader] = useState(false)

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const result = await reportService.getDashboard()
      setData(result)
    } catch (error) {
      toast.error('Error al cargar el dashboard')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  // Skeleton Loader mejorado (simula la estructura real)
  if (loading) {
    return (
      <div className="space-y-8 animate-pulse">
        <div className="space-y-2">
          <div className="h-8 w-64 bg-slate-200 rounded-md" />
          <div className="h-4 w-96 bg-slate-100 rounded-md" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-32 bg-slate-100 rounded-2xl" />
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-40 bg-slate-100 rounded-2xl" />
          <div className="h-40 bg-slate-100 rounded-2xl" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-64 bg-slate-100 rounded-2xl" />
          ))}
        </div>
      </div>
    )
  }

  // Preparar datos para los rankings (mapeo de estructura)
  const topProductos = data?.top_productos?.map(p => ({
    name: p.nombre,
    value: p.cantidad_vendida
  })) || []

  const topClientes = data?.top_clientes?.map(c => ({
    name: c.nombre,
    value: c.total_compras
  })) || []

  const topProveedores = data?.top_proveedores?.map(p => ({
    name: p.razon_social,
    value: p.total_compras
  })) || []

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header con jerarquía visual clara */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary-50 rounded-lg">
            <LayoutDashboard className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Dashboard</h1>
            <p className="text-sm text-slate-500 mt-0.5">
              Resumen general del negocio y métricas clave
            </p>
          </div>
        </div>
        
        {/* Botón para mostrar/ocultar uploader */}
        <button
          onClick={() => setShowUploader(!showUploader)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md"
        >
          {showUploader ? (
            <>
              <X className="h-5 w-5" />
              Cerrar
            </>
          ) : (
            <>
              <Upload className="h-5 w-5" />
              Cargar CSV
            </>
          )}
        </button>
      </div>

      {/* Sección de carga de CSV (colapsable) */}
      {showUploader && (
        <div className="animate-in slide-in-from-top duration-300">
          <CSVUploader onUploadComplete={loadDashboard} />
        </div>
      )}

      {/* Estadísticas principales con tarjetas rediseñadas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Ventas Hoy"
          value={formatCurrency(data?.ventas_hoy || 0)}
          icon={ShoppingBag}
          color="emerald"
          subtitle={data?.ventas_hoy > 0 ? "Actividad registrada" : "Sin ventas aún"}
        />
        <StatCard
          title="Ventas del Mes"
          value={formatCurrency(data?.ventas_mes || 0)}
          icon={TrendingUp}
          color="blue"
          subtitle="Acumulado mensual"
        />
        <StatCard
          title="Compras del Mes"
          value={formatCurrency(data?.compras_mes || 0)}
          icon={ShoppingCart}
          color="purple"
          subtitle="Egresos operativos"
        />
        <StatCard
          title="Productos en Stock"
          value={data?.inventario?.total_productos || 0}
          icon={Package}
          color="amber"
          subtitle={
            data?.inventario?.productos_stock_bajo > 0
              ? `${data.inventario.productos_stock_bajo} productos con bajo stock`
              : "Inventario saludable"
          }
          trend={data?.inventario?.productos_stock_bajo > 0 ? "down" : "up"}
        />
      </div>

      {/* Métricas financieras destacadas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-0 shadow-sm bg-gradient-to-br from-white to-emerald-50/30">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-500">Utilidad Bruta del Mes</p>
              <p className="text-3xl font-bold text-emerald-600 mt-2 tracking-tight">
                {formatCurrency(data?.utilidad_bruta || 0)}
              </p>
              <p className="text-xs text-slate-400 mt-1">Ganancia después de costos directos</p>
            </div>
            <div className="p-3 bg-emerald-100 rounded-full">
              <TrendingUp className="h-6 w-6 text-emerald-600" />
            </div>
          </div>
        </Card>

        <Card className="border-0 shadow-sm bg-gradient-to-br from-white to-blue-50/30">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-500">Margen Promedio</p>
              <p className="text-3xl font-bold text-blue-600 mt-2 tracking-tight">
                {formatPercentage(data?.margen_promedio || 0)}
              </p>
              <p className="text-xs text-slate-400 mt-1">Rentabilidad sobre ventas totales</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <TrendingUp className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Rankings (Top 5) con componentes reutilizables */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Columna Izquierda ANCHA - Actividad Reciente */}
        <div className="lg:col-span-2">
          <Card className="border-0 shadow-sm h-full">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-purple-50 rounded-lg">
                <Activity className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-slate-900">Actividad Reciente</h3>
                <p className="text-sm text-slate-500">Últimas acciones en el sistema</p>
              </div>
            </div>
            
            {data?.recent_activity && data.recent_activity.length > 0 ? (
              <div className="space-y-3">
                {data.recent_activity.map((activity) => {
                  const colorMap = {
                    emerald: 'bg-emerald-50 text-emerald-600',
                    blue: 'bg-blue-50 text-blue-600',
                    purple: 'bg-purple-50 text-purple-600',
                    amber: 'bg-amber-50 text-amber-600',
                  }
                  const iconMap = {
                    ShoppingBag: ShoppingBag,
                    ShoppingCart: ShoppingCart,
                    Package: Package,
                    TrendingUp: TrendingUp,
                  }
                  
                  const Icon = iconMap[activity.icon] || Activity
                  const colorClass = colorMap[activity.color] || colorMap.blue
                  
                  return (
                    <div
                      key={activity.id}
                      className="flex items-start gap-4 p-3 rounded-xl hover:bg-slate-50 transition-colors group"
                    >
                      <div className={`p-2.5 rounded-lg ${colorClass} flex-shrink-0 group-hover:scale-110 transition-transform`}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-slate-900 leading-snug">
                          {activity.title}
                        </p>
                        <p className="text-xs text-slate-500 mt-0.5">
                          {activity.description}
                        </p>
                      </div>
                      <span className="text-xs text-slate-400 whitespace-nowrap flex-shrink-0">
                        {activity.time}
                      </span>
                    </div>
                  )
                })}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-slate-400">
                <Activity className="h-12 w-12 mb-3 opacity-50" />
                <p className="text-sm">No hay actividad reciente</p>
              </div>
            )}
          </Card>
        </div>

        {/* Columna Derecha - Top 5 Productos */}
        <RankingList
          title="Top 5 Productos"
          data={topProductos}
          formatValue={(val) => `${val} uds.`}
          avatarColor="primary"
        />
      </div>
    </div>
  )
}