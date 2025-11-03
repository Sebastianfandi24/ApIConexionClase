"""
Schemas Pydantic para equipos NBA
Define los modelos de validación y serialización
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class TeamBase(BaseModel):
    """Schema base para equipos"""
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del equipo")
    city: str = Field(..., min_length=2, max_length=100, description="Ciudad del equipo")
    state: str = Field(..., min_length=2, max_length=100, description="Estado/Provincia")
    stadium: str = Field(..., min_length=3, max_length=150, description="Nombre del estadio")
    latitude: float = Field(..., ge=-90, le=90, description="Latitud (-90 a 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitud (-180 a 180)")
    conference: str = Field(..., description="Conferencia (East/West)")
    division: str = Field(..., description="División del equipo")
    
    @validator('conference')
    def validate_conference(cls, v):
        """Valida que la conferencia sea East o West"""
        if v not in ['East', 'West']:
            raise ValueError('La conferencia debe ser "East" o "West"')
        return v


class TeamCreate(TeamBase):
    """Schema para crear un equipo"""
    pass


class TeamUpdate(BaseModel):
    """Schema para actualizar un equipo (todos los campos opcionales)"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=100)
    stadium: Optional[str] = Field(None, min_length=3, max_length=150)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    conference: Optional[str] = None
    division: Optional[str] = None
    
    @validator('conference')
    def validate_conference(cls, v):
        """Valida que la conferencia sea East o West"""
        if v is not None and v not in ['East', 'West']:
            raise ValueError('La conferencia debe ser "East" o "West"')
        return v


class TeamResponse(TeamBase):
    """Schema para respuesta de equipo"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TeamWithPlayers(TeamResponse):
    """Schema para equipo con información de jugadores"""
    players_count: int = Field(default=0, description="Cantidad de jugadores en el equipo")
    
    class Config:
        from_attributes = True
