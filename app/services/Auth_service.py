from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.User_repository import UserRepository
from app.models.User_model import User
from app.utils.jwt_utils import jwt_manager
from app.Schema.Auth_Schema import TokenResponse, UserProfile
import logging

# Configurar logging para eventos de autenticación
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthService:
    """
    Servicio de autenticación siguiendo el patrón del repositorio de referencia
    Implementa la lógica de negocio para autenticación JWT
    """
    
    def __init__(self, db_session: Session):
        self.repository = UserRepository(db_session)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica un usuario verificando sus credenciales
        Siguiendo la implementación del repositorio de referencia
        """
        try:
            # Buscar usuario por email
            user = self.repository.get_user_by_email(email)
            
            if not user:
                logger.warning(f"Intento de login fallido: usuario '{email}' no encontrado")
                return None
            
            # Verificar si el usuario está activo
            if not user.is_active:
                logger.warning(f"Intento de login con usuario inactivo: '{email}'")
                return None
            
            # Verificar contraseña
            if not jwt_manager.verify_password(password, user.password):
                logger.warning(f"Intento de login fallido: contraseña incorrecta para '{email}'")
                return None
            
            logger.info(f"Login exitoso para usuario: '{email}'")
            return user
            
        except Exception as e:
            logger.error(f"Error durante autenticación: {str(e)}")
            raise ValueError(f"Error durante la autenticación: {str(e)}")
    
    def create_access_token(self, user: User) -> TokenResponse:
        """Crea un token JWT para el usuario autenticado"""
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "email": user.email
        }
        
        access_token = jwt_manager.create_access_token(data=token_data)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=jwt_manager.get_token_expires_seconds()
        )
    
    def create_access_token_custom(self, user: User, expires_in_seconds: int) -> TokenResponse:
        """Crea un token JWT con tiempo de expiración personalizado (SOLO PARA PRUEBAS)"""
        from datetime import timedelta
        
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "email": user.email
        }
        
        custom_expires = timedelta(seconds=expires_in_seconds)
        access_token = jwt_manager.create_access_token(data=token_data, expires_delta=custom_expires)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in_seconds
        )
    
    def create_user(self, email: str, password: str) -> User:
        """
        Crea un nuevo usuario con contraseña hasheada
        Siguiendo el patrón del repositorio de referencia
        """
        try:
            # Validaciones de negocio
            if not email or email.strip() == "":
                raise ValueError("El email no puede estar vacío")
            
            # EmailStr de Pydantic ya valida el formato de email
            if not password or len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            
            # Verificar si el usuario ya existe
            existing_user = self.repository.get_user_by_email(email)
            if existing_user:
                raise ValueError(f"El usuario con email '{email}' ya existe")
            
            # Hashear la contraseña
            hashed_password = jwt_manager.get_password_hash(password)
            
            # Crear el usuario
            new_user = self.repository.create_user_with_params(email, hashed_password)
            
            logger.info(f"Usuario creado exitosamente: '{email}'")
            return new_user
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error al crear usuario: {str(e)}")
            raise ValueError(f"Error al crear el usuario: {str(e)}")
    
    def get_current_user_profile(self, email: str) -> Optional[UserProfile]:
        """Obtiene el perfil del usuario actual"""
        try:
            user = self.repository.get_user_by_email(email)
            if not user or not user.is_active:
                return None
            
            return UserProfile(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at
            )
            
        except Exception as e:
            logger.error(f"Error al obtener perfil de usuario: {str(e)}")
            return None