import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/useAuth'
import { authService } from '@/api'
import { Button, Input } from '@/components/common'
import { Boxes, LogIn } from 'lucide-react'
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

  return <div className="flex min-h-screen items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary-700 via-slate-900 to-slate-950 p-4"><div className="w-full max-w-md"><div className="rounded-3xl border border-white/10 bg-white p-8 shadow-2xl sm:p-10"><div className="mb-8 text-center"><div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-50 text-primary-700"><Boxes className="h-7 w-7" /></div><h1 className="mt-5 text-2xl font-bold tracking-tight text-slate-900">ERP Ferretería</h1><p className="mt-2 text-sm text-slate-500">{setupRequired ? 'Configura tu cuenta administradora para comenzar.' : 'Inventario, ventas y compras en un solo lugar.'}</p></div>
    <form onSubmit={handleSubmit} className="space-y-4">
      {setupRequired ? <><Input label="Correo del administrador" name="email" type="email" value={formData.email} onChange={handleChange} placeholder="nombre@empresa.com" required /><div className="grid grid-cols-2 gap-3"><Input label="Nombre" name="nombre" value={formData.nombre} onChange={handleChange} required minLength="2" /><Input label="Apellido" name="apellido" value={formData.apellido} onChange={handleChange} required minLength="2" /></div></> : <Input label="Usuario" name="username" value={formData.username} onChange={handleChange} placeholder="admin" required />}
      <Input label="Contraseña" name="password" type="password" value={formData.password} onChange={handleChange} placeholder={setupRequired ? 'Crea una contraseña segura' : 'Ingresa tu contraseña'} required minLength={setupRequired ? 8 : 1} />
      <Button type="submit" loading={loading || checkingSetup} className="mt-2 w-full" size="lg">{checkingSetup ? 'Verificando sistema…' : setupRequired ? 'Crear administrador' : <><LogIn className="h-4 w-4" />Iniciar sesión</>}</Button>
    </form>
    {!setupRequired && <p className="mt-4 text-center text-xs text-slate-500">Acceso inicial: <strong>admin</strong> / <strong>admin123</strong></p>}
    {setupRequired && <p className="mt-5 rounded-xl bg-amber-50 p-3 text-xs leading-5 text-amber-800">Este paso aparece solo cuando todavía no hay usuarios. Después, solo un administrador podrá crear cuentas nuevas.</p>}
  </div><p className="mt-5 text-center text-xs text-slate-400">ERP Ferretería · Gestión integrada</p></div></div>
}
