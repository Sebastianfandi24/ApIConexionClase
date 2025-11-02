"""
Controlador de Roles
Maneja los endpoints HTTP para gestión de roles del sistema
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.config.NBA_database import get_db
from app.services.Role_service import RoleService
from app.Schema.Role_Schema import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    RoleWithUsers
)
from app.dependencies.permission_dependencies import is_admin
from app.models.User_model import User
import logging

logger = logging.getLogger('nba_api.controllers.role')

# Router para endpoints de roles (SOLO ADMINISTRADORES)
router = APIRouter(
    prefix="/api/v1/roles",
    tags=["Roles"],
    responses={
        401: {"description": "No autorizado - Token JWT requerido"},
        403: {"description": "Prohibido - Solo administradores"},
        404: {"description": "Rol no encontrado"},
        400: {"description": "Datos inválidos"},
        500: {"description": "Error interno del servidor"}
    }
)


# -------------------------------
# GET /roles → Listar todos los roles (SOLO ADMIN)
# -------------------------------
@router.get(
    "/",
    response_model=List[RoleResponse],
    summary="Obtener lista de roles",
    description="""
    **Obtiene todos los roles del sistema.**
    
    **Restricción:** Solo administradores pueden acceder.
    
    ### Casos de uso:
    - Ver todos los roles disponibles
    - Administrar permisos del sistema
    """
)
def get_roles(
    current_user: User = Depends(is_admin),
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    GET /roles/
    Lista todos los roles (SOLO ADMINISTRADORES)
    """
    try:
        service = RoleService(db)
        roles = service.get_all_roles(skip=skip, limit=limit)
        
        logger.info(f"Admin '{current_user.username}' listó {len(roles)} roles")
        return roles
        
    except Exception as e:
        logger.error(f"Error al listar roles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# GET /roles/{role_id} → Obtener rol por ID (SOLO ADMIN)
# -------------------------------
@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Obtener rol por ID",
    description="""
    **Obtiene información completa de un rol específico.**
    
    **Restricción:** Solo administradores.
    """
)
def get_role(
    role_id: int,
    current_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """
    GET /roles/{role_id}
    Obtiene un rol específico (SOLO ADMINISTRADORES)
    """
    try:
        service = RoleService(db)
        role = service.get_role_by_id(role_id)
        
        logger.info(f"Admin '{current_user.username}' consultó rol ID: {role_id}")
        return role
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener rol: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# POST /roles → Crear nuevo rol (SOLO ADMIN)
# -------------------------------
@router.post(
    "/",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo rol",
    description="""
    **Crea un nuevo rol en el sistema con sus permisos.**
    
    **Restricción:** Solo administradores.
    
    ### Campos requeridos:
    - name: Nombre único del rol
    - description: Descripción del rol
    - Permisos: can_create_players, can_read_players, etc.
    """
)
def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """
    POST /roles/
    Crea un nuevo rol (SOLO ADMINISTRADORES)
    """
    try:
        service = RoleService(db)
        new_role = service.create_role(role_data)
        
        logger.info(f"Admin '{current_user.username}' creó rol: '{new_role.name}'")
        return new_role
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al crear rol: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# PUT /roles/{role_id} → Actualizar rol (SOLO ADMIN)
# -------------------------------
@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Actualizar rol existente",
    description="""
    **Actualiza los permisos y datos de un rol.**
    
    **Restricción:** Solo administradores.
    """
)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """
    PUT /roles/{role_id}
    Actualiza un rol (SOLO ADMINISTRADORES)
    """
    try:
        service = RoleService(db)
        updated_role = service.update_role(role_id, role_data)
        
        logger.info(f"Admin '{current_user.username}' actualizó rol ID: {role_id}")
        return updated_role
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar rol: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# DELETE /roles/{role_id} → Eliminar rol (SOLO ADMIN)
# -------------------------------
@router.delete(
    "/{role_id}",
    summary="Eliminar rol",
    description="""
    **Elimina un rol del sistema.**
    
    **Restricción:** Solo administradores.
    
    **⚠️ Advertencia:** No se puede eliminar si tiene usuarios asignados.
    """
)
def delete_role(
    role_id: int,
    current_user: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """
    DELETE /roles/{role_id}
    Elimina un rol (SOLO ADMINISTRADORES)
    """
    try:
        service = RoleService(db)
        result = service.delete_role(role_id)
        
        logger.info(f"Admin '{current_user.username}' eliminó rol ID: {role_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar rol: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
