"""
Endpoints de Autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict
from app.schemas.auth import (
    Token, 
    LoginRequest, 
    UserCreate, 
    UserResponse, 
    ChangePasswordRequest
)
from app.services.auth_service import auth_service
from app.security.dependencies import get_current_active_user, require_role

router = APIRouter()


@router.get("/setup-status", summary="Verificar configuración inicial")
async def get_setup_status():
    return {"setup_required": auth_service.setup_required()}


@router.post("/setup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Crear el primer administrador")
async def setup_first_admin(user_data: UserCreate):
    return auth_service.setup_first_admin(user_data)


@router.post("/login", response_model=Token, summary="Iniciar sesión")
async def login(login_data: LoginRequest):
    """
    Inicia sesión y genera un token JWT
    
    **Cuenta inicial:** admin / admin123
    
    **Returns:**
    - Token JWT para usar en el header Authorization: Bearer {token}
    """
    return auth_service.login(login_data)


@router.post("/login/form", response_model=Token, summary="Login con OAuth2 form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Iniciar sesión usando OAuth2PasswordRequestForm (compatible con Swagger UI)
    
    **Cuenta inicial:** admin / admin123
    """
    # Usar username directamente en lugar de email
    return auth_service.login_with_username(form_data.username, form_data.password)


@router.post(
    "/register", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario"
)
async def register(
    user_data: UserCreate,
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Registra un nuevo usuario en el sistema
    
    **Requiere rol:** admin
    
    **Roles disponibles:**
    - admin: Acceso completo al sistema
    - vendedor: Acceso a Ventas y Clientes
    - almacenero: Acceso a Inventario y Compras
    """
    return auth_service.register(user_data)


@router.get("/me", response_model=UserResponse, summary="Obtener usuario actual")
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Obtiene la información del usuario autenticado actualmente
    
    **Requiere:** Token JWT válido
    """
    return current_user


@router.post("/change-password", response_model=Dict[str, str], summary="Cambiar contraseña")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Cambia la contraseña del usuario actual
    
    **Requiere:** Token JWT válido y contraseña actual correcta
    """
    return auth_service.change_password(current_user.id, password_data)


@router.get("/test/roles", summary="Probar acceso por roles")
async def test_roles(current_user: UserResponse = Depends(get_current_active_user)):
    """
    Endpoint de prueba para verificar roles
    
    **Accesible por:** Todos los usuarios autenticados
    """
    return {
        "message": f"Hola {current_user.nombre} {current_user.apellido}",
        "role": current_user.role,
        "email": current_user.email,
        "permissions": {
            "admin": current_user.role == "admin",
            "vendedor": current_user.role in ["admin", "vendedor"],
            "almacenero": current_user.role in ["admin", "almacenero"]
        }
    }


@router.get("/test/admin-only", summary="Prueba - Solo Admin")
async def test_admin_only(
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    """
    Endpoint de prueba accesible solo para administradores
    
    **Requiere rol:** admin
    """
    return {
        "message": "Acceso exitoso - Eres administrador",
        "user": current_user.nombre
    }


@router.get("/test/vendedor", summary="Prueba - Vendedor o Admin")
async def test_vendedor(
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    """
    Endpoint de prueba accesible para vendedores y administradores
    
    **Requiere rol:** admin o vendedor
    """
    return {
        "message": "Acceso exitoso - Puedes gestionar ventas",
        "user": current_user.nombre,
        "role": current_user.role
    }


@router.get("/test/almacenero", summary="Prueba - Almacenero o Admin")
async def test_almacenero(
    current_user: UserResponse = Depends(require_role(["admin", "almacenero"]))
):
    """
    Endpoint de prueba accesible para almaceneros y administradores
    
    **Requiere rol:** admin o almacenero
    """
    return {
        "message": "Acceso exitoso - Puedes gestionar inventario",
        "user": current_user.nombre,
        "role": current_user.role
    }
