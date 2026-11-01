"""
Script para cargar y validar archivos CSV
Ejecutar: python load_csv_data.py
"""
import sys
from pathlib import Path
import pandas as pd

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings
from app.core.csv_handler import CSVHandler


def inspect_csv(filepath: Path):
    """Inspecciona un archivo CSV y muestra su información"""
    print(f"\n{'='*60}")
    print(f"Archivo: {filepath.name}")
    print(f"{'='*60}")
    
    try:
        df = pd.read_csv(filepath)
        
        print(f"\n📊 Información General:")
        print(f"   - Filas: {len(df)}")
        print(f"   - Columnas: {len(df.columns)}")
        
        print(f"\n📋 Columnas encontradas:")
        for i, col in enumerate(df.columns, 1):
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            print(f"   {i}. {col:30} | Tipo: {str(dtype):10} | Nulos: {null_count}")
        
        print(f"\n📈 Primeras 3 filas:")
        print(df.head(3).to_string(index=False))
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False


def main():
    """Función principal"""
    print("="*60)
    print("INSPECTOR DE ARCHIVOS CSV - ERP FERRETERÍA")
    print("="*60)
    print()
    print(f"Directorio de datos: {settings.DATA_DIR.absolute()}")
    print()
    
    # Buscar todos los archivos CSV en el directorio de datos
    csv_files = list(settings.DATA_DIR.glob("*.csv"))
    
    if not csv_files:
        print("⚠️  No se encontraron archivos CSV en el directorio de datos.")
        print()
        print("Instrucciones:")
        print("1. Coloca tus archivos CSV en la carpeta 'backend/data/'")
        print("2. Ejecuta este script nuevamente")
        print()
        print("Archivos esperados:")
        expected_files = [
            "usuarios.csv", "categorias.csv", "productos.csv",
            "proveedores.csv", "clientes.csv", "compras.csv",
            "detalle_compras.csv", "ventas.csv", "detalle_ventas.csv",
            "pagos.csv", "movimientos_inventario.csv", "auditoria.csv"
        ]
        for f in expected_files:
            print(f"   - {f}")
        return
    
    print(f"✅ Se encontraron {len(csv_files)} archivo(s) CSV:")
    for f in csv_files:
        print(f"   - {f.name}")
    
    # Inspeccionar cada archivo
    success_count = 0
    for csv_file in csv_files:
        if inspect_csv(csv_file):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Archivos procesados exitosamente: {success_count}/{len(csv_files)}")
    print(f"{'='*60}")
    print()


if __name__ == "__main__":
    main()
