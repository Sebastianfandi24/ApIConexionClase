"""
Controlador para el mapa interactivo de equipos NBA
Proporciona endpoints para obtener las ubicaciones geográficas de los equipos NBA
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
import logging

from app.config.NBA_database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.dependencies.permission_dependencies import can_read_players
from app.models.User_model import User
from app.services.NBA_Map_service import NBAMapService

logger = logging.getLogger('nba_api.controllers.nba_map')

# Router para endpoints del mapa NBA
router = APIRouter(
    prefix="/api/v1/nba-map",
    tags=["NBA Map"],
    responses={
        401: {"description": "No autorizado - Token JWT requerido"},
        403: {"description": "Prohibido"},
        500: {"description": "Error interno del servidor"}
    }
)


@router.get(
    "/teams-locations",
    response_model=List[Dict],
    summary="Obtener ubicaciones de equipos NBA con clima",
    description="""
    **Obtiene las coordenadas geográficas y clima de todos los equipos NBA.**
    
    ### Características:
    - Agrupa jugadores por equipo
    - Devuelve coordenadas (latitud, longitud) de cada ciudad
    - Incluye contador de jugadores por equipo
    - **NUEVO**: Información del clima en tiempo real (OpenWeatherMap API)
    - Solo equipos con jugadores registrados
    
    ### Respuesta:
    - Lista de equipos con su ubicación geográfica
    - Datos meteorológicos de cada ciudad
    - Útil para visualización en mapas interactivos
    
    ### Seguridad:
    - Requiere autenticación JWT
    - Permiso de lectura de jugadores (can_read_players)
    """,
    responses={
        200: {
            "description": "Ubicaciones obtenidas exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "team": "Los Angeles Lakers",
                            "city": "Los Angeles",
                            "state": "California",
                            "latitude": 34.0522,
                            "longitude": -118.2437,
                            "players_count": 3,
                            "stadium": "Crypto.com Arena",
                            "weather": {
                                "temperature": 22.5,
                                "description": "cielo claro",
                                "humidity": 65,
                                "icon": "01d"
                            }
                        }
                    ]
                }
            }
        }
    }
)
async def get_teams_locations(
    current_user: User = Depends(can_read_players),  # ← Requiere permiso de lectura
    db: Session = Depends(get_db)
):
    """
    GET /nba-map/teams-locations
    
    Obtiene las ubicaciones geográficas y clima de todos los equipos NBA que tienen jugadores registrados.
    
    Args:
        current_user: Usuario autenticado (inyectado por dependencia)
        db: Sesión de base de datos (inyectado por dependencia)
    
    Returns:
        List[Dict]: Lista de equipos con sus coordenadas, jugadores y clima
        
    Raises:
        HTTPException: Si ocurre un error al obtener las ubicaciones
    """
    try:
        # Crear instancia del servicio
        service = NBAMapService(db)
        
        # Obtener ubicaciones de equipos CON CLIMA (ahora es async)
        locations = await service.get_teams_locations()
        
        # Log de auditoría
        logger.info(
            f"🗺️ ACCIÓN: El usuario '{current_user.username}' (ID: {current_user.id}) "
            f"consultó las ubicaciones de equipos NBA con clima - Total equipos: {len(locations)}"
        )
        
        return locations
        
    except Exception as e:
        logger.error(f"Error al obtener ubicaciones de equipos: {str(e)}")
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor al obtener ubicaciones: {str(e)}"
        )


@router.get(
    "/team-info/{team_name}",
    response_model=Dict,
    summary="Obtener información detallada de un equipo",
    description="""
    **Obtiene información detallada de un equipo específico incluyendo su ubicación.**
    
    ### Parámetros:
    - **team_name**: Nombre del equipo (ej: "Los Angeles Lakers")
    
    ### Respuesta:
    - Información completa del equipo
    - Ubicación geográfica
    - Lista de jugadores
    - Estadísticas del equipo
    """,
    responses={
        200: {
            "description": "Información obtenida exitosamente"
        },
        404: {
            "description": "Equipo no encontrado"
        }
    }
)
def get_team_info(
    team_name: str,
    current_user: User = Depends(can_read_players),
    db: Session = Depends(get_db)
):
    """
    GET /nba-map/team-info/{team_name}
    
    Obtiene información detallada de un equipo específico.
    
    Args:
        team_name: Nombre del equipo a consultar
        current_user: Usuario autenticado
        db: Sesión de base de datos
    
    Returns:
        Dict: Información completa del equipo
        
    Raises:
        HTTPException: Si el equipo no existe o hay un error
    """
    try:
        service = NBAMapService(db)
        
        # Obtener información del equipo
        team_info = service.get_team_info(team_name)
        
        if not team_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo '{team_name}' no encontrado"
            )
        
        # Log de auditoría
        logger.info(
            f"📊 ACCIÓN: El usuario '{current_user.username}' (ID: {current_user.id}) "
            f"consultó información del equipo '{team_name}'"
        )
        
        return team_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener información del equipo {team_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
