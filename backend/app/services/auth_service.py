"""
Servicio de Autenticación - Lógica de negocio
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.schemas.auth import LoginRequest, UserCreate, UserResponse, Token, ChangePasswordRequest
from app.repositories.user_repository import user_repository
from app.security.password import get_password_hash, verify_password
from app.security.jwt import create_access_token
from app.core.config import settings


class AuthService:
    """Servicio de autenticación y gestión de usuarios"""
    
    def __init__(self):
        self.user_repo = user_repository
    
    def login(self, login_data: LoginRequest) -> Token:
        """
        Autentica un usuario y genera un token JWT
        
        Args:
            login_data: Datos de login (email y password)
        
        Returns:
            Token JWT
        
        Raises:
            HTTPException: Si las credenciales son inválidas
        """
        # Buscar usuario por email
        user = self.user_repo.find_by_email(login_data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar que el usuario esté activo
        if not user.get('activo') in [True, 'True', '1', 1]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar contraseña
        if not verify_password(login_data.password, user.get('password_hash')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Crear token JWT
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.get('email'),
                "user_id": user.get('id'),
                "role": user.get('role')
            },
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    def login_with_username(self, username: str, password: str) -> Token:
        """
        Autentica un usuario usando username y genera un token JWT
        
        Args:
            username: Nombre de usuario
            password: Contraseña
        
        Returns:
            Token JWT
        
        Raises:
            HTTPException: Si las credenciales son inválidas
        """
        # Buscar usuario por username
        user = self.user_repo.find_by_username(username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar que el usuario esté activo
        if not user.get('activo') in [True, 'True', '1', 1]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar contraseña
        if not verify_password(password, user.get('password_hash')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Crear token JWT
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.get('email'),
                "user_id": user.get('id'),
                "role": user.get('role')
            },
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    def register(self, user_data: UserCreate) -> UserResponse:
        """
        Registra un nuevo usuario
        
        Args:
            user_data: Datos del nuevo usuario
        
        Returns:
            Datos del usuario creado
        
        Raises:
            HTTPException: Si el email ya existe o el rol es inválido
        """
        # Validar rol
        valid_roles = ["admin", "vendedor", "almacenero"]
        if user_data.role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Rol inválido. Debe ser uno de: {', '.join(valid_roles)}"
            )
        
        # Verificar si el email ya existe
        existing_user = self.user_repo.find_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {user_data.email} ya está registrado"
            )
        
        # Hashear contraseña
        password_hash = get_password_hash(user_data.password)
        
        # Crear usuario
        new_user_data = {
            "email": user_data.email,
            "nombre": user_data.nombre,
            "apellido": user_data.apellido,
            "password_hash": password_hash,
            "role": user_data.role,
            "activo": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            created_user = self.user_repo.create(new_user_data)
            return UserResponse(**created_user)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear usuario"
            )
    
    def get_current_user(self, user_id: int) -> UserResponse:
        """
        Obtiene los datos del usuario actual
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Datos del usuario
        
        Raises:
            HTTPException: Si el usuario no existe
        """
        user = self.user_repo.find_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return UserResponse(**user)
    
    def change_password(self, user_id: int, password_data: ChangePasswordRequest) -> Dict[str, str]:
        """
        Cambia la contraseña de un usuario
        
        Args:
            user_id: ID del usuario
            password_data: Contraseña actual y nueva
        
        Returns:
            Mensaje de éxito
        
        Raises:
            HTTPException: Si la contraseña actual es incorrecta
        """
        user = self.user_repo.find_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not verify_password(password_data.current_password, user.get('password_hash')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
        
        # Actualizar contraseña
        new_password_hash = get_password_hash(password_data.new_password)
        success = self.user_repo.update(user_id, {
            "password_hash": new_password_hash,
            "updated_at": datetime.now().isoformat()
        })
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al cambiar contraseña"
            )
        
        return {"message": "Contraseña cambiada exitosamente"}


# Singleton
auth_service = AuthService()
