# device_systems API 🖥️

**Autor:** Kerry Herrera  
**Versión:** 2.0.0  
**Actividad:** GA8 — FastAPI Intermedio: Evolución de device_systems con CRUD Completo, Manejo de Errores, Swagger/OpenAPI y Dependency Injection

---

## Descripción

`device_systems` es una API REST construida con FastAPI para la gestión de usuarios del sistema. Esta versión evoluciona la API inicial (GA anterior) incorporando un CRUD completo, manejo profesional de errores, códigos de estado HTTP correctos, documentación automática con Swagger/OpenAPI y reutilización de lógica mediante Dependency Injection.

---

## Tecnologías utilizadas

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic v2
- Git y GitHub

---

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── main.py
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── user_dependencies.py
│   └── data/
│       ├── __init__.py
│       └── users_db.py
├── pictures_v2/
├── requirements.txt
└── README.md
```

Cada carpeta tiene una responsabilidad clara:

- `routes/` — Definición de endpoints y métodos HTTP
- `schemas/` — Modelos Pydantic de entrada y salida
- `services/` — Lógica de negocio
- `dependencies/` — Funciones reutilizables con `Depends()`
- `data/` — Simulación de base de datos en memoria

---

## Instalación y ejecución

### 1. Clonar el repositorio y moverse a la rama

```bash
git clone https://github.com/Kerrykss/device_systems.git
cd device_systems
git checkout GA8-fastapi-intermedio
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

### 5. Acceder a la documentación

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Tabla de endpoints

| Método | Ruta | Descripción | Código exitoso |
|--------|------|-------------|----------------|
| GET | `/users/` | Listar todos los usuarios (filtros opcionales por `role` e `is_active`) | 200 OK |
| GET | `/users/{user_id}` | Obtener usuario por ID | 200 OK |
| POST | `/users/` | Crear nuevo usuario | 201 Created |
| PUT | `/users/{user_id}` | Actualizar completamente un usuario | 200 OK |
| PATCH | `/users/{user_id}` | Actualizar parcialmente un usuario | 200 OK |
| DELETE | `/users/{user_id}` | Eliminar un usuario | 204 No Content |

---

## Códigos de estado HTTP utilizados

| Código | Significado | Cuándo ocurre |
|--------|-------------|---------------|
| 200 | OK | GET exitoso, PUT exitoso, PATCH exitoso |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 400 | Bad Request | Email duplicado, PATCH sin campos, rol inválido |
| 404 | Not Found | Usuario no encontrado por ID |
| 422 | Unprocessable Entity | Validación Pydantic fallida (datos inválidos) |

---

## Ejemplos de peticiones y respuestas

### GET /users/
```http
GET http://127.0.0.1:8000/users/
```
```json
[
  { "id": 1, "name": "Carlos Pérez", "email": "carlos@gmail.com", "role": "admin", "is_active": true },
  { "id": 2, "name": "Ana González", "email": "ana@gmail.com", "role": "support", "is_active": true }
]
```

### GET /users/{user_id}
```http
GET http://127.0.0.1:8000/users/1
```
```json
{ "id": 1, "name": "Carlos Pérez", "email": "carlos@gmail.com", "role": "admin", "is_active": true }
```

### POST /users/
```http
POST http://127.0.0.1:8000/users/
Content-Type: application/json

{
  "name": "Kerry Herrera",
  "email": "kerry@gmail.com",
  "role": "admin",
  "is_active": true
}
```
```json
{ "id": 5, "name": "Kerry Herrera", "email": "kerry@gmail.com", "role": "admin", "is_active": true }
```

### PUT /users/{user_id}
```http
PUT http://127.0.0.1:8000/users/1
Content-Type: application/json

{
  "name": "Carlos Pérez Actualizado",
  "email": "carlos.nuevo@gmail.com",
  "role": "support",
  "is_active": false
}
```
```json
{ "id": 1, "name": "Carlos Pérez Actualizado", "email": "carlos.nuevo@gmail.com", "role": "support", "is_active": false }
```

### PATCH /users/{user_id}
```http
PATCH http://127.0.0.1:8000/users/2
Content-Type: application/json

{
  "role": "admin"
}
```
```json
{ "id": 2, "name": "Ana González", "email": "ana@gmail.com", "role": "admin", "is_active": true }
```

### DELETE /users/{user_id}
```http
DELETE http://127.0.0.1:8000/users/3
```
```
204 No Content
```

---

## Manejo de errores

La API controla los siguientes escenarios de error usando `HTTPException`:

### Usuario no encontrado (404)
```json
{ "detail": "Usuario con id 999 no encontrado" }
```

### Correo duplicado (400)
```json
{ "detail": "El correo ya está registrado" }
```

### PATCH sin campos (400)
```json
{ "detail": "Debes enviar al menos un campo para actualizar" }
```

### Datos inválidos — Pydantic (422)
```json
{
  "detail": [
    { "loc": ["body", "email"], "msg": "value is not a valid email address", "type": "value_error.email" }
  ]
}
```

---

## Dependency Injection con Depends()

La inyección de dependencias permite reutilizar lógica común entre múltiples endpoints sin duplicar código. En este proyecto se implementó en `app/dependencies/user_dependencies.py`.

### Dependencias creadas

**`get_user_or_404(user_id)`**  
Busca un usuario por ID y lanza `404` automáticamente si no existe. Se reutiliza en `GET /users/{user_id}` y `DELETE /users/{user_id}`.

```python
def get_user_or_404(user_id: int) -> dict:
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Usuario con id {user_id} no encontrado")
    return user
```

**`get_api_settings()`**  
Retorna la configuración general de la API sin necesidad de importarla en cada ruta.

**`verify_api_key(x_api_key)`**  
Simula autenticación básica mediante cabecera `X-API-Key`. Si la clave no es válida retorna `401 Unauthorized`.

**`validate_role(role)`**  
Valida que el rol recibido sea uno de los permitidos (`admin`, `support`, `user`).

### Uso en rutas con Depends()

```python
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    response: Response,
    user: dict = Depends(get_user_or_404),
):
    return user
```

FastAPI ejecuta `get_user_or_404` automáticamente antes de la función de la ruta, inyecta el resultado como parámetro `user` y lanza el error si corresponde. Esto elimina código repetido y centraliza la validación.

---

## Documentación Swagger/OpenAPI

### Swagger UI — Vista general

![Swagger UI](pictures_v2/Swagger_UI.png)

### ReDoc

![ReDoc](pictures_v2/ReDoc.png)

---

## Evidencia de pruebas

### GET /users/ — Listar todos los usuarios
![Listar todos](pictures_v2/Listar_todos.png)

### GET /users/{user_id} — Usuario existente
![Usuario existente](pictures_v2/Usuario_existente.png)

### GET /users/{user_id} — Usuario inexistente (404)
![Usuario inexistente](pictures_v2/Usuario_inexistente.png)

### POST /users/ — Crear usuario nuevo
![Crear usuario nuevo](pictures_v2/Crear_usuario_nuevo.png)

### POST /users/ — Email duplicado (400)
![Email duplicado](pictures_v2/Email_duplicado.png)

### POST /users/ — Datos inválidos (422)
![Datos inválidos](pictures_v2/Datos_invalidos.png)

### PUT /users/{user_id} — Actualizar usuario completo
![Actualizar usuario completo](pictures_v2/Actualizar_usuario_completo.png)

### PUT /users/{user_id} — Usuario inexistente (404)
![Usuario inexistente PUT](pictures_v2/Usuario_inexistete.png)

### PATCH /users/{user_id} — Actualizar parcialmente
![Actualizar parcialmente](pictures_v2/Actualizar_usuario_parcialmente.png)

### PATCH /users/{user_id} — Body vacío (400)
![Vacío error](pictures_v2/Vacio_(error).png)

### DELETE /users/{user_id} — Eliminar usuario
![Eliminar usuario](pictures_v2/Eliminar_usuario.png)

### DELETE /users/{user_id} — Usuario inexistente (404)
![Error controlado DELETE](pictures_v2/Error_controlado.png)

---

## Reflexión final

Esta actividad representó una evolución significativa respecto a la versión anterior de `device_systems`. Partiendo de una API con solo GET y POST, se construyó una solución más completa y profesional incorporando:

- **CRUD completo** con PUT, PATCH y DELETE correctamente implementados
- **Separación de responsabilidades** en capas (routes, services, schemas, dependencies, data)
- **Manejo profesional de errores** con `HTTPException` y códigos HTTP apropiados
- **Dependency Injection** con `Depends()` para eliminar duplicación de lógica
- **Documentación automática** enriquecida con metadatos, tags y descripciones en Swagger/OpenAPI

El patrón de Dependency Injection fue el concepto más valioso de esta actividad, ya que permite que el código sea más limpio, mantenible y fácil de probar, centralizando validaciones que de otro modo se repetirían en cada endpoint.