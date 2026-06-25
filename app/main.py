from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from slowapi.errors import RateLimitExceeded
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Conexión y base de datos
from app.database.connection import engine, Base

# Importar modelos para que SQLAlchemy los registre
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

# Rutas de la API
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router

# Middleware
from app.middlewares.request_middleware import RequestMiddleware

# Rate limiter compartido
from app.auth.limiter import limiter

# Crear tablas
Base.metadata.create_all(bind=engine)

# Configuración de FastAPI
app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos con autenticación OAuth2 y JWT",
    version="4.0.0",
    contact={
        "name": "Device Systems"
    },
    license_info={
        "name": "MIT"
    }
)

# Agregar state para rate limiter
app.state.limiter = limiter

# Configurar CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware personalizado
app.add_middleware(RequestMiddleware)

# Manejo de errores de rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."}
    )

# Manejo de errores de base de datos
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error. Please try again."}
    )

# Registrar rutas
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

# Ruta principal
@app.get(
    "/",
    tags=["Root"],
    summary="Bienvenida al sistema",
    description="Endpoint raíz que proporciona información de bienvenida"
)
def root():
    """Retorna mensaje de bienvenida"""
    return {
        "message": "Bienvenido a Device Systems API v4.0 (con autenticación)",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Verifica que la API esté funcionando"
)
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "app_name": os.getenv("APP_NAME", "device_systems"),
        "version": os.getenv("APP_VERSION", "4.0.0")
    }