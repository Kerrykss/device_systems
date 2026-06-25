# app/models/user_model.py

from sqlalchemy import Integer, String, Boolean, DateTime, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación: un usuario puede tener muchos préstamos
    loans = relationship("Loan", back_populates="user")