# Arquitectura Técnica - ERP Ferretería

Documento que describe la arquitectura técnica del sistema ERP para ferretería.

## 1. Visión General

### 1.1 Arquitectura de 3 Capas

```
┌─────────────────────────────────────────┐
│         FRONTEND (React + TS)           │
│  - Interfaz de Usuario                  │
│  - Validación de formularios            │
│  - Estado local (React Query)           │
└─────────────────┬───────────────────────┘
                  │ HTTP/REST (JSON)
                  │ JWT Token
┌─────────────────▼───────────────────────┐
│         BACKEND (FastAPI)               │
│  ┌─────────────────────────────────┐   │
│  │  API Layer (Endpoints REST)     │   │
│  └──────────┬──────────────────────┘   │
│  ┌──────────▼──────────────────────┐   │
│  │  Service Layer (Lógica Negocio) │   │
│  └──────────┬──────────────────────┘   │
│  ┌──────────▼──────────────────────┐   │
│  │  Repository Layer (Acceso Datos)│   │
│  └──────────┬──────────────────────┘   │
└─────────────┼───────────────────────────┘
              │ SQLAlchemy ORM
┌─────────────▼───────────────────────────┐
│      BASE DE DATOS (PostgreSQL)         │
│  - Tablas relacionales                  │
│  - Constraints e Índices                │
│  - Stored Procedures (opcional)         │
└─────────────────────────────────────────┘
```

## 2. Backend (FastAPI)

### 2.1 Estructura de Carpetas

```
backend/
├── app/
│   ├── api/                    # Capa de API
│   │   └── v1/
│   │       ├── endpoints/      # Controladores REST
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── products.py
│   │       │   ├── categories.py
│   │       │   ├── suppliers.py
│   │       │   ├── customers.py
│   │       │   ├── purchases.py
│   │       │   ├── sales.py
│   │       │   ├── payments.py
│   │       │   └── reports.py
│   │       └── router.py       # Router principal
│   │
│   ├── core/                   # Configuración central
│   │   ├── config.py           # Settings de la app
│   │   ├── database.py         # Conexión DB
│   │   └── utils.py            # Utilidades generales
│   │
│   ├── models/                 # Modelos SQLAlchemy (ORM)
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── supplier.py
│   │   ├── customer.py
│   │   ├── purchase.py
│   │   ├── sale.py
│   │   ├── payment.py
│   │   ├── inventory_movement.py
│   │   └── audit.py
│   │
│   ├── schemas/                # Schemas Pydantic (validación)
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── purchase.py
│   │   ├── sale.py
│   │   └── ...
│   │
│   ├── services/               # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── purchase_service.py
│   │   ├── sale_service.py
│   │   ├── inventory_service.py
│   │   └── ...
│   │
│   ├── repositories/           # Acceso a datos
│   │   ├── user_repository.py
│   │   ├── product_repository.py
│   │   ├── purchase_repository.py
│   │   └── ...
│   │
│   ├── security/               # Autenticación y autorización
│   │   ├── auth.py            # JWT handling
│   │   ├── permissions.py     # Control de acceso
│   │   └── password.py        # Hash de contraseñas
│   │
│   └── main.py                 # Aplicación FastAPI
│
├── alembic/                    # Migraciones DB
│   ├── versions/
│   └── env.py
│
├── tests/                      # Tests unitarios
├── requirements.txt
├── .env.example
└── run.py
```

### 2.2 Patrón de Diseño: Repository Pattern

**Flujo de una petición:**

```
1. Cliente → HTTP Request
           ↓
2. Endpoint (API Layer) → Validación de entrada (Pydantic)
           ↓
3. Service Layer → Lógica de negocio
           ↓
4. Repository Layer → Acceso a datos (SQLAlchemy)
           ↓
5. Base de Datos ← SQL Query
           ↓
6. Repository → Modelo ORM
           ↓
7. Service → DTO (Pydantic Schema)
           ↓
8. Endpoint → JSON Response
           ↓
9. Cliente ← HTTP Response
```

**Ejemplo práctico:**

```python
# 1. Endpoint (api/v1/endpoints/products.py)
@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return product_service.get_product_by_id(db, product_id)

# 2. Service (services/product_service.py)
def get_product_by_id(db: Session, product_id: int) -> ProductResponse:
    product = product_repository.find_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Calcular estado del stock
    estado = obtener_estado_stock(product.stock_actual, product.stock_minimo)
    
    return ProductResponse.from_orm(product, estado=estado)

# 3. Repository (repositories/product_repository.py)
def find_by_id(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()
```

### 2.3 Seguridad

**JWT (JSON Web Tokens):**

```python
# Estructura del token
{
    "sub": "user_id",
    "email": "user@example.com",
    "role": "admin",
    "exp": timestamp
}
```

**Middleware de autenticación:**

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Validar y decodificar token
    # Buscar usuario en DB
    # Retornar usuario o lanzar excepción
```

**Control de acceso basado en roles:**

```python
def require_role(allowed_roles: List[str]):
    def decorator(func):
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if current_user.role.name not in allowed_roles:
                raise HTTPException(status_code=403, detail="Acceso denegado")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Uso:
@router.post("/products")
@require_role(["admin", "almacenero"])
async def create_product(...):
    pass
```

## 3. Base de Datos (PostgreSQL)

### 3.1 Diagrama de Entidad-Relación

```
┌──────────────┐       ┌──────────────┐
│   usuarios   │──────<│    roles     │
└──────┬───────┘       └──────────────┘
       │
       │ (auditoría)
       │
┌──────▼───────┐       ┌──────────────┐
│  auditoria   │       │  categorias  │
└──────────────┘       └──────┬───────┘
                              │
       ┌──────────────────────▼───────┐
       │        productos             │
       └──┬────────────────────────┬──┘
          │                        │
          │                        │
┌─────────▼────┐         ┌────────▼──────┐
│ proveedores  │         │   clientes    │
└──────┬───────┘         └───────┬───────┘
       │                         │
┌──────▼───────┐         ┌───────▼───────┐
│   compras    │         │    ventas     │
└──────┬───────┘         └───────┬───────┘
       │                         │
┌──────▼────────┐        ┌───────▼───────┐
│detalle_compras│        │detalle_ventas │
└───────────────┘        └───────────────┘
                                │
                         ┌──────▼────────┐
                         │     pagos     │
                         └───────────────┘
       
       ┌───────────────────────┐
       │ movimientos_inventario│
       └───────────────────────┘
```

### 3.2 Tablas Principales

**usuarios**
```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    apellido VARCHAR(200) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**productos**
```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria_id INTEGER REFERENCES categorias(id),
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 0,
    costo_unitario DECIMAL(10,2) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_stock_no_negativo CHECK (stock_actual >= 0),
    CONSTRAINT chk_precios_positivos CHECK (costo_unitario > 0 AND precio_venta > 0)
);

CREATE INDEX idx_productos_sku ON productos(sku);
CREATE INDEX idx_productos_categoria ON productos(categoria_id);
CREATE INDEX idx_productos_nombre ON productos(nombre);
```

**ventas**
```sql
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    numero_comprobante VARCHAR(50) UNIQUE NOT NULL,
    cliente_id INTEGER REFERENCES clientes(id),
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL,
    igv DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    condicion VARCHAR(20) NOT NULL, -- 'CONTADO' o 'CREDITO'
    estado VARCHAR(20) DEFAULT 'COMPLETADA',
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_condicion CHECK (condicion IN ('CONTADO', 'CREDITO'))
);

CREATE INDEX idx_ventas_cliente ON ventas(cliente_id);
CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_ventas_numero ON ventas(numero_comprobante);
```

### 3.3 Índices para Optimización

```sql
-- Búsquedas frecuentes
CREATE INDEX idx_productos_stock_bajo ON productos(stock_actual) WHERE stock_actual <= stock_minimo;
CREATE INDEX idx_clientes_ruc_dni ON clientes(ruc, dni);
CREATE INDEX idx_ventas_estado ON ventas(estado);

-- Reportes
CREATE INDEX idx_ventas_fecha_total ON ventas(fecha, total);
CREATE INDEX idx_compras_fecha ON compras(fecha);
```

### 3.4 Triggers (opcional)

```sql
-- Actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_productos_updated_at BEFORE UPDATE ON productos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## 4. Frontend (React + TypeScript)

### 4.1 Estructura de Carpetas

```
frontend/
├── src/
│   ├── api/                    # Cliente API
│   │   ├── axios.config.ts
│   │   ├── auth.api.ts
│   │   ├── products.api.ts
│   │   └── ...
│   │
│   ├── components/             # Componentes reutilizables
│   │   ├── common/            # Botones, Inputs, Modals
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── DataTable.tsx
│   │   ├── layout/            # Layout de la app
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Layout.tsx
│   │   └── modules/           # Componentes específicos
│   │       ├── ProductCard.tsx
│   │       └── SaleForm.tsx
│   │
│   ├── contexts/               # React Contexts
│   │   ├── AuthContext.tsx
│   │   └── ThemeContext.tsx
│   │
│   ├── hooks/                  # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── useProducts.ts
│   │   └── useSales.ts
│   │
│   ├── pages/                  # Páginas
│   │   ├── auth/
│   │   │   ├── LoginPage.tsx
│   │   │   └── RegisterPage.tsx
│   │   ├── dashboard/
│   │   │   └── DashboardPage.tsx
│   │   ├── inventory/
│   │   │   ├── ProductsPage.tsx
│   │   │   └── CategoriesPage.tsx
│   │   ├── purchases/
│   │   │   ├── PurchasesPage.tsx
│   │   │   └── SuppliersPage.tsx
│   │   ├── sales/
│   │   │   ├── SalesPage.tsx
│   │   │   └── NewSalePage.tsx
│   │   └── customers/
│   │       ├── CustomersPage.tsx
│   │       └── PaymentsPage.tsx
│   │
│   ├── types/                  # Tipos TypeScript
│   │   ├── user.types.ts
│   │   ├── product.types.ts
│   │   ├── sale.types.ts
│   │   └── ...
│   │
│   ├── utils/                  # Utilidades
│   │   ├── format.ts          # Formateo de fechas, moneda
│   │   ├── validation.ts      # Validaciones
│   │   └── constants.ts       # Constantes
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── router.tsx
│
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

### 4.2 Gestión de Estado

**React Query para estado del servidor:**

```typescript
// hooks/useProducts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => productApi.getAll(),
  });
};

export const useCreateProduct = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateProductDto) => productApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
};
```

**Context API para estado global:**

```typescript
// contexts/AuthContext.tsx
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

export const AuthProvider: React.FC = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  // ... lógica de autenticación
  
  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### 4.3 Rutas Protegidas

```typescript
// ProtectedRoute.tsx
const ProtectedRoute: React.FC<Props> = ({ allowedRoles, children }) => {
  const { user, isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" />;
  }
  
  return <>{children}</>;
};

// Uso en router
<Route path="/inventory" element={
  <ProtectedRoute allowedRoles={['admin', 'almacenero']}>
    <InventoryPage />
  </ProtectedRoute>
} />
```

## 5. API REST

### 5.1 Convenciones

**Endpoints:**
- Base URL: `/api/v1`
- Recursos en plural: `/products`, `/sales`
- IDs en la ruta: `/products/{id}`

**Métodos HTTP:**
- `GET` - Obtener recursos
- `POST` - Crear recursos
- `PUT` - Actualizar recursos completos
- `PATCH` - Actualizar recursos parcialmente
- `DELETE` - Eliminar recursos

**Códigos de estado:**
- `200 OK` - Éxito
- `201 Created` - Recurso creado
- `400 Bad Request` - Error de validación
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - Sin permisos
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

### 5.2 Formato de Respuestas

**Éxito:**
```json
{
  "data": {
    "id": 1,
    "nombre": "Producto",
    ...
  }
}
```

**Lista con paginación:**
```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  }
}
```

**Error:**
```json
{
  "detail": "Mensaje de error",
  "error_code": "VALIDATION_ERROR",
  "fields": {
    "nombre": ["Campo requerido"]
  }
}
```

## 6. Despliegue en AWS

### 6.1 Arquitectura en la Nube

```
Internet
   │
   ▼
CloudFront (CDN)
   │
   ├──▶ S3 Bucket (Frontend estático)
   │
   └──▶ ALB (Application Load Balancer)
          │
          ▼
       EC2 Instance(s)
       ├── Nginx (Reverse Proxy)
       └── Gunicorn + FastAPI
               │
               ▼
          RDS PostgreSQL
               │
               ▼
          S3 Bucket (Documentos)
```

### 6.2 Componentes AWS

**EC2 (Backend):**
- Tipo: t3.small (mínimo para producción)
- OS: Ubuntu 22.04 LTS
- Software: Python, Nginx, Gunicorn
- Security Group: Puertos 80, 443, 22

**RDS PostgreSQL:**
- Instancia: db.t3.micro
- Versión: PostgreSQL 14+
- Multi-AZ: Sí (para alta disponibilidad)
- Backup automático: 7 días

**S3:**
- Bucket 1: Frontend estático
- Bucket 2: Documentos y archivos

**CloudWatch:**
- Logs de aplicación
- Métricas de rendimiento
- Alarmas automáticas

## 7. Seguridad

### 7.1 Capas de Seguridad

1. **Frontend:**
   - Validación de inputs
   - Sanitización de datos
   - HTTPS obligatorio

2. **Backend:**
   - JWT con expiración
   - Rate limiting
   - Validación con Pydantic
   - SQL Injection protection (ORM)
   - CORS configurado

3. **Base de Datos:**
   - Acceso solo desde backend
   - Contraseñas hasheadas (bcrypt)
   - Backups automáticos

4. **Infraestructura:**
   - Security Groups restrictivos
   - VPC privada para DB
   - SSL/TLS en todas las conexiones

### 7.2 Mejores Prácticas

- Variables de entorno para credenciales
- Secrets en AWS Secrets Manager
- Logs de auditoría en operaciones críticas
- Principio de mínimo privilegio
- Actualizar dependencias regularmente

## 8. Monitoreo y Logs

### 8.1 Logging

**Backend:**
```python
import logging

logger = logging.getLogger(__name__)

logger.info("Venta creada", extra={
    "venta_id": sale.id,
    "usuario": current_user.email,
    "total": sale.total
})
```

**Niveles:**
- `DEBUG` - Desarrollo
- `INFO` - Eventos normales
- `WARNING` - Advertencias
- `ERROR` - Errores recuperables
- `CRITICAL` - Errores críticos

### 8.2 Métricas

- Tiempo de respuesta de APIs
- Tasa de errores
- Uso de CPU y memoria
- Conexiones de base de datos activas
- Transacciones por minuto

---

**Versión**: 1.0  
**Última actualización**: Octubre 2026
