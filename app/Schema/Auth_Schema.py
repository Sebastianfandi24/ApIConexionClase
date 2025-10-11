from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

class TokenResponse(BaseModel):
    """Esquema para la respuesta del token JWT"""
    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer", 
                "expires_in": 3600
            }
        }
    )

class LoginRequest(BaseModel):
    """Esquema para la solicitud de login"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "password": "password123"
            }
        }
    )

class RegisterRequest(BaseModel):
    """Esquema para el registro de usuario"""
    email: EmailStr = Field(..., description="Email único del usuario")
    password: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "nuevo_usuario@example.com",
                "password": "password123"
            }
        }
    )

class UserProfile(BaseModel):
    """Esquema para el perfil del usuario autenticado"""
    id: int = Field(..., description="ID único del usuario")
    email: str = Field(..., description="Email del usuario")
    is_active: bool = Field(..., description="Estado activo del usuario")
    created_at: datetime = Field(..., description="Fecha de creación")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "admin@example.com",
                "is_active": True,
                "created_at": "2024-09-20T01:30:00"
            }
        }
    )