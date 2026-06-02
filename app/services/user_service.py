# app/services/user_service.py

from fastapi import HTTPException
from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserPartialUpdate


def get_all_users(role: str | None, is_active: bool | None) -> list[dict]:
    result = users_db

    if role is not None:
        result = [u for u in result if u["role"] == role]

    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]

    return result


def get_user_by_id(user_id: int) -> dict:
    user = next((u for u in users_db if u["id"] == user_id), None)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con id {user_id} no encontrado"
        )

    return user


def create_user(user: UserCreate) -> dict:
    # Verificar email duplicado
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

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


def update_user(user_id: int, user: UserUpdate) -> dict:
    existing = get_user_by_id(user_id)

    # Verificar email duplicado (ignorando el usuario actual)
    if any(u["email"] == user.email and u["id"] != user_id for u in users_db):
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado por otro usuario"
        )

    existing["name"] = user.name
    existing["email"] = user.email
    existing["role"] = user.role
    existing["is_active"] = user.is_active

    return existing


def partial_update_user(user_id: int, user: UserPartialUpdate) -> dict:
    existing = get_user_by_id(user_id)

    # Verificar que se envió al menos un campo
    update_data = user.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar"
        )

    # Verificar email duplicado si se está cambiando el email
    if "email" in update_data:
        if any(u["email"] == update_data["email"] and u["id"] != user_id for u in users_db):
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado por otro usuario"
            )

    for key, value in update_data.items():
        existing[key] = value

    return existing


def delete_user(user_id: int) -> None:
    user = get_user_by_id(user_id)
    users_db.remove(user)