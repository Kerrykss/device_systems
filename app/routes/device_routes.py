from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support, require_admin
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device_service
from app.models.user_model import User

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get(
    "/",
    response_model=List[DeviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar dispositivos",
    description="Retorna todos los dispositivos (requiere autenticación)"
)
def list_devices(
    device_type: Optional[str] = Query(None),
    is_available: Optional[bool] = Query(None),
    brand: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista dispositivos. Requiere estar autenticado."""
    return device_service.get_all_devices(db, device_type, is_available, brand, search)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener dispositivo por ID"
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene dispositivo por ID. Requiere autenticación."""
    return device_service.get_device_by_id(db, device_id)


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Crea nuevo dispositivo (admin o support)"
)
def create_device(
    data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    """Crea dispositivo. Solo admin o support."""
    return device_service.create_device(db, data)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo completo",
    description="Actualiza todos los campos (admin o support)"
)
def update_device(
    device_id: int,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    """Actualiza dispositivo. Solo admin o support."""
    return device_service.update_device(db, device_id, data)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo parcialmente"
)
def patch_device(
    device_id: int,
    data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    """Actualiza dispositivo parcialmente. Solo admin o support."""
    return device_service.update_device(db, device_id, data)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina dispositivo (solo admin)"
)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Elimina dispositivo. Solo admin."""
    device_service.delete_device(db, device_id)