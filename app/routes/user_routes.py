from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Se puede filtrar por rol, estado y ordenar por nombre o fecha de creación."
)
def list_users(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    order_by: Optional[str] = Query(None, description="Ordenar por: name, created_at"),
    db: Session = Depends(get_db)
):
    return user_service.get_users(db, role=role, is_active=is_active, order_by=order_by)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico por su ID.",
    responses={404: {"description": "Usuario no encontrado"}}
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario en la base de datos.",
    responses={
        400: {"description": "Email duplicado o datos inválidos"},
        422: {"description": "Error de validación"}
    }
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo",
    description="Actualiza todos los campos de un usuario (reemplazo completo).",
    responses={
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Email duplicado"}
    }
)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user_data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Actualiza solo los campos enviados de un usuario.",
    responses={
        404: {"description": "Usuario no encontrado"},
        400: {"description": "Email duplicado"}
    }
)
def patch_user(user_id: int, user_data: UserPatch, db: Session = Depends(get_db)):
    return user_service.patch_user(db, user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario por su ID.",
    responses={404: {"description": "Usuario no encontrado"}}
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)