# app/schemas/loan_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    status: Optional[str] = None
    return_date: Optional[datetime] = None


class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class DeviceBasic(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: UserBasic
    device: DeviceBasic

    model_config = {"from_attributes": True}