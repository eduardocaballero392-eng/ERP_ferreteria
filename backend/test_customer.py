"""
Test clientes
"""
import sys
sys.path.insert(0, '.')

from app.repositories.customer_repository import customer_repository

print("Buscando cliente ID 1...")
customer = customer_repository.find_by_id(1)

if customer:
    print(f"Cliente encontrado: {customer}")
    print(f"  nombre: '{customer.get('nombre')}' (type: {type(customer.get('nombre'))})")
    print(f"  apellido: '{customer.get('apellido')}' (type: {type(customer.get('apellido'))})")
    print(f"  razon_social: '{customer.get('razon_social')}' (type: {type(customer.get('razon_social'))})")
else:
    print("Cliente NO encontrado")
