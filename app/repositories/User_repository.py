from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.User_model import User
from typing import List, Optional


class UserRepository:
    """
    Repositorio para la gestión de usuarios en la base de datos.
    Solo maneja persistencia con SQLAlchemy (CRUD).
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Retorna todos los usuarios con paginación"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID numérico"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por su nombre de usuario"""
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: User) -> User:
        """Inserta un nuevo usuario en la base de datos"""
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update_user(self, user: User) -> User:
        """Actualiza los datos de un usuario existente"""
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_user(self, user: User) -> None:
        """Elimina un usuario existente"""
        try:
            self.db.delete(user)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e