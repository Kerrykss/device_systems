# app/services/loan_service.py

from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from datetime import datetime

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, UserBasic, DeviceBasic


def get_all_loans(
    db: Session,
    status: str = None,
    user_email: str = None,
    device_type: str = None
):
    query = db.query(Loan).join(User).join(Device)

    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.filter(Device.device_type == device_type)

    return query.all()


def get_loan_by_id(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan


def get_loan_details(db: Session):
    loans = db.query(Loan).options(
        joinedload(Loan.user),
        joinedload(Loan.device)
    ).all()

    result = []
    for loan in loans:
        result.append(LoanDetailResponse(
            loan_id=loan.id,
            status=loan.status,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
            user=UserBasic.model_validate(loan.user),
            device=DeviceBasic.model_validate(loan.device)
        ))
    return result


def get_loans_by_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Loan).filter(Loan.user_id == user_id).all()


def get_loans_by_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db.query(Loan).filter(Loan.device_id == device_id).all()


def create_loan(db: Session, data: LoanCreate):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    device = db.query(Device).filter(Device.id == data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not device.is_available:
        raise HTTPException(
            status_code=409,
            detail="El dispositivo no está disponible para préstamo"
        )

    loan = Loan(
        user_id=data.user_id,
        device_id=data.device_id,
        status="active"
    )
    device.is_available = False

    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan_id: int):
    loan = get_loan_by_id(db, loan_id)

    if loan.status == "returned":
        raise HTTPException(
            status_code=409,
            detail="Este préstamo ya fue devuelto"
        )

    loan.status = "returned"
    loan.return_date = datetime.utcnow()
    loan.device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan