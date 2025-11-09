"""
Dependencias de permisos
Verifican que el usuario tenga los permisos necesarios para realizar acciones
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.NBA_database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.User_model import User
from app.models.Role_model import Role


def require_permission(permission_name: str):
    """
    Factory para crear dependencias que verifican permisos específicos
    
    Args:
        permission_name: Nombre del permiso a verificar
        
    Returns:
        Función de dependencia que verifica el permiso
    """
    async def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """Verifica que el usuario tenga el permiso especificado"""
        
        # Obtener el rol del usuario con sus permisos
        role = db.query(Role).filter(Role.id == current_user.role_id).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin rol asignado"
            )
        
        # Verificar si el rol tiene el permiso
        has_permission = getattr(role, permission_name, False)
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permiso para realizar esta acción. Se requiere: {permission_name}"
            )
        
        return current_user
    
    return permission_dependency


# Dependencias específicas para cada permiso
def can_create_players(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Verifica permiso para crear jugadores"""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or not role.can_create_players:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear jugadores"
        )
    return current_user


def can_update_players(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Verifica permiso para actualizar jugadores"""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or not role.can_update_players:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar jugadores"
        )
    return current_user


def can_delete_players(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Verifica permiso para eliminar jugadores"""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or not role.can_delete_players:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar jugadores"
        )
    return current_user


def can_read_players(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Verifica permiso para leer jugadores"""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or not role.can_read_players:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver jugadores"
        )
    return current_user


def can_manage_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Verifica permiso para gestionar usuarios (solo admins)"""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or not role.can_manage_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para gestionar usuarios. Solo administradores."
        )
    return current_user


def is_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Verifica que el usuario sea administrador"""
    role = db.query(Role).filter(Role.id == current_user.role_id).first()
    if not role or role.name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden realizar esta acción"
        )
    return current_user
