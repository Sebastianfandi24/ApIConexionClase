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

# Variables de entorno
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("db_port")
DBNAME = os.getenv("dbname")

# URIs
SQLITE_URL = "sqlite:///./test_local.db"
POSTGRES_URL = None

if all([USER, PASSWORD, HOST, PORT, DBNAME]):
    POSTGRES_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

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
                echo=True  # Cambiar a True para depuración
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
