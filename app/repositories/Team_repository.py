"""
Repositorio para gestión de equipos NBA
Maneja las operaciones CRUD de la tabla 'teams'
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.Team_model import Team
from app.models.NBA_model import Player


class TeamRepository:
    """
    Repositorio para operaciones de base de datos con equipos.
    Implementa el patrón Repository para abstraer el acceso a datos.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión activa de SQLAlchemy
        """
        self.db = db
    
    def create_team(self, team_data: dict) -> Team:
        """
        Crea un nuevo equipo en la base de datos.
        
        Args:
            team_data: Diccionario con los datos del equipo
            
        Returns:
            Team: Equipo creado
        """
        team = Team(**team_data)
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team
    
    def get_team_by_id(self, team_id: int) -> Optional[Team]:
        """
        Obtiene un equipo por su ID.
        
        Args:
            team_id: ID del equipo a buscar
            
        Returns:
            Optional[Team]: Equipo encontrado o None
        """
        return self.db.query(Team).filter(Team.id == team_id).first()
    
    def get_team_by_name(self, name: str) -> Optional[Team]:
        """
        Obtiene un equipo por su nombre.
        
        Args:
            name: Nombre del equipo a buscar
            
        Returns:
            Optional[Team]: Equipo encontrado o None
        """
        return self.db.query(Team).filter(Team.name == name).first()
    
    def get_all_teams(self, skip: int = 0, limit: int = 100) -> List[Team]:
        """
        Obtiene todos los equipos con paginación.
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            
        Returns:
            List[Team]: Lista de equipos
        """
        return self.db.query(Team).offset(skip).limit(limit).all()
    
    def get_teams_by_conference(self, conference: str) -> List[Team]:
        """
        Obtiene equipos filtrados por conferencia.
        
        Args:
            conference: Nombre de la conferencia (East/West)
            
        Returns:
            List[Team]: Lista de equipos de la conferencia
        """
        return self.db.query(Team).filter(Team.conference == conference).all()
    
    def get_teams_by_division(self, division: str) -> List[Team]:
        """
        Obtiene equipos filtrados por división.
        
        Args:
            division: Nombre de la división
            
        Returns:
            List[Team]: Lista de equipos de la división
        """
        return self.db.query(Team).filter(Team.division == division).all()
    
    def update_team(self, team_id: int, team_data: dict) -> Optional[Team]:
        """
        Actualiza los datos de un equipo.
        
        Args:
            team_id: ID del equipo a actualizar
            team_data: Diccionario con los nuevos datos
            
        Returns:
            Optional[Team]: Equipo actualizado o None si no existe
        """
        team = self.get_team_by_id(team_id)
        if not team:
            return None
        
        for key, value in team_data.items():
            if value is not None and hasattr(team, key):
                setattr(team, key, value)
        
        self.db.commit()
        self.db.refresh(team)
        return team
    
    def delete_team(self, team_id: int) -> bool:
        """
        Elimina un equipo de la base de datos.
        
        Args:
            team_id: ID del equipo a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        team = self.get_team_by_id(team_id)
        if not team:
            return False
        
        self.db.delete(team)
        self.db.commit()
        return True
    
    def get_teams_with_player_count(self) -> List[dict]:
        """
        Obtiene todos los equipos con la cantidad de jugadores.
        Usa un JOIN con la tabla de jugadores.
        
        Returns:
            List[dict]: Lista de equipos con contador de jugadores
        """
        # Query con JOIN y COUNT
        results = (
            self.db.query(
                Team,
                func.count(Player.id).label('players_count')
            )
            .outerjoin(Player, Team.name == Player.team)
            .group_by(Team.id)
            .all()
        )
        
        # Convertir a lista de diccionarios
        teams_data = []
        for team, players_count in results:
            team_dict = team.to_dict()
            team_dict['players_count'] = players_count
            teams_data.append(team_dict)
        
        return teams_data
    
    def get_team_with_players(self, team_id: int) -> Optional[dict]:
        """
        Obtiene un equipo con sus jugadores.
        
        Args:
            team_id: ID del equipo
            
        Returns:
            Optional[dict]: Equipo con lista de jugadores o None
        """
        team = self.get_team_by_id(team_id)
        if not team:
            return None
        
        # Obtener jugadores del equipo
        players = self.db.query(Player).filter(Player.team == team.name).all()
        
        team_dict = team.to_dict()
        team_dict['players'] = [
            {
                'id': p.id,
                'name': p.name,
                'position': p.position,
                'height_m': p.height_m,
                'weight_kg': p.weight_kg
            }
            for p in players
        ]
        team_dict['players_count'] = len(players)
        
        return team_dict
