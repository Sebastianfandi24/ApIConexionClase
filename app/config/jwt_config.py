import os
from datetime import timedelta

class JWTConfig:
    """Configuración JWT siguiendo el patrón del repositorio de referencia"""
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "tu_clave_secreta_jwt_por_defecto")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(seconds=3600)  # 1 hora
    JWT_TOKEN_LOCATION: list = ["headers"]
    JWT_HEADER_NAME: str = "Authorization"
    JWT_HEADER_TYPE: str = "Bearer"
    
    @classmethod
    def get_secret_key(cls) -> str:
        return cls.JWT_SECRET_KEY
    
    @classmethod
    def get_algorithm(cls) -> str:
        return cls.JWT_ALGORITHM
    
    @classmethod
    def get_expires_delta(cls) -> timedelta:
        return cls.JWT_ACCESS_TOKEN_EXPIRES

jwt_config = JWTConfig()