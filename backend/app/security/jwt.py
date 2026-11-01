"""
Utilidades para manejo de JSON Web Tokens (JWT)
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings
from app.schemas.auth import TokenData


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token de acceso JWT
    
    Args:
        data: Diccionario con los datos a incluir en el token
        expires_delta: Tiempo de expiración opcional
    
    Returns:
        Token JWT como string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decodifica y valida un token JWT
    
    Args:
        token: Token JWT como string
    
    Returns:
        TokenData si el token es válido, None en caso contrario
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        
        if email is None:
            return None
        
        token_data = TokenData(email=email, user_id=user_id, role=role)
        return token_data
    
    except JWTError:
        return None


def verify_token(token: str) -> bool:
    """
    Verifica si un token es válido
    
    Args:
        token: Token JWT como string
    
    Returns:
        True si el token es válido, False en caso contrario
    """
    token_data = decode_access_token(token)
    return token_data is not None
