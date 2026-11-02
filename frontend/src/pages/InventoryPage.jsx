import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useLocation, useSearchParams } from 'react-router-dom'
import { ArrowDownToLine, Boxes, FileSpreadsheet, Package, Plus, Search, Tag, Trash2, UploadCloud } from 'lucide-react'
import toast from 'react-hot-toast'
import { productService, categoryService, reportService, uploadService } from '@/api'
import { Badge, Button, Card, Loading, Modal } from '@/components/common'
import { formatCurrency } from '@/utils'
import { useAuth } from '@/context/useAuth'

const stockState = (product) => Number(product.stock_actual) <= 0 ? 'AGOTADO' : Number(product.stock_actual) <= Number(product.stock_minimo) ? 'REPONER' : 'OK'

export const InventoryPage = () => {
  const { user } = useAuth()
  const [products, setProducts] = useState([])
  const [searchParams] = useSearchParams()
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [categoryId, setCategoryId] = useState(() => searchParams.get('categoria') || '')
  const [status, setStatus] = useState('')
  const [inventoryOrigin, setInventoryOrigin] = useState('')
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [dragging, setDragging] = useState(false)
  const [showNewProduct, setShowNewProduct] = useState(false)
  const [savingProduct, setSavingProduct] = useState(false)
  const [newProduct, setNewProduct] = useState({ sku: '', nombre: '', descripcion: '', categoria_id: '', stock_actual: 0, stock_minimo: 0, unidad_medida: 'UND', costo_unitario: '', precio_venta: '' })
  const [movementProductId, setMovementProductId] = useState('')
  const [movementReport, setMovementReport] = useState(null)
  const [movementLoading, setMovementLoading] = useState(false)
  const [clearingStock, setClearingStock] = useState(false)
  const inputRef = useRef(null)
  const location = useLocation()

  const loadData = async () => {
    setLoading(true)
    try {
      const [items, groups] = await Promise.all([productService.getProductsDetails(), categoryService.getCategories()])
      setProducts(items)
      setCategories(groups)
    } catch (error) {
      toast.error(error.message || 'No se pudo cargar el inventario')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadData() }, [])

  const filtered = useMemo(() => products.filter((product) => {
    const search = query.trim().toLowerCase()
    const matchesText = !search || [product.nombre, product.sku, product.categoria_nombre].some((value) => String(value || '').toLowerCase().includes(search))
    return matchesText && (!categoryId || String(product.categoria_id) === categoryId) && (!status || stockState(product) === status) && (!inventoryOrigin || product.origen_inventario === inventoryOrigin)
  }), [products, query, categoryId, status, inventoryOrigin])

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    try {
      const result = await uploadService.uploadStock(file)
      toast.success(`${result.updated} productos actualizados${result.unchanged ? ` · ${result.unchanged} sin cambios` : ''}`)
      if (result.errors?.length) toast(`${result.errors.length} filas necesitan revisión`, { icon: '⚠️', duration: 6000 })
      setFile(null)
      if (inputRef.current) inputRef.current.value = ''
      await loadData()
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'No se pudo importar el stock')
    } finally {
      setUploading(false)
    }
  }

  const createProduct = async (event) => {
    event.preventDefault()
    setSavingProduct(true)
    try {
      await productService.createProduct({ ...newProduct, categoria_id: Number(newProduct.categoria_id), stock_actual: Number(newProduct.stock_actual), stock_minimo: Number(newProduct.stock_minimo), costo_unitario: Number(newProduct.costo_unitario), precio_venta: Number(newProduct.precio_venta) })
      toast.success('Producto agregado al catálogo compartido')
      setShowNewProduct(false)
      setNewProduct({ sku: '', nombre: '', descripcion: '', categoria_id: '', stock_actual: 0, stock_minimo: 0, unidad_medida: 'UND', costo_unitario: '', precio_venta: '' })
      await loadData()
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'No se pudo guardar el producto')
    } finally {
      setSavingProduct(false)
    }
  }

  const adjustProduct = async (product) => {
    const amount = window.prompt(`Ajuste de ${product.nombre}. Usa un número positivo para entrada o negativo para salida:`, '0')
    if (amount === null) return
    const quantity = Number(amount)
    if (!Number.isInteger(quantity) || quantity === 0) return toast.error('Ingresa una cantidad entera distinta de cero')
    const reason = window.prompt('Motivo del ajuste (mínimo 5 caracteres):', '')
    if (reason === null) return
    try {
      await productService.adjustStock(product.id, quantity, reason)
      toast.success('Existencia ajustada')
      await loadData()
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'No se pudo ajustar el stock')
    }
  }

  const loadMovements = async () => {
    if (!movementProductId) return toast.error('Selecciona un producto')
    setMovementLoading(true)
    try {
      setMovementReport(await reportService.getProductMovements(movementProductId))
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'No se pudieron cargar los movimientos')
    } finally {
      setMovementLoading(false)
    }
  }

  const clearAllStock = async () => {
    const totalUnits = products.reduce((sum, product) => sum + Number(product.stock_actual || 0), 0)
    const confirmed = window.confirm(`Se pondrá en cero el stock de todos los productos (${totalUnits.toLocaleString('es-PE')} unidades). Los productos seguirán en el catálogo. ¿Deseas continuar?`)
    if (!confirmed) return

    setClearingStock(true)
    try {
      const result = await productService.clearAllStock()
      toast.success(`Stock limpiado: ${result.products_updated} productos · ${result.units_removed.toLocaleString('es-PE')} unidades`)
      await loadData()
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'No se pudo limpiar el stock')
    } finally {
      setClearingStock(false)
    }
  }

  const totals = products.reduce((sum, product) => {
    const state = stockState(product)
    sum.units += Number(product.stock_actual) || 0
    sum.value += (Number(product.stock_actual) || 0) * (Number(product.costo_unitario) || 0)
    if (state !== 'OK') sum.alerts += 1
    return sum
  }, { units: 0, value: 0, alerts: 0 })
  const section = location.pathname.split('/').at(-1)
  const title = section === 'categories' ? 'Productos por categoría' : section === 'movements' ? 'Existencias y movimientos' : section === 'adjustments' ? 'Control de existencias' : 'Inventario'

  if (loading) return <div className="flex h-64 items-center justify-center"><Loading /></div>

  return <div className="mx-auto max-w-7xl space-y-6">
    <header className="flex flex-wrap items-end justify-between gap-4">
      <div><p className="text-xs font-semibold uppercase tracking-[.18em] text-primary-600">Almacén · catálogo conectado</p><h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">{title}</h1><p className="mt-1 text-sm text-slate-500">El mismo stock alimenta ventas, compras y reportes.</p></div>
      <div className="flex flex-wrap gap-2"><Button onClick={() => setShowNewProduct(true)}><Plus className="h-4 w-4" />Nuevo producto</Button><Link to="/purchases/new" className="btn btn-secondary"><ArrowDownToLine className="h-4 w-4" />Registrar ingreso</Link>{(user?.role ?? user?.rol) === 'admin' && <Button variant="danger" onClick={clearAllStock} loading={clearingStock} disabled={!products.some((product) => Number(product.stock_actual) > 0)}><Trash2 className="h-4 w-4" />Limpiar stock</Button>}</div>
    </header>

    <div className="grid gap-4 sm:grid-cols-3">
      <Card className="border-0 shadow-sm"><p className="text-sm text-slate-500">Productos activos</p><p className="mt-2 text-2xl font-bold">{products.length}</p><p className="mt-1 text-xs text-slate-400">Catálogo disponible para ventas</p></Card>
      <Card className="border-0 shadow-sm"><p className="text-sm text-slate-500">Unidades disponibles</p><p className="mt-2 text-2xl font-bold">{totals.units.toLocaleString('es-PE')}</p><p className="mt-1 text-xs text-slate-400">Existencias actuales consolidadas</p></Card>
      <Card className="border-0 shadow-sm"><p className="text-sm text-slate-500">Alertas de reposición</p><p className={`mt-2 text-2xl font-bold ${totals.alerts ? 'text-amber-600' : 'text-emerald-600'}`}>{totals.alerts}</p><p className="mt-1 text-xs text-slate-400">Valor del stock: {formatCurrency(totals.value)}</p></Card>
    </div>

    <Card className="overflow-hidden border border-slate-200 bg-white shadow-sm">
      <div className="grid gap-5 lg:grid-cols-[1fr_auto] lg:items-center">
        <div className="flex items-start gap-4"><div className="rounded-xl bg-emerald-50 p-3"><FileSpreadsheet className="h-6 w-6 text-emerald-700" /></div><div><h2 className="text-lg font-semibold text-slate-900">Sincronizar stock del día</h2><p className="mt-1 max-w-2xl text-sm leading-6 text-slate-600">Carga un único CSV. Detectamos automáticamente SKU o código, encabezado de existencias y separador. El inventario actualizado se refleja en ventas y reportes.</p><p className="mt-2 text-xs text-slate-500">Columnas compatibles: SKU / Código / Producto y Stock / Existencia / Cantidad</p></div></div>
        <div className="flex flex-wrap items-center gap-2">
          <input ref={inputRef} type="file" accept=".csv,text/csv" className="hidden" onChange={(event) => setFile(event.target.files?.[0] || null)} />
          <button type="button" onClick={() => inputRef.current?.click()} onDragOver={(event) => { event.preventDefault(); setDragging(true) }} onDragLeave={() => setDragging(false)} onDrop={(event) => { event.preventDefault(); setDragging(false); const next = event.dataTransfer.files?.[0]; if (next?.name.toLowerCase().endsWith('.csv')) setFile(next); else toast.error('Selecciona un archivo CSV') }} className={`flex min-h-11 items-center gap-2 rounded-xl border px-4 text-sm font-semibold transition ${dragging ? 'border-emerald-400 bg-emerald-50 text-emerald-800' : 'border-slate-200 bg-slate-50 text-slate-700 hover:border-slate-300 hover:bg-white'}`}><UploadCloud className="h-4 w-4 text-primary-600" />{file ? file.name : 'Elegir o soltar CSV'}</button>
          {file && <Button onClick={handleUpload} disabled={uploading}>{uploading ? 'Sincronizando…' : 'Actualizar stock'}</Button>}
        </div>
      </div>
    </Card>

    {section === 'movements' && <Card className="border-0 shadow-sm"><div className="flex flex-wrap items-end gap-3"><label className="label min-w-64 flex-1">Producto<select className="input mt-1" value={movementProductId} onChange={(event) => setMovementProductId(event.target.value)}><option value="">Seleccionar producto</option>{products.map((product) => <option key={product.id} value={product.id}>{product.nombre} · {product.sku}</option>)}</select></label><Button onClick={loadMovements} loading={movementLoading}>Ver movimientos</Button></div>{movementReport && <div className="mt-5"><div className="grid gap-3 sm:grid-cols-3"><div className="rounded-xl bg-emerald-50 p-3"><p className="text-xs text-emerald-700">Entradas</p><p className="text-xl font-bold text-emerald-800">{movementReport.total_entradas}</p></div><div className="rounded-xl bg-rose-50 p-3"><p className="text-xs text-rose-700">Salidas</p><p className="text-xl font-bold text-rose-800">{movementReport.total_salidas}</p></div><div className="rounded-xl bg-slate-50 p-3"><p className="text-xs text-slate-500">Stock actual</p><p className="text-xl font-bold text-slate-900">{movementReport.stock_final}</p></div></div><div className="mt-4 overflow-x-auto"><table className="table"><thead><tr><th>Fecha</th><th>Tipo</th><th>Referencia</th><th>Cantidad</th><th>Stock resultante</th></tr></thead><tbody>{movementReport.movimientos.map((movement, index) => <tr key={`${movement.referencia}-${index}`}><td>{movement.fecha}</td><td>{movement.tipo}</td><td>{movement.referencia}</td><td>{movement.tipo_movimiento === 'ENTRADA' ? '+' : '−'}{movement.cantidad}</td><td>{movement.stock_nuevo ?? '—'}</td></tr>)}{!movementReport.movimientos.length && <tr><td colSpan="5" className="py-8 text-center text-sm text-slate-500">No hay movimientos en el período actual.</td></tr>}</tbody></table></div></div>}</Card>}

    <Card className="border-0 p-0 shadow-sm">
      <div className="flex flex-col gap-3 border-b border-slate-100 p-4 md:flex-row md:items-center">
        <label className="relative min-w-0 flex-1"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" /><input className="input pl-9" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Buscar producto, código o categoría" /></label>
        <select className="input md:w-52" value={categoryId} onChange={(event) => setCategoryId(event.target.value)}><option value="">Todas las categorías</option>{categories.map((category) => <option key={category.id} value={category.id}>{category.nombre}</option>)}</select>
        <select className="input md:w-44" value={status} onChange={(event) => setStatus(event.target.value)}><option value="">Todos los estados</option><option value="OK">Disponible</option><option value="REPONER">Por reponer</option><option value="AGOTADO">Agotado</option></select>
        <select className="input md:w-52" value={inventoryOrigin} onChange={(event) => setInventoryOrigin(event.target.value)}><option value="">Todos los tipos</option><option value="REPUESTO">Productos repuestos</option><option value="AGREGADO">Productos agregados</option></select>
        <Link to="/inventory/categories" className="btn btn-secondary whitespace-nowrap"><Tag className="h-4 w-4" />Categorías</Link>
      </div>
      <div className="overflow-x-auto"><table className="table"><thead><tr><th>Producto</th><th>Categoría</th><th>Existencia</th><th>Estado</th><th>Precio</th><th>Valor en almacén</th><th>Acciones</th></tr></thead><tbody>
        {filtered.map((product) => { const currentState = stockState(product); return <tr key={product.id}><td><div className="font-medium text-slate-900">{product.nombre}</div><div className="mt-0.5 font-mono text-xs text-slate-400">{product.sku}</div></td><td>{product.categoria_nombre || 'Sin categoría'}</td><td><span className="font-semibold">{product.stock_actual} {product.unidad_medida}</span><span className="ml-2 text-xs text-slate-400">mín. {product.stock_minimo}</span></td><td><Badge variant={currentState === 'OK' ? 'success' : currentState === 'REPONER' ? 'warning' : 'danger'}>{currentState}</Badge></td><td>{formatCurrency(product.precio_venta)}</td><td className="font-medium">{formatCurrency(Number(product.stock_actual) * Number(product.costo_unitario))}</td><td><button type="button" onClick={() => adjustProduct(product)} className="inline-flex items-center gap-1 rounded px-2 py-1 text-sm font-medium text-primary-700 hover:bg-primary-50" aria-label={`Ajustar stock de ${product.nombre}`}><Plus className="h-4 w-4" />Ajustar</button></td></tr> })}
        {!filtered.length && <tr><td colSpan="7" className="py-14 text-center text-sm text-slate-500"><Package className="mx-auto mb-2 h-7 w-7 text-slate-300" />No hay productos que coincidan con estos filtros.</td></tr>}
      </tbody></table></div>
      <div className="flex items-center justify-between border-t border-slate-100 px-4 py-3 text-xs text-slate-500"><span>Mostrando {filtered.length} de {products.length} productos</span><span className="flex items-center gap-1"><Boxes className="h-3.5 w-3.5" />Fuente compartida con Ventas</span></div>
    </Card>
    <Modal isOpen={showNewProduct} onClose={() => setShowNewProduct(false)} title="Agregar producto" size="lg"><form onSubmit={createProduct} className="grid gap-4 sm:grid-cols-2"><label className="label">Código SKU<input className="input mt-1" required minLength="2" value={newProduct.sku} onChange={(event) => setNewProduct({ ...newProduct, sku: event.target.value })} /></label><label className="label">Nombre<input className="input mt-1" required minLength="2" value={newProduct.nombre} onChange={(event) => setNewProduct({ ...newProduct, nombre: event.target.value })} /></label><label className="label">Categoría<select className="input mt-1" required value={newProduct.categoria_id} onChange={(event) => setNewProduct({ ...newProduct, categoria_id: event.target.value })}><option value="">Seleccionar</option>{categories.map((category) => <option key={category.id} value={category.id}>{category.nombre}</option>)}</select></label><label className="label">Unidad<input className="input mt-1" required value={newProduct.unidad_medida} onChange={(event) => setNewProduct({ ...newProduct, unidad_medida: event.target.value })} /></label><label className="label">Stock inicial<input className="input mt-1" type="number" min="0" required value={newProduct.stock_actual} onChange={(event) => setNewProduct({ ...newProduct, stock_actual: event.target.value })} /></label><label className="label">Stock mínimo<input className="input mt-1" type="number" min="0" required value={newProduct.stock_minimo} onChange={(event) => setNewProduct({ ...newProduct, stock_minimo: event.target.value })} /></label><label className="label">Costo unitario<input className="input mt-1" type="number" min="0.01" step="0.01" required value={newProduct.costo_unitario} onChange={(event) => setNewProduct({ ...newProduct, costo_unitario: event.target.value })} /></label><label className="label">Precio de venta<input className="input mt-1" type="number" min="0.01" step="0.01" required value={newProduct.precio_venta} onChange={(event) => setNewProduct({ ...newProduct, precio_venta: event.target.value })} /></label><label className="label sm:col-span-2">Descripción<textarea className="input mt-1" rows="2" value={newProduct.descripcion} onChange={(event) => setNewProduct({ ...newProduct, descripcion: event.target.value })} /></label><div className="sm:col-span-2"><Button type="submit" loading={savingProduct}>Guardar producto</Button>{!categories.length && <Link className="ml-3 text-sm font-medium text-primary-700" to="/inventory/categories">Crea primero una categoría</Link>}</div></form></Modal>
  </div>
}
