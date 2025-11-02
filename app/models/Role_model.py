"""
Modelo de Roles
Define los roles del sistema y sus permisos
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.config.NBA_database import Base


class Role(Base):
    """
    Modelo de Rol
    Define los diferentes roles y sus permisos en el sistema
    """
    __tablename__ = "roles"

    # ID único del rol
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)

    # Nombre del rol (admin, user, etc.)
    name = Column(String(50), unique=True, index=True, nullable=False)

    # Descripción del rol
    description = Column(String(255), nullable=True)

    # Permisos del rol
    can_create_players = Column(Boolean, default=False, nullable=False)
    can_read_players = Column(Boolean, default=True, nullable=False)
    can_update_players = Column(Boolean, default=False, nullable=False)
    can_delete_players = Column(Boolean, default=False, nullable=False)
    can_manage_users = Column(Boolean, default=False, nullable=False)

    # Estado activo del rol
    is_active = Column(Boolean, default=True, nullable=False)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relación con usuarios
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}', description='{self.description}')>"
