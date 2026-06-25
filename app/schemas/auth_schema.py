
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """Schema para registro de usuario"""
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email único")
    password: str = Field(..., min_length=8, description="Contraseña segura")
    role: str = Field(default="user", description="admin, support, user")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Valida que la contraseña sea segura"""
        if len(v) < 8:
            raise ValueError("Mínimo 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("Al menos una mayúscula")
        if not any(c.islower() for c in v):
            raise ValueError("Al menos una minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("Al menos un número")
        if " " in v:
            raise ValueError("No puede contener espacios")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Valida que el rol sea permitido"""
        valid_roles = ["admin", "support", "user"]
        if v not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return v


class UserLogin(BaseModel):
    """Schema para login"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")


class Token(BaseModel):
    """Schema de respuesta de token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema de datos dentro del token"""
    sub: str  # user_id
    email: str
    role: str


class UserAuthResponse(BaseModel):
    """Schema de respuesta del usuario autenticado"""
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}