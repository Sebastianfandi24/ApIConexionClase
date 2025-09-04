from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import re
from datetime import date

from app.config.NBA_database import get_db
from app.services.NBA_service import (
    listar_jugadores,
    obtener_jugador,
    crear_jugador,
    actualizar_jugador,
    eliminar_jugador
)
from app.Schema.NBA_Schema import (
    PlayerCreate, 
    PlayerUpdate, 
    PlayerResponse, 
    MessageResponse, 
    ErrorResponse
)


router = APIRouter(
    prefix="/players",
    tags=["NBA Players"],
    responses={
        404: {"model": ErrorResponse, "description": "Jugador no encontrado"},
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
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
@router.get(
    "/",
    response_model=list[PlayerResponse],
    summary="Obtener lista de jugadores",
    description="""
    **Obtiene una lista paginada de todos los jugadores de la NBA registrados en el sistema.**
    
    ### Parámetros de consulta:
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Máximo número de registros a retornar (1-100)
    
    ### Casos de uso:
    - Mostrar todos los jugadores en una interfaz
    - Implementar paginación en aplicaciones frontend
    - Obtener datos para análisis masivo
    """,
    responses={
        200: {
            "description": "Lista de jugadores obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "LeBron James",
                            "team": "Los Angeles Lakers",
                            "position": "Small Forward",
                            "height_m": 2.06,
                            "weight_kg": 113.4,
                            "birth_date": "1984-12-30T00:00:00",
                            "created_at": "2025-09-04T00:00:00"
                        }
                    ]
                }
            }
        }
    }
)
def get_players(
    skip: int = Query(
        0, 
        ge=0, 
        description="Número de registros a saltar para paginación",
        example=0
    ),
    limit: int = Query(
        50, 
        ge=1, 
        le=100, 
        description="Máximo número de jugadores a retornar",
        example=10
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna todos los jugadores registrados con paginación.
    """
    return listar_jugadores(db, skip, limit)


# -------------------------------
# GET /players/{player_id} → Obtener jugador por ID
# -------------------------------
@router.get(
    "/{player_id}",
    response_model=PlayerResponse,
    summary="Obtener jugador por ID",
    description="""
    **Obtiene la información completa de un jugador específico usando su ID único.**
    
    ### Parámetros:
    - **player_id**: ID único del jugador (número entero)
    
    ### Casos de uso:
    - Mostrar perfil detallado de un jugador
    - Verificar existencia de un jugador
    - Obtener datos para edición
    """,
    responses={
        200: {
            "description": "Jugador encontrado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "LeBron James",
                        "team": "Los Angeles Lakers",
                        "position": "Small Forward",
                        "height_m": 2.06,
                        "weight_kg": 113.4,
                        "birth_date": "1984-12-30T00:00:00",
                        "created_at": "2025-09-04T00:00:00"
                    }
                }
            }
        },
        404: {
            "description": "Jugador no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Jugador con id 999 no encontrado"}
                }
            }
        }
    }
)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """
    Retorna un jugador específico por su ID alfanumérico.
    """
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
@router.post(
    "/",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo jugador",
    description="""
    **Crea un nuevo jugador en el sistema con todos sus datos.**
    
    ### Campos requeridos:
    - **name**: Nombre completo del jugador
    - **team**: Equipo actual
    - **position**: Posición en el campo
    - **height_m**: Altura en metros (1.0 - 3.0)
    - **weight_kg**: Peso en kilogramos (50 - 200)
    - **birth_date**: Fecha de nacimiento en formato ISO
    
    ### Validaciones automáticas:
    - El ID se genera automáticamente
    - Se validan rangos de altura y peso
    - Se asigna timestamp de creación
    """,
    responses={
        201: {
            "description": "Jugador creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "LeBron James",
                        "team": "Los Angeles Lakers",
                        "position": "Small Forward",
                        "height_m": 2.06,
                        "weight_kg": 113.4,
                        "birth_date": "1984-12-30T00:00:00",
                        "created_at": "2025-09-04T00:00:00"
                    }
                }
            }
        },
        400: {
            "description": "Datos inválidos",
            "content": {
                "application/json": {
                    "example": {"detail": "La altura debe estar entre 1.0 y 3.0 metros"}
                }
            }
        }
    }
)
def post_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo jugador en el sistema. El id se autogenera en la base de datos.
    """
    # Convertir birth_date a date si viene como datetime
    player_dict = player.model_dump()
    if "birth_date" in player_dict and hasattr(player_dict["birth_date"], "date"):
        player_dict["birth_date"] = player_dict["birth_date"].date()
    
    # Crear jugador sin id, la base de datos lo asigna automáticamente
    return crear_jugador(db, player)


# -------------------------------
# PUT /players/{player_id} → Actualizar jugador
# -------------------------------
@router.put(
    "/{player_id}",
    response_model=PlayerResponse,
    summary="Actualizar jugador existente",
    description="""
    **Actualiza los datos de un jugador existente en el sistema.**
    
    ### Parámetros:
    - **player_id**: ID único del jugador a actualizar
    
    ### Campos actualizables:
    - Todos los campos son opcionales para actualizaciones parciales
    - Solo se actualizarán los campos proporcionados
    - Las validaciones se aplican a los campos modificados
    
    ### Casos de uso:
    - Actualizar equipo cuando hay un traspaso
    - Corregir información errónea
    - Actualizar datos físicos del jugador
    """,
    responses={
        200: {
            "description": "Jugador actualizado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "LeBron James",
                        "team": "Miami Heat",
                        "position": "Small Forward",
                        "height_m": 2.06,
                        "weight_kg": 113.4,
                        "birth_date": "1984-12-30T00:00:00",
                        "created_at": "2025-09-04T00:00:00"
                    }
                }
            }
        },
        404: {
            "description": "Jugador no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Jugador con id 999 no encontrado"}
                }
            }
        }
    }
)
def put_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un jugador existente.
    """
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
@router.delete(
    "/{player_id}",
    response_model=MessageResponse,
    summary="Eliminar jugador",
    description="""
    **Elimina permanentemente un jugador del sistema.**
    
    ### Parámetros:
    - **player_id**: ID único del jugador a eliminar
    
    ### ⚠️ Advertencia:
    - Esta operación es **irreversible**
    - Se eliminará toda la información del jugador
    - Verificar que el jugador existe antes de eliminar
    
    ### Casos de uso:
    - Limpiar datos obsoletos
    - Corregir registros duplicados
    - Cumplir con solicitudes de eliminación de datos
    """,
    responses={
        200: {
            "description": "Jugador eliminado exitosamente",
            "content": {
                "application/json": {
                    "example": {"message": "Jugador eliminado correctamente"}
                }
            }
        },
        404: {
            "description": "Jugador no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Jugador con id 999 no encontrado"}
                }
            }
        }
    }
)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    """
    Elimina un jugador por su ID.
    """
    db_player = obtener_jugador(db, player_id)
    if not db_player:
        raise HTTPException(
            status_code=404,
            detail=f"Jugador con id {player_id} no encontrado"
        )

    eliminar_jugador(db, player_id)
    return {"message": "Jugador eliminado correctamente"}
