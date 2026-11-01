"""
Script de prueba para el módulo de Compras
Prueba proveedores y órdenes de compra
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_purchases_module():
    """Prueba completa del módulo de compras"""
    
    print("=" * 60)
    print("🛒 PRUEBA DEL MÓDULO DE COMPRAS")
    print("=" * 60)
    
    # 1. Login como almacenero
    print("\n1️⃣  Login como almacenero...")
    login_data = {
        "username": "almacen@ferreteria.com",
        "password": "alm123"
    }
    response = requests.post(f"{BASE_URL}/auth/login/form", data=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login exitoso")
    else:
        print("❌ Error en login")
        return
    
    # 2. Listar proveedores
    print("\n2️⃣  Listar proveedores...")
    response = requests.get(f"{BASE_URL}/suppliers", headers=headers)
    
    if response.status_code == 200:
        suppliers = response.json()
        print(f"✅ {len(suppliers)} proveedores encontrados")
        if suppliers:
            print(f"   - {suppliers[0]['razon_social']} (RUC: {suppliers[0]['ruc']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 3. Proveedores con estadísticas
    print("\n3️⃣  Proveedores con estadísticas...")
    response = requests.get(f"{BASE_URL}/suppliers/with-stats", headers=headers)
    
    if response.status_code == 200:
        suppliers_stats = response.json()
        print("✅ Estadísticas obtenidas:")
        for supp in suppliers_stats[:3]:
            print(f"   - {supp['razon_social']}: {supp['total_compras']} compras, S/ {supp['monto_total_compras']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 4. Buscar proveedor
    print("\n4️⃣  Buscar proveedor por 'Andina'...")
    response = requests.get(f"{BASE_URL}/suppliers/search?query=Andina", headers=headers)
    
    if response.status_code == 200:
        results = response.json()
        print(f"✅ {len(results)} resultado(s) encontrado(s)")
        if results:
            supplier_id = results[0]['id']
            print(f"   - ID: {supplier_id}, {results[0]['razon_social']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 5. Listar compras
    print("\n5️⃣  Listar compras...")
    response = requests.get(f"{BASE_URL}/purchases", headers=headers)
    
    if response.status_code == 200:
        purchases = response.json()
        print(f"✅ {len(purchases)} compra(s) encontrada(s)")
        if purchases:
            print(f"   - {purchases[0]['numero_orden']}: S/ {purchases[0]['total']} ({purchases[0]['estado']})")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 6. Estadísticas de compras
    print("\n6️⃣  Estadísticas de compras...")
    response = requests.get(f"{BASE_URL}/purchases/stats", headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print("✅ Estadísticas generales:")
        print(f"   - Total compras: {stats['total_compras']}")
        print(f"   - Total gastado: S/ {stats['total_gastado']}")
        print(f"   - Compra promedio: S/ {stats['compra_promedio']}")
        print(f"   - Proveedor principal: {stats['proveedor_principal']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 7. Crear una compra nueva (IMPORTANTE: actualiza stock)
    print("\n7️⃣  Crear orden de compra...")
    new_purchase = {
        "proveedor_id": 1,
        "observaciones": "Compra de prueba - cemento",
        "detalles": [
            {
                "producto_id": 1,  # Cemento Andino
                "cantidad": 20,
                "costo_unitario": 22.50
            },
            {
                "producto_id": 6,  # Bolsa de cemento gris
                "cantidad": 100,
                "costo_unitario": 0.85
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/purchases",
        headers=headers,
        json=new_purchase
    )
    
    if response.status_code == 201:
        created = response.json()
        print("✅ Compra creada exitosamente:")
        print(f"   - Número de orden: {created['numero_orden']}")
        print(f"   - Subtotal: S/ {created['subtotal']}")
        print(f"   - IGV (18%): S/ {created['igv']}")
        print(f"   - TOTAL: S/ {created['total']}")
        print(f"   - Items: {len(created['detalles'])} producto(s)")
        print(f"   - ⚠️  Stock actualizado automáticamente (SUMA)")
        
        purchase_id = created['id']
    else:
        print(f"❌ Error al crear compra: {response.status_code}")
        print(response.json())
        return
    
    # 8. Obtener detalle de compra
    print(f"\n8️⃣  Obtener detalle de compra {purchase_id}...")
    response = requests.get(f"{BASE_URL}/purchases/{purchase_id}", headers=headers)
    
    if response.status_code == 200:
        purchase_detail = response.json()
        print("✅ Detalle obtenido:")
        print(f"   - Proveedor: {purchase_detail['proveedor_nombre']}")
        print(f"   - Items:")
        for item in purchase_detail['detalles']:
            print(f"     • {item['producto_nombre']} x{item['cantidad']} @ S/ {item['costo_unitario']} = S/ {item['subtotal']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 9. Verificar stock actualizado
    print("\n9️⃣  Verificar stock actualizado del producto...")
    response = requests.get(f"{BASE_URL}/products/1", headers=headers)  # Cemento Andino
    
    if response.status_code == 200:
        product = response.json()
        print("✅ Stock actualizado:")
        print(f"   - {product['nombre']}: {product['stock_actual']} unidades")
        print(f"   - Estado: {product['estado_stock']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    # 10. Actualizar observaciones de compra
    print(f"\n🔟 Actualizar observaciones de compra...")
    update_data = {
        "observaciones": "Compra de prueba - cemento y bolsas (ACTUALIZADO)"
    }
    
    response = requests.put(
        f"{BASE_URL}/purchases/{purchase_id}",
        headers=headers,
        json=update_data
    )
    
    if response.status_code == 200:
        print("✅ Compra actualizada")
    else:
        print(f"❌ Error: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)
    print("\n💡 NOTAS IMPORTANTES:")
    print("   - Las compras actualizan el stock automáticamente (SUMA)")
    print("   - El IGV se calcula automáticamente (18%)")
    print("   - El número de orden se genera automáticamente (OC-YYYY-###)")
    print("   - Al anular una compra, el stock NO se revierte automáticamente")
    print("\n🌐 Swagger UI: http://localhost:8000/api/docs")


if __name__ == "__main__":
    try:
        test_purchases_module()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   cd backend && python run.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
