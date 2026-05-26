from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems",
    description="API REST para la gestión de usuarios del sistema device_systems",
    version="1.0"
)

app.include_router(router)
