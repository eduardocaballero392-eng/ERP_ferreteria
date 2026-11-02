# ERP para Ferretería — documentación para exposición

## 1. Presentación del proyecto

El ERP para Ferretería es una aplicación web para centralizar operaciones de una ferretería: catálogo y existencias, ventas, compras, clientes, proveedores, usuarios y reportes. La interfaz web permite registrar y consultar información; una API valida las operaciones y persiste los datos en archivos CSV compartidos. Al compartir el catálogo, las ventas y las compras actualizan el mismo stock.

**Objetivo:** reducir registros dispersos y facilitar el seguimiento del inventario y de las operaciones comerciales desde un solo sistema.

**Alcance implementado:** autenticación, control por roles, productos y categorías, clientes, proveedores, compras, ventas, carga/sincronización de datos y reportes. No se debe presentar como un sistema contable completo: no se observa un libro contable ni una integración con SUNAT en el código actual.

## 2. Arquitectura y tecnologías

```text
Usuario
  ↓ navegador
Frontend React + Vite + Tailwind
  ↓ Axios / HTTP JSON (JWT Bearer)
API FastAPI (/api/v1)
  ↓ routers → servicios → repositorios
Archivos CSV en backend/data (fuente de datos compartida)
```

- **Frontend:** React 18, React Router, Vite, Tailwind CSS, Axios, Lucide y React Hot Toast. Las páginas y componentes están en `frontend/src`; las llamadas HTTP están agrupadas en `frontend/src/api`.
- **Backend:** Python, FastAPI y Pydantic. Los endpoints se agrupan por módulo en `backend/app/api/v1/endpoints`; la lógica está en `services`; los repositorios realizan la lectura y escritura CSV.
- **Persistencia:** CSV, no una base de datos relacional. Entre los archivos de datos están productos, categorías, clientes, proveedores, ventas, detalle de ventas, compras, detalle de compras, usuarios, pagos, movimientos y auditoría.
- **Comunicación:** JSON por HTTP bajo `/api/v1`. La API publica Swagger en `/api/docs`, ReDoc en `/api/redoc` y un chequeo de estado en `/health`.

## 3. Módulos funcionales

### Acceso y usuarios

El usuario inicia sesión con credenciales. El backend valida la contraseña, genera un JWT y el cliente HTTP del frontend lo envía como `Authorization: Bearer <token>`. Las rutas internas requieren autenticación. El backend obtiene el usuario asociado al token, comprueba que esté activo y aplica dependencias de autorización por rol. Existe cambio de contraseña y registro de usuarios protegido para administración. En el primer arranque se asegura la cuenta administrativa inicial; las credenciales deben cambiarse para cualquier entorno real.

### Inventario y categorías

El catálogo conserva identificador/SKU, nombre, categoría, costo, precio, stock actual y mínimo, entre otros datos. Las categorías permiten organizar y filtrar productos. El inventario muestra existencias y estados, y el sistema dispone de carga y sincronización diaria de stock. El reporte valorizado calcula `stock actual × costo unitario`; muestra estado (OK, REPONER o AGOTADO), valor y margen unitario/precio. El detalle disponible permite identificar artículos por reponer.

### Compras y proveedores

El módulo registra proveedores identificados por RUC y órdenes con detalle de productos, cantidades y costo unitario. Una compra completada incrementa el stock de los productos incluidos. Se puede consultar el listado, el total y la relación entre proveedor y compras. La validación del proveedor y de los campos se realiza en frontend y/o backend según cada operación.

### Ventas y clientes

La venta relaciona cliente, comprobante, condición de pago y líneas de producto. El flujo usa el stock disponible y, al completar la venta, descuenta las cantidades correspondientes. El reporte distingue contado y crédito. El backend calcula subtotal, IGV y total conforme a la lógica implementada. La interfaz contiene rutas de listado, nueva venta, cotizaciones y ventas a crédito; que compartan pantalla no significa que cada subruta disponga de flujos de cotización o cobranza completos: revisar el alcance antes de afirmarlo en una exposición.

### Reportes

Cada submódulo presenta ahora indicadores, tablas y acciones enfocadas a su propósito:

| Vista | Contenido y uso |
|---|---|
| Dashboard ejecutivo (`/reports`) | Ventas del día y del mes, compras del mes, valor de inventario, productos más vendidos y productos con alerta de stock. |
| Ventas por período (`/reports/sales`) | Fechas desde/hasta, número de operaciones, total vendido, contado/crédito y detalle por comprobante, cliente, utilidad y margen. Exportación CSV. |
| Inventario valorizado (`/reports/inventory`) | Cantidad de productos, valor al costo, productos por reponer/agotados, stock, estado, margen y valor de cada artículo. Exportación CSV. |
| Rentabilidad (`/reports/profitability`) | Filtra período de ventas y muestra ingresos, costo de ventas, utilidad bruta y margen promedio; incluye productos con mayor margen unitario y ventas del período. |

Las fechas se envían a la API como `fecha_inicio` y `fecha_fin` (YYYY-MM-DD). Ventas usa el endpoint `/reports/sales`; inventario usa `/reports/inventory`; el dashboard usa `/reports/dashboard`. El backend calcula los indicadores y retorna detalles. La vista de rentabilidad combina los reportes de ventas e inventario disponibles; el margen de producto que muestra es margen unitario de catálogo, no utilidad histórica agregada por producto vendido. Las tablas CSV corresponden a los reportes de ventas e inventario.

## 4. Reglas de negocio principales

- Una venta completada reduce el stock; una compra completada lo aumenta.
- Las operaciones usan productos del catálogo compartido, de modo que inventario y operación comercial se mantienen relacionados.
- La API reporta ventas y compras completadas y acepta fechas para filtrar los movimientos comerciales.
- Los precios y costos se manejan en soles (PEN); el reporte de ventas usa los campos de subtotal, IGV y total guardados por la operación.
- El valor del inventario es una valorización al costo actual. No representa necesariamente un valor de liquidación o precio de venta.
- El margen de catálogo se obtiene comparando precio de venta y costo unitario. La utilidad bruta de ventas se calcula en el servicio de reportes con los datos de costo disponibles.
- El CSV es el almacenamiento principal: las copias de seguridad de `backend/data` son importantes y la concurrencia/consistencia no tiene las garantías de una base de datos transaccional.

## 5. API y seguridad

Rutas principales bajo `/api/v1`:

| Recurso | Prefijo |
|---|---|
| Autenticación | `/auth` |
| Categorías y productos | `/categories`, `/products` |
| Proveedores y compras | `/suppliers`, `/purchases` |
| Clientes y ventas | `/customers`, `/sales` |
| Reportes | `/reports` |
| Carga de datos | `/upload` |

Los endpoints de reportes incluyen dashboard, inventario, ventas, compras, movimientos por producto y auditoría. El servicio JWT usa expiración configurable y el backend incluye validación de usuario activo y dependencias para restringir roles. Los endpoints de inventario/ventas/compras/auditoría aplican permisos según su definición. La restricción de rutas React por rol debe comprobarse módulo por módulo: `ProtectedRoute` exige inicio de sesión y sólo restringe por permiso cuando se le pasa explícitamente; no se debe asumir que la navegación por sí sola protege datos. La autorización efectiva debe residir en el backend.

## 6. Recorrido sugerido para la demostración

1. Iniciar sesión y explicar el rol del usuario.
2. Mostrar un producto y su stock en Inventario.
3. Registrar una compra de prueba y comprobar el aumento de existencias.
4. Registrar una venta de prueba y comprobar la disminución del stock y el comprobante.
5. Abrir Reportes → Ventas por período, elegir fechas y descargar CSV.
6. Abrir Inventario valorizado y localizar productos por reponer/agotados.
7. Abrir Rentabilidad y explicar ingresos menos costo de ventas, además del margen promedio.
8. Volver al Dashboard ejecutivo para resumir el estado del negocio.

Utilizar datos de demostración y revisar los CSV antes de la exposición. Evitar registrar operaciones reales si sólo se busca mostrar el flujo.

## 7. Instalación y ejecución local

### Backend

Desde `backend` y con el entorno virtual del proyecto activado:

```powershell
python run.py
```

La API se sirve en `http://localhost:8000`. Swagger: `http://localhost:8000/api/docs`.

### Frontend

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite muestra la dirección local en consola (comúnmente `http://localhost:5173`). El proxy/API se configura en `frontend/vite.config.js` y `frontend/src/config/api.js`.

## 8. Estructura del código

```text
backend/app/api/v1/endpoints/  endpoints HTTP por módulo
backend/app/services/          reglas y cálculos de negocio
backend/app/repositories/      persistencia y consultas CSV
backend/app/schemas/           validación/modelos de entrada y salida
backend/app/security/          JWT, contraseñas, permisos
backend/data/                  archivos de datos CSV
frontend/src/pages/            páginas funcionales
frontend/src/components/       layout y componentes reutilizables
frontend/src/api/              servicios Axios por módulo
frontend/src/context/          estado de autenticación
frontend/src/routes/           protección de navegación
```

## 9. Guion breve para explicar el sistema

> “Este proyecto es un ERP web para una ferretería. La interfaz se desarrolló con React y se comunica con una API FastAPI mediante solicitudes HTTP protegidas con JWT. El backend organiza la lógica por módulos y guarda la información en archivos CSV compartidos. Esto conecta compras y ventas con el inventario: las compras suman existencias y las ventas las descuentan. Los roles separan el acceso de administración, ventas y almacén. Finalmente, el módulo de reportes transforma las operaciones registradas en indicadores de ventas, existencias y rentabilidad, con filtros por período y exportación CSV para ventas e inventario.”

## 10. Limitaciones y oportunidades de mejora

- Migrar almacenamiento CSV a PostgreSQL u otra base transaccional si se necesita operación concurrente, integridad referencial y crecimiento.
- Revisar y completar auditoría de cambios para asegurar registro uniforme de usuario, fecha y acción.
- Incorporar pruebas automatizadas de negocio y permisos.
- Añadir exportación de rentabilidad, gráficos históricos y comparativa entre períodos.
- Completar o delimitar claramente cotizaciones, cuentas por cobrar/pagar y pagos; no asumir que las rutas existentes equivalen a procesos completos.
- Revisar configuración de secretos, CORS, copias de seguridad y credenciales antes de desplegar públicamente.

---

Documento preparado como guía de exposición y descripción del comportamiento observado en el repositorio. Conviene acompañar la presentación con una demostración en vivo y datos de muestra.
