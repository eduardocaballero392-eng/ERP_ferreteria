# Módulo de Ventas - Documentación

## Descripción General

El módulo de ventas permite gestionar clientes y ventas, con **actualización automática del inventario** al registrar ventas (resta stock), cálculo automático de IGV, y control de límite de crédito.

## Características

### Clientes
- ✅ CRUD completo (Crear, Leer, Actualizar, Eliminar)
- ✅ Soporte para DNI (8 dígitos) y RUC (11 dígitos)
- ✅ Búsqueda por nombres, apellidos, razón social o documento
- ✅ Límite de crédito configurable
- ✅ Estadísticas de compras por cliente
- ✅ Cálculo de saldo pendiente y crédito disponible
- ✅ Protección: no se puede eliminar si tiene ventas registradas

### Ventas
- ✅ Creación de comprobantes (BOLETA/FACTURA) con múltiples items
- ✅ Generación automática de número de comprobante (B/FYYYY-######)
- ✅ Cálculo automático de IGV (18%)
- ✅ **Actualización automática de stock** (resta cantidades)
- ✅ Validación de stock disponible antes de vender
- ✅ Condiciones de pago: CONTADO / CRÉDITO
- ✅ Validación de límite de crédito en ventas a crédito
- ✅ Historial de ventas con detalles
- ✅ Estadísticas generales de ventas
- ✅ Anulación de ventas (sin revertir stock automáticamente)

## Endpoints de la API

### Clientes

#### Listar clientes
```http
GET /api/v1/customers
```

**Query params:**
- `include_inactive` (bool, opcional): Incluir clientes inactivos

**Respuesta:**
```json
[
  {
    "id": 1,
    "tipo_documento": "DNI",
    "numero_documento": "45678912",
    "nombres": "Carlos",
    "apellidos": "Mendoza García",
    "razon_social": null,
    "nombre_comercial": null,
    "telefono": "987654321",
    "email": "carlos.mendoza@email.com",
    "direccion": "Av. Los Pinos 456, San Miguel",
    "limite_credito": 5000.00,
    "activo": true,
    "created_at": "2026-08-10 09:00:00",
    "updated_at": "2026-08-10 09:00:00"
  }
]
```

#### Clientes con estadísticas
```http
GET /api/v1/customers/with-stats
```

**Requiere rol:** admin o vendedor

**Respuesta:**
```json
[
  {
    "id": 1,
    "tipo_documento": "DNI",
    "numero_documento": "45678912",
    "nombres": "Carlos",
    "apellidos": "Mendoza García",
    "limite_credito": 5000.00,
    "total_compras": 8,
    "monto_total_compras": 3450.50,
    "saldo_pendiente": 1200.00,
    "disponible_credito": 3800.00
  }
]
```

#### Buscar clientes
```http
GET /api/v1/customers/search?query=Carlos
```

**Respuesta:** Lista de clientes que coinciden con la búsqueda

#### Obtener cliente por ID
```http
GET /api/v1/customers/{id}
```

#### Crear cliente
```http
POST /api/v1/customers
```

**Requiere rol:** admin o vendedor

**Body:**
```json
{
  "tipo_documento": "DNI",
  "numero_documento": "45678912",
  "nombres": "Carlos",
  "apellidos": "Mendoza García",
  "telefono": "987654321",
  "email": "carlos.mendoza@email.com",
  "direccion": "Av. Los Pinos 456, San Miguel",
  "limite_credito": 5000.00
}
```

#### Actualizar cliente
```http
PUT /api/v1/customers/{id}
```

**Requiere rol:** admin o vendedor

**Body:** Campos a actualizar (todos opcionales)

#### Eliminar cliente
```http
DELETE /api/v1/customers/{id}
```

**Requiere rol:** admin

**Nota:** No se puede eliminar si tiene ventas registradas

---

### Ventas

#### Listar ventas
```http
GET /api/v1/sales
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "numero_comprobante": "B2026-000001",
    "cliente_id": 1,
    "cliente_nombre": "Carlos Mendoza García",
    "cliente_documento": "45678912",
    "tipo_comprobante": "BOLETA",
    "condicion_pago": "CONTADO",
    "fecha": "2026-10-25 14:30:00",
    "subtotal": 850.00,
    "igv": 153.00,
    "total": 1003.00,
    "observaciones": "Venta de materiales de construcción",
    "estado": "COMPLETADA",
    "created_at": "2026-10-25 14:30:00"
  }
]
```

#### Estadísticas de ventas
```http
GET /api/v1/sales/stats
```

**Requiere rol:** admin o vendedor

**Respuesta:**
```json
{
  "total_ventas": 13,
  "total_vendido": 18750.50,
  "venta_promedio": 1442.35,
  "cliente_principal": "Carlos Mendoza García",
  "ventas_contado": 8,
  "ventas_credito": 5,
  "monto_contado": 12300.50,
  "monto_credito": 6450.00
}
```

#### Obtener venta con detalles
```http
GET /api/v1/sales/{id}
```

**Respuesta:**
```json
{
  "id": 1,
  "numero_comprobante": "B2026-000001",
  "cliente_id": 1,
  "cliente_nombre": "Carlos Mendoza García",
  "cliente_documento": "45678912",
  "tipo_comprobante": "BOLETA",
  "condicion_pago": "CONTADO",
  "fecha": "2026-10-25 14:30:00",
  "subtotal": 850.00,
  "igv": 153.00,
  "total": 1003.00,
  "observaciones": "Venta de materiales",
  "estado": "COMPLETADA",
  "detalles": [
    {
      "id": 1,
      "venta_id": 1,
      "producto_id": 1,
      "producto_nombre": "Cemento Andino Tipo I x 42.5 kg",
      "producto_sku": "CEM-001",
      "cantidad": 20,
      "precio_unitario": 28.00,
      "subtotal": 560.00,
      "created_at": "2026-10-25 14:30:00"
    }
  ]
}
```

#### Crear venta
```http
POST /api/v1/sales
```

**Requiere rol:** admin o vendedor

**⚠️ IMPORTANTE:** Esta operación:
- **Actualiza el stock automáticamente** (resta las cantidades vendidas)
- Valida que haya stock disponible antes de procesar
- Valida límite de crédito si la venta es a crédito
- Genera número de comprobante automático
- Calcula IGV automáticamente

**Body:**
```json
{
  "cliente_id": 1,
  "tipo_comprobante": "BOLETA",
  "condicion_pago": "CONTADO",
  "fecha": "2026-10-31 15:00:00",
  "observaciones": "Venta de materiales de construcción",
  "detalles": [
    {
      "producto_id": 1,
      "cantidad": 10,
      "precio_unitario": 28.00
    },
    {
      "producto_id": 2,
      "cantidad": 20,
      "precio_unitario": 45.00
    }
  ]
}
```

**Proceso automático:**
1. Valida cliente existe
2. Valida tipo de comprobante (BOLETA/FACTURA)
3. Valida condición de pago (CONTADO/CREDITO)
4. Si es CREDITO, valida límite de crédito disponible
5. Valida que todos los productos existen
6. **Valida que hay stock suficiente** para cada producto
7. Calcula subtotales de cada item
8. Calcula IGV (18%)
9. Calcula total
10. Genera número de comprobante automático (B/FYYYY-######)
11. Crea la venta
12. Crea los detalles
13. **RESTA el stock de cada producto automáticamente**

**Respuesta:** Venta creada con detalles completos

#### Actualizar venta
```http
PUT /api/v1/sales/{id}
```

**Requiere rol:** admin o vendedor

**Body:**
```json
{
  "observaciones": "Nueva observación",
  "estado": "ANULADA"
}
```

**Nota:** Solo se pueden actualizar observaciones y estado. No se pueden modificar los items después de crear la venta.

#### Anular venta
```http
DELETE /api/v1/sales/{id}
```

**Requiere rol:** admin

**⚠️ IMPORTANTE:** 
- Cambia el estado a "ANULADA"
- **NO revierte el stock automáticamente** (por seguridad)
- Si necesita ajustar stock, debe hacerse manualmente usando el endpoint de ajuste de inventario

---

## Reglas de Negocio

### Clientes
1. **Documento único:** No puede haber dos clientes con el mismo número de documento
2. **Validación de documento:** 
   - DNI: 8 dígitos, válido según algoritmo
   - RUC: 11 dígitos, válido según algoritmo
3. **Tipos de cliente:**
   - Persona natural: usa DNI, nombres y apellidos
   - Empresa: usa RUC, razón social
4. **Límite de crédito:** Monto máximo que el cliente puede deber
5. **Eliminación protegida:** No se puede eliminar un cliente que tenga ventas registradas

### Ventas
1. **Tipos de comprobante:**
   - **BOLETA:** Para personas naturales (DNI)
   - **FACTURA:** Para empresas (RUC)
2. **Número de comprobante automático:**
   - Formato: B/FYYYY-######
   - B = Boleta, F = Factura
   - YYYY = Año
   - ###### = Correlativo (6 dígitos)
3. **IGV:** Siempre 18%, se calcula automáticamente sobre el subtotal
4. **Stock automático:** Al crear una venta, el stock de los productos se decrementa (RESTA)
5. **Validación de stock:** No se puede vender más de lo disponible
6. **Condiciones de pago:**
   - **CONTADO:** Pago inmediato, sin validación de crédito
   - **CREDITO:** Pago diferido, se valida límite de crédito
7. **Límite de crédito:**
   ```
   disponible = limite_credito - saldo_pendiente
   ```
   No se puede crear una venta a crédito si excede el disponible
8. **Anulación:** Al anular una venta, el stock NO se revierte automáticamente
9. **Items mínimos:** Una venta debe tener al menos 1 item
10. **Validaciones:** 
   - El cliente debe existir y estar activo
   - Los productos deben existir
   - Las cantidades deben ser mayores a 0
   - Los precios deben ser mayores a 0

### Actualización de Stock

**Al crear venta:**
```
nuevo_stock = stock_actual - cantidad_vendida
```

**Al anular venta:**
- El stock NO se revierte automáticamente
- Se debe ajustar manualmente si es necesario
- Usar: `POST /api/v1/products/{id}/adjust-stock`

**Motivo:** Seguridad y trazabilidad. La reversión automática puede causar inconsistencias si:
- Ya se reabastecieron esos productos
- Se hicieron ajustes manuales posteriores
- Hay discrepancias físicas en el almacén
- La mercadería fue devuelta parcialmente

---

## Control de Acceso (Roles)

| Acción | admin | vendedor | almacenero |
|--------|-------|----------|------------|
| Ver clientes | ✅ | ✅ | ❌ |
| Crear/editar clientes | ✅ | ✅ | ❌ |
| Eliminar clientes | ✅ | ❌ | ❌ |
| Ver ventas | ✅ | ✅ | ❌ |
| Crear ventas | ✅ | ✅ | ❌ |
| Anular ventas | ✅ | ❌ | ❌ |
| Ver estadísticas | ✅ | ✅ | ❌ |

---

## Ejemplos de Uso

### Ejemplo 1: Crear un cliente persona natural

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login/form \
  -d "username=vendedor@ferreteria.com" \
  -d "password=ven123"

# Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}

# 2. Crear cliente
curl -X POST http://localhost:8000/api/v1/customers \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_documento": "DNI",
    "numero_documento": "45678912",
    "nombres": "Carlos",
    "apellidos": "Mendoza García",
    "telefono": "987654321",
    "email": "carlos.mendoza@email.com",
    "limite_credito": 5000.00
  }'
```

### Ejemplo 2: Crear una venta al contado

```bash
# Crear venta (actualiza stock automáticamente)
curl -X POST http://localhost:8000/api/v1/sales \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "tipo_comprobante": "BOLETA",
    "condicion_pago": "CONTADO",
    "observaciones": "Venta de cemento",
    "detalles": [
      {
        "producto_id": 1,
        "cantidad": 10,
        "precio_unitario": 28.00
      }
    ]
  }'

# Response:
{
  "id": 14,
  "numero_comprobante": "B2026-000014",
  "tipo_comprobante": "BOLETA",
  "condicion_pago": "CONTADO",
  "subtotal": 280.00,
  "igv": 50.40,
  "total": 330.40,
  "detalles": [...]
}
```

### Ejemplo 3: Crear una venta a crédito

```bash
# Crear venta a crédito (valida límite de crédito)
curl -X POST http://localhost:8000/api/v1/sales \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "tipo_comprobante": "FACTURA",
    "condicion_pago": "CREDITO",
    "observaciones": "Venta a crédito 30 días",
    "detalles": [
      {
        "producto_id": 1,
        "cantidad": 50,
        "precio_unitario": 28.00
      }
    ]
  }'

# Si excede el límite, responde con error 400:
{
  "detail": "Crédito insuficiente. Disponible: S/ 3800.00, Requerido: S/ 1650.00"
}
```

### Ejemplo 4: Verificar stock actualizado

```bash
# Ver producto después de la venta
curl -X GET http://localhost:8000/api/v1/products/1 \
  -H "Authorization: Bearer eyJ..."

# Response:
{
  "id": 1,
  "nombre": "Cemento Andino Tipo I x 42.5 kg",
  "stock_actual": 140,  # <- Se decrementó en 10
  "estado_stock": "OK"
}
```

---

## Flujo de Venta Típico

```
1. Cliente llega a la ferretería
   ↓
2. Vendedor busca/crea cliente
   ↓
3. Vendedor agrega productos al carrito
   ↓
4. Sistema valida stock disponible
   ↓
5. Si es a crédito: valida límite de crédito
   ↓
6. Sistema calcula IGV y total
   ↓
7. Sistema genera número de comprobante
   ↓
8. Sistema crea la venta
   ↓
9. Sistema RESTA stock automáticamente ⚡
   ↓
10. Cliente recibe comprobante
```

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
py test_sales.py
```

### Acceder a Swagger UI
```
http://localhost:8000/api/docs
```

---

## Datos de Ejemplo

El sistema incluye 15 clientes reales con datos de ferreterías peruanas:

**Personas Naturales (DNI):**
1. Carlos Mendoza García - DNI: 45678912
2. María Torres Quispe - DNI: 78945612
3. José Ramírez Flores - DNI: 12345678
4. Ana Díaz Paredes - DNI: 98765432
5. Luis Castro Vega - DNI: 55667788

**Empresas (RUC):**
6. Constructora Los Pinos SAC - RUC: 20456789123
7. Inversiones García EIRL - RUC: 10789456123
8. Ferretería San Martín SRL - RUC: 20123456789
9. Distribuidora Lima SAC - RUC: 20987654321
10. Construcciones del Norte SA - RUC: 20445566778

Y 13 ventas de ejemplo que cubren diferentes escenarios (contado/crédito, boletas/facturas).

---

## Arquitectura

```
Endpoints (API REST)
    ↓
Services (Lógica de negocio)
    ↓
Repositories (Acceso a datos CSV)
    ↓
CSV Files (Persistencia)
```

### Archivos involucrados

**Schemas:**
- `app/schemas/customer.py` - Validación de clientes
- `app/schemas/sale.py` - Validación de ventas

**Repositories:**
- `app/repositories/customer_repository.py` - CRUD clientes
- `app/repositories/sale_repository.py` - CRUD ventas

**Services:**
- `app/services/customer_service.py` - Lógica de clientes
- `app/services/sale_service.py` - Lógica de ventas + actualización de stock

**Endpoints:**
- `app/api/v1/endpoints/customers.py` - API clientes
- `app/api/v1/endpoints/sales.py` - API ventas

**CSV:**
- `data/clientes.csv` - Datos de clientes
- `data/ventas.csv` - Comprobantes de venta
- `data/detalle_ventas.csv` - Items de cada venta

---

## Próximos Pasos

**FASE 7: Módulo de Pagos y Cuentas por Cobrar**
- Registro de pagos de ventas a crédito
- Seguimiento de saldo por cobrar
- Alertas de pagos vencidos
- Historial de pagos por cliente

**FASE 8: Reportes y Auditoría**
- Reporte de utilidad bruta
- Movimientos de inventario
- Logs de auditoría
- Dashboard con indicadores

---

## Soporte

Para más información:
- Ver documentación en Swagger: http://localhost:8000/api/docs
- Revisar `backend/README.md`
- Consultar `REGLAS_NEGOCIO.md`
- Ver `MODULO_COMPRAS.md` para el flujo inverso (compras)
