from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


# Modelo de entrada (lo que recibe el POST)
class UserCreate(BaseModel):
    name: str = Field(min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: EmailStr = Field(description="Correo electrónico válido")
    role: RoleEnum = Field(description="Rol permitido: admin, support, user")
    is_active: bool = Field(description="Estado del usuario: activo o inactivo")


# Modelo de salida (lo que devuelve la API)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum
    is_active: bool
