# ERP Ferretería - Frontend

Frontend del sistema ERP para ferretería construido con React, Vite y Tailwind CSS.

## 🚀 Tecnologías

- **React 18** - Biblioteca de UI
- **Vite** - Build tool y dev server
- **React Router v6** - Enrutamiento
- **Tailwind CSS** - Framework de CSS
- **Axios** - Cliente HTTP
- **React Hook Form** - Manejo de formularios
- **Yup** - Validación de esquemas
- **React Hot Toast** - Notificaciones
- **Lucide React** - Iconos
- **date-fns** - Manejo de fechas

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── api/              # Servicios de API
│   │   ├── client.js     # Cliente Axios con interceptores
│   │   ├── auth.js       # Servicios de autenticación
│   │   ├── products.js   # Servicios de productos
│   │   ├── sales.js      # Servicios de ventas
│   │   └── reports.js    # Servicios de reportes
│   ├── components/       # Componentes reutilizables
│   │   ├── common/       # Button, Input, Card, Badge
│   │   ├── layout/       # Navbar, Sidebar, MainLayout
│   │   └── forms/        # Formularios específicos
│   ├── context/          # Context API
│   │   └── AuthContext.jsx
│   ├── pages/            # Páginas principales
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   └── InventoryPage.jsx
│   ├── routes/           # Configuración de rutas
│   │   └── ProtectedRoute.jsx
│   ├── utils/            # Utilidades
│   │   ├── format.js     # Formateo de moneda, fechas, etc.
│   │   └── validation.js # Validaciones
│   ├── constants/        # Constantes
│   │   ├── index.js      # Constantes generales
│   │   └── roles.js      # Roles y permisos
│   ├── config/           # Configuración
│   │   └── api.js        # Configuración de API
│   ├── App.jsx           # Componente principal
│   ├── main.jsx          # Punto de entrada
│   └── index.css         # Estilos globales
├── public/               # Archivos estáticos
├── index.html            # HTML principal
├── vite.config.js        # Configuración de Vite
├── tailwind.config.js    # Configuración de Tailwind
├── postcss.config.js     # Configuración de PostCSS
└── package.json          # Dependencias
```

## 🎨 Arquitectura

### Clean Architecture

El proyecto sigue los principios de Clean Architecture:

1. **Capa de Presentación** (`pages/`, `components/`)
   - Componentes de UI
   - Páginas y vistas
   - Lógica de presentación

2. **Capa de Aplicación** (`context/`, `hooks/`)
   - Estado global
   - Custom hooks
   - Lógica de negocio del cliente

3. **Capa de Infraestructura** (`api/`, `utils/`)
   - Comunicación con API
   - Servicios externos
   - Utilidades

### Gestión de Estado

- **Context API** para autenticación
- **useState/useEffect** para estado local
- **Custom hooks** para lógica reutilizable

### Enrutamiento

- Rutas públicas: `/login`
- Rutas protegidas: Requieren autenticación
- Rutas con permisos: Verifican rol del usuario

## 🔐 Autenticación y Autorización

### Flujo de Autenticación

1. Usuario ingresa credenciales
2. Backend valida y retorna JWT token
3. Token se guarda en localStorage
4. Token se envía en cada request (Authorization header)
5. Si token expira o es inválido, redirige a login

### Roles y Permisos

**Admin:**
- Acceso total al sistema
- Todos los módulos y reportes

**Vendedor:**
- Ventas y clientes
- Reportes de ventas

**Almacenero:**
- Inventario, compras y proveedores
- Reportes de inventario y compras

## 🎯 Características

### Implementado

✅ Estructura base con Vite + React
✅ Configuración de Tailwind CSS
✅ Sistema de rutas con React Router
✅ Autenticación con JWT
✅ Context de autenticación
✅ Cliente HTTP con interceptores
✅ Componentes comunes reutilizables
✅ Layout responsive (Navbar + Sidebar)
✅ Página de Login
✅ Dashboard con estadísticas
✅ Página de Inventario
✅ Control de acceso por roles
✅ Notificaciones con Toast
✅ Formateo de moneda, fechas y números
✅ Validaciones de formularios

### Por Implementar

⏳ Módulo de Ventas completo
⏳ Módulo de Compras completo
⏳ Módulo de Clientes completo
⏳ Módulo de Proveedores
⏳ Módulo de Reportes completo
⏳ Formularios con React Hook Form
⏳ Modales y diálogos
⏳ Paginación de tablas
⏳ Búsqueda y filtros
⏳ Exportación a Excel/PDF

## 🚀 Instalación

### Prerrequisitos

- Node.js 16 o superior
- npm o yarn

### Pasos

1. Navegar a la carpeta del frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Crear archivo de variables de entorno:
```bash
copy .env.example .env
```

4. Configurar la URL del backend en `.env`:
```
VITE_API_URL=http://localhost:8000
```

5. Iniciar el servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en: http://localhost:3000

## 📝 Scripts Disponibles

```bash
# Desarrollo
npm run dev          # Inicia servidor de desarrollo

# Build
npm run build        # Compila para producción

# Preview
npm run preview      # Preview de build de producción

# Linting
npm run lint         # Ejecuta ESLint
```

## 🔗 Integración con Backend

El frontend se comunica con el backend a través de:

- **Base URL:** `http://localhost:8000/api/v1`
- **Proxy Vite:** `/api` → `http://localhost:8000`
- **Autenticación:** JWT token en header Authorization

### Endpoints Principales

- `POST /auth/login/form` - Login
- `GET /auth/me` - Usuario actual
- `GET /products` - Lista de productos
- `GET /sales` - Lista de ventas
- `GET /reports/dashboard` - Dashboard

## 🎨 Guía de Estilos

### Colores Principales

- **Primary:** Blue (#3b82f6)
- **Success:** Green (#10b981)
- **Warning:** Yellow (#f59e0b)
- **Danger:** Red (#ef4444)

### Componentes

- **Button:** Variantes primary, secondary, danger, success
- **Badge:** Variantes success, warning, danger, info
- **Card:** Contenedor con padding y sombra
- **Input:** Campo de texto con label y error
- **Select:** Dropdown con opciones

### Clases Utilitarias

```css
.btn              /* Botón base */
.btn-primary      /* Botón primario */
.card             /* Tarjeta */
.input            /* Input */
.label            /* Label */
.badge            /* Badge */
.table            /* Tabla */
```

## 📱 Responsive Design

- **Mobile:** < 768px
- **Tablet:** 768px - 1024px
- **Desktop:** > 1024px

El sidebar se oculta en móvil y se muestra con menú hamburguesa.

## 🔒 Seguridad

- Tokens JWT en localStorage
- Interceptores de Axios para agregar token
- Redirección automática a login si token expira
- Validación de permisos en rutas
- Sanitización de inputs

## 📈 Próximos Pasos (FASE 10)

1. Completar páginas de Ventas, Compras, Clientes
2. Implementar formularios con validación
3. Agregar modales y diálogos
4. Implementar tablas con paginación
5. Agregar búsqueda y filtros
6. Implementar reportes visuales
7. Agregar gráficos con Chart.js
8. Exportación a Excel/PDF
9. Optimización de rendimiento
10. Testing con Vitest

## 👥 Credenciales de Prueba

**Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`

**Vendedor:**
- Usuario: `vendedor`
- Contraseña: `vendedor123`

**Almacenero:**
- Usuario: `almacenero`
- Contraseña: `almacenero123`

## 📄 Licencia

© 2026 ERP Ferretería. Todos los derechos reservados.
