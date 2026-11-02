# Datos del ERP

Los archivos CSV de esta carpeta son la fuente única de datos para usuarios, categorías, productos, proveedores, clientes, ventas, compras, pagos y movimientos. La API lee y actualiza estos mismos archivos; no migra ni guarda las operaciones en una base de datos.

Mantén juntos los archivos relacionados, en especial `ventas.csv` con `detalle_ventas.csv` y `compras.csv` con `detalle_compras.csv`. Haz copias de seguridad de la carpeta `backend/data` antes de reemplazar o editar los datos.

El CSV diario de existencias se puede cargar desde **Inventario → Sincronizar stock del día**. Ese archivo solo actualiza el stock del catálogo; no sustituye a `productos.csv`.
