from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """
    Esquema base para usuarios del sistema.
    Contiene los campos comunes entre operaciones.
    """
    username: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",
        example="john_doe123",
        description="Nombre de usuario único (solo letras, números y guiones bajos)"
    )

class UserCreate(UserBase):
    """
    Esquema para crear un nuevo usuario.
    
    **Campos requeridos:**
    - username: Nombre de usuario único
    - password: Contraseña del usuario
    """
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        example="mySecurePassword123",
        description="Contraseña del usuario (mínimo 6 caracteres)"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "john_doe123",
                "password": "mySecurePassword123"
            }
        }
    )

class UserUpdate(BaseModel):
    """
    Esquema para actualizar un usuario existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",
        example="new_username",
        description="Nuevo nombre de usuario (opcional)"
    )
    password: Optional[str] = Field(
        None,
        min_length=6,
        max_length=100,
        example="newSecurePassword456",
        description="Nueva contraseña (opcional)"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "new_username",
                "password": "newSecurePassword456"
            }
        }
    )

class UserResponse(UserBase):
    """
    Esquema para respuestas que incluyen información del usuario.
    Incluye campos adicionales como id y created_at.
    No incluye la contraseña por seguridad.
    """
    id: int = Field(
        ...,
        example=1,
        description="Identificador único del usuario"
    )
    created_at: datetime = Field(
        ...,
        example="2024-01-01T00:00:00",
        description="Fecha y hora de creación del usuario"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "john_doe123",
                "created_at": "2024-01-01T00:00:00"
            }
        }
    )

class MessageResponse(BaseModel):
    """Esquema para respuestas de mensajes generales"""
    message: str = Field(
        ...,
        example="Operación completada exitosamente",
        description="Mensaje descriptivo de la operación"
    )

class ErrorResponse(BaseModel):
    """Esquema para respuestas de error"""
    detail: str = Field(
        ...,
        example="Error en la operación",
        description="Descripción detallada del error"
    )