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

# Rutas de la API
from app.routes.user_routes import router as user_router


# =========================
# CREACIÓN DE TABLAS
# =========================
# SQLAlchemy crea automáticamente todas las tablas
# registradas en los modelos que heredan de Base.
# Si la base de datos no existe, SQLite la crea.
Base.metadata.create_all(bind=engine)


# =========================
# CONFIGURACIÓN DE FASTAPI
# =========================

app = FastAPI(
    title="Device Systems API",
    description=(
        "API REST para la gestión de usuarios del sistema Device Systems. "
        "Permite crear, consultar, actualizar y eliminar usuarios "
        "utilizando persistencia de datos con SQLAlchemy y SQLite."
    ),
    version="2.0.0",
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
    """
    Captura cualquier excepción relacionada con SQLAlchemy
    y devuelve una respuesta controlada al cliente.
    """

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

# Todas las rutas definidas en user_routes.py
# serán agregadas a la aplicación principal.
app.include_router(user_router)


# =========================
# RUTA PRINCIPAL
# =========================

@app.get(
    "/",
    tags=["Root"],
    summary="Bienvenida al sistema"
)
def root():
    """
    Endpoint principal de verificación.
    Permite comprobar que la API está funcionando correctamente.
    """

    return {
        "message": "Bienvenido a Device Systems API v2.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }