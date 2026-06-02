# app/main.py

from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems API",
    description="""
## API REST para la gestión de usuarios del sistema device_systems

Esta API permite administrar los usuarios del sistema con operaciones completas CRUD.

### Funcionalidades
- **Listar usuarios** con filtros por rol y estado
- **Consultar usuario** por ID
- **Crear usuarios** con validación de datos
- **Actualizar completamente** un usuario (PUT)
- **Actualizar parcialmente** un usuario (PATCH)
- **Eliminar usuarios**

### Roles permitidos
- `admin` — Administrador del sistema
- `support` — Soporte técnico
- `user` — Usuario estándar

### Manejo de errores
- `400` — Datos inválidos o correo duplicado
- `401` — API Key inválida
- `404` — Usuario no encontrado
- `422` — Error de validación Pydantic
""",
    version="2.0.0",
    contact={
        "name": "Kerry",
        "email": "kerry@device_systems.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operaciones sobre el recurso usuarios: crear, listar, actualizar y eliminar.",
        }
    ],
)

app.include_router(router)