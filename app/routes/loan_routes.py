# app/routes/loan_routes.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services import loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos con detalle de usuario y dispositivo"
)
def loan_details(db: Session = Depends(get_db)):
    return loan_service.get_loan_details(db)


@router.get(
    "/",
    response_model=list[LoanResponse],
    summary="Listar préstamos con filtros opcionales"
)
def list_loans(
    status: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return loan_service.get_all_loans(db, status, user_email, device_type)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Obtener préstamo por ID"
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loan_by_id(db, loan_id)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=201,
    summary="Crear préstamo",
    description="Valida usuario, dispositivo y disponibilidad antes de crear el préstamo."
)
def create_loan(data: LoanCreate, db: Session = Depends(get_db)):
    return loan_service.create_loan(db, data)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Marca el préstamo como devuelto y libera el dispositivo."
)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.return_loan(db, loan_id)