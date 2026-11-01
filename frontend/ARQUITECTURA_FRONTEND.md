# Arquitectura del Frontend - ERP Ferretería

## 🏗️ Visión General

El frontend está construido siguiendo los principios de **Clean Architecture** y **Component-Driven Development**, con énfasis en:

- ✅ **Separación de responsabilidades**
- ✅ **Componentes reutilizables**
- ✅ **Gestión de estado predecible**
- ✅ **Escalabilidad**
- ✅ **Mantenibilidad**

## 📐 Arquitectura en Capas

```
┌─────────────────────────────────────────────┐
│         CAPA DE PRESENTACIÓN                │
│  (pages/, components/common, components/    │
│   layout, components/forms)                 │
│  - Componentes visuales                     │
│  - Lógica de presentación                   │
│  - Interacción con usuario                  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│       CAPA DE APLICACIÓN                    │
│  (context/, hooks/, routes/)                │
│  - Estado global de la aplicación           │
│  - Lógica de negocio del cliente            │
│  - Custom hooks reutilizables               │
│  - Gestión de rutas y navegación            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      CAPA DE INFRAESTRUCTURA                │
│  (api/, utils/, config/, constants/)        │
│  - Comunicación con backend                 │
│  - Servicios externos                       │
│  - Utilidades y helpers                     │
│  - Configuración                            │
└─────────────────────────────────────────────┘
```

## 📂 Estructura de Directorios

```
frontend/
├── public/                     # Archivos estáticos
├── src/
│   ├── api/                   # Capa de API
│   │   ├── client.js          # Cliente Axios configurado
│   │   ├── auth.js            # Servicios de autenticación
│   │   ├── products.js        # Servicios de productos
│   │   ├── sales.js           # Servicios de ventas
│   │   ├── reports.js         # Servicios de reportes
│   │   └── index.js           # Barrel export
│   │
│   ├── components/            # Componentes reutilizables
│   │   ├── common/            # Componentes base
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Badge.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Select.jsx
│   │   │   └── index.js
│   │   │
│   │   ├── layout/            # Componentes de layout
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── MainLayout.jsx
│   │   │   └── index.js
│   │   │
│   │   └── forms/             # Formularios específicos (TODO)
│   │       ├── ProductForm.jsx
│   │       ├── SaleForm.jsx
│   │       └── PurchaseForm.jsx
│   │
│   ├── config/                # Configuración
│   │   └── api.js             # Configuración de API y endpoints
│   │
│   ├── constants/             # Constantes del sistema
│   │   ├── index.js           # Constantes generales
│   │   └── roles.js           # Roles y permisos
│   │
│   ├── context/               # Context API
│   │   └── AuthContext.jsx    # Contexto de autenticación
│   │
│   ├── hooks/                 # Custom hooks (TODO)
│   │   ├── useProducts.js
│   │   ├── useSales.js
│   │   └── useDebounce.js
│   │
│   ├── pages/                 # Páginas/Vistas
│   │   ├── LoginPage.jsx      # Página de login
│   │   ├── DashboardPage.jsx  # Dashboard principal
│   │   ├── InventoryPage.jsx  # Gestión de inventario
│   │   └── index.js
│   │
│   ├── routes/                # Configuración de rutas
│   │   └── ProtectedRoute.jsx # HOC para rutas protegidas
│   │
│   ├── utils/                 # Utilidades
│   │   ├── format.js          # Formateo de datos
│   │   ├── validation.js      # Validaciones
│   │   └── index.js
│   │
│   ├── App.jsx                # Componente raíz
│   ├── main.jsx               # Punto de entrada
│   └── index.css              # Estilos globales con Tailwind
│
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos ignorados por git
├── .eslintrc.cjs              # Configuración de ESLint
├── index.html                 # HTML principal
├── package.json               # Dependencias
├── postcss.config.js          # Configuración de PostCSS
├── tailwind.config.js         # Configuración de Tailwind CSS
├── vite.config.js             # Configuración de Vite
└── README.md                  # Documentación
```

## 🔄 Flujo de Datos

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │ Interacción
       ↓
┌─────────────────────┐
│   Componente Page   │
│  (LoginPage.jsx)    │
└──────┬──────────────┘
       │ Llama a
       ↓
┌─────────────────────┐
│   Context/Hook      │
│  (useAuth)          │
└──────┬──────────────┘
       │ Ejecuta
       ↓
┌─────────────────────┐
│   API Service       │
│  (authService)      │
└──────┬──────────────┘
       │ HTTP Request
       ↓
┌─────────────────────┐
│   API Client        │
│  (axios)            │
└──────┬──────────────┘
       │ Request
       ↓
┌─────────────────────┐
│   Backend API       │
│  (FastAPI)          │
└──────┬──────────────┘
       │ Response
       ↓
┌─────────────────────┐
│   Interceptor       │
│  (maneja errores)   │
└──────┬──────────────┘
       │ Retorna datos
       ↓
┌─────────────────────┐
│   Context/Hook      │
│  (actualiza estado) │
└──────┬──────────────┘
       │ Re-render
       ↓
┌─────────────────────┐
│   Componente        │
│  (muestra datos)    │
└─────────────────────┘
```

## 🎯 Patrones de Diseño Utilizados

### 1. **Component Composition Pattern**

Componentes pequeños y reutilizables que se componen para formar UIs complejas.

```jsx
<Card title="Productos" actions={<Button>Nuevo</Button>}>
  <Table data={products} />
</Card>
```

### 2. **Container/Presentational Pattern**

- **Container Components** (Pages): Lógica y estado
- **Presentational Components** (Common): Solo UI

### 3. **Custom Hooks Pattern**

Encapsular lógica reutilizable:

```jsx
const { user, login, logout } = useAuth()
const { products, loading, error } = useProducts()
```

### 4. **Higher-Order Component (HOC)**

`ProtectedRoute` envuelve componentes para agregar funcionalidad:

```jsx
<ProtectedRoute permission="inventory">
  <InventoryPage />
</ProtectedRoute>
```

### 5. **Service Layer Pattern**

Servicios de API encapsulan la comunicación con el backend:

```jsx
// En lugar de axios directo:
authService.login(username, password)
productService.getProducts()
```

### 6. **Proxy Pattern**

Vite proxy redirige `/api` al backend:

```js
proxy: {
  '/api': { target: 'http://localhost:8000' }
}
```

## 🔐 Autenticación y Autorización

### Flujo de Autenticación

```
┌──────────────────────────────────────────────┐
│ 1. Usuario ingresa credenciales             │
└────────────────┬─────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────┐
│ 2. authService.login() hace POST al backend  │
└────────────────┬─────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────┐
│ 3. Backend valida y retorna JWT token        │
└────────────────┬─────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────┐
│ 4. Token se guarda en localStorage           │
└────────────────┬─────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────┐
│ 5. authService.getCurrentUser() obtiene      │
│    información del usuario                   │
└────────────────┬─────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────┐
│ 6. AuthContext actualiza estado global       │
└────────────────┬─────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────┐
│ 7. Usuario autenticado, redirige a dashboard │
└──────────────────────────────────────────────┘
```

### Interceptor de Axios

```js
// Agrega token a cada request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Maneja errores y redirecciones
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado, redirigir a login
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

### Control de Acceso

```jsx
// En ProtectedRoute.jsx
if (!isAuthenticated) {
  return <Navigate to="/login" />
}

if (permission && !hasPermission(permission)) {
  return <div>403 - Sin permisos</div>
}

return children
```

## 🎨 Sistema de Diseño

### Paleta de Colores

```js
primary: {
  50: '#eff6ff',
  500: '#3b82f6',  // Azul principal
  600: '#2563eb',
  700: '#1d4ed8',
}
success: '#10b981',  // Verde
warning: '#f59e0b',  // Amarillo
danger: '#ef4444',   // Rojo
```

### Componentes Base

**Button:**
```jsx
<Button variant="primary" size="md" loading={false}>
  Guardar
</Button>
```

**Card:**
```jsx
<Card title="Título" subtitle="Subtítulo" actions={<Button />}>
  Contenido
</Card>
```

**Badge:**
```jsx
<Badge variant="success">Activo</Badge>
```

**Input:**
```jsx
<Input
  label="Nombre"
  error="Campo requerido"
  required
/>
```

### Clases Utilitarias (Tailwind)

```css
/* Botones */
.btn           /* Base button */
.btn-primary   /* Botón azul */
.btn-danger    /* Botón rojo */

/* Cards */
.card          /* Tarjeta con sombra */

/* Inputs */
.input         /* Input estilizado */
.label         /* Label consistente */

/* Badges */
.badge         /* Badge base */
.badge-success /* Verde */
.badge-warning /* Amarillo */
.badge-danger  /* Rojo */

/* Tables */
.table         /* Tabla estilizada */
```

## 📱 Responsive Design

### Breakpoints

```js
// Tailwind breakpoints
sm: '640px',   // Móvil grande
md: '768px',   // Tablet
lg: '1024px',  // Desktop
xl: '1280px',  // Desktop grande
```

### Layout Adaptativo

**Móvil (<768px):**
- Sidebar oculto (menú hamburguesa)
- Navegación en overlay
- Tablas con scroll horizontal

**Desktop (>1024px):**
- Sidebar fijo visible
- Navegación siempre visible
- Tablas completas

## 🚀 Optimizaciones

### 1. **Code Splitting**

Vite automáticamente divide el código por rutas.

### 2. **Lazy Loading**

```jsx
const DashboardPage = lazy(() => import('./pages/DashboardPage'))
```

### 3. **Memoization**

```jsx
const MemoizedComponent = memo(ExpensiveComponent)
```

### 4. **Debounce en Búsquedas**

```jsx
const debouncedSearch = useDebounce(searchTerm, 500)
```

### 5. **Caching de Datos**

Context API mantiene datos en memoria para evitar requests repetidos.

## 🧪 Testing (Futuro)

### Herramientas

- **Vitest** - Test runner
- **React Testing Library** - Testing de componentes
- **MSW** - Mock Service Worker para APIs

### Estructura de Tests

```
src/
├── components/
│   └── Button.test.jsx
├── pages/
│   └── LoginPage.test.jsx
└── utils/
    └── format.test.js
```

## 📦 Build y Deploy

### Build de Producción

```bash
npm run build
```

Genera carpeta `dist/` con:
- HTML, CSS, JS optimizados
- Assets con hash para cache busting
- Code splitting automático

### Variables de Entorno

```
VITE_API_URL=https://api.ejemplo.com
```

### Deploy

Compatible con:
- **Vercel** - Recomendado para Vite
- **Netlify**
- **AWS S3 + CloudFront**
- **Nginx** - Servidor estático

## 🔄 Estado de la Aplicación

### Global State (Context API)

```jsx
AuthContext
├── user (objeto con datos del usuario)
├── isAuthenticated (boolean)
├── loading (boolean)
├── login(username, password)
├── logout()
└── hasPermission(permission)
```

### Local State (useState)

Cada página/componente maneja su propio estado local:

```jsx
const [products, setProducts] = useState([])
const [loading, setLoading] = useState(true)
const [error, setError] = useState(null)
```

## 🛣️ Rutas y Navegación

### Estructura de Rutas

```
/login                 (público)
/
├── /dashboard         (protegido)
├── /inventory         (protegido + permiso)
├── /sales             (protegido + permiso)
├── /purchases         (protegido + permiso)
├── /customers         (protegido + permiso)
└── /reports           (protegido + permiso)
```

### Guardias de Ruta

```jsx
// Requiere autenticación
<ProtectedRoute>
  <DashboardPage />
</ProtectedRoute>

// Requiere autenticación + permiso específico
<ProtectedRoute permission="inventory">
  <InventoryPage />
</ProtectedRoute>
```

## 📊 Integración con Backend

### Endpoints

Base URL: `http://localhost:8000/api/v1`

### Formato de Request

```js
// Con autenticación
GET /products
Headers: {
  Authorization: 'Bearer <token>'
}
```

### Formato de Response

```json
{
  "id": 1,
  "nombre": "Producto",
  "precio": 100.00,
  "stock_actual": 50
}
```

### Manejo de Errores

```json
{
  "detail": "Mensaje de error"
}
```

## 🎯 Próximos Pasos

### FASE 10 - Interfaces Completas

1. ✅ Estructura base
2. ✅ Autenticación
3. ✅ Dashboard
4. ✅ Inventario básico
5. ⏳ Formularios con React Hook Form
6. ⏳ Módulo de Ventas completo
7. ⏳ Módulo de Compras completo
8. ⏳ Módulo de Clientes completo
9. ⏳ Módulo de Reportes con gráficos
10. ⏳ Tablas con paginación y filtros
11. ⏳ Modales y diálogos
12. ⏳ Exportación a Excel/PDF

## 📚 Referencias

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [React Router](https://reactrouter.com)
- [Axios](https://axios-http.com)

---

**Última actualización:** 31 de Octubre de 2026
**Versión:** 1.0.0
