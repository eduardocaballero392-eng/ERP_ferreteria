# API del ERP Ferretería

Backend FastAPI para inventario, ventas, clientes, compras y reportes.

## Iniciar en desarrollo

Desde la carpeta `backend`, activa el entorno Python del proyecto e inicia:

```powershell
..\.venv\Scripts\Activate.ps1
python run.py
```

La API queda en `http://localhost:8000`; la documentación está en `/api/docs` y el estado en `/health`.

Al arrancar se crea la cuenta inicial `admin` / `admin123` si todavía no existe. Cambia esa contraseña después del primer acceso.

## Persistencia compartida

Los CSV de `backend/data/` son el almacenamiento principal y compartido de todos los módulos. La API lee y escribe directamente en `productos.csv`, `categorias.csv`, `clientes.csv`, `proveedores.csv`, `ventas.csv`, `detalle_ventas.csv`, `compras.csv`, `detalle_compras.csv`, `usuarios.csv`, `pagos.csv`, `movimientos_inventario.csv` y `auditoria.csv`.

Las compras y ventas actualizan el inventario del mismo `productos.csv`. Haz copias de seguridad de toda la carpeta `backend/data` antes de reemplazar o editar archivos. Para el CSV diario de existencias, usa **Inventario → Sincronizar stock del día**.
