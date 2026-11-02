# ERP Ferretería

Sistema web para gestionar inventario, compras, ventas, clientes, proveedores y reportes. Los módulos comparten el catálogo y las existencias: una compra suma stock, una venta lo descuenta y el dashboard refleja los datos del sistema.

## Inicio local

Requisitos: Python 3.10 o superior y Node.js 18 o superior.

Instala dependencias del backend desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

En una terminal inicia la API:

```powershell
cd backend
..\.venv\Scripts\python.exe run.py
```

En otra terminal instala e inicia el frontend:

```powershell
cd frontend
npm ci
npm run dev
```

Frontend: `http://localhost:3000`

API: `http://localhost:8000`

Documentación: `http://localhost:8000/api/docs`

Si `backend/data/usuarios.csv` no tiene usuarios activos, al iniciar se crea la cuenta `admin` con contraseña `admin123`. Cambia esa contraseña después del primer acceso.

## Datos y módulos

Los archivos CSV de `backend/data/` son la fuente de datos compartida del sistema. La API los lee y escribe directamente: productos, categorías, clientes, proveedores, ventas, compras, usuarios y sus detalles. No se necesita una base de datos local.

- **Dashboard:** ventas, compras, alertas y accesos rápidos.
- **Inventario:** catálogo, categorías, filtros, ajustes y sincronización del stock.
- **Ventas:** registra comprobantes con clientes y productos disponibles.
- **Compras:** selecciona proveedor y productos; al confirmarla, incrementa sus existencias.
- **Clientes y proveedores:** datos relacionados con las transacciones y sus reportes.
- **Reportes:** resume ventas, compras y valorización de inventario.

### Sincronizar el stock diario

Abre **Inventario → Sincronizar stock del día** y carga el único CSV de existencias. El importador detecta coma, punto y coma o tabulador, y reconoce nombres habituales de columnas en español o inglés. Incluye un código o SKU —también puede relacionar por nombre— y una cantidad de stock. Los códigos se comparan con los productos del catálogo; las filas no reconocidas se muestran como errores y no crean transacciones falsas.

Los nuevos productos y categorías se registran desde Inventario. Haz copias de seguridad de `backend/data/` para conservar el catálogo y las transacciones.

## Publicar en Render y Vercel

La configuración está preparada en `render.yaml` y `frontend/vercel.json`.

1. Sube el repositorio a GitHub.
2. En Render, crea un **Blueprint** desde el repositorio usando `render.yaml`. El blueprint despliega la API y monta un disco en `/var/data` para conservar los CSV modificados entre reinicios y despliegues. El disco persistente requiere un plan de servicio de pago en Render.
3. En Vercel, importa el mismo repositorio y establece **Root Directory** en `frontend`. Vercel detectará Vite; `frontend/vercel.json` permite abrir directamente rutas internas como `/inventory`.
4. En Vercel, define `VITE_API_URL` con la URL HTTPS del servicio Render, por ejemplo `https://erp-ferreteria-api.onrender.com`, sin añadir `/api/v1`, y vuelve a desplegar.
5. En Render, cambia `ALLOWED_ORIGINS` a la URL exacta de producción de Vercel, por ejemplo `https://mi-ferreteria.vercel.app`. Separa varios dominios con comas. Guarda y redepliega la API.
6. Ingresa con el usuario inicial `admin` y contraseña `admin123`; cambia la contraseña después de entrar.

Render copia los CSV iniciales al disco persistente la primera vez. Las siguientes ejecuciones conservan los archivos existentes y no los reemplazan. No elimines el disco si necesitas mantener los datos registrados.

## Estructura

```text
backend/   API FastAPI, servicios y archivos CSV del ERP
frontend/  Aplicación React y Vite
README.md  Guía de inicio
```
