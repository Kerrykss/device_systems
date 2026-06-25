# app/models/device_model.py

from sqlalchemy import Integer, String, Boolean, DateTime, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=False, index=True)
    device_type = Column(String(50), nullable=False)  # laptop, tablet, proyector...
    brand = Column(String(100), nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación: un dispositivo puede aparecer en muchos préstamos
    loans = relationship("Loan", back_populates="device")