"""
Configuración de documentación para la API NBA Players.
Define metadata, tags y configuraciones para la documentación interactiva.
"""

from typing import Dict, List, Any

# Tags para organizar los endpoints en la documentación
TAGS_METADATA: List[Dict[str, Any]] = [
    {
        "name": "NBA Players",
        "description": """
        **Operaciones CRUD para jugadores de la NBA** 🏀
        
        **⚠️ REQUIERE AUTENTICACIÓN JWT ⚠️**
        
        Este conjunto de endpoints permite gestionar completamente la información 
        de jugadores de la NBA, incluyendo:
        
        - **Crear** nuevos jugadores con validaciones robustas
        - **Consultar** jugadores individuales o listas paginadas
        - **Actualizar** información existente (parcial o completa)
        - **Eliminar** jugadores del sistema
        
        ### Validaciones incluidas:
        - Rangos de altura (1.0 - 3.0 metros)
        - Rangos de peso (50 - 200 kg)
        - Formatos de fecha válidos
        - Longitudes de texto apropiadas
        
        ### Autenticación:
        - Todos los endpoints requieren token JWT válido
        - Usar el header: `Authorization: Bearer <token>`
        - Lista limitada a 10 registros máximo para usuarios autenticados
        """,
        "externalDocs": {
            "description": "Documentación oficial de la NBA",
            "url": "https://www.nba.com/",
        },
    },
    {
        "name": "Autenticación",
        "description": """
        **Sistema de autenticación JWT** 🔐
        
        Endpoints para gestión de autenticación y autorización:
        
        - **Login**: Autenticación con username/password, retorna token JWT
        - **Register**: Registro de nuevos usuarios en el sistema
        - **Profile**: Información del usuario autenticado actual
        
        ### Flujo de autenticación:
        1. Registrar usuario con `/api/v1/auth/register`
        2. Hacer login con `/api/v1/auth/login` (retorna token)
        3. Usar token en header `Authorization: Bearer <token>`
        4. Acceder a endpoints protegidos
        
        ### Características de seguridad:
        - Contraseñas hasheadas con bcrypt
        - Tokens JWT con expiración (1 hora)
        - Validación de usuarios activos
        - Logging de eventos de autenticación
        """,
        "externalDocs": {
            "description": "JWT.io - Información sobre tokens JWT",
            "url": "https://jwt.io/",
        },
    },
    {
        "name": "Users",
        "description": """
        **Operaciones CRUD para usuarios del sistema** 👥
        
        Este conjunto de endpoints permite gestionar completamente la información 
        de usuarios del sistema, incluyendo:
        
        - **Crear** nuevos usuarios con validaciones robustas
        - **Consultar** usuarios individuales o listas paginadas
        - **Actualizar** información existente (parcial o completa)
        - **Eliminar** usuarios del sistema
        - **Buscar** usuarios por nombre de usuario
        
        ### Características de seguridad:
        - Contraseñas hasheadas automáticamente
        - Validación de nombres de usuario únicos
        - Formatos de entrada validados
        - Longitudes mínimas y máximas
        """,
        "externalDocs": {
            "description": "Mejores prácticas de gestión de usuarios",
            "url": "https://fastapi.tiangolo.com/tutorial/security/",
        },
    },
    {
        "name": "System",
        "description": """
        **Endpoints del sistema para monitoreo y estado** ⚙️
        
        Endpoints utilitarios para verificar el estado de la aplicación:
        
        - **Health Check**: Verifica conectividad con la base de datos
        - **Root**: Información general y navegación de la API
        - **Metrics**: Estadísticas de uso y rendimiento
        
        ### Uso recomendado:
        - Implementar en sistemas de monitoreo
        - Verificar estado antes de operaciones críticas
        - Debugging y troubleshooting
        """,
        "externalDocs": {
            "description": "Guía de monitoreo",
            "url": "https://fastapi.tiangolo.com/advanced/monitoring/",
        },
    },
]

# Información de contacto y licencia
CONTACT_INFO = {
    "name": "Equipo de Desarrollo NBA API",
    "url": "https://github.com/tu-usuario/nba-api",
    "email": "api-support@nbaapi.com",
}

LICENSE_INFO = {
    "name": "MIT License",
    "url": "https://opensource.org/licenses/MIT",
}

# Configuración de servidores
SERVERS = [
    {
        "url": "http://localhost:8000",
        "description": "Servidor de desarrollo local"
    },
    {
        "url": "https://api.nba-players.com",
        "description": "Servidor de producción"
    },
    {
        "url": "https://staging-api.nba-players.com", 
        "description": "Servidor de staging"
    }
]

# Configuración de respuestas comunes
COMMON_RESPONSES = {
    400: {
        "description": "Datos inválidos o formato incorrecto",
        "content": {
            "application/json": {
                "example": {
                    "detail": "La altura debe estar entre 1.0 y 3.0 metros"
                }
            }
        }
    },
    404: {
        "description": "Recurso no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Jugador con id 999 no encontrado"
                }
            }
        }
    },
    422: {
        "description": "Error de validación de datos",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "height_m"],
                            "msg": "ensure this value is greater than 1.0",
                            "type": "value_error.number.not_gt",
                            "ctx": {"limit_value": 1.0}
                        }
                    ]
                }
            }
        }
    },
    500: {
        "description": "Error interno del servidor",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Error interno del servidor. Por favor, inténtalo más tarde."
                }
            }
        }
    }
}

# Configuración de security schemes (para futuras implementaciones)
SECURITY_SCHEMES = {
    "ApiKeyAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key"
    },
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}

# Ejemplos de datos para la documentación
EXAMPLE_PLAYER = {
    "id": 1,
    "name": "LeBron James",
    "team": "Los Angeles Lakers",
    "position": "Small Forward",
    "height_m": 2.06,
    "weight_kg": 113.4,
    "birth_date": "1984-12-30T00:00:00",
    "created_at": "2025-09-04T00:00:00"
}

EXAMPLE_PLAYER_CREATE = {
    "name": "Stephen Curry",
    "team": "Golden State Warriors",
    "position": "Point Guard",
    "height_m": 1.91,
    "weight_kg": 84.8,
    "birth_date": "1988-03-14T00:00:00"
}

EXAMPLE_PLAYER_UPDATE = {
    "team": "Miami Heat",
    "position": "Power Forward"
}
