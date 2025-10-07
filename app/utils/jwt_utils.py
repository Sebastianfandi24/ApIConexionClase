from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config.jwt_config import jwt_config

# Contexto para hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class JWTManager:
    """Gestor de JWT siguiendo el patrón del repositorio de referencia"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Genera el hash de una contraseña"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Crea un token JWT de acceso"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + jwt_config.get_expires_delta()
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            jwt_config.get_secret_key(), 
            algorithm=jwt_config.get_algorithm()
        )
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verifica y decodifica un token JWT"""
        try:
            payload = jwt.decode(
                token, 
                jwt_config.get_secret_key(), 
                algorithms=[jwt_config.get_algorithm()]
            )
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def get_token_expires_seconds() -> int:
        """Obtiene el tiempo de expiración en segundos"""
        return int(jwt_config.get_expires_delta().total_seconds())

jwt_manager = JWTManager()