"""
Script para regenerar contraseñas hasheadas correctamente
"""
from app.security.password import get_password_hash

# Generar hashes para las contraseñas
passwords = {
    "admin123": get_password_hash("admin123"),
    "vendedor123": get_password_hash("vendedor123"),
    "almacenero123": get_password_hash("almacenero123"),
}

print("Contraseñas hasheadas:")
for pwd, hash in passwords.items():
    print(f"{pwd}: {hash}")

# Crear CSV con las contraseñas correctas
csv_content = """id,username,email,nombre,apellido,password_hash,role,activo,created_at,updated_at,nombre_completo
1,admin,admin@ferreteria.com,Carlos,Mendoza,{},admin,True,2026-10-01 08:00:00,2026-10-01 08:00:00,Carlos Mendoza
2,vendedor,vendedor@ferreteria.com,María,Rodríguez,{},vendedor,True,2026-10-01 08:00:00,2026-10-01 08:00:00,María Rodríguez
3,almacenero,almacen@ferreteria.com,José,Torres,{},almacenero,True,2026-10-01 08:00:00,2026-10-01 08:00:00,José Torres
""".format(
    passwords["admin123"],
    passwords["vendedor123"],
    passwords["almacenero123"]
)

# Guardar CSV
with open("data/usuarios.csv", "w", encoding="utf-8") as f:
    f.write(csv_content)

print("\n✅ Archivo usuarios.csv actualizado correctamente")
print("\nCredenciales:")
print("- admin / admin123")
print("- vendedor / vendedor123")
print("- almacenero / almacenero123")
