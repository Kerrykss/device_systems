# app/schemas/device_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DeviceCreate(BaseModel):
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None
    is_available: bool = True


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None
    is_available: bool
    created_at: datetime

    model_config = {"from_attributes": True}