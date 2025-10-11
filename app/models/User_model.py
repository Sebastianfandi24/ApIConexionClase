# Importaciones de librerías:
# - datetime: para manejar fechas y tiempos (ej. created_at).
# - sqlalchemy: proporciona herramientas para definir modelos de bases de datos mediante ORM.
#   - Column: define columnas de la tabla.
#   - String, Integer, DateTime: tipos de datos que se pueden usar en columnas.
# - sqlalchemy.orm:
#   - declarative_base: se usa para crear una clase base de la cual heredan los modelos ORM.

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from app.models.NBA_model import Base

"""
La clase User representa un usuario del sistema.
Cada instancia corresponde a un usuario específico con información básica como su email único
y contraseña.

Este modelo está mapeado a la tabla 'users' en la base de datos y se diseñó bajo las siguientes normas:
- Seguridad → uso de constraints (ej. unique en email).
- Normalización → los atributos siguen tipos de datos adecuados (ej. password como String).
- Escalabilidad → se puede ampliar con más atributos sin afectar la estructura.
- Auditoría → el campo created_at permite llevar control de creación de registros.
"""
class User(Base):
    __tablename__ = "users"

    # Identificador único del usuario (numérico).
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)

    # Email único del usuario (usado para autenticación).
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Contraseña del usuario (se almacenará hasheada).
    password = Column(String(255), nullable=False)

    # Estado activo del usuario (para poder habilitar/deshabilitar usuarios).
    is_active = Column(Boolean, default=True, nullable=False)

    # Fecha y hora de creación del registro.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Fecha y hora de última actualización del registro.
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_active={self.is_active}, created_at='{self.created_at}')>"