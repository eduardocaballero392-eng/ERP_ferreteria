# Módulo de Reportes y Auditoría - Documentación

## Descripción General

El módulo de reportes proporciona análisis detallados del negocio, incluyendo utilidad bruta, valorización de inventario, movimientos de productos y logs de auditoría.

## Características

### Dashboard
- ✅ Estadísticas en tiempo real
- ✅ Ventas del día y del mes
- ✅ Compras del mes
- ✅ Estado del inventario
- ✅ Utilidad bruta y margen promedio
- ✅ Top 5 productos más vendidos
- ✅ Top 5 clientes principales
- ✅ Top 5 proveedores principales

### Reporte de Inventario
- ✅ Valor total del inventario
- ✅ Productos por estado (OK/REPONER/AGOTADO)
- ✅ Detalle por producto con márgenes
- ✅ Valorización a costo

### Reporte de Ventas
- ✅ **Utilidad bruta por venta**
- ✅ **Margen de utilidad promedio**
- ✅ Total vendido vs costo
- ✅ Desglose por condición de pago
- ✅ Filtros por rango de fechas

### Reporte de Compras
- ✅ Total gastado en el período
- ✅ Compra promedio
- ✅ Detalle por proveedor
- ✅ Filtros por rango de fechas

### Movimientos de Inventario
- ✅ Entradas (compras)
- ✅ Salidas (ventas)
- ✅ Stock inicial y final
- ✅ Historial de movimientos por producto
- ✅ Trazabilidad completa

### Auditoría
- ✅ Logs de todas las operaciones
- ✅ Usuario y fecha/hora
- ✅ Módulo afectado
- ✅ Detalles de la acción

## Endpoints de la API

### Dashboard

#### Obtener estadísticas del dashboard
```http
GET /api/v1/reports/dashboard
```

**Requiere rol:** admin

**Respuesta:**
```json
{
  "ventas_hoy": 3,
  "ventas_mes": 13,
  "total_vendido_mes": 18750.50,
  "compras_mes": 8,
  "total_gastado_mes": 15750.50,
  "productos_total": 53,
  "productos_stock_bajo": 5,
  "valor_inventario": 125000.00,
  "utilidad_bruta_mes": 3250.75,
  "margen_promedio_mes": 17.34,
  "top_productos": [
    {
      "producto_id": 1,
      "nombre": "Cemento Andino Tipo I x 42.5 kg",
      "sku": "CEM-001",
      "cantidad_vendida": 150,
      "monto_total": 4200.00
    }
  ],
  "top_clientes": [
    {
      "cliente_id": 1,
      "nombre": "Carlos Mendoza García",
      "documento": "45678912",
      "total_compras": 8,
      "monto_total": 3450.50
    }
  ],
  "top_proveedores": [
    {
      "proveedor_id": 1,
      "razon_social": "Distribuidora Andina SAC",
      "ruc": "20518520442",
      "total_compras": 5,
      "monto_total": 12500.00
    }
  ]
}
```

---

### Reporte de Inventario

#### Generar reporte de inventario
```http
GET /api/v1/reports/inventory
```

**Requiere rol:** admin o almacenero

**Respuesta:**
```json
{
  "total_productos": 53,
  "valor_total_inventario": 125000.00,
  "productos_ok": 40,
  "productos_reponer": 8,
  "productos_agotados": 5,
  "items": [
    {
      "producto_id": 1,
      "sku": "CEM-001",
      "nombre": "Cemento Andino Tipo I x 42.5 kg",
      "categoria": "Cemento",
      "stock_actual": 150,
      "stock_minimo": 50,
      "estado_stock": "OK",
      "costo_unitario": 22.50,
      "precio_venta": 28.00,
      "valor_inventario": 3375.00,
      "margen_unitario": 5.50,
      "margen_porcentaje": 19.64
    }
  ]
}
```

---

### Reporte de Ventas

#### Generar reporte de ventas con utilidad
```http
GET /api/v1/reports/sales?fecha_inicio=2026-10-01&fecha_fin=2026-10-31
```

**Requiere rol:** admin o vendedor

**Query params:**
- `fecha_inicio` (opcional): Fecha inicio (YYYY-MM-DD). Por defecto: inicio del mes actual
- `fecha_fin` (opcional): Fecha fin (YYYY-MM-DD). Por defecto: hoy

**Respuesta:**
```json
{
  "fecha_inicio": "2026-10-01",
  "fecha_fin": "2026-10-31",
  "total_ventas": 13,
  "total_vendido": 18750.50,
  "total_costo": 15500.00,
  "utilidad_bruta": 3250.50,
  "margen_promedio": 17.34,
  "ventas_contado": 8,
  "ventas_credito": 5,
  "monto_contado": 12300.50,
  "monto_credito": 6450.00,
  "items": [
    {
      "venta_id": 1,
      "numero_comprobante": "B2026-000001",
      "fecha": "2026-10-25 14:30:00",
      "cliente_nombre": "Carlos Mendoza García",
      "tipo_comprobante": "BOLETA",
      "condicion_pago": "CONTADO",
      "subtotal": 850.00,
      "igv": 153.00,
      "total": 1003.00,
      "utilidad_bruta": 187.50,
      "margen_porcentaje": 18.69
    }
  ]
}
```

**Cálculo de Utilidad Bruta:**
```
utilidad_bruta = total_venta - (costo_productos * 1.18)
margen_porcentaje = (utilidad_bruta / total_venta) * 100
```

---

### Reporte de Compras

#### Generar reporte de compras
```http
GET /api/v1/reports/purchases?fecha_inicio=2026-10-01&fecha_fin=2026-10-31
```

**Requiere rol:** admin o almacenero

**Query params:**
- `fecha_inicio` (opcional): Fecha inicio (YYYY-MM-DD)
- `fecha_fin` (opcional): Fecha fin (YYYY-MM-DD)

**Respuesta:**
```json
{
  "fecha_inicio": "2026-10-01",
  "fecha_fin": "2026-10-31",
  "total_compras": 8,
  "total_gastado": 15750.50,
  "compra_promedio": 1968.81,
  "items": [
    {
      "compra_id": 1,
      "numero_orden": "OC-2026-001",
      "fecha": "2026-10-20 10:30:00",
      "proveedor_nombre": "Distribuidora Andina SAC",
      "subtotal": 2500.00,
      "igv": 450.00,
      "total": 2950.00
    }
  ]
}
```

---

### Movimientos de Inventario

#### Obtener movimientos de un producto
```http
GET /api/v1/reports/movements/1?fecha_inicio=2026-10-01&fecha_fin=2026-10-31
```

**Requiere rol:** admin o almacenero

**Path params:**
- `producto_id` (requerido): ID del producto

**Query params:**
- `fecha_inicio` (opcional): Fecha inicio
- `fecha_fin` (opcional): Fecha fin

**Respuesta:**
```json
{
  "producto_id": 1,
  "producto_nombre": "Cemento Andino Tipo I x 42.5 kg",
  "sku": "CEM-001",
  "fecha_inicio": "2026-10-01",
  "fecha_fin": "2026-10-31",
  "stock_inicial": 120,
  "total_entradas": 80,
  "total_salidas": 50,
  "stock_final": 150,
  "movimientos": [
    {
      "fecha": "2026-10-20 10:30:00",
      "tipo": "COMPRA",
      "referencia": "OC-2026-001",
      "cantidad": 50,
      "tipo_movimiento": "ENTRADA",
      "stock_anterior": 120,
      "stock_nuevo": 170,
      "motivo": null
    },
    {
      "fecha": "2026-10-25 14:30:00",
      "tipo": "VENTA",
      "referencia": "B2026-000001",
      "cantidad": 20,
      "tipo_movimiento": "SALIDA",
      "stock_anterior": 170,
      "stock_nuevo": 150,
      "motivo": null
    }
  ]
}
```

---

### Auditoría

#### Obtener logs de auditoría
```http
GET /api/v1/reports/audit?usuario=admin@ferreteria.com&modulo=ventas
```

**Requiere rol:** admin

**Query params:**
- `fecha_inicio` (opcional): Filtrar desde fecha
- `fecha_fin` (opcional): Filtrar hasta fecha
- `usuario` (opcional): Filtrar por usuario
- `modulo` (opcional): Filtrar por módulo

**Respuesta:**
```json
[
  {
    "id": 1,
    "fecha": "2026-10-31 15:30:00",
    "usuario": "vendedor@ferreteria.com",
    "accion": "CREAR_VENTA",
    "modulo": "ventas",
    "registro_id": 14,
    "detalles": "Venta B2026-000014 por S/ 1327.50",
    "ip_address": "192.168.1.100"
  }
]
```

**Nota:** Retorna los últimos 100 registros

---

## Métricas Clave

### Utilidad Bruta
```
Utilidad Bruta = Total Ventas - Costo de Ventas (con IGV)
```

Representa la ganancia antes de gastos operativos.

### Margen de Utilidad
```
Margen % = (Utilidad Bruta / Total Ventas) * 100
```

Indica el porcentaje de ganancia por cada sol vendido.

### Valor de Inventario
```
Valor = Σ (Stock Actual × Costo Unitario)
```

Capital invertido en inventario.

### Rotación de Inventario
```
Rotación = Costo de Ventas / Valor Promedio de Inventario
```

Indica cuántas veces se renueva el inventario.

---

## Control de Acceso (Roles)

| Reporte | admin | vendedor | almacenero |
|---------|-------|----------|------------|
| Dashboard | ✅ | ❌ | ❌ |
| Inventario | ✅ | ❌ | ✅ |
| Ventas | ✅ | ✅ | ❌ |
| Compras | ✅ | ❌ | ✅ |
| Movimientos | ✅ | ❌ | ✅ |
| Auditoría | ✅ | ❌ | ❌ |

---

## Casos de Uso

### Caso 1: Análisis de Rentabilidad Mensual

**Objetivo:** Saber cuánto se ganó en el mes

```bash
# Obtener reporte de ventas del mes
curl -X GET "http://localhost:8000/api/v1/reports/sales?fecha_inicio=2026-10-01&fecha_fin=2026-31" \
  -H "Authorization: Bearer {token}"

# Resultado:
# - Total vendido: S/ 18,750.50
# - Costo: S/ 15,500.00
# - Utilidad bruta: S/ 3,250.50 ✅
# - Margen: 17.34%
```

### Caso 2: Identificar Productos de Baja Rotación

**Objetivo:** Saber qué productos no se venden

```bash
# 1. Ver reporte de inventario
curl -X GET "http://localhost:8000/api/v1/reports/inventory" \
  -H "Authorization: Bearer {token}"

# 2. Filtrar productos con alto stock y poco movimiento
# 3. Para cada producto de interés, ver movimientos
curl -X GET "http://localhost:8000/api/v1/reports/movements/10" \
  -H "Authorization: Bearer {token}"
```

### Caso 3: Evaluar Desempeño de Proveedores

**Objetivo:** Saber cuánto se compra a cada proveedor

```bash
# Ver dashboard con top proveedores
curl -X GET "http://localhost:8000/api/v1/reports/dashboard" \
  -H "Authorization: Bearer {token}"

# Resultado: Top 5 proveedores con monto total
```

### Caso 4: Auditar Operación Específica

**Objetivo:** Ver quién realizó una acción

```bash
# Filtrar logs por módulo y fecha
curl -X GET "http://localhost:8000/api/v1/reports/audit?modulo=ventas&fecha_inicio=2026-10-31" \
  -H "Authorization: Bearer {token}"

# Ver quién creó, modificó o anuló ventas
```

---

## Interpretación de Reportes

### Dashboard

**Indicadores Positivos:**
- Ventas crecientes mes a mes
- Margen promedio > 15%
- Productos con stock bajo < 10%
- Utilidad bruta positiva

**Indicadores de Alerta:**
- Ventas a crédito > 40% del total
- Productos agotados > 5%
- Margen promedio < 10%
- Stock bajo en productos top

### Reporte de Ventas

**Análisis:**
- Productos con bajo margen: revisar precio o costo
- Clientes con alto volumen: ofrecer descuentos por volumen
- Ventas a crédito altas: revisar políticas de crédito

### Reporte de Inventario

**Análisis:**
- Valor muy alto: posible sobre-stock
- Productos REPONER: planificar compra
- Márgenes bajos: revisar precios

---

## Pruebas

### Ejecutar servidor
```bash
cd backend
.\venv\Scripts\Activate.ps1
py run.py
```

### Ejecutar script de pruebas
```bash
py test_reports.py
```

### Acceder a Swagger UI
```
http://localhost:8000/api/docs
```

---

## Próximas Mejoras

**Reportes Adicionales:**
- [ ] Reporte de cuentas por cobrar
- [ ] Reporte de productos más rentables
- [ ] Proyección de ventas
- [ ] Análisis ABC de inventario

**Exportación:**
- [ ] Exportar a Excel
- [ ] Exportar a PDF
- [ ] Envío por email

**Visualizaciones:**
- [ ] Gráficos de tendencias
- [ ] Comparativas período anterior
- [ ] Dashboard interactivo

---

## Arquitectura

```
Endpoints (API REST)
    ↓
Services (Lógica de cálculo)
    ↓
Repositories (Acceso a datos)
    ↓
CSV Files (Persistencia)
```

### Archivos involucrados

**Schemas:**
- `app/schemas/report.py` - Modelos de reportes

**Services:**
- `app/services/report_service.py` - Lógica de reportes y auditoría

**Endpoints:**
- `app/api/v1/endpoints/reports.py` - API de reportes

**CSV:**
- `data/auditoria.csv` - Logs de auditoría
- Usa datos de otros CSVs para generar reportes

---

## Soporte

Para más información:
- Ver documentación en Swagger: http://localhost:8000/api/docs
- Revisar `backend/README.md`
- Consultar `REGLAS_NEGOCIO.md`
