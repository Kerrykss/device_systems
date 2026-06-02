# app/routes/user_routes.py

from fastapi import APIRouter, Depends, Response, status
from typing import Optional

from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserPartialUpdate
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    partial_update_user,
    delete_user,
)
from app.dependencies.user_dependencies import (
    get_user_or_404,
    get_api_settings,
    verify_api_key,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def add_custom_headers(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0.0"


# GET /users — listar todos los usuarios con filtros opcionales
@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna la lista completa de usuarios. Permite filtrar por rol y/o estado activo.",
    response_description="Lista de usuarios encontrados",
)
def list_users(
    response: Response,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
):
    add_custom_headers(response)
    return get_all_users(role, is_active)


# GET /users/{user_id} — obtener usuario por ID
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna la información de un usuario específico según su ID.",
    response_description="Usuario encontrado",
)
def get_user(
    response: Response,
    user: dict = Depends(get_user_or_404),
):
    add_custom_headers(response)
    return user


# POST /users — crear nuevo usuario
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario en el sistema. El correo debe ser único y el rol debe ser válido.",
    response_description="Usuario creado exitosamente",
)
def post_user(
    user: UserCreate,
    response: Response,
):
    add_custom_headers(response)
    return create_user(user)


# PUT /users/{user_id} — actualización completa
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo",
    description="Reemplaza completamente la información de un usuario existente. Todos los campos son requeridos.",
    response_description="Usuario actualizado exitosamente",
)
def put_user(
    user_id: int,
    user: UserUpdate,
    response: Response,
):
    add_custom_headers(response)
    return update_user(user_id, user)


# PATCH /users/{user_id} — actualización parcial
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Actualiza solo los campos enviados de un usuario existente. Se debe enviar al menos un campo.",
    response_description="Usuario actualizado parcialmente",
)
def patch_user(
    user_id: int,
    user: UserPartialUpdate,
    response: Response,
):
    add_custom_headers(response)
    return partial_update_user(user_id, user)


# DELETE /users/{user_id} — eliminar usuario
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente del sistema según su ID.",
    response_description="Usuario eliminado exitosamente",
)
def remove_user(
    user_id: int,
    user: dict = Depends(get_user_or_404),
):
    delete_user(user_id)