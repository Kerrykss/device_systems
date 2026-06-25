import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class RequestMiddleware(BaseHTTPMiddleware):
    """
    Middleware personalizado que:
    - Mide tiempo de respuesta
    - Agrega headers personalizados
    - Genera/propaga X-Request-ID
    - Registra peticiones
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Generar o usar X-Request-ID existente
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Registrar inicio
        start_time = time.time()
        
        # Procesar petición
        response = await call_next(request)
        
        # Calcular tiempo
        process_time = time.time() - start_time
        
        # Agregar headers
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-App-Name"] = "device_systems"
        
        # Registrar (opcional - para logging)
        print(f"[{request_id}] {request.method} {request.url.path} - {response.status_code} ({process_time:.4f}s)")
        
        return response