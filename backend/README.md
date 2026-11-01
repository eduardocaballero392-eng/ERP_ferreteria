# ERP Ferretería - Backend

Sistema ERP para gestión de ferretería en Perú desarrollado con Python y FastAPI.
**Sistema basado en archivos CSV** para almacenamiento de datos (sin base de datos).

## Características

- **Inventario**: Gestión de productos, categorías, control de stock
- **Compras**: Proveedores, órdenes de compra, actualización automática de stock
- **Ventas**: Comprobantes, clientes, cálculo de IGV (18%), condiciones de pago
- **Clientes**: Límite de crédito, gestión de pagos, saldo por cobrar
- **Autenticación**: JWT con roles (admin, vendedor, almacenero)
- **Reportes**: Utilidad bruta, movimientos de inventario, auditoría
- **Almacenamiento**: Archivos CSV para persistencia de datos

## Estructura del Proyecto

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # Endpoints de cada módulo
│   │       └── router.py      # Router principal de API v1
│   ├── core/
│   │   ├── config.py          # Configuración de la aplicación
│   │   ├── csv_handler.py     # Manejador de archivos CSV
│   │   └── utils.py           # Utilidades generales
│   ├── models/                # Modelos Pydantic (estructuras de datos)
│   ├── schemas/               # Esquemas Pydantic para validación
│   ├── services/              # Lógica de negocio
│   ├── repositories/          # Capa de acceso a datos CSV
│   ├── security/              # Autenticación y autorización
│   └── main.py                # Aplicación FastAPI principal
├── data/                      # Archivos CSV con los datos
│   ├── productos.csv
│   ├── clientes.csv
│   ├── ventas.csv
│   └── ...
├── requirements.txt           # Dependencias Python
└── .env                       # Variables de entorno (crear desde .env.example)
```

## Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno (opcional)

Copiar `.env.example` a `.env` y configurar las variables:

```bash
cp .env.example .env
```

### 4. Preparar tus archivos CSV

Coloca tus archivos CSV en la carpeta `backend/data/`:

```
backend/data/
├── productos.csv
├── categorias.csv
├── clientes.csv
├── proveedores.csv
├── ventas.csv
├── compras.csv
└── ... (ver data/README.md para lista completa)
```

**Nota**: El sistema puede funcionar sin archivos CSV iniciales. Se crearán automáticamente al agregar datos.

### 5. Inspeccionar tus CSV (opcional)

```bash
python load_csv_data.py
```

Este script te mostrará:
- Qué archivos CSV se encontraron
- Columnas de cada archivo
- Primeras filas de datos
- Validación de formato

## Ejecución

### Modo desarrollo

```bash
# Desde la carpeta backend
python run.py

# O usando uvicorn directamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Modo producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Acceso a la API

- **API**: http://localhost:8000
- **Documentación interactiva (Swagger)**: http://localhost:8000/api/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

## Formato de los Archivos CSV

### Estructura General

- **Codificación**: UTF-8
- **Separador**: Coma (,)
- **Formato de fechas**: ISO 8601 (YYYY-MM-DD HH:MM:SS)
- **Booleanos**: True/False o 1/0
- **Decimales**: Punto como separador (ej: 123.45)

### Ejemplo: productos.csv

```csv
id,sku,nombre,descripcion,categoria_id,stock_actual,stock_minimo,unidad_medida,costo_unitario,precio_venta,activo,created_at,updated_at
1,CEM-001,Cemento Andino Tipo I x 42.5 kg,Cemento portland tipo I,1,150,50,UND,22.50,28.00,True,2026-10-01 10:00:00,2026-10-01 10:00:00
2,FIE-001,Fierro de 1/2 pulgada x 9m,Varilla de construcción,2,200,30,UND,35.00,45.00,True,2026-10-01 10:00:00,2026-10-01 10:00:00
```

Ver `data/README.md` para la lista completa de archivos y columnas esperadas.

## Endpoints API

### Autenticación ✅
- `POST /api/v1/auth/login/form` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrar usuario
- `GET /api/v1/auth/me` - Obtener usuario actual
- `PUT /api/v1/auth/change-password` - Cambiar contraseña

### Categorías ✅
- `GET /api/v1/categories` - Listar categorías
- `GET /api/v1/categories/with-count` - Con conteo de productos
- `GET /api/v1/categories/{id}` - Obtener categoría
- `POST /api/v1/categories` - Crear categoría
- `PUT /api/v1/categories/{id}` - Actualizar categoría
- `DELETE /api/v1/categories/{id}` - Eliminar categoría

### Productos ✅
- `GET /api/v1/products` - Listar productos
- `GET /api/v1/products/details` - Con detalles completos
- `GET /api/v1/products/low-stock` - Productos con stock bajo
- `POST /api/v1/products/search` - Buscar con filtros
- `GET /api/v1/products/{id}` - Obtener producto
- `POST /api/v1/products` - Crear producto
- `PUT /api/v1/products/{id}` - Actualizar producto
- `POST /api/v1/products/{id}/adjust-stock` - Ajustar stock
- `DELETE /api/v1/products/{id}` - Eliminar producto

### Proveedores ✅
- `GET /api/v1/suppliers` - Listar proveedores
- `GET /api/v1/suppliers/with-stats` - Con estadísticas de compras
- `GET /api/v1/suppliers/search?query=` - Buscar proveedores
- `GET /api/v1/suppliers/{id}` - Obtener proveedor
- `POST /api/v1/suppliers` - Crear proveedor
- `PUT /api/v1/suppliers/{id}` - Actualizar proveedor
- `DELETE /api/v1/suppliers/{id}` - Eliminar proveedor

### Compras ✅
- `GET /api/v1/purchases` - Listar compras
- `GET /api/v1/purchases/stats` - Estadísticas de compras
- `GET /api/v1/purchases/{id}` - Obtener compra con detalles
- `POST /api/v1/purchases` - Crear compra (actualiza stock automáticamente)
- `PUT /api/v1/purchases/{id}` - Actualizar compra
- `DELETE /api/v1/purchases/{id}` - Anular compra

### Ventas ✅
- `GET /api/v1/sales` - Listar ventas
- `GET /api/v1/sales/stats` - Estadísticas de ventas
- `GET /api/v1/sales/{id}` - Obtener venta con detalles
- `POST /api/v1/sales` - Crear venta (actualiza stock automáticamente)
- `PUT /api/v1/sales/{id}` - Actualizar venta
- `DELETE /api/v1/sales/{id}` - Anular venta

### Clientes ✅
- `GET /api/v1/customers` - Listar clientes
- `GET /api/v1/customers/with-stats` - Con estadísticas de compras
- `GET /api/v1/customers/search?query=` - Buscar clientes
- `GET /api/v1/customers/{id}` - Obtener cliente
- `POST /api/v1/customers` - Crear cliente
- `PUT /api/v1/customers/{id}` - Actualizar cliente
- `DELETE /api/v1/customers/{id}` - Eliminar cliente

### Pagos (próximamente)
- `GET /api/v1/payments` - Listar pagos
- `POST /api/v1/payments` - Registrar pago

### Reportes y Auditoría ✅
- `GET /api/v1/reports/dashboard` - Dashboard con estadísticas generales
- `GET /api/v1/reports/inventory` - Reporte de inventario valorizado
- `GET /api/v1/reports/sales` - Reporte de ventas con utilidad bruta
- `GET /api/v1/reports/purchases` - Reporte de compras
- `GET /api/v1/reports/movements/{producto_id}` - Movimientos de producto
- `GET /api/v1/reports/audit` - Logs de auditoría

## Reglas de Negocio

1. **Control de Stock**: 
   - Stock actual = stock inicial + compras - ventas
   - No permitir ventas con stock insuficiente
   - Estados: OK / REPONER (stock <= mínimo) / AGOTADO (stock <= 0)

2. **Cálculo de IGV**:
   - IGV = 18% en Perú
   - Los precios de productos se registran SIN IGV
   - El IGV se calcula en la venta

3. **Gestión de Crédito**:
   - Saldo por cobrar = ventas a crédito - pagos
   - Alertar si el saldo supera el límite de crédito del cliente

4. **Roles y Permisos**:
   - **Admin**: Acceso total
   - **Vendedor**: Ventas y Clientes
   - **Almacenero**: Inventario y Compras

## Seguridad

- Autenticación con JWT (JSON Web Tokens)
- Contraseñas hasheadas con bcrypt
- Validación de datos con Pydantic
- Control de acceso basado en roles (RBAC)
- Registro de auditoría en operaciones críticas

## Respaldo de Datos

Los archivos CSV están en `backend/data/`. Para hacer respaldo:

### Windows
```cmd
xcopy data data_backup /E /I /Y
```

### Linux/Mac
```bash
cp -r data data_backup
```

## Desarrollo

### Pruebas de configuración

```bash
python test_config.py
```

### Inspeccionar archivos CSV

```bash
python load_csv_data.py
```

## Migración desde/hacia otros formatos

### Exportar a Excel

```python
import pandas as pd
df = pd.read_csv('data/productos.csv')
df.to_excel('productos.xlsx', index=False)
```

### Importar desde Excel

```python
import pandas as pd
df = pd.read_excel('productos.xlsx')
df.to_csv('data/productos.csv', index=False)
```

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos
- **Pandas**: Manejo de datos CSV
- **JWT**: Autenticación sin estado
- **Uvicorn**: Servidor ASGI

## Licencia

Proyecto privado - ERP Ferretería Perú
