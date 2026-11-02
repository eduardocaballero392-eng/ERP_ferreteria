# 🚀 Inicio Rápido - Frontend ERP Ferretería

## ✅ Prerrequisitos

- Node.js 16 o superior
- npm o yarn
- Backend corriendo en `http://localhost:8000`

## 📦 Instalación

### 1. Navegar a la carpeta del frontend

```bash
cd frontend
```

### 2. Instalar dependencias

```bash
npm install
```

### 3. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env y configurar:
# En desarrollo, Vite usa el proxy hacia http://localhost:8000.
# VITE_API_URL solo se configura para producción, con la URL pública del backend.
```

### 4. Iniciar servidor de desarrollo

```bash
npm run dev
```

El frontend estará disponible en: **http://localhost:3000**

## 🔑 Credenciales de Prueba

### Administrador (Acceso Total)
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Todos los módulos

### Vendedor
- **Usuario:** `vendedor`
- **Contraseña:** `vendedor123`
- **Permisos:** Ventas, Clientes, Reportes

### Almacenero
- **Usuario:** `almacenero`
- **Contraseña:** `almacenero123`
- **Permisos:** Inventario, Compras, Proveedores, Reportes

## 📱 Navegación

Una vez logueado, verás:

### Dashboard Principal
- Estadísticas del día y del mes
- Utilidad bruta
- Margen promedio
- Top 5 productos, clientes y proveedores

### Inventario
- Lista de productos con stock
- Alertas de stock bajo
- Valor del inventario

### Módulos (En construcción)
- Ventas
- Compras
- Clientes
- Reportes

## 🛠️ Scripts Disponibles

```bash
# Desarrollo
npm run dev          # Inicia servidor de desarrollo en puerto 3000

# Build
npm run build        # Compila para producción en carpeta dist/

# Preview
npm run preview      # Preview del build de producción

# Linting
npm run lint         # Ejecuta ESLint para verificar código
```

## 🔍 Verificar Integración con Backend

### 1. Verificar que el backend esté corriendo

```bash
# En otra terminal, navegar a backend/
cd backend
py run.py
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Probar endpoints desde el navegador

```
http://localhost:8000/api/docs
```

### 3. Login desde el frontend

1. Abrir `http://localhost:3000`
2. Usar credenciales de prueba
3. Deberías ver el dashboard

## ⚠️ Solución de Problemas

### Error: "Cannot connect to backend"

**Problema:** Frontend no puede conectarse al backend

**Solución:**
1. Verificar que el backend esté corriendo en puerto 8000
2. Verificar que la variable `VITE_API_URL` esté configurada correctamente
3. Verificar que no haya CORS errors en la consola del navegador

### Error: "Token expired" o redirige a login

**Problema:** Token JWT expiró

**Solución:**
1. Volver a iniciar sesión
2. El token tiene validez limitada por seguridad

### Error: "403 - Sin permisos"

**Problema:** El usuario no tiene permisos para esa sección

**Solución:**
- Usar usuario con permisos adecuados
- Admin tiene acceso a todo
- Vendedor: solo ventas y clientes
- Almacenero: solo inventario y compras

### Error en npm install

**Problema:** Dependencias no se instalan

**Solución:**
```bash
# Limpiar cache
npm cache clean --force

# Eliminar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Puerto 3000 en uso

**Problema:** Puerto 3000 ya está ocupado

**Solución:**
```bash
# Vite asignará automáticamente el siguiente puerto disponible (3001, 3002, etc)
# O especificar puerto manualmente en vite.config.js:
server: {
  port: 3001
}
```

## 📂 Archivos Importantes

```
frontend/
├── src/
│   ├── App.jsx               # Componente raíz con rutas
│   ├── main.jsx              # Punto de entrada
│   ├── api/
│   │   └── client.js         # Cliente Axios con interceptores
│   ├── context/
│   │   └── AuthContext.jsx   # Gestión de autenticación
│   ├── pages/
│   │   ├── LoginPage.jsx     # Página de login
│   │   ├── DashboardPage.jsx # Dashboard principal
│   │   └── InventoryPage.jsx # Inventario
│   └── components/
│       ├── common/           # Componentes reutilizables
│       └── layout/           # Navbar y Sidebar
├── vite.config.js            # Configuración de Vite (proxy)
├── tailwind.config.js        # Configuración de Tailwind CSS
└── package.json              # Dependencias
```

## 🎨 Estructura Visual

```
┌─────────────────────────────────────────────┐
│  Navbar (Top)                               │
│  [Logo] ERP Ferretería         [User Menu]  │
└─────────────────────────────────────────────┘
│         │                                    │
│ Sidebar │  Main Content Area                │
│         │                                    │
│ ≡ Menu  │  ┌───────────────────────────┐   │
│         │  │                           │   │
│ Dashboard│  │   Contenido de Página    │   │
│ Inventario│ │                           │   │
│ Ventas  │  │                           │   │
│ Compras │  └───────────────────────────┘   │
│ Clientes│                                   │
│ Reportes│                                   │
│         │                                    │
└─────────────────────────────────────────────┘
```

## 🔄 Flujo de Trabajo

1. **Login:**
   - Usuario ingresa credenciales
   - Frontend envía a `/api/v1/auth/login/form`
   - Backend valida y retorna JWT
   - Token se guarda en localStorage
   - Redirige a dashboard

2. **Navegación:**
   - Usuario hace clic en módulo
   - ProtectedRoute verifica autenticación y permisos
   - Si OK: muestra página
   - Si NO: redirige o muestra error 403

3. **Carga de Datos:**
   - Página llama a servicio API
   - Cliente Axios agrega token automáticamente
   - Backend procesa y retorna datos
   - Página actualiza UI con datos

## 🌐 URLs Importantes

| Descripción | URL |
|-------------|-----|
| Frontend Dev | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/api/docs |
| Login | http://localhost:3000/login |
| Dashboard | http://localhost:3000/dashboard |

## ✨ Características Implementadas

✅ Login con JWT  
✅ Dashboard con estadísticas  
✅ Inventario con lista de productos  
✅ Navbar responsive  
✅ Sidebar con navegación  
✅ Control de acceso por roles  
✅ Notificaciones toast  
✅ Formateo de moneda y fechas  
✅ Componentes reutilizables  
✅ Layout responsive  

## 📚 Próximos Pasos

Después de iniciar el frontend:

1. ✅ Explorar el Dashboard
2. ✅ Ver lista de productos en Inventario
3. ⏳ Probar crear una venta (próxima fase)
4. ⏳ Ver reportes con gráficos (próxima fase)
5. ⏳ Gestionar clientes y proveedores (próxima fase)

## 🆘 Ayuda

Si tienes problemas:

1. Verificar que el backend esté corriendo
2. Revisar la consola del navegador (F12)
3. Verificar la terminal donde corre el frontend
4. Revisar documentación en `README.md`
5. Revisar arquitectura en `ARQUITECTURA_FRONTEND.md`

---

**¡Listo para empezar! 🎉**

Ejecuta `npm run dev` y abre http://localhost:3000
