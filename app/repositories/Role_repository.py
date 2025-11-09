"""
Repositorio de Roles
Maneja las operaciones CRUD de roles en la base de datos
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.Role_model import Role
from app.Schema.Role_Schema import RoleCreate, RoleUpdate
from typing import List, Optional


class RoleRepository:
    """Repositorio para gestionar operaciones de roles"""

    def __init__(self, db: Session):
        self.db = db

    def get_all_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Obtiene todos los roles"""
        try:
            return self.db.query(Role).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener roles: {str(e)}")

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """Obtiene un rol por ID"""
        try:
            return self.db.query(Role).filter(Role.id == role_id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener rol: {str(e)}")

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Obtiene un rol por nombre"""
        try:
            return self.db.query(Role).filter(Role.name == name).first()
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener rol por nombre: {str(e)}")

    def create_role(self, role_data: RoleCreate) -> Role:
        """Crea un nuevo rol"""
        try:
            # Verificar si el rol ya existe
            existing_role = self.get_role_by_name(role_data.name)
            if existing_role:
                raise ValueError(f"El rol '{role_data.name}' ya existe")

            new_role = Role(**role_data.model_dump())
            self.db.add(new_role)
            self.db.commit()
            self.db.refresh(new_role)
            return new_role
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al crear rol: {str(e)}")

    def update_role(self, role_id: int, role_data: RoleUpdate) -> Optional[Role]:
        """Actualiza un rol existente"""
        try:
            role = self.get_role_by_id(role_id)
            if not role:
                return None

            # Actualizar solo los campos proporcionados
            update_data = role_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(role, key, value)

            self.db.commit()
            self.db.refresh(role)
            return role
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar rol: {str(e)}")

    def delete_role(self, role_id: int) -> bool:
        """Elimina un rol (solo si no tiene usuarios asignados)"""
        try:
            role = self.get_role_by_id(role_id)
            if not role:
                return False

            # Verificar si tiene usuarios asignados
            if role.users:
                raise ValueError(f"No se puede eliminar el rol '{role.name}' porque tiene usuarios asignados")

            self.db.delete(role)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar rol: {str(e)}")
