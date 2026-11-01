# Guía de Autenticación - ERP Ferretería

Sistema de autenticación JWT con control de acceso basado en roles.

## 🔐 Sistema de Autenticación

### Tecnologías
- **JWT (JSON Web Tokens)**: Tokens sin estado para autenticación
- **BCrypt**: Hash seguro de contraseñas
- **OAuth2**: Esquema de autenticación estándar
- **FastAPI Security**: Dependencias de seguridad integradas

### Roles de Usuario

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **admin** | Administrador del sistema | Acceso completo a todos los módulos |
| **vendedor** | Vendedor | Acceso a Ventas y Clientes |
| **almacenero** | Encargado de almacén | Acceso a Inventario y Compras |

---

## 📝 Credenciales de Prueba

```
👨‍💼 Administrador:
Email: admin@ferreteria.com
Password: admin123
Role: admin

👨‍💼 Vendedor:
Email: vendedor@ferreteria.com
Password: vend123
Role: vendedor

👨‍💼 Almacenero:
Email: almacen@ferreteria.com
Password: alm123
Role: almacenero
```

---

## 🚀 Cómo Usar la API

### 1. Iniciar Sesión

**Endpoint:** `POST /api/v1/auth/login`

**Request:**
```json
{
  "email": "admin@ferreteria.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Usar el Token

Incluye el token en el header `Authorization` de todas las peticiones:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Obtener Usuario Actual

**Endpoint:** `GET /api/v1/auth/me`

**Headers:**
```http
Authorization: Bearer {tu_token}
```

**Response:**
```json
{
  "id": 1,
  "email": "admin@ferreteria.com",
  "nombre": "Carlos",
  "apellido": "Mendoza",
  "role": "admin",
  "activo": true,
  "created_at": "2026-10-01 08:00:00"
}
```

---

## 🧪 Probar en Swagger UI

### Paso 1: Abrir Swagger
```
http://localhost:8000/api/docs
```

### Paso 2: Hacer Login
1. Busca el endpoint `POST /api/v1/auth/login/form`
2. Click en "Try it out"
3. Ingresa:
   - **username**: admin@ferreteria.com
   - **password**: admin123
4. Click "Execute"
5. Copia el `access_token` de la respuesta

### Paso 3: Autorizar
1. Click en el botón **"Authorize"** 🔒 (arriba a la derecha)
2. Pega el token en el campo "Value"
3. Click "Authorize"
4. Click "Close"

### Paso 4: Probar Endpoints Protegidos
Ahora puedes probar cualquier endpoint que requiera autenticación:
- `GET /api/v1/auth/me` - Ver tu perfil
- `GET /api/v1/auth/test/roles` - Probar roles
- `GET /api/v1/auth/test/admin-only` - Solo admin

---

## 💻 Usar con cURL

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ferreteria.com","password":"admin123"}'
```

### Usar Token
```bash
# Guardar token
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Hacer petición autenticada
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🐍 Usar con Python

### Ejemplo con requests
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "email": "admin@ferreteria.com",
        "password": "admin123"
    }
)

token = response.json()["access_token"]
print(f"Token: {token}")

# Usar token
headers = {"Authorization": f"Bearer {token}"}

# Obtener perfil
profile = requests.get(
    "http://localhost:8000/api/v1/auth/me",
    headers=headers
)

print(profile.json())
```

---

## 🔒 Control de Acceso por Roles

### En FastAPI (Backend)

#### Ejemplo 1: Solo Admin
```python
from fastapi import Depends
from app.security.dependencies import require_role
from app.schemas.auth import UserResponse

@router.get("/admin-only")
async def admin_endpoint(
    current_user: UserResponse = Depends(require_role(["admin"]))
):
    return {"message": "Solo admin puede ver esto"}
```

#### Ejemplo 2: Admin o Vendedor
```python
@router.get("/ventas")
async def listar_ventas(
    current_user: UserResponse = Depends(require_role(["admin", "vendedor"]))
):
    return {"ventas": [...]}
```

#### Ejemplo 3: Todos los autenticados
```python
from app.security.dependencies import get_current_active_user

@router.get("/public")
async def endpoint_publico(
    current_user: UserResponse = Depends(get_current_active_user)
):
    return {"message": "Accesible para todos los usuarios autenticados"}
```

---

## 🔄 Cambiar Contraseña

**Endpoint:** `POST /api/v1/auth/change-password`

**Headers:**
```http
Authorization: Bearer {tu_token}
```

**Request:**
```json
{
  "current_password": "admin123",
  "new_password": "newpassword456"
}
```

**Response:**
```json
{
  "message": "Contraseña cambiada exitosamente"
}
```

---

## 👥 Registrar Nuevo Usuario

**Endpoint:** `POST /api/v1/auth/register`

**Requiere:** Rol admin

**Headers:**
```http
Authorization: Bearer {admin_token}
```

**Request:**
```json
{
  "email": "nuevo@ferreteria.com",
  "nombre": "Juan",
  "apellido": "Pérez",
  "password": "password123",
  "role": "vendedor"
}
```

**Response:**
```json
{
  "id": 4,
  "email": "nuevo@ferreteria.com",
  "nombre": "Juan",
  "apellido": "Pérez",
  "role": "vendedor",
  "activo": true,
  "created_at": "2026-10-31 18:00:00"
}
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# Seguridad
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Generar SECRET_KEY seguro

```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🔍 Endpoints de Prueba

| Endpoint | Roles Permitidos | Descripción |
|----------|------------------|-------------|
| `GET /api/v1/auth/test/roles` | Todos | Ver permisos del usuario actual |
| `GET /api/v1/auth/test/admin-only` | admin | Solo administradores |
| `GET /api/v1/auth/test/vendedor` | admin, vendedor | Admin y vendedores |
| `GET /api/v1/auth/test/almacenero` | admin, almacenero | Admin y almaceneros |

---

## 🛡️ Seguridad

### Características de Seguridad

✅ **Contraseñas hasheadas** con BCrypt (12 rounds)
✅ **Tokens JWT** con expiración configurable
✅ **Validación de roles** en cada endpoint
✅ **Usuarios inactivos** no pueden autenticarse
✅ **Protección contra** fuerza bruta (implementar rate limiting en producción)

### Buenas Prácticas

1. **Cambiar SECRET_KEY** en producción
2. **Usar HTTPS** en producción
3. **Tokens de corta duración** (30 min por defecto)
4. **No compartir tokens** entre usuarios
5. **Logout del frontend** (eliminar token del almacenamiento local)

---

## 🧪 Ejecutar Pruebas

```bash
# Pruebas de autenticación
python test_auth.py

# Iniciar servidor
python run.py

# Abrir Swagger UI
# http://localhost:8000/api/docs
```

---

## 📊 Flujo de Autenticación

```
┌─────────┐                 ┌─────────┐                 ┌──────────┐
│ Cliente │                 │   API   │                 │   CSV    │
└────┬────┘                 └────┬────┘                 └────┬─────┘
     │                           │                           │
     │  POST /auth/login         │                           │
     │  {email, password}        │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │                           │  Buscar usuario           │
     │                           ├──────────────────────────>│
     │                           │                           │
     │                           │  Usuario encontrado       │
     │                           │<──────────────────────────┤
     │                           │                           │
     │                           │  Verificar password       │
     │                           │  (bcrypt)                 │
     │                           │                           │
     │                           │  Generar JWT              │
     │                           │                           │
     │  {access_token}           │                           │
     │<──────────────────────────┤                           │
     │                           │                           │
     │  GET /api/resource        │                           │
     │  Authorization: Bearer... │                           │
     ├──────────────────────────>│                           │
     │                           │                           │
     │                           │  Decodificar JWT          │
     │                           │  Verificar expiración     │
     │                           │  Verificar rol            │
     │                           │                           │
     │  {data}                   │                           │
     │<──────────────────────────┤                           │
     │                           │                           │
```

---

## ❓ Preguntas Frecuentes

### ¿Cuánto dura el token?
30 minutos por defecto. Configurable en `.env` con `ACCESS_TOKEN_EXPIRE_MINUTES`.

### ¿Cómo renovar el token?
Hacer login nuevamente para obtener un nuevo token.

### ¿Los tokens se almacenan en el servidor?
No, los JWT son sin estado. El servidor solo valida la firma.

### ¿Puedo tener múltiples sesiones?
Sí, cada login genera un nuevo token independiente.

### ¿Cómo hago logout?
En el frontend, simplemente elimina el token del almacenamiento local.

---

**Última actualización**: 31 de octubre de 2026  
**Versión**: 1.0
