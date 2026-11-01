"""
Script para probar la autenticación
Ejecutar: python test_auth.py
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app.security.password import get_password_hash, verify_password
from app.security.jwt import create_access_token, decode_access_token
from app.repositories.user_repository import user_repository


def test_password_hashing():
    """Prueba de hash de contraseñas"""
    print("=" * 60)
    print("1. PRUEBA DE HASH DE CONTRASEÑAS")
    print("=" * 60)
    
    password = "admin123"
    hashed = get_password_hash(password)
    
    print(f"Contraseña original: {password}")
    print(f"Hash: {hashed[:50]}...")
    print(f"Verificación correcta: {verify_password(password, hashed)}")
    print(f"Verificación incorrecta: {verify_password('wrong', hashed)}")
    print()


def test_jwt_tokens():
    """Prueba de tokens JWT"""
    print("=" * 60)
    print("2. PRUEBA DE TOKENS JWT")
    print("=" * 60)
    
    # Crear token
    data = {
        "sub": "admin@ferreteria.com",
        "user_id": 1,
        "role": "admin"
    }
    token = create_access_token(data)
    
    print(f"Token creado: {token[:50]}...")
    print()
    
    # Decodificar token
    decoded = decode_access_token(token)
    if decoded:
        print("Token decodificado exitosamente:")
        print(f"  - Email: {decoded.email}")
        print(f"  - User ID: {decoded.user_id}")
        print(f"  - Role: {decoded.role}")
    else:
        print("❌ Error al decodificar token")
    print()


def test_user_repository():
    """Prueba del repositorio de usuarios"""
    print("=" * 60)
    print("3. PRUEBA DE REPOSITORIO DE USUARIOS")
    print("=" * 60)
    
    # Listar todos los usuarios
    users = user_repository.find_all()
    print(f"Total de usuarios activos: {len(users)}")
    
    for user in users:
        print(f"\n  Usuario ID {user.get('id')}:")
        print(f"    - Email: {user.get('email')}")
        print(f"    - Nombre: {user.get('nombre')} {user.get('apellido')}")
        print(f"    - Role: {user.get('role')}")
        print(f"    - Activo: {user.get('activo')}")
    print()
    
    # Buscar por email
    admin = user_repository.find_by_email("admin@ferreteria.com")
    if admin:
        print("✓ Usuario admin encontrado por email")
    else:
        print("❌ Usuario admin no encontrado")
    print()
    
    # Buscar por rol
    vendedores = user_repository.find_by_role("vendedor")
    print(f"Vendedores encontrados: {len(vendedores)}")
    print()


def test_authentication():
    """Prueba de autenticación completa"""
    print("=" * 60)
    print("4. PRUEBA DE AUTENTICACIÓN COMPLETA")
    print("=" * 60)
    
    test_cases = [
        ("admin@ferreteria.com", "admin123", True),
        ("vendedor@ferreteria.com", "vend123", True),
        ("almacen@ferreteria.com", "alm123", True),
        ("admin@ferreteria.com", "wrongpass", False),
        ("noexiste@test.com", "anypass", False),
    ]
    
    for email, password, should_succeed in test_cases:
        user = user_repository.find_by_email(email)
        
        if user and verify_password(password, user.get('password_hash')):
            result = "✓ ÉXITO"
            status = "autenticado"
        else:
            result = "✗ FALLO"
            status = "rechazado"
        
        expected = "✓" if should_succeed else "✗"
        match = "✓" if (result == "✓ ÉXITO") == should_succeed else "❌"
        
        print(f"{match} {email} / {password}: {result} ({status})")
    print()


def main():
    """Función principal"""
    print()
    print("="*60)
    print("PRUEBAS DE AUTENTICACIÓN - ERP FERRETERÍA")
    print("="*60)
    print()
    
    try:
        test_password_hashing()
        test_jwt_tokens()
        test_user_repository()
        test_authentication()
        
        print("="*60)
        print("✓ TODAS LAS PRUEBAS COMPLETADAS")
        print("="*60)
        print()
        print("Próximos pasos:")
        print("1. Iniciar el servidor: python run.py")
        print("2. Abrir Swagger UI: http://localhost:8000/api/docs")
        print("3. Probar login con: admin@ferreteria.com / admin123")
        print("4. Copiar el token y usarlo en 'Authorize' (🔒)")
        print()
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
