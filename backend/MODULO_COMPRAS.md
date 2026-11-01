# Módulo de Compras - Documentación

## Descripción General

El módulo de compras permite gestionar proveedores y órdenes de compra, con **actualización automática del inventario** al registrar compras.

## Características

### Proveedores
- ✅ CRUD completo (Crear, Leer, Actualizar, Eliminar)
- ✅ Búsqueda por razón social, nombre comercial o RUC
- ✅ Validación de RUC (11 dígitos)
- ✅ Estadísticas de compras por proveedor
- ✅ Protección: no se puede eliminar si tiene compras registradas

### Compras
- ✅ Creación de órdenes de compra con múltiples items
- ✅ Generación automática de número de orden (OC-YYYY-###)
- ✅ Cálculo automático de IGV (18%)
- ✅ **Actualización automática de stock** (suma cantidades)
- ✅ Historial de compras con detalles
- ✅ Estadísticas generales de compras
- ✅ Anulación de compras (sin revertir stock automáticamente)

## Endpoints de la API

### Proveedores

#### Listar proveedores
```http
GET /api/v1/suppliers
```

**Query params:**
- `include_inactive` (bool, opcional): Incluir proveedores inactivos

**Respuesta:**
```json
[
  {
    "id": 1,
    "ruc": "20518520442",
    "razon_social": "Distribuidora Andina SAC",
    "nombre_comercial": "Dist. Andina",
    "telefono": "015551234",
    "email": "ventas@andina.com.pe",
    "direccion": "Av. Argentina 2850, Callao",
    "contacto_nombre": "Roberto Paredes",
    "contacto_telefono": "987654321",
    "activo": true,
    "created_at": "2026-09-15 09:00:00",
    "updated_at": "2026-09-15 09:00:00"
  }
]
```

#### Proveedores con estadísticas
```http
GET /api/v1/suppliers/with-stats
```

**Requiere rol:** admin o almacenero

**Respuesta:**
```json
[
  {
    "id": 1,
    "ruc": "20518520442",
    "razon_social": "Distribuidora Andina SAC",
    "total_compras": 5,
    "monto_total_compras": 12500.00
  }
]
```

#### Buscar proveedores
```http
GET /api/v1/suppliers/search?query=Andina
```

**Respuesta:** Lista de proveedores que coinciden con la búsqueda

#### Obtener proveedor por ID
```http
GET /api/v1/suppliers/{id}
```

#### Crear proveedor
```http
POST /api/v1/suppliers
```

**Requiere rol:** admin o almacenero

**Body:**
```json
{
  "ruc": "20518520442",
  "razon_social": "Distribuidora Andina SAC",
  "nombre_comercial": "Dist. Andina",
  "telefono": "015551234",
  "email": "ventas@andina.com.pe",
  "direccion": "Av. Argentina 2850, Callao",
  "contacto_nombre": "Roberto Paredes",
  "contacto_telefono": "987654321"
}
```

#### Actualizar proveedor
```http
PUT /api/v1/suppliers/{id}
```

**Requiere rol:** admin o almacenero

**Body:** Campos a actualizar (todos opcionales)

#### Eliminar proveedor
```http
DELETE /api/v1/suppliers/{id}
```

**Requiere rol:** admin

**Nota:** No se puede eliminar si tiene compras registradas

---

### Compras

#### Listar compras
```http
GET /api/v1/purchases
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "numero_orden": "OC-2026-001",
    "proveedor_id": 1,
    "proveedor_nombre": "Distribuidora Andina SAC",
    "proveedor_ruc": "20518520442",
    "fecha": "2026-10-20 10:30:00",
    "subtotal": 2500.00,
    "igv": 450.00,
    "total": 2950.00,
    "observaciones": "Compra de cemento",
    "estado": "COMPLETADA",
    "created_at": "2026-10-20 10:30:00"
  }
]
```

#### Estadísticas de compras
```http
GET /api/v1/purchases/stats
```

**Requiere rol:** admin o almacenero

**Respuesta:**
```json
{
  "total_compras": 8,
  "total_gastado": 15750.50,
  "compra_promedio": 1968.81,
  "proveedor_principal": "Distribuidora Andina SAC"
}
```

#### Obtener compra con detalles
```http
GET /api/v1/purchases/{id}
```

**Respuesta:**
```json
{
  "id": 1,
  "numero_orden": "OC-2026-001",
  "proveedor_id": 1,
  "proveedor_nombre": "Distribuidora Andina SAC",
  "proveedor_ruc": "20518520442",
  "fecha": "2026-10-20 10:30:00",
  "subtotal": 2500.00,
  "igv": 450.00,
  "total": 2950.00,
  "observaciones": "Compra de cemento",
  "estado": "COMPLETADA",
  "detalles": [
    {
      "id": 1,
      "compra_id": 1,
      "producto_id": 1,
      "producto_nombre": "Cemento Andino Tipo I x 42.5 kg",
      "producto_sku": "CEM-001",
      "cantidad": 100,
      "costo_unitario": 22.50,
      "subtotal": 2250.00,
      "created_at": "2026-10-20 10:30:00"
    }
  ]
}
```

#### Crear compra
```http
POST /api/v1/purchases
```

**Requiere rol:** admin o almacenero

**⚠️ IMPORTANTE:** Esta operación **actualiza el stock automáticamente** (suma las cantidades compradas)

**Body:**
```json
{
  "proveedor_id": 1,
  "fecha": "2026-10-31 10:00:00",
  "observaciones": "Compra de cemento y agregados",
  "detalles": [
    {
      "producto_id": 1,
      "cantidad": 50,
      "costo_unitario": 22.50
    },
    {
      "producto_id": 6,
      "cantidad": 500,
      "costo_unitario": 0.85
    }
  ]
}
```

**Proceso automático:**
1. Valida proveedor y productos
2. Calcula subtotales de cada item
3. Calcula IGV (18%)
4. Calcula total
5. Genera número de orden automático (OC-YYYY-###)
6. Crea la compra
7. Crea los detalles
8. **SUMA el stock de cada producto automáticamente**

**Respuesta:** Compra creada con detalles completos

#### Actualizar compra
```http
PUT /api/v1/purchases/{id}
```

**Requiere rol:** admin o almacenero

**Body:**
```json
{
  "observaciones": "Nueva observación",
  "estado": "ANULADA"
}
```

**Nota:** Solo se pueden actualizar observaciones y estado. No se pueden modificar los items después de crear la compra.

#### Anular compra
```http
DELETE /api/v1/purchases/{id}
```

**Requiere rol:** admin

**⚠️ IMPORTANTE:** 
- Cambia el estado a "ANULADA"
- **NO revierte el stock automáticamente** (por seguridad)
- Si necesita ajustar stock, debe hacerse manualmente usando el endpoint de ajuste de inventario

---

## Reglas de Negocio

### Proveedores
1. **RUC único:** No puede haber dos proveedores con el mismo RUC
2. **Validación de RUC:** Debe ser de 11 dígitos y válido
3. **Eliminación protegida:** No se puede eliminar un proveedor que tenga compras registradas
4. **Desactivación:** Al eliminar, el proveedor se marca como inactivo (soft delete)

### Compras
1. **Número de orden automático:** Formato OC-YYYY-###, se genera automáticamente
2. **IGV:** Siempre 18%, se calcula automáticamente sobre el subtotal
3. **Stock automático:** Al crear una compra, el stock de los productos se incrementa (SUMA)
4. **Anulación:** Al anular una compra, el stock NO se revierte automáticamente
5. **Items mínimos:** Una compra debe tener al menos 1 item
6. **Validaciones:** 
   - El proveedor debe existir y estar activo
   - Los productos deben existir
   - Las cantidades deben ser mayores a 0
   - Los costos deben ser mayores a 0

### Actualización de Stock

**Al crear compra:**
```
nuevo_stock = stock_actual + cantidad_comprada
```

**Al anular compra:**
- El stock NO se revierte automáticamente
- Se debe ajustar manualmente si es necesario
- Usar: `POST /api/v1/products/{id}/adjust-stock`

**Motivo:** Seguridad y trazabilidad. La reversión automática puede causar inconsistencias si:
- Ya se vendieron productos de esa compra
- Se hicieron ajustes manuales posteriores
- Hay discrepancias físicas en el almacén

---

## Control de Acceso (Roles)

| Acción | admin | almacenero | vendedor |
|--------|-------|------------|----------|
| Ver proveedores | ✅ | ✅ | ❌ |
| Crear/editar proveedores | ✅ | ✅ | ❌ |
| Eliminar proveedores | ✅ | ❌ | ❌ |
| Ver compras | ✅ | ✅ | ❌ |
| Crear compras | ✅ | ✅ | ❌ |
| Anular compras | ✅ | ❌ | ❌ |
| Ver estadísticas | ✅ | ✅ | ❌ |

---

## Ejemplos de Uso

### Ejemplo 1: Crear un proveedor

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login/form \
  -d "username=almacen@ferreteria.com" \
  -d "password=alm123"

# Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}

# 2. Crear proveedor
curl -X POST http://localhost:8000/api/v1/suppliers \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "ruc": "20518520442",
    "razon_social": "Distribuidora Andina SAC",
    "telefono": "015551234",
    "email": "ventas@andina.com.pe"
  }'
```

### Ejemplo 2: Crear una orden de compra

```bash
# Crear compra (actualiza stock automáticamente)
curl -X POST http://localhost:8000/api/v1/purchases \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "proveedor_id": 1,
    "observaciones": "Compra de cemento",
    "detalles": [
      {
        "producto_id": 1,
        "cantidad": 50,
        "costo_unitario": 22.50
      }
    ]
  }'

# Response:
{
  "id": 9,
  "numero_orden": "OC-2026-009",
  "subtotal": 1125.00,
  "igv": 202.50,
  "total": 1327.50,
  "detalles": [...]
}
```

### Ejemplo 3: Verificar stock actualizado

```bash
# Ver producto después de la compra
curl -X GET http://localhost:8000/api/v1/products/1 \
  -H "Authorization: Bearer eyJ..."

# Response:
{
  "id": 1,
  "nombre": "Cemento Andino Tipo I x 42.5 kg",
  "stock_actual": 200,  # <- Se incrementó en 50
  "estado_stock": "OK"
}
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
py test_purchases.py
```

### Acceder a Swagger UI
```
http://localhost:8000/api/docs
```

---

## Datos de Ejemplo

El sistema incluye 8 proveedores reales con datos de ferreterías peruanas:

1. **Distribuidora Andina SAC** - RUC: 20518520442
2. **Aceros Comerciales del Perú SA** - RUC: 20156987412
3. **Sodimac Perú SA** - RUC: 20112273922
4. **Maestro Perú SA** - RUC: 20493020618
5. **Corporación Miyasato SAC** - RUC: 20109072177
6. **Distribuidora Ferretera Los Andes EIRL** - RUC: 20601234567
7. **Pinturas Técnicas SA** - RUC: 20445678901
8. **Importadora de Herramientas SAC** - RUC: 20556789012

Y 8 compras de ejemplo que cubren diferentes escenarios y productos.

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
- `app/schemas/supplier.py` - Validación de proveedores
- `app/schemas/purchase.py` - Validación de compras

**Repositories:**
- `app/repositories/supplier_repository.py` - CRUD proveedores
- `app/repositories/purchase_repository.py` - CRUD compras

**Services:**
- `app/services/supplier_service.py` - Lógica de proveedores
- `app/services/purchase_service.py` - Lógica de compras + actualización de stock

**Endpoints:**
- `app/api/v1/endpoints/suppliers.py` - API proveedores
- `app/api/v1/endpoints/purchases.py` - API compras

**CSV:**
- `data/proveedores.csv` - Datos de proveedores
- `data/compras.csv` - Órdenes de compra
- `data/detalle_compras.csv` - Items de cada compra

---

## Próximos Pasos

**FASE 6: Módulo de Ventas**
- CRUD de clientes
- Creación de ventas con IGV
- **Actualización automática de stock** (resta cantidades)
- Condiciones de pago (contado/crédito)
- Gestión de saldo por cobrar

---

## Soporte

Para más información:
- Ver documentación en Swagger: http://localhost:8000/api/docs
- Revisar `backend/README.md`
- Consultar `REGLAS_NEGOCIO.md`
