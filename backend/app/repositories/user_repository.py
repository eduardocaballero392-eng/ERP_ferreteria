"""
Repositorio de Usuarios - Capa de acceso a datos CSV
"""
from typing import Optional, List, Dict, Any
from app.core.csv_handler import get_csv_handler


class UserRepository:
    """Repositorio para operaciones CRUD de usuarios"""
    
    def __init__(self):
        self.csv_handler = get_csv_handler("usuarios.csv")
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Obtiene todos los usuarios activos"""
        users = self.csv_handler.read_all()
        return [u for u in users if u.get('activo') in [True, 'True', '1', 1]]
    
    def find_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca un usuario por ID"""
        return self.csv_handler.read_by_id(user_id)
    
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca un usuario por email"""
        users = self.csv_handler.find_by_field("email", email)
        return users[0] if users else None
    
    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Busca un usuario por username"""
        users = self.csv_handler.find_by_field("username", username)
        return users[0] if users else None
    
    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo usuario"""
        # Verificar si el email ya existe
        existing_user = self.find_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError(f"El email {user_data.get('email')} ya está registrado")
        
        # Crear usuario
        success = self.csv_handler.append(user_data)
        if not success:
            raise Exception("Error al crear usuario")
        
        # Retornar el usuario creado
        return self.find_by_email(user_data.get("email"))
    
    def update(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """Actualiza un usuario existente"""
        return self.csv_handler.update(user_id, user_data)
    
    def delete(self, user_id: int) -> bool:
        """Elimina (desactiva) un usuario"""
        return self.csv_handler.delete(user_id)
    
    def find_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Busca usuarios por rol"""
        return self.csv_handler.filter({"role": role, "activo": True})
    
    def authenticate(self, email: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """Verifica credenciales de usuario"""
        user = self.find_by_email(email)
        
        if not user:
            return None
        
        if not user.get('activo') in [True, 'True', '1', 1]:
            return None
        
        if user.get('password_hash') != password_hash:
            return None
        
        return user


# Singleton
user_repository = UserRepository()
