from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

logger = logging.getLogger('nba_api.middleware')

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging de requests HTTP
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Obtener información del request
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        
        # Filtrar logs de endpoints que no necesitamos ver
        skip_logging = any(endpoint in url for endpoint in [
            "/docs", "/openapi.json", "/favicon.ico", "/scalar"
        ])
        
        if not skip_logging:
            logger.info(f"🌐 REQUEST: {method} {url} desde IP: {client_ip}")
        
        # Procesar request
        response: Response = await call_next(request)
        
        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time
        
        if not skip_logging:
            status_emoji = "✅" if response.status_code < 400 else "❌"
            logger.info(f"{status_emoji} RESPONSE: {response.status_code} en {process_time:.3f}s")
        
        # Agregar header con tiempo de procesamiento
        response.headers["X-Process-Time"] = str(process_time)
        
        return response