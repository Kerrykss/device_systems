from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


def create_user(db: Session, user_data: UserCreate) -> User:
    """Crea un nuevo usuario en la base de datos."""
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el email '{user_data.email}'"
        )
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email duplicado. Ya existe un usuario con ese email."
        )


def get_users(
    db: Session,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None
) -> List[User]:
    """Lista todos los usuarios con filtros opcionales."""
    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if order_by == "name":
        query = query.order_by(User.name)
    elif order_by == "created_at":
        query = query.order_by(User.created_at)

    return query.all()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Busca un usuario por su ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca un usuario por su email."""
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    """Actualiza completamente un usuario (PUT)."""
    user = get_user_by_id(db, user_id)

    # Verificar email duplicado si cambió
    if user.email != user_data.email:
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el email '{user_data.email}'"
            )

    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar: email duplicado."
        )


def patch_user(db: Session, user_id: int, user_data: UserPatch) -> User:
    """Actualiza parcialmente un usuario (PATCH)."""
    user = get_user_by_id(db, user_id)

    update_data = user_data.model_dump(exclude_unset=True)

    # Verificar email duplicado si se está cambiando
    if "email" in update_data and update_data["email"] != user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el email '{update_data['email']}'"
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar: email duplicado."
        )


def delete_user(db: Session, user_id: int) -> None:
    """Elimina un usuario por su ID."""
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()