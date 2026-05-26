from fastapi import APIRouter, HTTPException, Response
from typing import Optional
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

# Base de datos simulada en memoria
users_db: list[dict] = [
    {"id": 1, "name": "Carlos Pérez",   "email": "carlos@gmail.com",  "role": "admin",   "is_active": True},
    {"id": 2, "name": "Ana González",   "email": "ana@gmail.com",     "role": "support", "is_active": True},
    {"id": 3, "name": "Luis Martínez",  "email": "luis@gmail.com",    "role": "user",    "is_active": False},
    {"id": 4, "name": "María Rodríguez","email": "maria@gmail.com",   "role": "user",    "is_active": True},
]


def add_custom_headers(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"


# GET /users — listar todos los usuarios, con filtros opcionales por role e is_active
@router.get("/users", response_model=list[UserResponse])
def get_users(
    
    response: Response,
    role: Optional[str] = None,
    is_active: Optional[bool] = None
):
    add_custom_headers(response)
    result = users_db

    if role is not None:
        result = [u for u in result if u["role"] == role]

    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]

    return result


# GET /users/{user_id} — obtener usuario por ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, response: Response):
    add_custom_headers(response)

    user = next((u for u in users_db if u["id"] == user_id), None)

    if user is None:
        raise HTTPException(status_code=404, detail=f"Usuario con id {user_id} no encontrado")

    return user


# POST /users — crear nuevo usuario
@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, response: Response):
    add_custom_headers(response)

    # Verificar email duplicado
    email_exists = any(u["email"] == user.email for u in users_db)
    if email_exists:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Generar nuevo ID
    new_id = max(u["id"] for u in users_db) + 1

    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }

    users_db.append(new_user)
    return new_user
