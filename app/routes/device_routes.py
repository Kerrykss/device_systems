# app/routes/device_routes.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device_service

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get(
    "/",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Retorna todos los dispositivos con filtros opcionales."
)
def list_devices(
    device_type: Optional[str] = Query(None),
    is_available: Optional[bool] = Query(None),
    brand: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return device_service.get_all_devices(db, device_type, is_available, brand, search)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID"
)
def get_device(device_id: int, db: Session = Depends(get_db)):
    return device_service.get_device_by_id(db, device_id)


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=201,
    summary="Crear dispositivo"
)
def create_device(data: DeviceCreate, db: Session = Depends(get_db)):
    return device_service.create_device(db, data)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo"
)
def update_device(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db)):
    return device_service.update_device(db, device_id, data)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcialmente"
)
def patch_device(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db)):
    return device_service.update_device(db, device_id, data)


@router.delete(
    "/{device_id}",
    status_code=204,
    summary="Eliminar dispositivo"
)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device_service.delete_device(db, device_id)