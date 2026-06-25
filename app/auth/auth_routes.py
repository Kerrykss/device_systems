from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.dependencies.database_dependency import get_db
from app.schemas.auth_schema import UserRegister, UserLogin, Token, UserAuthResponse
from app.auth.auth_service import register_user, login_user
from app.dependencies.auth_dependency import get_current_user
from app.auth.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=UserAuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crea un nuevo usuario con contraseña segura"
)
@limiter.limit("3/minute")
def register(request: Request, user_data: UserRegister, db: Session = Depends(get_db)):
    """Registra un nuevo usuario"""
    user = register_user(db, user_data)
    return user


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login de usuario",
    description="Autentica usuario y retorna JWT token"
)
@limiter.limit("5/minute")
def login(request: Request, login_data: UserLogin, db: Session = Depends(get_db)):
    """Autentica usuario y retorna token"""
    token = login_user(db, login_data)
    return token


@router.get(
    "/me",
    response_model=UserAuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario actual",
    description="Retorna datos del usuario autenticado"
)
def get_me(current_user=Depends(get_current_user)):
    """Retorna datos del usuario autenticado"""
    return current_user