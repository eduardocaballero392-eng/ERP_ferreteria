import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/useAuth'
import { authService } from '@/api'
import { Button, Input } from '@/components/common'
import { ArrowUpRight, LogIn, PackageCheck, ShieldCheck } from 'lucide-react'
import toast from 'react-hot-toast'

export const LoginPage = () => {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [setupRequired, setSetupRequired] = useState(false)
  const [checkingSetup, setCheckingSetup] = useState(true)
  const [formData, setFormData] = useState({ username: '', email: '', nombre: '', apellido: '', password: '' })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    authService.getSetupStatus().then((status) => setSetupRequired(status.setup_required)).catch(() => {}).finally(() => setCheckingSetup(false))
  }, [])

  const handleChange = (event) => setFormData((current) => ({ ...current, [event.target.name]: event.target.value }))

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    try {
      if (setupRequired) {
        await authService.setupAdmin({ email: formData.email, nombre: formData.nombre, apellido: formData.apellido, password: formData.password, role: 'admin' })
        const result = await login(formData.email, formData.password)
        if (!result.success) throw new Error(result.error || 'No se pudo iniciar sesión')
        toast.success('Administrador configurado')
        navigate('/dashboard')
        return
      }
      const result = await login(formData.username, formData.password)
      if (!result.success) throw new Error(result.error || 'Usuario o contraseña incorrectos')
      toast.success('Inicio de sesión exitoso')
      navigate('/dashboard')
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'No se pudo completar la solicitud')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="grid min-h-screen bg-white lg:grid-cols-[1.08fr_.92fr]">
      <section className="relative hidden min-h-screen overflow-hidden bg-[#101b2e] px-12 py-10 text-white lg:flex lg:flex-col lg:justify-between xl:px-20">
        <div className="absolute -right-36 -top-32 h-[30rem] w-[30rem] rounded-full bg-blue-500/15 blur-[100px]" />
        <div className="absolute -bottom-52 -left-24 h-[34rem] w-[34rem] rounded-full bg-indigo-500/15 blur-[110px]" />
        <div className="relative flex items-center gap-3"><div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-500 text-lg font-extrabold shadow-xl shadow-blue-950/30">EF</div><div><p className="font-extrabold tracking-tight">ERP Ferretería</p><p className="mt-0.5 text-xs font-semibold uppercase tracking-[.16em] text-slate-400">Gestión integrada</p></div></div>
        <div className="relative max-w-2xl py-14">
          <span className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[.06] px-3 py-1.5 text-xs font-semibold text-blue-200"><span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />Control operativo en un solo lugar</span>
          <h1 className="mt-6 text-4xl font-extrabold leading-[1.12] tracking-tight xl:text-5xl">Más claridad para gestionar cada parte de tu negocio.</h1>
          <p className="mt-5 max-w-xl text-base leading-7 text-slate-300">Administra inventario, ventas, compras y clientes desde una plataforma diseñada para el trabajo diario de tu ferretería.</p>
          <div className="mt-10 grid max-w-xl gap-3 sm:grid-cols-2">
            <div className="rounded-2xl border border-white/10 bg-white/[.055] p-4"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-400/15 text-blue-200"><PackageCheck className="h-5 w-5" /></div><p className="mt-4 text-sm font-bold">Inventario conectado</p><p className="mt-1 text-xs leading-5 text-slate-400">Existencias disponibles en cada operación.</p></div>
            <div className="rounded-2xl border border-white/10 bg-white/[.055] p-4"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-400/15 text-emerald-200"><ShieldCheck className="h-5 w-5" /></div><p className="mt-4 text-sm font-bold">Acceso protegido</p><p className="mt-1 text-xs leading-5 text-slate-400">Herramientas según el perfil de cada usuario.</p></div>
          </div>
        </div>
        <div className="relative flex items-center justify-between border-t border-white/10 pt-5 text-xs text-slate-500"><span>Operación y control comercial</span><span>Versión 1.0</span></div>
      </section>

      <section className="flex min-h-screen items-center justify-center px-5 py-10 sm:px-10 lg:px-12">
        <div className="w-full max-w-[430px]">
          <div className="mb-10 flex items-center gap-3 lg:hidden"><div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 font-extrabold text-white shadow-lg shadow-blue-900/20">EF</div><div><p className="font-extrabold text-slate-900">ERP Ferretería</p><p className="text-xs text-slate-500">Gestión integrada</p></div></div>
          <div className="mb-8"><p className="text-xs font-bold uppercase tracking-[.16em] text-primary-600">{setupRequired ? 'Configuración inicial' : 'Portal de gestión'}</p><h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900">{setupRequired ? 'Crea tu cuenta administradora' : 'Bienvenido de nuevo'}</h2><p className="mt-2 text-sm leading-6 text-slate-500">{setupRequired ? 'Completa tus datos para preparar el acceso principal al sistema.' : 'Ingresa tus credenciales para continuar con la operación.'}</p></div>
          <form onSubmit={handleSubmit} className="space-y-5">
            {setupRequired ? <><Input label="Correo del administrador" name="email" type="email" value={formData.email} onChange={handleChange} placeholder="nombre@empresa.com" autoComplete="email" required /><div className="grid grid-cols-2 gap-3"><Input label="Nombre" name="nombre" value={formData.nombre} onChange={handleChange} autoComplete="given-name" required minLength="2" /><Input label="Apellido" name="apellido" value={formData.apellido} onChange={handleChange} autoComplete="family-name" required minLength="2" /></div></> : <Input label="Usuario o correo" name="username" value={formData.username} onChange={handleChange} placeholder="Ingresa tu usuario" autoComplete="username" required />}
            <Input label="Contraseña" name="password" type="password" value={formData.password} onChange={handleChange} placeholder={setupRequired ? 'Crea una contraseña segura' : 'Ingresa tu contraseña'} autoComplete={setupRequired ? 'new-password' : 'current-password'} required minLength={setupRequired ? 8 : 1} />
            <Button type="submit" loading={loading || checkingSetup} className="mt-2 w-full" size="lg">{checkingSetup ? 'Verificando sistema…' : setupRequired ? <>Crear cuenta administradora<ArrowUpRight className="h-4 w-4" /></> : <><LogIn className="h-4 w-4" />Iniciar sesión</>}</Button>
          </form>
          {setupRequired && <p className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-3.5 text-xs leading-5 text-amber-800">Esta configuración aparece cuando todavía no existen usuarios. Después, el administrador podrá crear las demás cuentas.</p>}
          <div className="mt-8 flex items-center justify-center gap-2 text-xs text-slate-400"><ShieldCheck className="h-4 w-4" />Conexión segura · ERP Ferretería</div>
        </div>
      </section>
    </main>
  )
}
