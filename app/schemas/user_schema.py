# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional


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

# Modelo para PUT (actualización completa — todos los campos requeridos)
class UserUpdate(BaseModel):
    name: str = Field(min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: EmailStr = Field(description="Correo electrónico válido")
    role: RoleEnum = Field(description="Rol permitido: admin, support, user")
    is_active: bool = Field(description="Estado del usuario: activo o inactivo")


# Modelo para PATCH (actualización parcial — todos los campos opcionales)
class UserPartialUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(default=None, description="Correo electrónico válido")
    role: Optional[RoleEnum] = Field(default=None, description="Rol permitido: admin, support, user")
    is_active: Optional[bool] = Field(default=None, description="Estado del usuario")