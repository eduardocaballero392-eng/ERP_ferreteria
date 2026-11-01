"""
Utilidades para manejo de contraseñas
"""
from passlib.context import CryptContext

# Contexto de encriptación con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con el hash
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada
    
    Returns:
        True si coinciden, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash de la contraseña usando bcrypt
    
    Args:
        password: Contraseña en texto plano
    
    Returns:
        Hash de la contraseña
    """
    return pwd_context.hash(password)
