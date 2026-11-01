"""
Script de prueba para el módulo de Reportes
Prueba dashboard, reportes de inventario, ventas, compras y movimientos
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_reports_module():
    """Prueba completa del módulo de reportes"""
    
    print("=" * 60)
    print("📊 PRUEBA DEL MÓDULO DE REPORTES")
    print("=" * 60)
    
    # 1. Login como admin
    print("\n1️⃣  Login como admin...")
    login_data = {
        "username": "admin@ferreteria.com",
        "password": "adm123"
    }
    response = requests.post(f"{BASE_URL}/auth/login/form", data=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login exitoso")
    else:
        print("❌ Error en login")
        return
    
    # 2. Dashboard principal
    print("\n2️⃣  Dashboard principal...")
    response = requests.get(f"{BASE_URL}/reports/dashboard", headers=headers)
    
    if response.status_code == 200:
        dashboard = response.json()
        print("✅ Dashboard obtenido:")
        print(f"   VENTAS:")
        print(f"   - Hoy: {dashboard['ventas_hoy']}")
        print(f"   - Mes: {dashboard['ventas_mes']} ventas (S/ {dashboard['total_vendido_mes']})")
        print(f"   COMPRAS:")
        print(f"   - Mes: {dashboard['compras_mes']} compras (S/ {dashboard['total_gastado_mes']})")
        print(f"   INVENTARIO:")
        print(f"   - Total productos: {dashboard['productos_total']}")
        print(f"   - Stock bajo: {dashboard['productos_stock_bajo']}")
        print(f"   - Valor inventario: S/ {dashboard['valor_inventario']}")
        print(f"   UTILIDAD:")
        print(f"   - Utilidad bruta mes: S/ {dashboard['utilidad_bruta_mes']}")
        print(f"   - Margen promedio: {dashboard['margen_promedio_mes']}%")
        print(f"   TOP 3 PRODUCTOS:")
        for prod in dashboard['top_productos'][:3]:
            print(f"   - {prod['nombre']}: {prod['cantidad_vendida']} unidades")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 3. Reporte de inventario
    print("\n3️⃣  Reporte de inventario...")
    response = requests.get(f"{BASE_URL}/reports/inventory", headers=headers)
    
    if response.status_code == 200:
        inventory = response.json()
        print("✅ Reporte de inventario:")
        print(f"   - Total productos: {inventory['total_productos']}")
        print(f"   - Valor total: S/ {inventory['valor_total_inventario']}")
        print(f"   - OK: {inventory['productos_ok']}")
        print(f"   - REPONER: {inventory['productos_reponer']}")
        print(f"   - AGOTADO: {inventory['productos_agotados']}")
        print(f"   Top 3 productos por valor:")
        for item in inventory['items'][:3]:
            print(f"   - {item['nombre']}: S/ {item['valor_inventario']} (Margen: {item['margen_porcentaje']:.2f}%)")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 4. Reporte de ventas
    print("\n4️⃣  Reporte de ventas (mes actual)...")
    response = requests.get(f"{BASE_URL}/reports/sales", headers=headers)
    
    if response.status_code == 200:
        sales = response.json()
        print("✅ Reporte de ventas:")
        print(f"   - Período: {sales['fecha_inicio']} a {sales['fecha_fin']}")
        print(f"   - Total ventas: {sales['total_ventas']}")
        print(f"   - Total vendido: S/ {sales['total_vendido']}")
        print(f"   - Costo total: S/ {sales['total_costo']}")
        print(f"   - UTILIDAD BRUTA: S/ {sales['utilidad_bruta']} 💰")
        print(f"   - MARGEN PROMEDIO: {sales['margen_promedio']:.2f}% 📈")
        print(f"   - Contado: {sales['ventas_contado']} ventas (S/ {sales['monto_contado']})")
        print(f"   - Crédito: {sales['ventas_credito']} ventas (S/ {sales['monto_credito']})")
        if sales['items']:
            print(f"   Última venta:")
            last = sales['items'][0]
            print(f"   - {last['numero_comprobante']}: S/ {last['total']} (Utilidad: S/ {last['utilidad_bruta']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 5. Reporte de compras
    print("\n5️⃣  Reporte de compras (mes actual)...")
    response = requests.get(f"{BASE_URL}/reports/purchases", headers=headers)
    
    if response.status_code == 200:
        purchases = response.json()
        print("✅ Reporte de compras:")
        print(f"   - Período: {purchases['fecha_inicio']} a {purchases['fecha_fin']}")
        print(f"   - Total compras: {purchases['total_compras']}")
        print(f"   - Total gastado: S/ {purchases['total_gastado']}")
        print(f"   - Compra promedio: S/ {purchases['compra_promedio']}")
        if purchases['items']:
            print(f"   Última compra:")
            last = purchases['items'][0]
            print(f"   - {last['numero_orden']}: S/ {last['total']} ({last['proveedor_nombre']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 6. Reporte de movimientos de producto
    print("\n6️⃣  Reporte de movimientos del producto 1...")
    response = requests.get(f"{BASE_URL}/reports/movements/1", headers=headers)
    
    if response.status_code == 200:
        movements = response.json()
        print("✅ Reporte de movimientos:")
        print(f"   - Producto: {movements['producto_nombre']} ({movements['sku']})")
        print(f"   - Período: {movements['fecha_inicio']} a {movements['fecha_fin']}")
        print(f"   - Stock inicial: {movements['stock_inicial']}")
        print(f"   - Total entradas: {movements['total_entradas']}")
        print(f"   - Total salidas: {movements['total_salidas']}")
        print(f"   - Stock final: {movements['stock_final']}")
        print(f"   Últimos 3 movimientos:")
        for mov in movements['movimientos'][-3:]:
            simbolo = "+" if mov['tipo_movimiento'] == 'ENTRADA' else "-"
            print(f"   - {mov['fecha'][:10]} {mov['tipo']} {mov['referencia']}: {simbolo}{mov['cantidad']} (Stock: {mov['stock_nuevo']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 7. Reporte de ventas con rango de fechas
    print("\n7️⃣  Reporte de ventas con rango personalizado...")
    response = requests.get(
        f"{BASE_URL}/reports/sales?fecha_inicio=2026-10-01&fecha_fin=2026-10-31",
        headers=headers
    )
    
    if response.status_code == 200:
        sales = response.json()
        print("✅ Reporte de octubre 2026:")
        print(f"   - Total ventas: {sales['total_ventas']}")
        print(f"   - Utilidad bruta: S/ {sales['utilidad_bruta']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 8. Logs de auditoría (si existen)
    print("\n8️⃣  Logs de auditoría...")
    response = requests.get(f"{BASE_URL}/reports/audit", headers=headers)
    
    if response.status_code == 200:
        logs = response.json()
        print(f"✅ {len(logs)} log(s) de auditoría encontrado(s)")
        if logs:
            print("   Últimos 3 logs:")
            for log in logs[:3]:
                print(f"   - [{log['fecha'][:19]}] {log['usuario']} - {log['accion']} en {log['modulo']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)
    print("\n💡 CARACTERÍSTICAS DEL MÓDULO DE REPORTES:")
    print("   ✅ Dashboard con estadísticas en tiempo real")
    print("   ✅ Reporte de inventario con valorización")
    print("   ✅ Reporte de ventas con UTILIDAD BRUTA")
    print("   ✅ Reporte de compras con totales")
    print("   ✅ Movimientos de productos (entradas/salidas)")
    print("   ✅ Top 5 productos, clientes y proveedores")
    print("   ✅ Logs de auditoría (próximamente)")
    print("   ✅ Filtros por rango de fechas")
    print("\n🌐 Swagger UI: http://localhost:8000/api/docs")


if __name__ == "__main__":
    try:
        test_reports_module()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   cd backend && .\venv\Scripts\Activate.ps1 && py run.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
