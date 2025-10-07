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

logger = logging.getLogger(__name__)

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
# GET /users → Listar usuarios (PROTEGIDO)
# -------------------------------
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Obtener lista de usuarios",
    description="""
    **Obtiene una lista paginada de todos los usuarios registrados en el sistema.**
    
    ### Parámetros de consulta:
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Máximo número de registros a retornar (1-100)
    
    ### Casos de uso:
    - Mostrar todos los usuarios en una interfaz de administración
    - Implementar paginación en aplicaciones frontend
    - Obtener datos para análisis masivo
    """,
    responses={
        200: {
            "description": "Lista de usuarios obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "username": "john_doe123",
                            "created_at": "2024-01-01T00:00:00"
                        }
                    ]
                }
            }
        }
    }
)
def get_users(
    current_user: User = Depends(get_current_user),  # ← Requiere JWT
    skip: int = Query(
        0, 
        ge=0, 
        description="Número de registros a saltar para paginación",
        example=0
    ),
    limit: int = Query(
        50, 
        ge=1, 
        le=100, 
        description="Máximo número de usuarios a retornar",
        example=10
    ),
    db: Session = Depends(get_db)
):
    """
    GET /users/
    Lista usuarios del sistema (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = UserService(db)
        users = service.get_all_users(skip=skip, limit=limit)
        
        logger.info(f"Usuario {current_user.username} consultó lista de usuarios (skip={skip}, limit={limit})")
        return users
        
    except Exception as e:
        logger.error(f"Error al listar usuarios: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# -------------------------------
# GET /users/{user_id} → Obtener usuario por ID
# -------------------------------
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="""
    **Obtiene un usuario específico mediante su identificador único.**
    
    ### Parámetros:
    - **user_id**: Identificador numérico del usuario
    
    ### Casos de uso:
    - Mostrar perfil de usuario
    - Obtener detalles específicos de un usuario
    - Validar existencia de usuario
    """,
    responses={
        200: {
            "description": "Usuario encontrado exitosamente",
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
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),  # ← Requiere JWT
    db: Session = Depends(get_db)
):
    """
    GET /users/{user_id}
    Obtiene un usuario específico por ID (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = UserService(db)
        user = service.obtener_usuario(user_id)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        logger.info(f"Usuario {current_user.username} consultó usuario ID: {user_id}")
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
# GET /users/username/{username} → Obtener usuario por username
# -------------------------------
@router.get(
    "/username/{username}",
    response_model=UserResponse,
    summary="Obtener usuario por nombre de usuario",
    description="""
    **Obtiene un usuario específico mediante su nombre de usuario.**
    
    ### Parámetros:
    - **username**: Nombre de usuario único
    
    ### Casos de uso:
    - Buscar usuario por nombre de usuario
    - Validar disponibilidad de username
    - Autenticación y login
    """,
    responses={
        200: {
            "description": "Usuario encontrado exitosamente"
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
    Obtiene un usuario específico por username (SOLO USUARIOS AUTENTICADOS)
    Requiere token JWT válido.
    """
    try:
        service = UserService(db)
        user = service.obtener_usuario_por_username(username)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con username '{username}' no encontrado"
            )
        
        logger.info(f"Usuario {current_user.username} consultó usuario por username: {username}")
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