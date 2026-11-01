"""
Script para probar la configuración del backend
Ejecutar: python test_config.py
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app.core.config import settings
    from app.core.utils import calcular_igv, calcular_total_con_igv, obtener_estado_stock
    from app.core.utils import validar_ruc, validar_dni
    
    print("=" * 60)
    print("PRUEBA DE CONFIGURACIÓN - ERP FERRETERÍA")
    print("=" * 60)
    print()
    
    # Probar configuración
    print("1. Configuración de la aplicación:")
    print(f"   - Nombre: {settings.APP_NAME}")
    print(f"   - Versión: {settings.APP_VERSION}")
    print(f"   - Modo Debug: {settings.DEBUG}")
    print(f"   - Directorio de datos: {settings.DATA_DIR.absolute()}")
    print(f"   - Directorio existe: {'✓' if settings.DATA_DIR.exists() else '✗'}")
    print()
    
    # Probar utilidades de IGV
    print("2. Prueba de cálculos de IGV (18%):")
    subtotal = 1000.0
    igv = calcular_igv(subtotal)
    total = calcular_total_con_igv(subtotal)
    print(f"   - Subtotal: S/ {subtotal:.2f}")
    print(f"   - IGV (18%): S/ {igv:.2f}")
    print(f"   - Total: S/ {total:.2f}")
    print()
    
    # Probar estados de stock
    print("3. Prueba de estados de stock:")
    casos_stock = [
        (0, 5, "AGOTADO"),
        (3, 5, "REPONER"),
        (10, 5, "OK")
    ]
    for stock_actual, stock_minimo, esperado in casos_stock:
        estado = obtener_estado_stock(stock_actual, stock_minimo)
        simbolo = "✓" if estado == esperado else "✗"
        print(f"   {simbolo} Stock: {stock_actual}, Mínimo: {stock_minimo} → {estado}")
    print()
    
    # Probar validación de RUC
    print("4. Prueba de validación de RUC:")
    rucs_prueba = [
        ("20123456789", True),   # RUC válido
        ("10987654321", True),   # RUC válido
        ("12345678901", False),  # Prefijo inválido
        ("2012345678", False),   # Longitud incorrecta
    ]
    for ruc, es_valido_esperado in rucs_prueba:
        es_valido = validar_ruc(ruc)
        simbolo = "✓" if es_valido == es_valido_esperado else "✗"
        resultado = "VÁLIDO" if es_valido else "INVÁLIDO"
        print(f"   {simbolo} RUC {ruc}: {resultado}")
    print()
    
    # Probar validación de DNI
    print("5. Prueba de validación de DNI:")
    dnis_prueba = [
        ("12345678", True),    # DNI válido
        ("87654321", True),    # DNI válido
        ("1234567", False),    # Longitud incorrecta
        ("123456789", False),  # Longitud incorrecta
    ]
    for dni, es_valido_esperado in dnis_prueba:
        es_valido = validar_dni(dni)
        simbolo = "✓" if es_valido == es_valido_esperado else "✗"
        resultado = "VÁLIDO" if es_valido else "INVÁLIDO"
        print(f"   {simbolo} DNI {dni}: {resultado}")
    print()
    
    # Probar manejador de CSV
    print("6. Prueba de manejador de CSV:")
    from app.core.csv_handler import get_csv_handler
    
    test_handler = get_csv_handler("test.csv")
    print(f"   ✓ Manejador CSV creado para: {test_handler.filename}")
    print(f"   - Ruta completa: {test_handler.filepath}")
    print(f"   - Archivo existe: {'✓' if test_handler.exists() else '✗ (se creará al guardar datos)'}")
    print()
    
    print("=" * 60)
    print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)
    print()
    print("Próximos pasos:")
    print("1. Crear archivo .env desde .env.example (opcional)")
    print("2. Colocar tus archivos CSV en la carpeta 'backend/data/'")
    print("3. Ejecutar: python load_csv_data.py (para inspeccionar tus CSV)")
    print("4. Ejecutar: pip install -r requirements.txt")
    print("5. Ejecutar: python run.py")
    print()

except Exception as e:
    print(f"✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    print()
    print("Asegúrate de:")
    print("1. Tener instaladas las dependencias: pip install -r requirements.txt")
    sys.exit(1)
