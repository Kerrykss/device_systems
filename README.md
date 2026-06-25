# Device Systems API v4.0

## 📋 Descripción

API REST profesional y segura para gestión de usuarios, dispositivos y préstamos, construida con **FastAPI**, **SQLAlchemy** y **Alembic**. El proyecto implementa arquitectura por capas (modelos, schemas, servicios, rutas), migraciones de base de datos versionadas, consultas avanzadas con JOINs, y un sistema completo de seguridad con autenticación **JWT (Bearer)**, hash de contraseñas, control de roles, rate limiting, middleware personalizado y configuración de CORS.

---

## 🎥 Video explicativo

En el siguiente video se explican todas las funcionalidades implementadas, los cambios respecto a la versión anterior, la protección de rutas, el hash de contraseñas, el flujo de login con OAuth2 y JWT, el middleware y CORS, el rate limiting, y las lecciones aprendidas sobre seguridad en APIs REST:

🔗 **[Ver video en YouTube](https://youtu.be/SFTznXQnSVg)**

[![Video explicativo - Device Systems API](https://img.youtube.com/vi/SFTznXQnSVg/0.jpg)](https://youtu.be/SFTznXQnSVg)

---

## 🔄 Historial de cambios

### v3.0 — Alembic, relaciones y consultas avanzadas

La versión anterior solo incluía gestión de usuarios. En v3.0 se implementó:

- ✅ **Modelo Device** — Gestión completa de dispositivos (laptops, tablets, proyectores, etc.)
- ✅ **Modelo Loan** — Sistema de préstamos con seguimiento de devoluciones
- ✅ **Alembic configurado** — Versionamiento profesional de migraciones de BD
- ✅ **Relaciones One-to-Many** — User ↔ Loan y Device ↔ Loan
- ✅ **CRUD completo** — Operaciones Create, Read, Update, Delete en todas las entidades
- ✅ **Consultas con JOINs** — Optimización de queries para evitar el problema N+1
- ✅ **Filtros avanzados** — Búsquedas complejas y ordenamiento
- ✅ **Manejo robusto de errores** — Status codes apropiados y mensajes claros

### v4.0 — Seguridad (esta versión)

Sobre la base de v3.0, se agregó una capa completa de seguridad:

- ✅ **Autenticación JWT** — Registro y login con tokens firmados (esquema HTTPBearer)
- ✅ **Hash de contraseñas** — bcrypt vía `passlib`, nunca se almacena texto plano
- ✅ **Control de roles** — `admin`, `support`, `user`, con dependencias de autorización
- ✅ **Middleware personalizado** — Cabeceras de trazabilidad (`x-app-name`, `x-process-time`, `x-request-id`)
- ✅ **Rate limiting** — Límite de peticiones con `slowapi` contra fuerza bruta
- ✅ **CORS configurado** — Orígenes permitidos vía variable de entorno
- ✅ **Migración Alembic adicional** — Campos de autenticación en la tabla `users`

---

## 🔧 Configuración de Alembic

### Inicializar Alembic

Se ejecutó el comando para crear la estructura de migraciones:

```bash
alembic init alembic
```

**Captura de ejecución:**

![Alembic Init](./pictures_final_V1/Alembic_pictures/ejecucion_alembic_init.png)

### Configuración de env.py

El archivo `alembic/env.py` se configuró para usar SQLAlchemy automáticamente:

```python
from app.database.connection import Base
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

target_metadata = Base.metadata
```

Esto permite que Alembic detecte automáticamente los cambios en los modelos.

---

## 📊 Migraciones generadas

### Primera migración — Modelos y relaciones

```bash
alembic revision --autogenerate -m "Initial migration with User Device Loan models and relationships"
```

**Captura de creación de migración:**

![Revision Autogenerate](./pictures_final_V1/Alembic_pictures/alembic_revision_autogenerate.png)

Se generó automáticamente el archivo `alembic/versions/6f8780b86cdd_create_devices_and_loans_tables.py` con:

- ✅ Tabla `devices` con todos los campos y constraints
- ✅ Tabla `loans` con Foreign Keys a `users` y `devices`
- ✅ Índices (unique en `serial_number`)
- ✅ Funciones `upgrade()` y `downgrade()` para migración y rollback

### Segunda migración — Campos de autenticación

Para soportar el login con JWT y hash de contraseñas, se generó una migración adicional que agrega los campos de autenticación a la tabla `users` (contraseña hasheada, rol, estado activo), sobre el archivo `alembic/versions/a5fef7dedc4b_add_authentication_fields_to_users.py`.

**Captura de migración aplicada:**

![Migración Alembic aplicada](./pictures_final_V2/migracion_alembic.png)

### Aplicación de migraciones

```bash
alembic upgrade head
```

**Captura de aplicación:**

![Upgrade Head](./pictures_final_V1/Alembic_pictures/alembic_upgrade_head.png)

La migración se aplicó correctamente y las tablas fueron creadas en SQLite.

---

## 🗂️ Estructura de tablas generadas

**Captura de estructura completa:**

![Estructura BD](./pictures_final_V1/Alembic_pictures/alembic_history.png)

### Tabla: users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,           -- admin, support, user
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Constraints:**
- `id`: Primary Key (auto-increment)
- `email`: UNIQUE (no duplicados)
- `hashed_password`: contraseña en formato bcrypt, nunca texto plano
- `is_active`: DEFAULT TRUE

---

### Tabla: devices

```sql
CREATE TABLE devices (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    serial_number VARCHAR(100) UNIQUE NOT NULL,
    device_type VARCHAR(50) NOT NULL,   -- laptop, tablet, proyector
    brand VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Constraints:**
- `id`: Primary Key (auto-increment)
- `serial_number`: UNIQUE (identificación del dispositivo)
- `is_available`: DEFAULT TRUE

---

### Tabla: loans

```sql
CREATE TABLE loans (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL FOREIGN KEY REFERENCES users(id),
    device_id INTEGER NOT NULL FOREIGN KEY REFERENCES devices(id),
    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    return_date DATETIME NULL,
    status VARCHAR(20) DEFAULT 'active'  -- active, returned, overdue
);
```

**Constraints:**
- `id`: Primary Key (auto-increment)
- `user_id`: Foreign Key → users.id
- `device_id`: Foreign Key → devices.id
- Integridad referencial garantizada

---

## 🔗 Relaciones entre modelos

### User ↔ Loan (One-to-Many)

```python
class User(Base):
    loans = relationship("Loan", back_populates="user")

class Loan(Base):
    user = relationship("User", back_populates="loans")
```

**Ventaja:** Un usuario puede tener múltiples préstamos. Acceso fácil: `user.loans`

### Device ↔ Loan (One-to-Many)

```python
class Device(Base):
    loans = relationship("Loan", back_populates="device")

class Loan(Base):
    device = relationship("Device", back_populates="loans")
```

**Ventaja:** Un dispositivo puede aparecer en múltiples préstamos. Acceso fácil: `device.loans`

---

## 🌐 Swagger UI — Documentación interactiva

### Interfaz general

![Swagger UI General](./pictures_final_V1/swagger_pictures/swagger_docs.png)

La documentación automática de FastAPI es accesible en `/docs` y muestra todos los endpoints organizados por categoría.

### Esquema de seguridad HTTPBearer

A partir de v4.0, Swagger también muestra el esquema de autenticación **HTTPBearer**, permitiendo autorizar las peticiones directamente desde la interfaz con el botón "Authorize".

![Swagger con esquema de autenticación Bearer](./pictures_final_V2/Swagger_OpenAPI_HTTPBearer_auth.png)

---

## 🔐 Autenticación y autorización (v4.0)

### Registro de usuario

Se valida que el email sea único y que la contraseña cumpla reglas de seguridad (mínimo 8 caracteres, al menos una mayúscula, una minúscula, un número, y sin espacios).

![Registro de usuario](./pictures_final_V2/Auth_POST_registrar_ususario.png)

### Login y generación de token

Al autenticarse correctamente, el sistema genera un JWT firmado que incluye el `id`, `email` y `role` del usuario como claims, evitando consultas repetidas a la base de datos en cada request protegido.

![Login y token generado](./pictures_final_V2/Auth_POST_login_token.png)

### Obtener usuario autenticado (`/auth/me`)

Con un token válido, el endpoint `/auth/me` decodifica el JWT y retorna los datos del usuario autenticado.

![Respuesta de /auth/me](./pictures_final_V2/Auth_GET_obtener_info_token_admin.png)

### Acceso sin token

Cualquier endpoint protegido rechaza las peticiones que no incluyan un token Bearer válido, devolviendo `401 Unauthorized`.

![Acceso sin token](./pictures_final_V2/Auth_GET_sin_token_401.png)

### Acceso con rol no permitido

Los endpoints administrativos (como la creación de usuarios) están protegidos con una dependencia `require_admin`. Un usuario autenticado pero sin el rol adecuado recibe `403 Forbidden`.

![Acceso con rol no permitido](./pictures_final_V2/Users_POST_rol_no_permitido_403.png)

---

## 🧩 Middleware personalizado

Cada respuesta de la API incluye cabeceras personalizadas inyectadas por un middleware propio (`RequestMiddleware`), útiles para trazabilidad y monitoreo:

- `x-app-name`: nombre de la aplicación.
- `x-process-time`: tiempo de procesamiento de la petición.
- `x-request-id`: identificador único de la petición, útil para rastrear errores en los logs del servidor.

![Cabeceras del middleware](./pictures_final_V2/Middleware_response_headers.png)

---

## 🚦 Rate limiting

Se implementó limitación de peticiones con `slowapi` para proteger los endpoints de autenticación contra abuso (por ejemplo, ataques de fuerza bruta sobre el login):

- `POST /auth/register`: máximo 3 peticiones por minuto.
- `POST /auth/login`: máximo 5 peticiones por minuto.

Al superar el límite, la API responde con `429 Too Many Requests`.

![Prueba de rate limiting](./pictures_final_V2/Auth_POST_login_rate_limiting_429.png)

---

## 🌐 CORS configurado

El proyecto utiliza `CORSMiddleware` de FastAPI para controlar qué orígenes externos pueden consumir la API desde un navegador:

```python
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Explicación de la configuración:**

- **`allow_origins`**: la lista de orígenes permitidos se obtiene de la variable de entorno `CORS_ORIGINS`, con un valor por defecto orientado a desarrollo local (`localhost:5173` para Vite, `localhost:3000` para React/Next, y `localhost:8000` para pruebas directas contra el propio backend).
- **`allow_credentials=True`**: permite que el navegador envíe credenciales (cookies, headers de autorización como el JWT) en las peticiones cross-origin. Es necesario porque el flujo de autenticación de esta API depende del header `Authorization: Bearer <token>`.
- **`allow_methods=["*"]`**: permite todos los métodos HTTP, ya que la API expone operaciones CRUD completas sobre usuarios, dispositivos y préstamos.
- **`allow_headers=["*"]`**: permite cualquier header en las peticiones entrantes, dando flexibilidad al frontend.

Esta configuración es adecuada para desarrollo. En un entorno de producción real, lo recomendable sería restringir `allow_origins` únicamente al dominio real del frontend, y acotar `allow_methods` y `allow_headers` a los estrictamente necesarios.

---

## 🧪 Pruebas de endpoints (CRUD)

### Crear Usuario (POST /users/)

![POST Usuario](./pictures_final_V1/users_pictures/POST_crear_usuario.png)

**Request:**
```json
{
  "name": "Carlos López",
  "email": "carlos.lopez@example.com",
  "role": "admin",
  "is_active": true
}
```

### Listar Usuarios (GET /users/)

![GET Listar Usuarios](./pictures_final_V1/users_pictures/GET_listar_usuarios.png)

Con parámetros opcionales: `?role=admin`, `?is_active=true`, `?order_by=name`

### Obtener Usuario por ID (GET /users/{user_id})

![GET Usuario por ID](./pictures_final_V1/users_pictures/GET_usuario_por_ID.png)

### Actualizar Usuario Completo (PUT /users/{user_id})

![PUT Actualizar Usuario](./pictures_final_V1/users_pictures/PUT_actualizar_usuario_completo.png)

### Actualizar Usuario Parcialmente (PATCH /users/{user_id})

![PATCH Actualizar Parcialmente](./pictures_final_V1/users_pictures/PATCH_actualizar_parcialmente.png)

Nota: PUT reemplaza todos los campos, PATCH solo actualiza los enviados.

### Crear Dispositivo (POST /devices/)

![POST Dispositivo](./pictures_final_V1/Devices_pictures/POST_crear_dispositivo.png)

**Request:**
```json
{
  "name": "Laptop Dell XPS 15",
  "serial_number": "DELL-XPS-2024-001",
  "device_type": "laptop",
  "brand": "Dell",
  "is_available": true
}
```

### Listar Dispositivos (GET /devices/)

![GET Listar Dispositivos](./pictures_final_V1/Devices_pictures/GET_listar_dispositivos.png)

Con filtros: `?device_type=laptop`, `?is_available=true`, `?brand=Dell`, `?search=XPS`

### Crear Préstamo (POST /loans/)

![POST Préstamo](./pictures_final_V1/Loans_Pictures/POST_crear_prestamo.png)

**Request:**
```json
{
  "user_id": 1,
  "device_id": 1
}
```

---

## 🔍 Consultas con JOINs

### GET /loans/details — Préstamos con detalles completos

![GET Loans Details](./pictures_final_V1/Loans_Pictures/GET_loans_details.png)

**¿Por qué JOINs?**

Sin JOINs: 1 query para el préstamo + 1 query para el usuario + 1 query para el dispositivo → **3 queries por préstamo** ❌ (problema N+1)

Con JOINs: una sola query trae todo → **1 query** ✅

```python
loans = db.query(Loan).options(
    joinedload(Loan.user),
    joinedload(Loan.device)
).all()
```

---

## 🔎 Filtros avanzados

### Filtros en GET /loans/

![GET Loans Filtrados](./pictures_final_V1/Loans_Pictures/GET_listar_prestamos_filtrados.png)

```bash
GET /loans/?status=active
GET /loans/?user_email=carlos.lopez@example.com
GET /loans/?device_type=laptop
GET /loans/?status=active&device_type=laptop&user_email=carlos.lopez@example.com
```

### Filtros en GET /devices/

![GET Devices Filtrados](./pictures_final_V1/Devices_pictures/GET_obtener_por_ID.png)

```bash
GET /devices/?device_type=laptop&is_available=true
GET /devices/?brand=Dell
GET /devices/?search=XPS
GET /devices/?order_by=created_at
```

### Filtros en GET /users/

```bash
GET /users/?role=admin
GET /users/?is_active=true&role=support
GET /users/?order_by=name
```

---

## 📦 Devolución de dispositivo

### PATCH /loans/{loan_id}/return

![PATCH Devolver Dispositivo](./pictures_final_V1/Loans_Pictures/PATCH_devolver_dispositivo.png)

**Lógica implementada:**
1. Busca el préstamo por ID
2. Valida que exista
3. Marca `return_date` con fecha actual
4. Cambia status a "returned"
5. Libera el dispositivo (`is_available = true`)
6. Retorna el préstamo actualizado

---

## 📱 Root Endpoint

### GET /

![GET Root](./pictures_final_V1/Root_pictures/Bienvenida_al_sistema.png)

---

## 🛠️ Manejo de errores

```python
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno de base de datos"}
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."}
    )
```

**Status codes implementados:**

| Status | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | OK | GET exitoso |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 400 | Bad Request | Email duplicado, datos inválidos |
| 401 | Unauthorized | Sin token o token inválido |
| 403 | Forbidden | Rol no permitido |
| 404 | Not Found | Usuario/Dispositivo no existe |
| 422 | Validation Error | Fallo validación Pydantic |
| 429 | Too Many Requests | Límite de rate limiting excedido |
| 500 | Server Error | Error en BD |

---

## 🏗️ Estructura del proyecto

![Estructura del proyecto](./pictures_final_V2/Estructura_proyecto_device_systems.png)

```
device_systems/
├── alembic/
│   ├── versions/
│   │   ├── 6f8780b86cdd_create_devices_and_loans_tables.py
│   │   └── a5fef7dedc4b_add_authentication_fields_to_users.py
│   ├── script.py.mako
│   ├── env.py
│   └── alembic.ini
│
├── app/
│   ├── auth/
│   │   ├── auth_routes.py
│   │   ├── auth_service.py
│   │   ├── limiter.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth_dependency.py
│   │   └── database_dependency.py
│   │
│   ├── middlewares/
│   │   └── request_middleware.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   └── loan_model.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   └── loan_schema.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   └── loan_routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── device_service.py
│   │   └── loan_service.py
│   │
│   └── main.py
│
├── pictures_final_V1/
│   ├── Alembic_pictures/
│   ├── Devices_pictures/
│   ├── Loans_Pictures/
│   ├── Root_pictures/
│   ├── swagger_pictures/
│   └── users_pictures/
│
├── pictures_final_V2/
│   (capturas de seguridad: auth, roles, middleware, rate limiting, swagger bearer)
│
├── .env.example
├── device_systems.db
├── requirements.txt
└── README.md
```

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Kerrykss/device_systems.git
cd device_systems
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` con tus propios valores, especialmente `SECRET_KEY`.

### 5. Aplicar migraciones

```bash
alembic upgrade head
```

### 6. Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

### 7. Acceder a la documentación

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📦 Dependencias principales

```
fastapi==0.115.0
uvicorn==0.30.6
sqlalchemy==2.0.35
pydantic==2.9.2
pydantic[email]==2.9.2
email-validator==2.2.0
alembic==1.13.3
python-jose==3.3.0
passlib[bcrypt]==1.7.4
slowapi==0.1.9
python-dotenv==1.0.1
```

---

## 💡 Reflexión v3.0: Importancia de migraciones, relaciones y consultas avanzadas

### 🔄 Migraciones (Alembic) — Por qué son críticas

**Problema sin migraciones:**
- Cambios manuales en tablas = riesgo de inconsistencia
- No hay historial de cambios
- Imposible hacer rollback si algo sale mal
- En producción, cambiar estructura es arriesgado

**Solución con Alembic:**
- ✅ Versionamiento del schema (como Git para BD)
- ✅ Cada cambio está documentado
- ✅ Rollback automático si algo falla
- ✅ Reproducible en cualquier máquina
- ✅ Seguro para producción

### 🔗 Relaciones (SQLAlchemy ORM) — Por qué importan

**Problema sin relaciones:**
```python
user = db.query(User).filter(User.id == 1).first()
loans = db.query(Loan).filter(Loan.user_id == user.id).all()
for loan in loans:
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    print(f"{user.name} prestó {device.name}")
```

**Solución con relaciones:**
```python
user = db.query(User).filter(User.id == 1).first()
for loan in user.loans:
    print(f"{user.name} prestó {loan.device.name}")
```

**Beneficios:** normalización, integridad referencial, acceso directo (`user.loans`, `device.loans`), código más limpio, mantenibilidad centralizada.

### 🚀 Consultas con JOINs — Por qué optimizan performance

**Problema N+1 (sin JOINs):** 1 query por préstamo + 2 queries adicionales (usuario y dispositivo) por cada uno → con 10 préstamos, 21 queries ❌

**Solución con JOINs (eager loading):**
```python
loans = db.query(Loan).options(
    joinedload(Loan.user),
    joinedload(Loan.device)
).all()
```
→ 1 sola query, sin importar cuántos préstamos existan ✅

### 🔎 Filtros avanzados — Por qué mejoran la UX

Filtrar en el servidor (`GET /loans/?status=active&device_type=laptop`) en vez de traer todo y filtrar en el cliente reduce la transferencia de datos, mejora los tiempos de respuesta y escala mejor con el crecimiento de los datos.

### 🎯 Conclusión v3.0

Device Systems API v3.0 es profesional y escalable gracias a Alembic (migraciones seguras), SQLAlchemy ORM (relaciones bien definidas), JOINs inteligentes (performance óptimo), filtros avanzados (flexibilidad), validaciones Pydantic (datos seguros) y manejo robusto de errores (confiabilidad).

---

## 🪞 Reflexión v4.0: Importancia de la seguridad en APIs REST

Construir esta capa de seguridad dejó en evidencia que la seguridad de un backend no se reduce a "agregar un login" — es un conjunto de capas que deben trabajar de forma coherente entre sí. Un solo detalle mal definido, como declarar el campo `sub` de un JWT como `int` en lugar de `str`, fue suficiente para romper por completo el flujo de autenticación, a pesar de que cada pieza individual (login, firma del token, decodificación) parecía estar bien implementada por separado. Esto demuestra que la seguridad de una API depende tanto del cumplimiento de estándares externos (como el RFC 7519 para JWT) como del comportamiento interno de las herramientas que se usan (como la coerción de tipos de Pydantic), y que ambos deben entenderse en conjunto, no de forma aislada.

Más allá del bug puntual, el proyecto reforzó varios principios fundamentales:

- **La autenticación no es lo mismo que la autorización.** Verificar que un usuario es quien dice ser (JWT válido) es solo el primer paso; decidir qué puede hacer ese usuario (control de roles con `admin`, `support`, `user`) es una capa adicional e igualmente necesaria.
- **Los errores de seguridad no deben revelar información interna.** Atrapar la excepción técnica de `python-jose` y traducirla a un mensaje genérico ("Invalid or expired token") evita filtrar detalles internos de implementación a un posible atacante, aunque a costa de dificultar el debugging — por eso la importancia de tener logs detallados en el servidor, separados de lo que ve el cliente final.
- **Limitar la tasa de peticiones (rate limiting) es una defensa básica pero crítica**, especialmente en endpoints de autenticación, donde un atacante podría intentar adivinar credenciales por fuerza bruta si no existiera ningún límite.
- **CORS no es solo una configuración molesta que "hay que desactivar para que funcione"**, sino un mecanismo de seguridad del propio navegador que decide qué orígenes externos pueden interactuar con la API; configurarlo de forma demasiado permisiva puede abrir la puerta a ataques de robo de sesión desde sitios maliciosos.
- **La trazabilidad importa.** Tener un middleware que asigna un `x-request-id` único a cada petición permite correlacionar errores reportados por un usuario con los logs exactos del servidor.

### 🎯 Conclusión v4.0

La seguridad en una API REST no es un checkbox que se marca una sola vez, sino una serie de decisiones de diseño que deben revisarse constantemente, probarse activamente (incluyendo los casos negativos: sin token, con rol incorrecto, con rate limiting excedido) y documentarse para que cualquier persona que continúe el proyecto entienda no solo qué se implementó, sino por qué.

---

## 📄 Licencia

MIT

## ✉️ Contacto

**Device Systems** — Sistema profesional y seguro de gestión de dispositivos

---

**Estado:** ✅ Completado
**Versión:** 4.0.0
**Fecha:** Junio 2026