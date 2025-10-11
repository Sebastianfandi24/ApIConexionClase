from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.utils.jwt_utils import jwt_manager
from app.repositories.User_repository import UserRepository
from app.config.NBA_database import get_db
from app.models.User_model import User
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency que actúa como @jwt_required() de Flask
    Valida el token JWT y retorna el usuario actual
    """
    try:
        token = credentials.credentials
        payload = jwt_manager.verify_token(token)
        
        if not payload:
            logger.warning("Token JWT inválido o expirado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Token JWT malformado - sin email")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token malformado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_repo = UserRepository(db)
        user = user_repo.get_user_by_email(email)
        
        if user is None:
            logger.warning(f"Usuario no encontrado en token: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            logger.warning(f"Usuario inactivo intentó acceder: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en validación de token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error de autenticación",
            headers={"WWW-Authenticate": "Bearer"},
        )