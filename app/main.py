from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.NBA_model import Base
from app.models.User_model import User  # Importar modelo User
from app.config.NBA_database import engine
from app.controllers.NBA_controller import router as nba_router
from app.controllers.User_controller import router as user_router
from app.controllers.Auth_controller import router as auth_router
from app.config.documentation import (
    TAGS_METADATA, 
    CONTACT_INFO, 
    LICENSE_INFO, 
    SERVERS
)
from scalar_fastapi import get_scalar_api_reference
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Iniciando aplicación...")

    # La conexión se verifica automáticamente al crear el engine

    # Crear tablas si no existen
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas verificadas/creadas correctamente")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")

    yield

    # Shutdown
    logger.info("⏹️ Cerrando aplicación...")

# Configuración de la aplicación FastAPI
app = FastAPI(
    title="🏀 NBA Players API",
    description="""
    ## 🏀 API para gestión de jugadores de la NBA
    
    Esta API permite gestionar información completa de jugadores de la NBA, 
    incluyendo operaciones CRUD (Crear, Leer, Actualizar, Eliminar) con validaciones 
    robustas y documentación interactiva.
    
    ### 🚀 Características principales:
    
    * **CRUD completo**: Operaciones completas para jugadores
    * **Validaciones automáticas**: Rangos de altura, peso y formatos de fecha
    * **Paginación**: Lista de jugadores con control de límites
    * **Documentación interactiva**: Swagger UI, ReDoc y Scalar
    * **Base de datos PostgreSQL**: Almacenamiento persistente y confiable
    * **Arquitectura en capas**: Separación clara de responsabilidades
    
    ### 📊 Endpoints disponibles:
    
    * `GET /api/v1/players/` - Lista todos los jugadores (con paginación)
    * `GET /api/v1/players/{id}` - Obtiene un jugador específico
    * `POST /api/v1/players/` - Crea un nuevo jugador
    * `PUT /api/v1/players/{id}` - Actualiza un jugador existente
    * `DELETE /api/v1/players/{id}` - Elimina un jugador
    
    ### 🛠️ Tecnologías utilizadas:
    
    * **FastAPI** - Framework web moderno y rápido
    * **SQLAlchemy** - ORM para manejo de base de datos
    * **PostgreSQL** - Base de datos relacional
    * **Pydantic** - Validación de datos y serialización
    * **Uvicorn** - Servidor ASGI de alta performance
    
    ### 📚 Documentación adicional:
    
    * [Swagger UI](/docs) - Interfaz interactiva clásica
    * [ReDoc](/redoc) - Documentación elegante y responsive
    * [Scalar](/scalar) - Interfaz moderna y avanzada
    * [Health Check](/health) - Estado de la aplicación y BD
    """,
    version="1.2.0",
    terms_of_service="https://example.com/terms/",
    contact=CONTACT_INFO,
    license_info=LICENSE_INFO,
    openapi_tags=TAGS_METADATA,
    servers=SERVERS,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Middleware CORS (si se conecta con frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringir a dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)  # ← Nuevo router de autenticación
app.include_router(nba_router)
app.include_router(user_router)  # Sin prefix adicional porque ya tiene prefix="/api/v1/users"

# Configurar Scalar para documentación de API
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    """Documentación Scalar - Interfaz moderna para explorar la API"""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

@app.get("/", tags=["System"])
async def root():
    """
    **Endpoint principal de bienvenida**
    
    Retorna información básica sobre la API y enlaces útiles.
    """
    return {
        "message": "🏀 Bienvenido a la NBA Players API",
        "version": "1.2.0",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc", 
            "scalar": "/scalar"
        },
        "api_endpoints": "/api/v1/players",
        "health_check": "/health"
    }

@app.get("/health", tags=["System"])
async def health_check():
    """
    **Endpoint de verificación de estado**
    
    Verifica el estado de la aplicación y la conectividad con la base de datos.
    Útil para monitoreo y sistemas de alertas.
    
    ### Estados posibles:
    - **healthy**: Todo funciona correctamente
    - **unhealthy**: Hay problemas de conectividad
    
    ### Verificaciones:
    - Conectividad con PostgreSQL
    - Estado general de la aplicación
    """
    try:
        # Intentar conectar usando el engine
        with engine.connect():
            db_status = True
            db_message = "Conectado correctamente"
    except Exception as e:
        db_status = False
        db_message = f"Error de conexión: {str(e)}"
        
    return {
        "status": "healthy" if db_status else "unhealthy",
        "timestamp": "2025-09-04T00:00:00Z",
        "database": {
            "status": "connected" if db_status else "disconnected",
            "message": db_message
        },
        "version": "1.2.0"
    }
