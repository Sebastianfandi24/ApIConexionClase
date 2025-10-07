import logging
import sys
from datetime import datetime

class NBALogFormatter(logging.Formatter):
    """
    Formateador personalizado para los logs de la NBA API
    """
    
    def __init__(self):
        super().__init__()
        
    def format(self, record):
        # Colores para diferentes niveles
        colors = {
            'DEBUG': '\033[36m',    # Cyan
            'INFO': '\033[32m',     # Verde
            'WARNING': '\033[33m',  # Amarillo
            'ERROR': '\033[31m',    # Rojo
            'CRITICAL': '\033[35m', # Magenta
        }
        
        # Color de reset
        reset = '\033[0m'
        
        # Obtener color para el nivel
        color = colors.get(record.levelname, '')
        
        # Formatear timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Emojis para diferentes tipos de acciones
        emoji_map = {
            '🔐 ACCIÓN': '🔐',  # Login
            '🏀 ACCIÓN': '🏀',  # Jugadores
            '👥 ACCIÓN': '👥',  # Usuarios lista
            '👤 ACCIÓN': '👤',  # Usuario específico
            '🔍 ACCIÓN': '🔍',  # Búsquedas
            '➕ ACCIÓN': '➕',  # Crear
            '✏️ ACCIÓN': '✏️',   # Actualizar
            '🗑️ ACCIÓN': '🗑️',   # Eliminar
            '❌': '❌',         # Errores
        }
        
        # Buscar emoji en el mensaje
        mensaje = record.getMessage()
        emoji_usado = ''
        for patron, emoji in emoji_map.items():
            if patron in mensaje:
                emoji_usado = emoji + ' '
                break
        
        # Crear mensaje formateado
        if record.name == '__main__' or 'NBA' in record.name or any(x in mensaje for x in ['ACCIÓN', '🔐', '🏀', '👥', '👤', '🔍', '➕', '✏️', '🗑️']):
            # Logs de nuestra aplicación
            formatted_message = f"{color}{timestamp} [NBA-API] {emoji_usado}{mensaje}{reset}"
        else:
            # Logs de FastAPI/sistema
            formatted_message = f"{timestamp} [{record.levelname}] {mensaje}"
            
        return formatted_message

def setup_nba_logging():
    """
    Configura el sistema de logging para la NBA API
    """
    
    # Crear handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(NBALogFormatter())
    
    # Configurar logger principal
    root_logger = logging.getLogger()
    
    # Limpiar handlers existentes
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Agregar nuestro handler
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)
    
    # Configurar loggers específicos
    nba_logger = logging.getLogger('nba_api')
    nba_logger.setLevel(logging.INFO)
    
    # Silenciar algunos logs muy verbosos
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    return nba_logger

# Crear logger específico para NBA
nba_logger = setup_nba_logging()