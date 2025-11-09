# Importaciones de librerías:
# - datetime: para manejar fechas y tiempos (ej. created_at).
# - sqlalchemy: proporciona herramientas para definir modelos de bases de datos mediante ORM.
#   - Column: define columnas de la tabla.
#   - String, Float, Date, DateTime, Integer: tipos de datos que se pueden usar en columnas.
# - app.config.NBA_database:
#   - Base: clase base declarativa de SQLAlchemy de la cual heredan todos los modelos ORM.

from datetime import datetime
from sqlalchemy import Column, String, Float, Date, DateTime, Integer
from app.config.NBA_database import Base


"""
La clase Player representa un jugador de la NBA dentro del sistema.
Cada instancia corresponde a un jugador específico con información básica como su nombre, posición,
altura, peso y fecha de nacimiento.

Este modelo está mapeado a la tabla 'players' en la base de datos y se diseñó bajo las siguientes normas:
- Seguridad → uso de constraints (ej. unique si aplica en name o id).
- Normalización → los atributos siguen tipos de datos adecuados (ej. height_m como Float).
- Escalabilidad → se puede ampliar con más atributos sin afectar la estructura.
- Auditoría → el campo created_at permite llevar control de creación de registros.
"""
class Player(Base):
    __tablename__ = "players"

    # Identificador único del jugador (numérico).
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)


    # Nombre completo del jugador.
    name = Column(String(255), nullable=False)

    # Equipo del jugador.
    team = Column(String(255), nullable=False)

    # Posición en la cancha (ej: Guard, Forward, Center).
    position = Column(String(50), nullable=False)

    # Altura del jugador en metros (ej: 2.05).
    height_m = Column(Float, nullable=False)

    # Peso del jugador en kilogramos (ej: 102.5).
    weight_kg = Column(Float, nullable=False)

    # Fecha de nacimiento del jugador.
    birth_date = Column(Date, nullable=False)

    # Fecha de creación del registro → útil para trazabilidad/auditoría.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
