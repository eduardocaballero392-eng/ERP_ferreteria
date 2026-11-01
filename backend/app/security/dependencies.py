"""
Dependencias de autenticación y autorización para FastAPI
"""
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.jwt import decode_access_token
from app.repositories.user_repository import user_repository
from app.schemas.auth import UserResponse

# OAuth2 scheme para extraer el token del header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    Obtiene el usuario actual desde el token JWT
    
    Args:
        token: Token JWT del header Authorization
    
    Returns:
        Datos del usuario actual
    
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodificar token
    token_data = decode_access_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    # Buscar usuario
    user = user_repository.find_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    
    # Verificar que esté activo
    if not user.get('activo') in [True, 'True', '1', 1]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    return UserResponse(**user)


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Obtiene el usuario actual y verifica que esté activo
    
    Args:
        current_user: Usuario actual
    
    Returns:
        Usuario activo
    
    Raises:
        HTTPException: Si el usuario está inactivo
    """
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user


class RoleChecker:
    """
    Clase para verificar roles de usuario
    Uso: depends=Depends(RoleChecker(["admin", "vendedor"]))
    """
    
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: UserResponse = Depends(get_current_active_user)) -> UserResponse:
        """
        Verifica que el usuario tenga uno de los roles permitidos
        
        Args:
            current_user: Usuario actual
        
        Returns:
            Usuario si tiene permiso
        
        Raises:
            HTTPException: Si el usuario no tiene permiso
        """
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene permisos suficientes. Se requiere uno de estos roles: {', '.join(self.allowed_roles)}"
            )
        return current_user


def require_role(allowed_roles: List[str]):
    """
    Función helper para crear un RoleChecker
    
    Args:
        allowed_roles: Lista de roles permitidos
    
    Returns:
        Instancia de RoleChecker
    
    Ejemplo:
        @router.get("/admin-only")
        async def admin_endpoint(user = Depends(require_role(["admin"]))):
            return {"message": "Solo admin"}
    """
    return RoleChecker(allowed_roles)
