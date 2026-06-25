from typing import Generator
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia que provee una sesión de base de datos por request.
    Se cierra automáticamente al terminar cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        