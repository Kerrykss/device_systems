from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services import loan_service
from app.models.user_model import User

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.get(
    "/details",
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos con detalles",
    description="Retorna préstamos con usuario y dispositivo (admin o support)"
)
def loan_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    """Obtiene detalles de préstamos. Solo admin o support."""
    return loan_service.get_loan_details(db)


@router.get(
    "/",
    response_model=List[LoanResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos con filtros"
)
def list_loans(
    status: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista préstamos. Requiere autenticación."""
    return loan_service.get_all_loans(db, status, user_email, device_type)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener préstamo por ID"
)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtiene préstamo. Requiere autenticación."""
    return loan_service.get_loan_by_id(db, loan_id)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Crea nuevo préstamo (requiere autenticación)"
)
def create_loan(
    data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crea préstamo. Requiere autenticación."""
    return loan_service.create_loan(db, data)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Devolver dispositivo",
    description="Marca préstamo como devuelto (admin o support)"
)
def return_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    """Devuelve dispositivo. Solo admin o support."""
    return loan_service.return_loan(db, loan_id)