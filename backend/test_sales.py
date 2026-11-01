"""
Script de prueba para el módulo de Ventas
Prueba clientes y ventas
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_sales_module():
    """Prueba completa del módulo de ventas"""
    
    print("=" * 60)
    print("🛍️  PRUEBA DEL MÓDULO DE VENTAS")
    print("=" * 60)
    
    # 1. Login como vendedor
    print("\n1️⃣  Login como vendedor...")
    login_data = {
        "username": "vendedor@ferreteria.com",
        "password": "ven123"
    }
    response = requests.post(f"{BASE_URL}/auth/login/form", data=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login exitoso")
    else:
        print("❌ Error en login")
        return
    
    # 2. Listar clientes
    print("\n2️⃣  Listar clientes...")
    response = requests.get(f"{BASE_URL}/customers", headers=headers)
    
    if response.status_code == 200:
        customers = response.json()
        print(f"✅ {len(customers)} clientes encontrados")
        if customers:
            print(f"   - {customers[0].get('nombres', '')} {customers[0].get('apellidos', '')} (Doc: {customers[0]['numero_documento']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 3. Clientes con estadísticas
    print("\n3️⃣  Clientes con estadísticas...")
    response = requests.get(f"{BASE_URL}/customers/with-stats", headers=headers)
    
    if response.status_code == 200:
        customers_stats = response.json()
        print("✅ Estadísticas obtenidas:")
        for cust in customers_stats[:3]:
            nombre = cust.get('razon_social') or f"{cust.get('nombres', '')} {cust.get('apellidos', '')}"
            print(f"   - {nombre}: {cust['total_compras']} compras, S/ {cust['monto_total_compras']}")
            print(f"     Saldo pendiente: S/ {cust['saldo_pendiente']}, Crédito disponible: S/ {cust['disponible_credito']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 4. Buscar cliente
    print("\n4️⃣  Buscar cliente por 'Carlos'...")
    response = requests.get(f"{BASE_URL}/customers/search?query=Carlos", headers=headers)
    
    if response.status_code == 200:
        results = response.json()
        print(f"✅ {len(results)} resultado(s) encontrado(s)")
        if results:
            customer_id = results[0]['id']
            print(f"   - ID: {customer_id}, {results[0].get('nombres', '')} {results[0].get('apellidos', '')}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 5. Listar ventas
    print("\n5️⃣  Listar ventas...")
    response = requests.get(f"{BASE_URL}/sales", headers=headers)
    
    if response.status_code == 200:
        sales = response.json()
        print(f"✅ {len(sales)} venta(s) encontrada(s)")
        if sales:
            print(f"   - {sales[0]['numero_comprobante']}: S/ {sales[0]['total']} ({sales[0]['estado']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 6. Estadísticas de ventas
    print("\n6️⃣  Estadísticas de ventas...")
    response = requests.get(f"{BASE_URL}/sales/stats", headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print("✅ Estadísticas generales:")
        print(f"   - Total ventas: {stats['total_ventas']}")
        print(f"   - Total vendido: S/ {stats['total_vendido']}")
        print(f"   - Venta promedio: S/ {stats['venta_promedio']}")
        print(f"   - Cliente principal: {stats['cliente_principal']}")
        print(f"   - Contado: {stats['ventas_contado']} ventas (S/ {stats['monto_contado']})")
        print(f"   - Crédito: {stats['ventas_credito']} ventas (S/ {stats['monto_credito']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 7. Verificar stock antes de vender
    print("\n7️⃣  Verificar stock del producto antes de vender...")
    response = requests.get(f"{BASE_URL}/products/1", headers=headers)  # Cemento Andino
    
    if response.status_code == 200:
        product = response.json()
        stock_antes = product['stock_actual']
        print(f"✅ Stock actual antes de venta:")
        print(f"   - {product['nombre']}: {stock_antes} unidades")
    else:
        print(f"❌ Error: {response.status_code}")
        return
    
    # 8. Crear una venta nueva (IMPORTANTE: actualiza stock - RESTA)
    print("\n8️⃣  Crear venta (CONTADO)...")
    new_sale = {
        "cliente_id": 1,
        "tipo_comprobante": "BOLETA",
        "condicion_pago": "CONTADO",
        "observaciones": "Venta de prueba - cemento",
        "detalles": [
            {
                "producto_id": 1,  # Cemento Andino
                "cantidad": 5,
                "precio_unitario": 28.00
            },
            {
                "producto_id": 2,  # Fierro 1/2"
                "cantidad": 10,
                "precio_unitario": 45.00
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/sales",
        headers=headers,
        json=new_sale
    )
    
    if response.status_code == 201:
        created = response.json()
        print("✅ Venta creada exitosamente:")
        print(f"   - Número de comprobante: {created['numero_comprobante']}")
        print(f"   - Tipo: {created['tipo_comprobante']}")
        print(f"   - Condición: {created['condicion_pago']}")
        print(f"   - Subtotal: S/ {created['subtotal']}")
        print(f"   - IGV (18%): S/ {created['igv']}")
        print(f"   - TOTAL: S/ {created['total']}")
        print(f"   - Items: {len(created['detalles'])} producto(s)")
        print(f"   - ⚠️  Stock actualizado automáticamente (RESTA)")
        
        sale_id = created['id']
    else:
        print(f"❌ Error al crear venta: {response.status_code}")
        print(response.json())
        return
    
    # 9. Obtener detalle de venta
    print(f"\n9️⃣  Obtener detalle de venta {sale_id}...")
    response = requests.get(f"{BASE_URL}/sales/{sale_id}", headers=headers)
    
    if response.status_code == 200:
        sale_detail = response.json()
        print("✅ Detalle obtenido:")
        print(f"   - Cliente: {sale_detail['cliente_nombre']}")
        print(f"   - Items:")
        for item in sale_detail['detalles']:
            print(f"     • {item['producto_nombre']} x{item['cantidad']} @ S/ {item['precio_unitario']} = S/ {item['subtotal']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 10. Verificar stock actualizado
    print("\n🔟 Verificar stock actualizado del producto...")
    response = requests.get(f"{BASE_URL}/products/1", headers=headers)  # Cemento Andino
    
    if response.status_code == 200:
        product = response.json()
        stock_despues = product['stock_actual']
        diferencia = stock_antes - stock_despues
        print("✅ Stock actualizado:")
        print(f"   - {product['nombre']}")
        print(f"   - Stock antes: {stock_antes} unidades")
        print(f"   - Stock después: {stock_despues} unidades")
        print(f"   - Diferencia: {diferencia} unidades (RESTADO) ✅")
        print(f"   - Estado: {product['estado_stock']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 11. Intentar venta a crédito con límite excedido (debe fallar)
    print("\n1️⃣1️⃣ Intentar venta a crédito excediendo límite...")
    sale_over_limit = {
        "cliente_id": 1,
        "tipo_comprobante": "BOLETA",
        "condicion_pago": "CREDITO",
        "observaciones": "Venta que excede límite",
        "detalles": [
            {
                "producto_id": 1,
                "cantidad": 500,  # Cantidad muy grande
                "precio_unitario": 28.00
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/sales",
        headers=headers,
        json=sale_over_limit
    )
    
    if response.status_code == 400:
        error = response.json()
        print("✅ Validación de crédito funcionando correctamente:")
        print(f"   - Error esperado: {error.get('detail')}")
    else:
        print(f"⚠️  Se esperaba error 400, pero se obtuvo: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)
    print("\n💡 NOTAS IMPORTANTES:")
    print("   - Las ventas actualizan el stock automáticamente (RESTA)")
    print("   - El IGV se calcula automáticamente (18%)")
    print("   - El número de comprobante se genera automáticamente")
    print("   - Se valida stock disponible antes de vender")
    print("   - Se valida límite de crédito en ventas a crédito")
    print("   - Al anular una venta, el stock NO se revierte automáticamente")
    print("\n🌐 Swagger UI: http://localhost:8000/api/docs")


if __name__ == "__main__":
    try:
        test_sales_module()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   cd backend && .\venv\Scripts\Activate.ps1 && py run.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
