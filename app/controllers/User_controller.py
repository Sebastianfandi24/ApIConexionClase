from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.config.NBA_database import get_db
from app.services.User_service import UserService
from app.Schema.User_Schema import (
    UserCreate, 
    UserUpdate, 
    UserResponse, 
    MessageResponse, 
    ErrorResponse
)
from app.dependencies.auth_dependencies import get_current_user
from app.models.User_model import User
import logging

logger = logging.getLogger('nba_api.controllers.user')

# Router para endpoints de usuarios (TODOS PROTEGIDOS CON JWT)
router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    responses={
        401: {"description": "No autorizado - Token JWT requerido"},
        403: {"description": "Prohibido"},
        404: {"model": ErrorResponse, "description": "Usuario no encontrado"},
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)


# -------------------------------
# GET /users/me → Obtener mi perfil (PROTEGIDO)
# -------------------------------
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener mi perfil",
    description="""
    **Obtiene el perfil del usuario autenticado.**
    
    ### Seguridad:
    - Solo puedes ver tu propio perfil
    - Requiere token JWT válido
    
    ### Casos de uso:
    - Mostrar información del perfil del usuario logueado
    - Verificar datos personales
    - Obtener ID del usuario actual
    """,
    responses={
        200: {
            "description": "Perfil obtenido exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "john_doe123",
                        "created_at": "2024-01-01T00:00:00"
                    }
                }
            }
        }
    }
)
def get_my_profile(
    current_user: User = Depends(get_current_user),  # ← Requiere JWT
    db: Session = Depends(get_db)
):
    """
    GET /users/me
    Obtiene el perfil del usuario autenticado (SOLO SU PROPIO PERFIL)
    Requiere token JWT válido.
    """
    try:
        # Log detallado con información del usuario
        logger.info(f"� ACCIÓN: El usuario '{current_user.username}' (ID: {current_user.id}) consultó su propio perfil")
        
        return UserResponse(
            id=current_user.id,
            username=current_user.username,
            created_at=current_user.created_at
        )
        
    except Exception as e:
        logger.error(f"Error al obtener perfil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# GET /users/{user_id} → Solo permite ver tu propio perfil por ID
# -------------------------------
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID (solo tu propio perfil)",
    description="""
    **Obtiene la información de un usuario por ID, pero solo si es tu propio perfil.**
    
    ### Seguridad:
    - Solo puedes consultar tu propio ID de usuario
    - Si intentas ver otro ID, recibirás un error 403 Forbidden
    
    ### Parámetros:
    - **user_id**: Tu propio ID de usuario
    """,
    responses={
        200: {
            "description": "Tu perfil encontrado exitosamente"
        },
        403: {
            "description": "No puedes ver el perfil de otros usuarios"
        },
        404: {
            "description": "Usuario no encontrado"
        }
    }
)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),  # ← Requiere JWT
    db: Session = Depends(get_db)
):
    """
    GET /users/{user_id}
    Solo permite obtener tu propio perfil por ID
    Requiere token JWT válido.
    """
    try:
        # Verificar que el usuario solo pueda ver su propio perfil
        if user_id != current_user.id:
            logger.warning(f"🚫 SEGURIDAD: El usuario '{current_user.username}' (ID: {current_user.id}) intentó acceder al perfil del usuario ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ver el perfil de otros usuarios"
            )
        
        service = UserService(db)
        user = service.obtener_usuario(user_id)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        # Log detallado con información del usuario
        logger.info(f"👤 ACCIÓN: El usuario '{current_user.username}' (ID: {current_user.id}) consultó su propio perfil por ID")
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# GET /users/username/{username} → Solo permite buscar tu propio username
# -------------------------------
@router.get(
    "/username/{username}",
    response_model=UserResponse,
    summary="Obtener usuario por username (solo tu propio username)",
    description="""
    **Obtiene un usuario por nombre de usuario, pero solo si es tu propio username.**
    
    ### Seguridad:
    - Solo puedes buscar tu propio username
    - Si intentas buscar otro username, recibirás un error 403 Forbidden
    
    ### Parámetros:
    - **username**: Tu propio nombre de usuario
    """,
    responses={
        200: {
            "description": "Tu perfil encontrado exitosamente"
        },
        403: {
            "description": "No puedes buscar otros usuarios"
        },
        404: {
            "description": "Usuario no encontrado"
        }
    }
)
def get_user_by_username(
    username: str,
    current_user: User = Depends(get_current_user),  # ← Requiere JWT
    db: Session = Depends(get_db)
):
    """
    GET /users/username/{username}
    Solo permite buscar tu propio username
    Requiere token JWT válido.
    """
    try:
        # Verificar que el usuario solo pueda buscar su propio username
        if username != current_user.username:
            logger.warning(f"🚫 SEGURIDAD: El usuario '{current_user.username}' (ID: {current_user.id}) intentó buscar al usuario '{username}'")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para buscar otros usuarios"
            )
        
        service = UserService(db)
        user = service.obtener_usuario_por_username(username)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con username '{username}' no encontrado"
            )
        
        # Log detallado con información del usuario
        logger.info(f"🔍 ACCIÓN: El usuario '{current_user.username}' (ID: {current_user.id}) consultó su propio perfil por username")
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener usuario por username: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# POST /users → Crear nuevo usuario
# -------------------------------
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo usuario",
    description="""
    **Crea un nuevo usuario en el sistema.**
    
    ### Campos requeridos:
    - **username**: Nombre de usuario único (3-50 caracteres, solo letras, números y guiones bajos)
    - **password**: Contraseña del usuario (mínimo 6 caracteres)
    
    ### Validaciones automáticas:
    - Username único en el sistema
    - Formato de username válido
    - Longitud mínima de contraseña
    - Contraseña se almacena hasheada por seguridad
    """,
    responses={
        201: {
            "description": "Usuario creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "username": "john_doe123",
                        "created_at": "2024-01-01T00:00:00"
                    }
                }
            }
        },
        400: {
            "description": "Datos de entrada inválidos",
            "content": {
                "application/json": {
                    "example": {"detail": "El nombre de usuario 'john_doe123' ya está en uso"}
                }
            }
        }
    }
)
def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),  # ← Requiere JWT
    db: Session = Depends(get_db)
):
    """
    POST /users/
    Crea un nuevo usuario (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = UserService(db)
        new_user = service.crear_usuario(
            username=user_data.username,
            password=user_data.password
        )
        
        logger.info(f"Usuario {current_user.username} creó nuevo usuario: {user_data.username}")
        return new_user
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error al crear usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# PUT /users/{user_id} → Actualizar usuario
# -------------------------------
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="""
    **Actualiza los datos de un usuario existente.**
    
    ### Parámetros:
    - **user_id**: ID del usuario a actualizar
    
    ### Campos opcionales para actualizar:
    - **username**: Nuevo nombre de usuario (debe ser único)
    - **password**: Nueva contraseña (se hasheará automáticamente)
    
    ### Validaciones:
    - El usuario debe existir
    - Username único si se proporciona
    - Formato válido para todos los campos
    """,
    responses={
        200: {
            "description": "Usuario actualizado exitosamente"
        },
        404: {
            "description": "Usuario no encontrado"
        },
        400: {
            "description": "Datos de entrada inválidos"
        }
    }
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),  # ← Requiere JWT
    db: Session = Depends(get_db)
):
    """
    PUT /users/{user_id}
    Actualiza un usuario existente (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = UserService(db)
        updated_user = service.actualizar_usuario(
            user_id=user_id,
            username=user_data.username,
            password=user_data.password
        )
        
        logger.info(f"Usuario {current_user.username} actualizó usuario ID: {user_id}")
        return updated_user
        
    except ValueError as ve:
        if "no encontrado" in str(ve):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
    except Exception as e:
        logger.error(f"Error al actualizar usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


# -------------------------------
# DELETE /users/{user_id} → Eliminar usuario
# -------------------------------
@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Eliminar usuario",
    description="""
    **Elimina un usuario del sistema.**
    
    ### Parámetros:
    - **user_id**: ID del usuario a eliminar
    
    ### Comportamiento:
    - Elimina permanentemente el usuario de la base de datos
    - Retorna mensaje de confirmación
    - Error 404 si el usuario no existe
    """,
    responses={
        200: {
            "description": "Usuario eliminado exitosamente",
            "content": {
                "application/json": {
                    "example": {"message": "Usuario 'john_doe123' eliminado exitosamente"}
                }
            }
        },
        404: {
            "description": "Usuario no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Usuario con ID 999 no encontrado"}
                }
            }
        }
    }
)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),  # ← Requiere JWT
    db: Session = Depends(get_db)
):
    """
    DELETE /users/{user_id}
    Elimina un usuario (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = UserService(db)
        deleted_user = service.eliminar_usuario(user_id)
        
        logger.info(f"Usuario {current_user.username} eliminó usuario ID: {user_id}")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Usuario con ID {user_id} eliminado exitosamente"}
        )
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error al eliminar usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )