from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.config.NBA_database import get_db
from app.services.NBA_service import PlayerService
from app.Schema.NBA_Schema import (
    PlayerCreate, 
    PlayerUpdate, 
    PlayerResponse, 
    MessageResponse, 
    ErrorResponse
)
from app.dependencies.auth_dependencies import get_current_user
from app.models.User_model import User
import logging

logger = logging.getLogger(__name__)

# Router para endpoints de jugadores NBA (PROTEGIDOS CON JWT)
router = APIRouter(
    prefix="/api/v1/players",
    tags=["NBA Players"],
    responses={
        401: {"description": "No autorizado - Token JWT requerido"},
        403: {"description": "Prohibido"},
        404: {"model": ErrorResponse, "description": "Jugador no encontrado"},
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)

# -------------------------------
# GET /players → Listar jugadores (PROTEGIDO)
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
    current_user: User = Depends(get_current_user),  # ← Equivale a @jwt_required()
    skip: int = Query(
        0, 
        ge=0, 
        description="Número de registros a saltar para paginación",
        example=0
    ),
    limit: int = Query(
        10, 
        ge=1, 
        le=10, 
        description="Máximo número de jugadores a retornar (limitado a 10 para usuarios autenticados)",
        example=5
    ),
    db: Session = Depends(get_db)
):
    """
    GET /players/
    Lista jugadores NBA (SOLO USUARIOS AUTENTICADOS)
    Limitado a 10 registros máximo por seguridad.
    Requiere token JWT válido.
    """
    try:
        service = PlayerService(db)
        players = service.listar_jugadores(skip=skip, limit=limit)
        
        logger.info(f"Usuario {current_user.username} consultó lista de jugadores (skip={skip}, limit={limit})")
        return players
        
    except Exception as e:
        logger.error(f"Error al listar jugadores: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


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
def get_player(
    player_id: int,
    current_user: User = Depends(get_current_user),  # ← Equivale a @jwt_required()
    db: Session = Depends(get_db)
):
    """
    GET /players/{player_id}
    Obtiene un jugador específico por ID (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = PlayerService(db)
        player = service.obtener_jugador(player_id)
        
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jugador con ID {player_id} no encontrado"
            )
        
        logger.info(f"Usuario {current_user.username} consultó jugador ID: {player_id}")
        return player
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener jugador: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


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
def post_player(
    player_data: PlayerCreate,
    current_user: User = Depends(get_current_user),  # ← Equivale a @jwt_required()
    db: Session = Depends(get_db)
):
    """
    POST /players/
    Crea un nuevo jugador NBA (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = PlayerService(db)
        new_player = service.crear_jugador(
            name=player_data.name,
            team=player_data.team,
            position=player_data.position,
            height_m=player_data.height_m,
            weight_kg=player_data.weight_kg,
            birth_date=player_data.birth_date
        )
        
        logger.info(f"Usuario {current_user.username} creó jugador: {player_data.name}")
        return new_player
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error al crear jugador: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


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
def put_player(
    player_id: int,
    player_data: PlayerUpdate,
    current_user: User = Depends(get_current_user),  # ← Equivale a @jwt_required()
    db: Session = Depends(get_db)
):
    """
    PUT /players/{player_id}
    Actualiza un jugador existente (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = PlayerService(db)
        updated_player = service.actualizar_jugador(player_id, player_data.model_dump(exclude_unset=True))
        
        if not updated_player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jugador con ID {player_id} no encontrado"
            )
        
        logger.info(f"Usuario {current_user.username} actualizó jugador ID: {player_id}")
        return updated_player
        
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error al actualizar jugador: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


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
def delete_player(
    player_id: int,
    current_user: User = Depends(get_current_user),  # ← Equivale a @jwt_required()
    db: Session = Depends(get_db)
):
    """
    DELETE /players/{player_id}
    Elimina un jugador (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = PlayerService(db)
        deleted_player = service.eliminar_jugador(player_id)
        
        if not deleted_player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jugador con ID {player_id} no encontrado"
            )
        
        logger.info(f"Usuario {current_user.username} eliminó jugador ID: {player_id}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Jugador con ID {player_id} eliminado exitosamente"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar jugador: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
