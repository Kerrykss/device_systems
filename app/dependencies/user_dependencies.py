# app/dependencies/user_dependencies.py

from fastapi import HTTPException, Header
from app.data.users_db import users_db


def get_user_or_404(user_id: int) -> dict:
    """Busca un usuario por ID. Si no existe lanza 404."""
    user = next((u for u in users_db if u["id"] == user_id), None)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con id {user_id} no encontrado"
        )

    return user


def verify_email_not_exists(email: str, exclude_id: int = None) -> None:
    """Verifica que el correo no esté registrado por otro usuario."""
    for u in users_db:
        if u["email"] == email and u["id"] != exclude_id:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )


def validate_role(role: str) -> str:
    """Valida que el rol sea uno de los permitidos."""
    allowed_roles = ["admin", "support", "user"]

    if role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Rol no permitido. Los roles válidos son: {allowed_roles}"
        )

    return role


def get_api_settings() -> dict:
    """Retorna configuración general de la API."""
    return {
        "app_name": "device_systems",
        "version": "2.0.0",
        "author": "Kerry"
    }


def verify_api_key(x_api_key: str = Header(default=None)) -> str:
    """Simula autenticación básica mediante cabecera X-API-Key."""
    valid_key = "device-secret-2024"

    if x_api_key != valid_key:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida o no proporcionada"
        )

    return x_api_key