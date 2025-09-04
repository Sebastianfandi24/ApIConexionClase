from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class PlayerBase(BaseModel):
    """
    Esquema base para jugadores de la NBA.
    Contiene los campos comunes entre operaciones.
    """
    name: str = Field(
        ..., 
        min_length=2,
        max_length=100,
        example="LeBron James",
        description="Nombre completo del jugador"
    )
    team: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example="Los Angeles Lakers", 
        description="Equipo actual del jugador"
    )
    position: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="Small Forward",
        description="Posición del jugador en el campo (PG, SG, SF, PF, C)"
    )

class PlayerCreate(PlayerBase):
    """
    Esquema para crear un nuevo jugador.
    
    **Campos requeridos:**
    - name: Nombre del jugador
    - team: Equipo actual
    - position: Posición en el campo
    - height_m: Altura en metros
    - weight_kg: Peso en kilogramos
    - birth_date: Fecha de nacimiento
    """
    height_m: float = Field(
        ...,
        gt=1.0,
        lt=3.0,
        example=2.06,
        description="Altura del jugador en metros (debe estar entre 1.0 y 3.0)"
    )
    weight_kg: float = Field(
        ...,
        gt=50.0,
        lt=200.0,
        example=113.4,
        description="Peso del jugador en kilogramos (debe estar entre 50 y 200)"
    )
    birth_date: datetime = Field(
        ...,
        example="1984-12-30T00:00:00",
        description="Fecha de nacimiento del jugador en formato ISO"
    )

class PlayerUpdate(PlayerBase):
    """
    Esquema para actualizar un jugador existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        example="LeBron James",
        description="Nombre completo del jugador"
    )
    team: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        example="Los Angeles Lakers",
        description="Equipo actual del jugador"
    )
    position: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
        example="Small Forward",
        description="Posición del jugador en el campo"
    )
    height_m: Optional[float] = Field(
        None,
        gt=1.0,
        lt=3.0,
        example=2.06,
        description="Altura del jugador en metros"
    )
    weight_kg: Optional[float] = Field(
        None,
        gt=50.0,
        lt=200.0,
        example=113.4,
        description="Peso del jugador en kilogramos"
    )
    birth_date: Optional[datetime] = Field(
        None,
        example="1984-12-30T00:00:00",
        description="Fecha de nacimiento del jugador"
    )

class PlayerResponse(PlayerBase):
    """
    Esquema de respuesta para jugadores.
    Incluye todos los datos del jugador más metadatos del sistema.
    """
    id: int = Field(
        ...,
        example=1,
        description="Identificador único del jugador generado automáticamente"
    )
    height_m: float = Field(
        ...,
        example=2.06,
        description="Altura del jugador en metros"
    )
    weight_kg: float = Field(
        ...,
        example=113.4,
        description="Peso del jugador en kilogramos"
    )
    birth_date: datetime = Field(
        ...,
        example="1984-12-30T00:00:00",
        description="Fecha de nacimiento del jugador"
    )
    created_at: datetime = Field(
        ...,
        example="2025-09-04T00:00:00",
        description="Fecha y hora de creación del registro"
    )

    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    """
    Esquema estándar para respuestas de error.
    """
    detail: str = Field(
        ...,
        example="Jugador con id 999 no encontrado",
        description="Descripción detallada del error"
    )

class MessageResponse(BaseModel):
    """
    Esquema para respuestas con mensaje simple.
    """
    message: str = Field(
        ...,
        example="Jugador eliminado correctamente",
        description="Mensaje de confirmación de la operación"
    )