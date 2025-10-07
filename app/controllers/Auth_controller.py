from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.NBA_database import get_db
from app.services.Auth_service import AuthService
from app.Schema.Auth_Schema import LoginRequest, RegisterRequest, TokenResponse, UserProfile
from app.dependencies.auth_dependencies import get_current_user
from app.models.User_model import User
import logging

logger = logging.getLogger(__name__)

# Router para endpoints de autenticación
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Autenticación"],
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Prohibido"},
        500: {"description": "Error interno del servidor"}
    }
)

@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    POST /auth/login
    Autentica un usuario y genera un token JWT.
    Equivalente al endpoint /login del repositorio de referencia.
    """
    try:
        service = AuthService(db)
        
        # Autenticar usuario
        user = service.authenticate_user(login_data.username, login_data.password)
        
        if not user:
            logger.warning(f"Intento de login fallido para: {login_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        # Crear token JWT
        token_response = service.create_access_token(user)
        
        logger.info(f"Login exitoso para usuario: {login_data.username}")
        return token_response
        
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/register", response_model=dict)
def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    POST /auth/register
    Registra un nuevo usuario en el sistema.
    Equivalente al endpoint /registry del repositorio de referencia.
    """
    try:
        service = AuthService(db)
        
        # Crear usuario
        new_user = service.create_user(register_data.username, register_data.password)
        
        logger.info(f"Usuario registrado exitosamente: {register_data.username}")
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Usuario creado exitosamente",
                "user_id": new_user.id,
                "username": new_user.username
            }
        )
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/profile", response_model=UserProfile)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET /auth/profile
    Obtiene el perfil del usuario autenticado.
    Requiere token JWT válido.
    """
    try:
        service = AuthService(db)
        profile = service.get_current_user_profile(current_user.username)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de usuario no encontrado"
            )
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener perfil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )