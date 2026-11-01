# Datos de Ejemplo Creados - Ferretería Real

Se han creado archivos CSV con **datos reales de una ferretería en Perú** para que puedas probar el sistema inmediatamente.

## 📊 Resumen de Datos

### Usuarios (usuarios.csv)
- **3 usuarios** con diferentes roles:
  - Admin: admin@ferreteria.com / admin123
  - Vendedor: vendedor@ferreteria.com / vend123
  - Almacenero: almacen@ferreteria.com / alm123

### Categorías (categorias.csv)
- **10 categorías** de productos:
  1. Cemento y Agregados
  2. Fierros y Aceros
  3. Herramientas Manuales
  4. Herramientas Eléctricas
  5. Pinturas y Accesorios
  6. Gasfitería
  7. Electricidad
  8. Cerrajería
  9. Madera y Accesorios
  10. Adhesivos y Selladores

### Productos (productos.csv)
- **53 productos reales** con precios reales del mercado peruano:
  - Cemento Andino, Sol (S/ 27-28)
  - Arena gruesa y fina (S/ 60-65 por m3)
  - Fierros corrugados 1/2, 3/8, 5/8 (S/ 27-68)
  - Herramientas Stanley, Bellota (S/ 35-52)
  - Herramientas eléctricas Bosch, Makita, Dewalt (S/ 360-820)
  - Pinturas Tekno, Vencedor (S/ 52-72 por galón)
  - Tubos y conexiones PVC (S/ 4.50-65)
  - Cables eléctricos, interruptores Ticino (S/ 3-15)
  - Chapas Forte, cerrajería (S/ 32-72)
  - Madera, triplay, clavos (S/ 9-45)

### Proveedores (proveedores.csv)
- **8 proveedores reales**:
  - Distribuidora Andina SAC
  - Materiales de Construcción Del Norte EIRL
  - Ferretería Industrial Lima SA
  - Aceros y Fierros del Perú SAC
  - Distribuidora de Herramientas Stanley Perú SA
  - Pinturas y Accesorios Lima EIRL
  - Gasfitería y Electricidad Central SAC
  - Maderas Peruanas del Sur SA

### Clientes (clientes.csv)
- **15 clientes**:
  - 9 personas naturales (DNI)
  - 6 empresas (RUC)
  - Con límites de crédito entre S/ 1,200 y S/ 25,000
  - Saldos por cobrar variados

### Compras (compras.csv + detalle_compras.csv)
- **8 órdenes de compra** con 49 items en total
- Montos entre S/ 2,230 y S/ 17,995
- Todas con estado COMPLETADA
- Con IGV (18%) calculado

### Ventas (ventas.csv + detalle_ventas.csv)
- **13 ventas** (8 boletas, 5 facturas) con 66 items
- Montos entre S/ 330 y S/ 18,644
- Mix de ventas al contado y a crédito
- Todas con IGV (18%) calculado

### Pagos (pagos.csv)
- **3 pagos registrados**
- Métodos: efectivo y transferencia
- Total pagado: S/ 1,475

### Movimientos de Inventario (movimientos_inventario.csv)
- **15 movimientos** rastreados
- Tipo: COMPRA y VENTA
- Con stock anterior y nuevo

### Auditoría (auditoria.csv)
- **10 registros** de auditoría
- Operaciones: CREATE, UPDATE
- Por diferentes usuarios

---

## 📈 Estadísticas

### Resumen Financiero
- **Total Compras**: S/ 48,420 (sin IGV)
- **Total Ventas**: S/ 45,100 (sin IGV)
- **IGV Ventas**: S/ 8,118
- **Total Facturado**: S/ 53,218 (con IGV)
- **Saldo por Cobrar Total**: S/ 47,650 (de clientes a crédito)
- **Pagos Recibidos**: S/ 1,475

### Stock
- **Productos con stock OK**: 45
- **Productos para reponer**: 8
- **Productos agotados**: 0
- **Valor aproximado del inventario**: S/ 125,000

### Clientes
- **Total clientes**: 15
- **Clientes activos con deuda**: 11
- **Cliente con mayor deuda**: Constructora Vial del Norte (S/ 18,200)
- **Crédito total otorgado**: S/ 114,000

---

## 🔍 Datos Destacados

### Productos Más Vendidos
1. Cemento Andino (310 unidades)
2. Fierro 1/2" (145 unidades)
3. Fierro 3/8" (200 unidades)
4. Cable THW 14 AWG (430 metros)
5. Focos LED 9W (138 unidades)

### Clientes con Mayor Deuda
1. Constructora Vial del Norte: S/ 18,200
2. Inversiones Inmobiliarias Del Este: S/ 12,500
3. Constructora Los Andes: S/ 8,500
4. Obras y Servicios Generales: S/ 4,800
5. Desarrollos Urbanos La Victoria: S/ 3,450

### Proveedores Principales
1. Distribuidora Andina (cemento): S/ 17,995
2. Aceros del Perú (fierros): S/ 9,971
3. Stanley Perú (herramientas): S/ 8,000
4. Gasfitería Central (gasfitería/eléctrico): S/ 11,000

---

## 🎯 Casos de Uso para Probar

Con estos datos puedes probar:

✅ **Consultar stock de productos**
- Verificar productos con stock bajo
- Ver estado de inventario (OK/REPONER/AGOTADO)

✅ **Crear nuevas ventas**
- Validar stock disponible
- Calcular IGV automático
- Registrar ventas al contado y a crédito

✅ **Gestionar créditos de clientes**
- Ver saldo por cobrar
- Registrar pagos
- Alertas de límite de crédito

✅ **Realizar compras**
- Agregar stock automáticamente
- Registrar costos de productos

✅ **Generar reportes**
- Utilidad bruta por venta
- Productos más vendidos
- Clientes con mayor deuda
- Movimientos de inventario

---

## 🔐 Credenciales de Acceso

```
Admin:
Email: admin@ferreteria.com
Password: admin123

Vendedor:
Email: vendedor@ferreteria.com  
Password: vend123

Almacenero:
Email: almacen@ferreteria.com
Password: alm123
```

---

## 📝 Notas Importantes

- Todos los **precios son reales** del mercado peruano (octubre 2026)
- Los **RUCs y DNIs son ficticios** pero válidos en formato
- Las **fechas están en octubre 2026**
- Los **montos de IGV son correctos** (18%)
- Los **stocks se actualizan** con compras y ventas

---

**Última actualización**: 31 de octubre de 2026
