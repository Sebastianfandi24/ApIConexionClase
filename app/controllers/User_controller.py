from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import re

from app.config.NBA_database import get_db
from app.services.User_service import (
    listar_usuarios,
    obtener_usuario,
    obtener_usuario_por_username,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario
)
from app.Schema.User_Schema import (
    UserCreate, 
    UserUpdate, 
    UserResponse, 
    MessageResponse, 
    ErrorResponse
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        404: {"model": ErrorResponse, "description": "Usuario no encontrado"},
        400: {"model": ErrorResponse, "description": "Datos inválidos"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)


# -------------------------------
# Helper → Validación de user_id
# -------------------------------
def validar_id(user_id: str):
    if not re.match(r"^[0-9]+$", user_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del usuario debe ser un número válido."
        )


# -------------------------------
# GET /users → Listar usuarios
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
    Endpoint para obtener una lista paginada de usuarios.
    """
    try:
        users = listar_usuarios(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
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
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un usuario específico por su ID.
    """
    try:
        user = obtener_usuario(db, user_id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
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
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un usuario específico por su username.
    """
    try:
        user = obtener_usuario_por_username(db, username=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con username '{username}' no encontrado"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
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
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo usuario.
    """
    try:
        new_user = crear_usuario(
            db,
            username=user_data.username,
            password=user_data.password
        )
        return new_user
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
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
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar un usuario existente.
    """
    try:
        updated_user = actualizar_usuario(
            db,
            user_id=user_id,
            username=user_data.username,
            password=user_data.password
        )
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
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar un usuario.
    """
    try:
        deleted_user = eliminar_usuario(db, user_id=user_id)
        return MessageResponse(
            message=f"Usuario '{deleted_user.username}' eliminado exitosamente"
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )