from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """
    Esquema base para usuarios del sistema.
    Contiene los campos comunes entre operaciones.
    """
    email: EmailStr = Field(
        ..., 
        example="john.doe@example.com",
        description="Email único del usuario"
    )

class UserCreate(UserBase):
    """
    Esquema para crear un nuevo usuario.
    
    **Campos requeridos:**
    - email: Email único del usuario
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
                "email": "john.doe@example.com",
                "password": "mySecurePassword123"
            }
        }
    )

class UserUpdate(BaseModel):
    """
    Esquema para actualizar un usuario existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    email: Optional[EmailStr] = Field(
        None,
        example="new.email@example.com",
        description="Nuevo email del usuario"
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
                "email": "new.email@example.com",
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
                "email": "john.doe@example.com",
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