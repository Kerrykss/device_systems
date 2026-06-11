# Device Systems API v3.0

API REST para la gestión de usuarios con persistencia en base de datos mediante SQLAlchemy y FastAPI.

## Estructura del proyecto

```
device_systems/
│── app/
│   │── main.py                          # Punto de entrada de la aplicación
│   │── database/
│   │   └── connection.py                # Engine, SessionLocal y Base
│   │── models/
│   │   └── user_model.py                # Modelo SQLAlchemy de la tabla users
│   │── schemas/
│   │   └── user_schema.py               # Schemas Pydantic (entrada/salida)
│   │── routes/
│   │   └── user_routes.py               # Endpoints del recurso /users
│   │── services/
│   │   └── user_service.py              # Lógica CRUD sobre la base de datos
│   │── dependencies/
│   │   └── database_dependency.py       # Dependencia de sesión DB
│── requirements.txt
│── README.md
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

## Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /users | Listar todos los usuarios |
| GET | /users/{id} | Obtener usuario por ID |
| POST | /users | Crear nuevo usuario |
| PUT | /users/{id} | Actualizar usuario completo |
| PATCH | /users/{id} | Actualizar usuario parcialmente |
| DELETE | /users/{id} | Eliminar usuario |

### Filtros disponibles en GET /users

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| role | string | Filtrar por rol: `admin`, `support`, `user` |
| is_active | boolean | Filtrar por estado: `true` / `false` |
| order_by | string | Ordenar por: `name`, `created_at` |

## Códigos de respuesta

| Caso | Código |
|------|--------|
| Usuario creado | 201 Created |
| Consulta/Actualización correcta | 200 OK |
| Eliminación correcta | 204 No Content |
| Usuario no encontrado | 404 Not Found |
| Email duplicado | 400 Bad Request |
| Error de validación | 422 Unprocessable Entity |

## Modelo de datos - User

| Campo | Tipo | Restricción |
|-------|------|-------------|
| id | Integer | Primary Key, autoincrement |
| name | String | Obligatorio, mínimo 3 caracteres |
| email | String | Único, obligatorio, formato válido |
| role | String | admin / support / user |
| is_active | Boolean | Default: True |
| created_at | DateTime | Se asigna automáticamente |

## Diferencia entre Modelo SQLAlchemy y Schema Pydantic

| Aspecto | Modelo SQLAlchemy | Schema Pydantic |
|---------|-------------------|-----------------|
| Propósito | Representa la tabla en la BD | Define la estructura de datos en la API |
| Validación | Constraints de BD (unique, nullable) | Validaciones de entrada (formato, longitud) |
| Uso | Operaciones ORM, consultas | Serialización/deserialización de requests |
| Ubicación | `models/` | `schemas/` |

## Reflexión sobre persistencia

Sin persistencia, todos los datos se pierden al reiniciar la aplicación. SQLAlchemy permite que los usuarios sobrevivan reinicios, sean consultados eficientemente y mantengan integridad referencial. Esto es fundamental en cualquier sistema real donde los datos tienen valor más allá de la sesión actual.