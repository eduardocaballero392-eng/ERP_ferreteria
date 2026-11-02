import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Activity, AlertTriangle, ArrowDownToLine, ArrowRight, ArrowUpRight, BarChart3, Boxes, CircleDollarSign, Package, ShoppingBag, ShoppingCart } from 'lucide-react'
import toast from 'react-hot-toast'
import { reportService } from '@/api'
import { Card } from '@/components/common'
import { formatCurrency, formatPercentage } from '@/utils'

const shortcuts = [
  { title: 'Registrar venta', description: 'Elige cliente y productos del inventario actual.', href: '/sales/new', icon: ShoppingBag, tone: 'bg-emerald-50 text-emerald-700' },
  { title: 'Registrar compra', description: 'Recibe mercadería y actualiza las existencias.', href: '/purchases/new', icon: ShoppingCart, tone: 'bg-blue-50 text-blue-700' },
  { title: 'Sincronizar stock', description: 'Carga el CSV maestro de existencias del día.', href: '/inventory', icon: ArrowDownToLine, tone: 'bg-violet-50 text-violet-700' },
  { title: 'Revisar reportes', description: 'Consulta actividad de ventas e inventario.', href: '/reports', icon: BarChart3, tone: 'bg-amber-50 text-amber-700' },
]

const Stat = ({ label, value, note, icon: Icon, color }) => <Card className="relative overflow-hidden border-0 shadow-sm"><div className="flex items-start justify-between gap-3"><div><p className="text-sm font-medium text-slate-500">{label}</p><p className="mt-3 text-2xl font-bold tracking-tight text-slate-900">{value}</p><p className="mt-1 text-xs text-slate-400">{note}</p></div><div className={`rounded-xl p-3 ${color}`}><Icon className="h-5 w-5" /></div></div><div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-primary-500/70 to-transparent" /></Card>

export const DashboardPage = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    reportService.getDashboard().then(setData).catch((error) => {
      toast.error(error.message || 'No se pudo cargar el resumen')
    }).finally(() => setLoading(false))
  }, [])

  const inventoryCount = data?.productos_total ?? 0
  const lowStock = data?.productos_stock_bajo ?? 0

  return <div className="mx-auto max-w-7xl space-y-8">
    <section className="relative overflow-hidden rounded-3xl bg-slate-950 px-6 py-8 text-white shadow-xl shadow-slate-900/10 sm:px-9 sm:py-10">
      <div className="absolute -right-12 -top-24 h-72 w-72 rounded-full bg-primary-500/20 blur-3xl" /><div className="absolute bottom-0 right-1/4 h-24 w-64 rounded-full bg-emerald-400/10 blur-3xl" />
      <div className="relative flex flex-wrap items-end justify-between gap-6"><div><p className="text-xs font-semibold uppercase tracking-[.2em] text-emerald-300">Ferretería · centro de operaciones</p><h1 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">Todo tu negocio, conectado.</h1><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-300">Ventas consumen el inventario, compras lo reponen y los reportes reflejan cada movimiento en un solo lugar.</p></div><Link to="/inventory" className="btn bg-white text-slate-900 hover:bg-emerald-50"><Package className="h-4 w-4" />Ir al inventario<ArrowRight className="h-4 w-4" /></Link></div>
    </section>

    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <Stat label="Ventas de hoy" value={loading ? '…' : `${data?.ventas_hoy || 0} ventas`} note="Operaciones registradas hoy" icon={ShoppingBag} color="bg-emerald-50 text-emerald-700" />
      <Stat label="Ventas del mes" value={loading ? '…' : formatCurrency(data?.total_vendido_mes || 0)} note={`${data?.ventas_mes || 0} operaciones · IGV incluido`} icon={ArrowUpRight} color="bg-blue-50 text-blue-700" />
      <Stat label="Compras del mes" value={loading ? '…' : formatCurrency(data?.total_gastado_mes || 0)} note={`${data?.compras_mes || 0} órdenes recibidas`} icon={ShoppingCart} color="bg-violet-50 text-violet-700" />
      <Stat label="Productos en catálogo" value={loading ? '…' : (data?.productos_total ?? inventoryCount).toLocaleString('es-PE')} note={lowStock ? `${lowStock} necesitan reposición` : 'Inventario sincronizado'} icon={lowStock ? AlertTriangle : Boxes} color={lowStock ? 'bg-amber-50 text-amber-700' : 'bg-emerald-50 text-emerald-700'} />
    </section>

    <section className="grid gap-6 lg:grid-cols-[1.2fr_.8fr]">
      <div><div className="mb-4 flex items-end justify-between"><div><p className="text-xs font-semibold uppercase tracking-[.16em] text-primary-600">Acceso rápido</p><h2 className="mt-1 text-xl font-bold text-slate-900">Continúa trabajando</h2></div></div><div className="grid gap-3 sm:grid-cols-2">{shortcuts.map(({ title, description, href, icon: Icon, tone }) => <Link key={href} to={href} className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-primary-200 hover:shadow-md"><div className="flex items-start justify-between"><div className={`rounded-xl p-2.5 ${tone}`}><Icon className="h-5 w-5" /></div><ArrowRight className="h-4 w-4 text-slate-300 transition group-hover:translate-x-1 group-hover:text-primary-600" /></div><h3 className="mt-4 font-semibold text-slate-900">{title}</h3><p className="mt-1 text-sm leading-5 text-slate-500">{description}</p></Link>)}</div></div>
      <Card className="border-0 shadow-sm"><div className="flex items-center gap-3"><div className="rounded-xl bg-primary-50 p-2.5 text-primary-700"><Activity className="h-5 w-5" /></div><div><h2 className="font-semibold text-slate-900">Salud del negocio</h2><p className="text-xs text-slate-500">Indicadores desde tus módulos</p></div></div><div className="mt-5 space-y-4"><div className="flex items-center justify-between rounded-xl bg-slate-50 p-3"><div className="flex items-center gap-3"><Package className="h-4 w-4 text-slate-500" /><span className="text-sm text-slate-600">Productos por reponer</span></div><span className="font-semibold">{loading ? '…' : data?.productos_stock_bajo ?? 0}</span></div><div className="flex items-center justify-between rounded-xl bg-slate-50 p-3"><div className="flex items-center gap-3"><CircleDollarSign className="h-4 w-4 text-emerald-600" /><span className="text-sm text-slate-600">Utilidad bruta del mes</span></div><span className="font-semibold text-emerald-700">{loading ? '…' : formatCurrency(data?.utilidad_bruta_mes || 0)}</span></div><div className="flex items-center justify-between rounded-xl bg-slate-50 p-3"><div className="flex items-center gap-3"><BarChart3 className="h-4 w-4 text-blue-600" /><span className="text-sm text-slate-600">Margen promedio</span></div><span className="font-semibold text-blue-700">{loading ? '…' : formatPercentage(data?.margen_promedio_mes || 0)}</span></div></div><Link to="/reports" className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-primary-700 hover:text-primary-800">Abrir reportes<ArrowRight className="h-4 w-4" /></Link></Card>
    </section>
  </div>
}
