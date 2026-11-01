# Reglas de Negocio - ERP Ferretería

Este documento detalla todas las reglas de negocio implementadas en el sistema ERP para ferretería.

## 1. Gestión de Inventario

### 1.1 Control de Stock

**Cálculo de Stock Actual:**
```
Stock Actual = Stock Inicial + Total Compras - Total Ventas
```

**Estados de Stock:**

| Estado | Condición | Descripción |
|--------|-----------|-------------|
| AGOTADO | stock_actual <= 0 | Sin unidades disponibles |
| REPONER | 0 < stock_actual <= stock_minimo | Necesita reposición |
| OK | stock_actual > stock_minimo | Stock suficiente |

**Validaciones:**
- No se permite registrar ventas si el stock es insuficiente
- Se debe generar alerta automática cuando stock <= stock_minimo
- El stock nunca puede ser negativo

### 1.2 Precios

- Los precios de venta se registran **SIN IGV**
- El costo de compra se registra por unidad
- Se debe mantener historial de cambios de precio para análisis

## 2. Gestión de Compras

### 2.1 Registro de Compras

**Proceso:**
1. Se registra la orden de compra con proveedor
2. Se detallan los productos y cantidades
3. Al confirmar la compra, se actualiza el stock:
   ```
   Stock Nuevo = Stock Actual + Cantidad Comprada
   ```

**Validaciones:**
- Proveedor debe estar activo
- Cantidad debe ser mayor a 0
- Costo unitario debe ser mayor a 0
- Se debe registrar la fecha de compra

### 2.2 Proveedores

**Campos obligatorios:**
- RUC (11 dígitos)
- Razón social
- Datos de contacto

**Validación RUC:**
- Debe tener 11 dígitos
- Debe comenzar con: 10, 15, 17 o 20
- Solo caracteres numéricos

## 3. Gestión de Ventas

### 3.1 Cálculo de IGV

**IGV en Perú: 18%**

```python
subtotal = suma(precio_sin_igv * cantidad)
igv = subtotal * 0.18
total = subtotal + igv
```

**Ejemplo:**
```
Producto A: S/ 100.00 x 2 unidades = S/ 200.00
Producto B: S/ 50.00 x 1 unidad = S/ 50.00
-------------------------------------------
Subtotal:           S/ 250.00
IGV (18%):          S/  45.00
-------------------------------------------
TOTAL:              S/ 295.00
```

### 3.2 Condiciones de Pago

**Contado:**
- Pago inmediato
- No afecta el límite de crédito del cliente

**Crédito:**
- Se registra como cuenta por cobrar
- Suma al saldo por cobrar del cliente
- Se debe validar límite de crédito antes de aprobar

### 3.3 Actualización de Stock

Al registrar una venta:
```
Stock Nuevo = Stock Actual - Cantidad Vendida
```

**Validaciones:**
- Verificar stock suficiente antes de confirmar venta
- No permitir venta si stock_actual < cantidad_solicitada
- Actualizar el estado del producto según el nuevo stock

### 3.4 Cálculo de Utilidad

```python
utilidad_bruta = subtotal_venta - suma(costo_unitario * cantidad)
margen_utilidad = (utilidad_bruta / subtotal_venta) * 100
```

## 4. Gestión de Clientes

### 4.1 Límite de Crédito

**Cálculo de Saldo por Cobrar:**
```
Saldo por Cobrar = Total Ventas a Crédito (con IGV) - Total Pagos
```

**Validación de Crédito:**
```python
if saldo_por_cobrar + nueva_venta_total > limite_credito:
    generar_alerta()
    solicitar_aprobacion_especial()
```

**Reglas:**
- El límite de crédito se establece por cliente
- Se puede modificar con autorización de administrador
- Si el saldo supera el límite, se debe alertar al vendedor

### 4.2 Registro de Pagos

**Proceso:**
1. Cliente realiza pago (total o parcial)
2. Se registra el pago con fecha y método
3. Se actualiza el saldo por cobrar:
   ```
   Nuevo Saldo = Saldo Anterior - Monto Pago
   ```

**Validaciones:**
- Monto del pago > 0
- Monto del pago <= saldo por cobrar
- Registrar método de pago (efectivo, transferencia, cheque)

### 4.3 Validación de Documentos

**DNI (Personas Naturales):**
- 8 dígitos numéricos
- Ejemplo: 12345678

**RUC (Personas Jurídicas):**
- 11 dígitos numéricos
- Prefijos válidos: 10, 15, 17, 20
- Ejemplo: 20123456789

## 5. Seguridad y Acceso

### 5.1 Roles de Usuario

| Rol | Módulos Permitidos | Permisos |
|-----|-------------------|----------|
| **Admin** | Todos | Lectura, Escritura, Eliminación |
| **Vendedor** | Ventas, Clientes | Lectura, Escritura |
| **Almacenero** | Inventario, Compras | Lectura, Escritura |

### 5.2 Operaciones Críticas

**Requieren auditoría:**
- Creación/modificación de ventas
- Creación/modificación de compras
- Modificación de precios
- Ajustes de inventario
- Eliminación de registros

**Registro de auditoría incluye:**
- Usuario que realizó la operación
- Fecha y hora
- Tipo de operación
- Datos antes y después (si aplica)
- IP del usuario

## 6. Reportes

### 6.1 Indicadores Clave (KPIs)

**Ventas:**
- Total ventas del día/mes
- Ticket promedio
- Productos más vendidos
- Vendedor con más ventas

**Inventario:**
- Productos con stock bajo (REPONER)
- Productos agotados
- Valor del inventario
- Rotación de productos

**Clientes:**
- Total cuentas por cobrar
- Clientes con deuda vencida
- Clientes cerca del límite de crédito

**Rentabilidad:**
- Utilidad bruta total
- Margen de utilidad promedio
- Productos más rentables

## 7. Notificaciones y Alertas

### 7.1 Alertas Automáticas

**Stock:**
- ⚠️ Producto en estado REPONER
- 🚫 Producto AGOTADO
- 📉 Stock crítico (< 20% del stock mínimo)

**Crédito:**
- ⚠️ Cliente cerca del límite (> 80%)
- 🚫 Cliente excede límite de crédito
- 📅 Pagos vencidos (> 30 días)

**Ventas:**
- 🎯 Meta diaria alcanzada
- 📊 Venta inusual (monto muy alto)

## 8. Reglas de Validación

### 8.1 Productos

- SKU único por producto
- Nombre obligatorio (máx. 200 caracteres)
- Categoría obligatoria
- Precio de venta > 0
- Costo > 0
- Stock mínimo >= 0

### 8.2 Compras

- Fecha de compra <= fecha actual
- Cantidad > 0
- Costo unitario > 0
- Proveedor válido y activo

### 8.3 Ventas

- Fecha de venta <= fecha actual
- Al menos 1 producto en el detalle
- Cantidad > 0
- Cliente válido
- Verificar stock disponible

### 8.4 Pagos

- Monto > 0
- Monto <= saldo por cobrar
- Fecha de pago <= fecha actual
- Cliente válido

## 9. Proceso de Negocio: Venta Completa

**Flujo:**

```
1. Vendedor busca productos
   ↓
2. Verifica stock disponible
   ↓
3. Agrega productos al carrito
   ↓
4. Sistema calcula subtotal
   ↓
5. Sistema calcula IGV (18%)
   ↓
6. Sistema calcula total
   ↓
7. Selecciona cliente
   ↓
8. Selecciona condición (Contado/Crédito)
   ↓
9. Si es Crédito → Valida límite de crédito
   ↓
10. Confirma venta
    ↓
11. Sistema actualiza stock (resta)
    ↓
12. Sistema genera comprobante
    ↓
13. Si es Crédito → Actualiza saldo por cobrar
    ↓
14. Sistema registra auditoría
```

## 10. Proceso de Negocio: Compra Completa

**Flujo:**

```
1. Almacenero selecciona proveedor
   ↓
2. Agrega productos y cantidades
   ↓
3. Ingresa costos unitarios
   ↓
4. Sistema calcula total de compra
   ↓
5. Confirma orden de compra
   ↓
6. Sistema actualiza stock (suma)
   ↓
7. Sistema registra movimiento en historial
   ↓
8. Sistema registra auditoría
   ↓
9. Sistema actualiza estado de productos
```

## 11. Consideraciones Especiales

### 11.1 Manejo de Decimales

- Precios: 2 decimales
- Cantidades: enteros (no se permiten fracciones)
- IGV: 2 decimales
- Totales: 2 decimales

### 11.2 Moneda

- Todas las transacciones en Soles (PEN)
- Formato: S/ 1,234.56

### 11.3 Fechas

- Formato: DD/MM/YYYY HH:mm:ss
- Zona horaria: America/Lima (Perú)

### 11.4 Eliminación de Registros

- **Soft delete**: Los registros no se eliminan físicamente
- Se marca con campo `activo = false` o `eliminado = true`
- Preserva la integridad referencial
- Permite auditoría completa

---

**Nota**: Estas reglas deben ser implementadas en el backend (validaciones de negocio) y reforzadas en el frontend (validaciones de UI para mejor UX).

**Última actualización**: Octubre 2026  
**Versión**: 1.0
