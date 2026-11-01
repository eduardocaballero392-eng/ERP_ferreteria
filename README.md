# ERP Ferretería - Sistema de Gestión para Ferreterías en Perú

Sistema ERP (Enterprise Resource Planning) completo para la gestión de ferreterías en Perú, desarrollado con arquitectura moderna y escalable.

## 📋 Descripción

Sistema web que permite gestionar de manera integral los procesos clave de una ferretería:
- Control de inventario con alertas de reposición
- Gestión de compras y proveedores
- Registro de ventas con cálculo automático de IGV (18%)
- Control de créditos y pagos de clientes
- Reportes y análisis de utilidad

## 🏗️ Arquitectura

### Backend
- **Framework**: FastAPI (Python)
- **Base de datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migraciones**: Alembic
- **Autenticación**: JWT (JSON Web Tokens)
- **Validación**: Pydantic

### Frontend
- **Framework**: React 18
- **Lenguaje**: TypeScript
- **Build Tool**: Vite
- **Estilo**: Tailwind CSS
- **Estado**: TanStack Query (React Query)
- **Formularios**: React Hook Form + Zod

### Infraestructura (AWS)
- **API**: EC2
- **Base de datos**: RDS PostgreSQL
- **Almacenamiento**: S3
- **Logs**: CloudWatch

## 📦 Módulos del Sistema

### 1. Inventario
- Gestión de productos y categorías
- Control de stock actual y stock mínimo
- Estados: OK / REPONER / AGOTADO
- Registro de costos y precios de venta (sin IGV)

### 2. Compras
- Gestión de proveedores
- Órdenes de compra
- Actualización automática de stock al registrar compra

### 3. Ventas
- Registro de comprobantes
- Gestión de clientes
- Detalle de venta con cálculo automático de IGV (18%)
- Condiciones: Contado / Crédito
- Actualización automática de stock (resta)

### 4. Clientes
- Control de límite de crédito
- Gestión de pagos
- Cálculo automático de saldo por cobrar
- Alertas cuando se supera el límite de crédito

### 5. Seguridad y Auditoría
- Autenticación con JWT
- Roles de usuario:
  - **Admin**: Acceso completo
  - **Vendedor**: Solo Ventas y Clientes
  - **Almacenero**: Solo Inventario y Compras
- Registro de auditoría en operaciones críticas

### 6. Dashboard y Reportes
- Indicadores clave de negocio
- Reporte de utilidad bruta (subtotal - costo)
- Movimientos de inventario
- Análisis de ventas y compras

## 🔧 Reglas de Negocio

1. **Control de Stock**
   ```
   Stock actual = Stock inicial + Compras - Ventas
   ```
   - No se permite vender con stock insuficiente
   - Estado AGOTADO: stock <= 0
   - Estado REPONER: stock <= stock_mínimo
   - Estado OK: stock > stock_mínimo

2. **Cálculo de IGV**
   - IGV en Perú: 18%
   - Precios de productos se registran SIN IGV
   - En ventas se calcula: `Total = Subtotal + (Subtotal * 0.18)`

3. **Gestión de Crédito**
   ```
   Saldo por cobrar = Ventas a crédito (con IGV) - Pagos
   ```
   - Alertar si el saldo supera el límite de crédito del cliente

4. **Utilidad Bruta**
   ```
   Utilidad = Subtotal de venta - Costo de productos vendidos
   ```

## 📊 Base de Datos

### Tablas Principales

1. **usuarios** - Usuarios del sistema
2. **roles** - Roles de acceso
3. **categorias** - Categorías de productos
4. **productos** - Catálogo de productos
5. **proveedores** - Proveedores
6. **clientes** - Clientes
7. **compras** - Órdenes de compra
8. **detalle_compras** - Items de compras
9. **ventas** - Ventas realizadas
10. **detalle_ventas** - Items de ventas
11. **pagos** - Pagos de clientes
12. **movimientos_inventario** - Historial de movimientos
13. **auditoria** - Log de operaciones críticas

### Características
- Claves foráneas para integridad referencial
- Índices en campos de búsqueda frecuente
- Migraciones versionadas con Alembic
- Datos de ejemplo incluidos

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd ERP_ferreteria
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Crear base de datos PostgreSQL
createdb erp_ferreteria

# Ejecutar migraciones (después de crearlas)
alembic upgrade head

# Ejecutar aplicación
python run.py
```

La API estará disponible en: http://localhost:8000

### 3. Configurar Frontend (en las siguientes fases)

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env

# Ejecutar en modo desarrollo
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## 📚 Documentación de la API

Una vez ejecutado el backend, la documentación interactiva está disponible en:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 🔐 Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrar usuario
- `GET /api/v1/auth/me` - Usuario actual

### Inventario
- `GET /api/v1/categories` - Listar categorías
- `GET /api/v1/products` - Listar productos
- `POST /api/v1/products` - Crear producto

### Compras
- `GET /api/v1/suppliers` - Listar proveedores
- `GET /api/v1/purchases` - Listar compras
- `POST /api/v1/purchases` - Crear compra

### Ventas
- `GET /api/v1/sales` - Listar ventas
- `POST /api/v1/sales` - Crear venta

### Clientes
- `GET /api/v1/customers` - Listar clientes
- `GET /api/v1/payments` - Listar pagos
- `POST /api/v1/payments` - Registrar pago

### Reportes
- `GET /api/v1/reports/inventory` - Reporte de inventario
- `GET /api/v1/reports/sales` - Reporte de ventas

## 🏢 Estructura del Proyecto

```
ERP_ferreteria/
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       └── router.py
│   │   ├── core/           # Configuración
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── utils.py
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Lógica de negocio
│   │   ├── repositories/   # Acceso a datos
│   │   ├── security/       # Autenticación
│   │   └── main.py
│   ├── alembic/            # Migraciones
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
├── frontend/               # Frontend React
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── contexts/
│   │   ├── hooks/
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

## 📦 Despliegue

### AWS (Producción)

#### Backend (EC2)
1. Lanzar instancia EC2 con Ubuntu
2. Instalar Python, PostgreSQL client, nginx
3. Configurar Gunicorn + Nginx
4. Configurar variables de entorno con credenciales RDS

#### Base de Datos (RDS)
1. Crear instancia RDS PostgreSQL
2. Configurar security groups
3. Ejecutar migraciones

#### Frontend (S3 + CloudFront)
1. Build: `npm run build`
2. Subir a S3 bucket
3. Configurar CloudFront para CDN

#### Monitoreo (CloudWatch)
- Logs de aplicación
- Métricas de rendimiento
- Alertas automáticas

## 📝 Fases de Desarrollo

✅ **FASE 1**: Estructura base del backend (COMPLETADA)
- [x] Estructura de carpetas
- [x] Configuración FastAPI
- [x] Variables de entorno
- [x] Utilidades básicas

⏳ **FASE 2**: Base de datos y migraciones
⏳ **FASE 3**: Autenticación y seguridad
⏳ **FASE 4**: Módulo Inventario
⏳ **FASE 5**: Módulo Compras
⏳ **FASE 6**: Módulo Ventas
⏳ **FASE 7**: Módulo Clientes
⏳ **FASE 8**: Reportes y auditoría
⏳ **FASE 9**: Frontend React (estructura)
⏳ **FASE 10**: Interfaces de usuario
⏳ **FASE 11**: Datos de ejemplo y AWS

## 👥 Usuarios de Ejemplo (se crearán en fase de datos)

### Administrador
- Usuario: `admin@ferreteria.com`
- Password: `admin123`

### Vendedor
- Usuario: `vendedor@ferreteria.com`
- Password: `vend123`

### Almacenero
- Usuario: `almacen@ferreteria.com`
- Password: `alm123`

## 🛠️ Tecnologías y Librerías

### Backend
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- Alembic 1.13.1
- Pydantic 2.5.3
- python-jose (JWT)
- passlib (bcrypt)
- psycopg2-binary

### Frontend
- React 18
- TypeScript 5
- Vite 5
- Tailwind CSS 3
- React Router 6
- Axios
- TanStack Query v5
- React Hook Form
- Zod

## 📄 Licencia

Proyecto privado - Uso exclusivo para ERP Ferretería Perú

## 🤝 Contribución

Este es un proyecto privado. Para cualquier consulta o sugerencia, contactar al equipo de desarrollo.

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema, contactar a:
- Email: soporte@ferreteria.com
- Teléfono: +51 XXX XXX XXX

---

**Versión**: 1.0.0  
**Última actualización**: Octubre 2026  
**Estado**: En desarrollo - MVP
