from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import re

from app.config.NBA_database import get_db
from app.services.NBA_service import (
    listar_jugadores,
    obtener_jugador,
    crear_jugador,
    actualizar_jugador,
    eliminar_jugador
)
from app.schemas.NBA_schema import PlayerCreate, PlayerUpdate, PlayerResponse
from pydantic import BaseModel


# -------------------------------
# Modelo de respuesta genérica
# -------------------------------
class MessageResponse(BaseModel):
    message: str


router = APIRouter(
    prefix="/players",
    tags=["NBA Players"]
)


# -------------------------------
# Helper → Validación de player_id
# -------------------------------
def validar_id(player_id: str):
    if not re.match(r"^[a-zA-Z0-9_-]+$", player_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del jugador solo puede contener letras, números, guiones y guiones bajos."
        )


# -------------------------------
# GET /players → Listar jugadores
# -------------------------------
@router.get("/", response_model=list[PlayerResponse])
def get_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retorna todos los jugadores registrados con paginación.
    """
    return listar_jugadores(db, skip, limit)


# -------------------------------
# GET /players/{player_id} → Obtener jugador por ID
# -------------------------------
@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: str, db: Session = Depends(get_db)):
    """
    Retorna un jugador específico por su ID alfanumérico.
    """
    validar_id(player_id)
    player = obtener_jugador(db, player_id)
    if not player:
        raise HTTPException(
            status_code=404,
            detail=f"Jugador con id {player_id} no encontrado"
        )
    return player


# -------------------------------
# POST /players → Crear nuevo jugador
# -------------------------------
@router.post("/", response_model=PlayerResponse, status_code=201)
def post_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo jugador en el sistema.
    """
    # Verificar duplicados por ID antes de crear
    existing = obtener_jugador(db, player.id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un jugador con id {player.id}"
        )

    return crear_jugador(db, player)


# -------------------------------
# PUT /players/{player_id} → Actualizar jugador
# -------------------------------
@router.put("/{player_id}", response_model=PlayerResponse)
def put_player(player_id: str, player: PlayerUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un jugador existente.
    """
    validar_id(player_id)
    db_player = obtener_jugador(db, player_id)
    if not db_player:
        raise HTTPException(
            status_code=404,
            detail=f"Jugador con id {player_id} no encontrado"
        )
    return actualizar_jugador(db, player_id, player)


# -------------------------------
# DELETE /players/{player_id} → Eliminar jugador
# -------------------------------
@router.delete("/{player_id}", response_model=MessageResponse)
def delete_player(player_id: str, db: Session = Depends(get_db)):
    """
    Elimina un jugador por su ID.
    """
    validar_id(player_id)
    db_player = obtener_jugador(db, player_id)
    if not db_player:
        raise HTTPException(
            status_code=404,
            detail=f"Jugador con id {player_id} no encontrado"
        )

    eliminar_jugador(db, player_id)
    return {"message": "Jugador eliminado correctamente"}
