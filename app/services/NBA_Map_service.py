"""
Servicio para gestión del mapa interactivo de equipos NBA
Maneja la lógica de negocio para obtener y procesar ubicaciones de equipos
AHORA USA LA BASE DE DATOS E INCLUYE INFORMACIÓN DEL CLIMA
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Optional
import logging
import asyncio

from app.repositories.Team_repository import TeamRepository
from app.repositories.NBA_repository import PlayerRepository
from app.models.NBA_model import Player
from app.models.Team_model import Team
from app.services.Weather_service import WeatherService

logger = logging.getLogger('nba_api.services.nba_map')


class NBAMapService:
    """
    Servicio para manejar operaciones relacionadas con el mapa de equipos NBA.
    
    Proporciona métodos para:
    - Obtener ubicaciones geográficas de equipos desde la BD
    - Agrupar jugadores por equipo
    - Calcular estadísticas por equipo
    - Obtener información del clima de cada ciudad
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.
        
        Args:
            db: Sesión activa de SQLAlchemy
        """
        self.db = db
        self.team_repository = TeamRepository(db)
        self.player_repository = PlayerRepository(db)
        self.weather_service = WeatherService()
    
    async def get_teams_locations(self) -> List[Dict]:
        """
        Obtiene las ubicaciones de todos los equipos con sus jugadores Y CLIMA.
        
        Proceso:
        1. Obtiene todos los equipos de la base de datos
        2. Para cada equipo, cuenta cuántos jugadores tiene
        3. Obtiene los nombres de los jugadores
        4. Consulta el clima actual de cada ciudad (API OpenWeatherMap)
        5. Retorna lista de equipos con ubicación, jugadores y clima
        
        Returns:
            List[Dict]: Lista de equipos con sus coordenadas, jugadores y clima
            
        Example:
            [
                {
                    "team": "Los Angeles Lakers",
                    "city": "Los Angeles",
                    "state": "California",
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                    "stadium": "Crypto.com Arena",
                    "players_count": 5,
                    "players": ["LeBron James", "Anthony Davis", ...],
                    "weather": {
                        "temperature": 22.5,
                        "description": "cielo claro",
                        "humidity": 65,
                        "icon": "01d"
                    }
                }
            ]
        """
        try:
            logger.info("🗺️ Obteniendo ubicaciones de equipos desde la BD...")
            
            # Obtener todos los equipos con JOIN a jugadores
            results = (
                self.db.query(
                    Team,
                    func.count(Player.id).label('players_count')
                )
                .outerjoin(Player, Team.name == Player.team)
                .group_by(Team.id)
                .all()
            )
            
            logger.info(f"📊 Se encontraron {len(results)} equipos en la BD")
            
            # Construir la lista de ubicaciones
            locations = []
            
            # Obtener clima para cada equipo de forma asíncrona
            for team, players_count in results:
                # Obtener los jugadores del equipo
                players = self.db.query(Player).filter(Player.team == team.name).all()
                
                # Obtener información del clima
                logger.info(f"🌤️ Consultando clima para {team.city}...")
                weather_data = await self.weather_service.get_weather(
                    team.latitude, 
                    team.longitude
                )
                
                location_data = {
                    "team": team.name,
                    "city": team.city,
                    "state": team.state,
                    "latitude": team.latitude,
                    "longitude": team.longitude,
                    "stadium": team.stadium,
                    "conference": team.conference,
                    "division": team.division,
                    "players_count": players_count,
                    "players": [player.name for player in players],
                    "weather": weather_data  # Agregar datos del clima
                }
                
                locations.append(location_data)
                
                # Log con emoji según temperatura
                if weather_data:
                    temp = weather_data.get('temperature', 0)
                    emoji = "🥵" if temp > 30 else "🌡️" if temp > 20 else "🥶"
                    logger.debug(
                        f"   ✅ {team.name}: {players_count} jugadores, "
                        f"{emoji} {temp}°C - {weather_data.get('description', 'N/A')}"
                    )
                else:
                    logger.debug(f"   ✅ {team.name}: {players_count} jugadores (sin datos de clima)")
            
            logger.info(f"✅ Ubicaciones obtenidas: {len(locations)} equipos con clima")
            return locations
            
        except Exception as e:
            logger.error(f"❌ Error al obtener ubicaciones: {str(e)}")
            logger.exception(e)
            raise
    
    def get_team_info(self, team_name: str) -> Optional[Dict]:
        """
        Obtiene información detallada de un equipo específico.
        
        Args:
            team_name: Nombre del equipo a buscar
            
        Returns:
            Optional[Dict]: Información del equipo o None si no existe
        """
        try:
            # Buscar equipo en la BD
            team = self.team_repository.get_team_by_name(team_name)
            
            if not team:
                logger.warning(f"⚠️ Equipo no encontrado: {team_name}")
                return None
            
            # Obtener jugadores del equipo
            all_players = self.player_repository.listar_jugadores(skip=0, limit=1000)
            team_players = [p for p in all_players if p.team == team_name]
            
            # Construir respuesta
            team_info = {
                "team": team.name,
                "city": team.city,
                "state": team.state,
                "latitude": team.latitude,
                "longitude": team.longitude,
                "stadium": team.stadium,
                "conference": team.conference,
                "division": team.division,
                "players_count": len(team_players),
                "players": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "position": p.position,
                        "height_m": p.height_m,
                        "weight_kg": p.weight_kg
                    }
                    for p in team_players
                ]
            }
            
            logger.info(f"✅ Información obtenida para: {team_name}")
            return team_info
            
        except Exception as e:
            logger.error(f"❌ Error al obtener info del equipo: {str(e)}")
            raise
