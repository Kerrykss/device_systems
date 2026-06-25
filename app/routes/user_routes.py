from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services import user_service
from app.models.user_model import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna todos los usuarios (requiere autenticación)"
)
def list_users(
    role: Optional[str] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado"),
    order_by: Optional[str] = Query(None, description="Ordenar por"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista usuarios. Requiere estar autenticado."""
    return user_service.get_users(db, role=role, is_active=is_active, order_by=order_by)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico (requiere autenticación)"
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene usuario por ID. Requiere estar autenticado."""
    return user_service.get_user_by_id(db, user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario (solo admin)"
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Crea usuario. Solo admin."""
    return user_service.create_user(db, user_data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo",
    description="Actualiza todos los campos (solo admin)"
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Actualiza usuario completo. Solo admin."""
    return user_service.update_user(db, user_id, user_data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Actualiza campos específicos (solo admin)"
)
def patch_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Actualiza usuario parcialmente. Solo admin."""
    return user_service.patch_user(db, user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario (solo admin)"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Elimina usuario. Solo admin."""
    user_service.delete_user(db, user_id)