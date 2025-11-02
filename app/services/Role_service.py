"""
Servicio de Roles
Contiene la lógica de negocio para gestión de roles
"""
from sqlalchemy.orm import Session
from app.repositories.Role_repository import RoleRepository
from app.Schema.Role_Schema import RoleCreate, RoleUpdate, RoleResponse, RoleWithUsers
from typing import List
from fastapi import HTTPException, status


class RoleService:
    """Servicio para gestionar la lógica de negocio de roles"""

    def __init__(self, db: Session):
        self.role_repository = RoleRepository(db)

    def get_all_roles(self, skip: int = 0, limit: int = 100) -> List[RoleResponse]:
        """Obtiene todos los roles"""
        try:
            roles = self.role_repository.get_all_roles(skip=skip, limit=limit)
            return [RoleResponse.model_validate(role) for role in roles]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener roles: {str(e)}"
            )

    def get_role_by_id(self, role_id: int) -> RoleResponse:
        """Obtiene un rol por ID"""
        try:
            role = self.role_repository.get_role_by_id(role_id)
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {role_id} no encontrado"
                )
            return RoleResponse.model_validate(role)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener rol: {str(e)}"
            )

    def create_role(self, role_data: RoleCreate) -> RoleResponse:
        """Crea un nuevo rol"""
        try:
            new_role = self.role_repository.create_role(role_data)
            return RoleResponse.model_validate(new_role)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear rol: {str(e)}"
            )

    def update_role(self, role_id: int, role_data: RoleUpdate) -> RoleResponse:
        """Actualiza un rol existente"""
        try:
            updated_role = self.role_repository.update_role(role_id, role_data)
            if not updated_role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {role_id} no encontrado"
                )
            return RoleResponse.model_validate(updated_role)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar rol: {str(e)}"
            )

    def delete_role(self, role_id: int) -> dict:
        """Elimina un rol"""
        try:
            deleted = self.role_repository.delete_role(role_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {role_id} no encontrado"
                )
            return {"message": f"Rol con ID {role_id} eliminado exitosamente"}
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar rol: {str(e)}"
            )
