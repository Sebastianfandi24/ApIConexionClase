from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.NBA_model import Player
from typing import List, Optional


class PlayerRepository:
    """
    Repositorio para la gestión de jugadores NBA en la base de datos.
    Solo maneja persistencia con SQLAlchemy (CRUD).
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_players(self, skip: int = 0, limit: int = 100) -> List[Player]:
        """Retorna todos los jugadores con paginación"""
        return self.db.query(Player).offset(skip).limit(limit).all()

    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """Busca un jugador por su ID numérico"""
        return self.db.query(Player).filter(Player.id == player_id).first()

    def create_player(self, player: Player) -> Player:
        """Inserta un nuevo jugador en la base de datos"""
        try:
            self.db.add(player)
            self.db.commit()
            self.db.refresh(player)
            return player
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update_player(self, player: Player) -> Player:
        """Actualiza los datos de un jugador existente"""
        try:
            self.db.commit()
            self.db.refresh(player)
            return player
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_player(self, player: Player) -> None:
        """Elimina un jugador existente"""
        try:
            self.db.delete(player)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
