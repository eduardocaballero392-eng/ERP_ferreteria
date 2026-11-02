"""
Test directo para debug
"""
import sys
sys.path.insert(0, '.')

try:
    print("1. Importando config...")
    from app.core.config import settings
    print(f"   DATA_DIR = {settings.DATA_DIR}")
    print(f"   DATA_DIR exists = {settings.DATA_DIR.exists()}")
    
    print("\n2. Importando csv_handler...")
    from app.core.csv_handler import get_csv_handler
    
    print("\n3. Creando handler de ventas...")
    handler = get_csv_handler("ventas.csv")
    print(f"   Filepath = {handler.filepath}")
    print(f"   File exists = {handler.filepath.exists()}")
    
    print("\n4. Leyendo ventas...")
    ventas = handler.read_all()
    print(f"   Total ventas = {len(ventas)}")
    
    print("\n5. Importando sale_repository...")
    from app.repositories.sale_repository import sale_repository
    
    print("\n6. Obteniendo todas las ventas desde repository...")
    sales = sale_repository.find_all()
    print(f"   Total ventas desde repo = {len(sales)}")
    
    print("\n7. Importando sale_service...")
    from app.services.sale_service import sale_service
    
    print("\n8. Obteniendo ventas desde service...")
    result = sale_service.get_all_sales()
    print(f"   Total ventas desde service = {len(result)}")
    print(f"   Primera venta: {result[0] if result else 'N/A'}")
    
    print("\n✅ TODO OK!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
