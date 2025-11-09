"""
Schemas de Roles
Definen la estructura de datos para entrada/salida de roles
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    """Schema base de rol"""
    name: str = Field(..., min_length=1, max_length=50, description="Nombre del rol")
    description: Optional[str] = Field(None, max_length=255, description="Descripción del rol")
    can_create_players: bool = Field(default=False, description="Permiso para crear jugadores")
    can_read_players: bool = Field(default=True, description="Permiso para ver jugadores")
    can_update_players: bool = Field(default=False, description="Permiso para actualizar jugadores")
    can_delete_players: bool = Field(default=False, description="Permiso para eliminar jugadores")
    can_manage_users: bool = Field(default=False, description="Permiso para gestionar usuarios")


class RoleCreate(RoleBase):
    """Schema para crear un rol"""
    pass


class RoleUpdate(BaseModel):
    """Schema para actualizar un rol"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    can_create_players: Optional[bool] = None
    can_read_players: Optional[bool] = None
    can_update_players: Optional[bool] = None
    can_delete_players: Optional[bool] = None
    can_manage_users: Optional[bool] = None
    is_active: Optional[bool] = None


class RoleResponse(RoleBase):
    """Schema de respuesta de rol"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleWithUsers(RoleResponse):
    """Schema de rol con conteo de usuarios"""
    users_count: int = Field(default=0, description="Cantidad de usuarios con este rol")

    class Config:
        from_attributes = True
