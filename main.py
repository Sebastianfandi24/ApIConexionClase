from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.NBA_model import Base
from app.config.database import engine, test_connection
from app.controllers.player_controller import router as player_router
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Iniciando aplicación...")

    # Verificar conexión a la base de datos
    if test_connection():
        logger.info("✅ Base de datos conectada correctamente")
    else:
        logger.error("❌ Error al conectar con la base de datos")

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
    title="NBA Players API",
    description="API para consultar y administrar información de jugadores de la NBA",
    version="1.0.0",
    lifespan=lifespan
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
app.include_router(player_router, prefix="/players", tags=["Players"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la NBA Players API"}

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la aplicación y base de datos"""
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected"
    }
