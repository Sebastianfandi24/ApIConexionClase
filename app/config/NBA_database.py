import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Cargar variables de entorno (.env) solo si no estamos en GitHub Actions
if not os.getenv("GITHUB_ACTIONS"):
    load_dotenv()

# Prioridad 1: DATABASE_URL (Railway/producción)
# Prioridad 2: Variables individuales (desarrollo local)
DATABASE_URL = os.getenv("DATABASE_URL")

# Variables de entorno individuales (compatibilidad con configuración anterior)
USER = os.getenv("user") or os.getenv("PGUSER")
PASSWORD = os.getenv("password") or os.getenv("PGPASSWORD")
HOST = os.getenv("host") or os.getenv("PGHOST")
PORT = os.getenv("db_port") or os.getenv("PGPORT")
DBNAME = os.getenv("dbname") or os.getenv("PGDATABASE")

# URIs
SQLITE_URL = "sqlite:///./test_local.db"
POSTGRES_URL = None

# Usar DATABASE_URL si está disponible (Railway)
if DATABASE_URL:
    # Railway puede proporcionar DATABASE_URL directamente
    POSTGRES_URL = DATABASE_URL
    # Si no incluye el driver, agregarlo
    if POSTGRES_URL.startswith("postgresql://"):
        POSTGRES_URL = POSTGRES_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    # Agregar SSL mode si no está presente y no es conexión local
    if "sslmode=" not in POSTGRES_URL and "localhost" not in POSTGRES_URL and "127.0.0.1" not in POSTGRES_URL and "db:" not in POSTGRES_URL:
        separator = "&" if "?" in POSTGRES_URL else "?"
        POSTGRES_URL = f"{POSTGRES_URL}{separator}sslmode=require"
    logging.info("🔗 Usando DATABASE_URL de Railway")
# Construir URL desde variables individuales
elif all([USER, PASSWORD, HOST, PORT, DBNAME]):
    # Determinar si necesitamos SSL (no para conexiones locales)
    ssl_mode = ""
    if HOST not in ["localhost", "127.0.0.1", "db"]:
        ssl_mode = "?sslmode=require"
    POSTGRES_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}{ssl_mode}"
    logging.info("🔗 Usando variables de entorno individuales")
else:
    logging.warning("⚠️  No se encontró configuración de PostgreSQL, usando SQLite como fallback")

# Declarative Base
Base = declarative_base()

# Motor y sesión global (se definen más abajo)
engine = None
SessionLocal = None


def get_engine():
    """
    Crea un engine de SQLAlchemy con prioridad a PostgreSQL.
    Si falla la conexión, usa SQLite como fallback.
    """
    global POSTGRES_URL, SQLITE_URL

    if POSTGRES_URL:
        try:
            engine = create_engine(
                POSTGRES_URL,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800,
                echo=False  # Cambiar a True para depuración
            )
            # Probar conexión
            with engine.connect():
                logging.info("✅ Conexión a PostgreSQL exitosa")
            return engine
        except OperationalError as e:
            logging.warning(f"⚠️ No se pudo conectar a PostgreSQL: {e}. Usando SQLite local.")
        except SQLAlchemyError as e:
            logging.error(f"❌ Error general de SQLAlchemy: {e}. Usando SQLite local.")

    # Fallback automático a SQLite
    engine = create_engine(SQLITE_URL, echo=False)
    logging.info("👉 Usando SQLite local como base de datos alternativa")
    return engine


# Inicializar engine y session
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Retorna una sesión de base de datos que se cierra automáticamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
