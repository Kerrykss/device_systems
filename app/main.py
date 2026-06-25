# app/main.py

# =========================
# IMPORTACIONES
# =========================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

# Conexión y base de datos
from app.database.connection import engine, Base

# Importar modelos para que SQLAlchemy los registre
from app.models.user_model import User
from app.models.device_model import Device  # LÍNEA AGREGADA
from app.models.loan_model import Loan      # LÍNEA AGREGADA

# Rutas de la API
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router  # LÍNEA AGREGADA
from app.routes.loan_routes import router as loan_router      # LÍNEA AGREGADA


# =========================
# CREACIÓN DE TABLAS
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# CONFIGURACIÓN DE FASTAPI
# =========================

app = FastAPI(
    title="Device Systems API",
    description=(
        "API REST para la gestión de usuarios, dispositivos y préstamos "
        "del sistema Device Systems. Utiliza SQLAlchemy, Alembic y SQLite."
    ),
    version="3.0.0",  # ACTUALIZADO
    contact={
        "name": "Device Systems"
    },
    license_info={
        "name": "MIT"
    }
)


# =========================
# MANEJO GLOBAL DE ERRORES
# =========================

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                "Error interno de base de datos. "
                "Por favor, intenta nuevamente."
            )
        }
    )


# =========================
# REGISTRO DE RUTAS
# =========================

app.include_router(user_router)
app.include_router(device_router)  # LÍNEA AGREGADA
app.include_router(loan_router)    # LÍNEA AGREGADA


# =========================
# RUTA PRINCIPAL
# =========================

@app.get(
    "/",
    tags=["Root"],
    summary="Bienvenida al sistema"
)
def root():
    return {
        "message": "Bienvenido a Device Systems API v3.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }