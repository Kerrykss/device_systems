from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserLogin, Token, TokenData
from app.auth.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status


def register_user(db: Session, user_data: UserRegister) -> User:
    """Registra un nuevo usuario"""
    # Verificar email único
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Crear usuario con hash de contraseña
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(db: Session, login_data: UserLogin) -> Token:
    """Autentica usuario y retorna token"""
    # Buscar usuario
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verificar contraseña
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verificar que esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    
   # Crear token
    token_data = TokenData(sub=str(user.id), email=user.email, role=user.role)
    access_token = create_access_token(data=token_data.dict())
    
    return Token(access_token=access_token, token_type="bearer")


def get_user_by_id(db: Session, user_id: int) -> User:
    """Obtiene usuario por ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user