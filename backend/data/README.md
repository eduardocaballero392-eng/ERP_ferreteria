# Directorio de Datos CSV

Este directorio contiene todos los archivos CSV que el sistema ERP utiliza para almacenar datos.

## Archivos CSV Principales

### 1. usuarios.csv
Usuarios del sistema con sus roles y credenciales

**Columnas:**
- id, email, nombre, apellido, password_hash, role, activo, created_at, updated_at

### 2. categorias.csv
Categorías de productos de ferretería

**Columnas:**
- id, nombre, descripcion, activo, created_at, updated_at

### 3. productos.csv
Catálogo de productos

**Columnas:**
- id, sku, nombre, descripcion, categoria_id, stock_actual, stock_minimo, unidad_medida, costo_unitario, precio_venta, activo, created_at, updated_at

### 4. proveedores.csv
Proveedores de la ferretería

**Columnas:**
- id, ruc, razon_social, nombre_comercial, telefono, email, direccion, contacto_nombre, contacto_telefono, activo, created_at, updated_at

### 5. clientes.csv
Clientes de la ferretería

**Columnas:**
- id, tipo_documento, numero_documento, nombre, apellido, razon_social, telefono, email, direccion, limite_credito, saldo_por_cobrar, activo, created_at, updated_at

### 6. compras.csv
Órdenes de compra

**Columnas:**
- id, numero_orden, proveedor_id, fecha, subtotal, igv, total, observaciones, estado, created_at, updated_at

### 7. detalle_compras.csv
Detalle de las compras (items)

**Columnas:**
- id, compra_id, producto_id, cantidad, costo_unitario, subtotal, created_at

### 8. ventas.csv
Ventas/Comprobantes

**Columnas:**
- id, numero_comprobante, tipo_comprobante, cliente_id, usuario_id, fecha, subtotal, igv, total, condicion, estado, observaciones, created_at, updated_at

### 9. detalle_ventas.csv
Detalle de las ventas (items)

**Columnas:**
- id, venta_id, producto_id, cantidad, precio_unitario, subtotal, costo_unitario, created_at

### 10. pagos.csv
Pagos de clientes

**Columnas:**
- id, numero_recibo, cliente_id, fecha, monto, metodo_pago, referencia, observaciones, created_at, updated_at

### 11. movimientos_inventario.csv
Historial de movimientos de inventario

**Columnas:**
- id, producto_id, tipo_movimiento, cantidad, stock_anterior, stock_nuevo, referencia_tipo, referencia_id, referencia_numero, descripcion, fecha, created_at

### 12. auditoria.csv
Registro de auditoría de operaciones

**Columnas:**
- id, usuario_id, operacion, entidad, entidad_id, descripcion, ip_address, fecha, created_at

## Instrucciones

1. **Cargar tus propios datos**: Puedes colocar tus archivos CSV existentes en este directorio
2. **Formato**: Asegúrate de que los nombres de las columnas coincidan con los especificados arriba
3. **Codificación**: Los archivos deben estar en UTF-8
4. **Separador**: Usar coma (,) como separador
5. **Fechas**: Formato ISO 8601 (YYYY-MM-DD HH:MM:SS)

## Ejemplos de Datos

Si no tienes archivos CSV, el sistema puede generar ejemplos automáticamente o puedes crearlos manualmente siguiendo las plantillas.

## Respaldo

Se recomienda hacer respaldos periódicos de estos archivos CSV:
```bash
# Windows
xcopy data data_backup /E /I /Y

# Linux/Mac
cp -r data data_backup
```
