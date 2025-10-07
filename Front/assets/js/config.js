// Configuración de la aplicación
export const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api/v1',
    PLAYERS_PER_PAGE: 10,
    TOKEN_KEY: 'auth_token',
    USER_KEY: 'current_user'
};

// Estados de la aplicación
export const APP_STATE = {
    currentUser: null,
    authToken: null,
    currentPage: 1,
    players: [],
    editingPlayerId: null
};

// Configuración de endpoints
export const ENDPOINTS = {
    AUTH: {
        LOGIN: '/auth/login',
        REGISTER: '/auth/register',
        PROFILE: '/auth/profile'
    },
    PLAYERS: {
        LIST: '/players/',
        GET: (id) => `/players/${id}`,
        CREATE: '/players/',
        UPDATE: (id) => `/players/${id}`,
        DELETE: (id) => `/players/${id}`
    },
    HEALTH: '/health'
};

// Mensajes de la aplicación
export const MESSAGES = {
    SUCCESS: {
        LOGIN: '¡Bienvenido! Sesión iniciada correctamente.',
        REGISTER: '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.',
        LOGOUT: 'Sesión cerrada correctamente.',
        PLAYER_CREATED: 'Jugador creado correctamente',
        PLAYER_UPDATED: 'Jugador actualizado correctamente',
        PLAYER_DELETED: 'Jugador eliminado correctamente'
    },
    ERROR: {
        LOGIN_FAILED: 'Error al iniciar sesión',
        REGISTER_FAILED: 'Error al crear la cuenta',
        CONNECTION: 'Error de conexión. Verifica que el servidor esté ejecutándose.',
        UNAUTHORIZED: 'Sesión expirada. Por favor, inicia sesión nuevamente.',
        PLAYER_NOT_FOUND: 'Jugador no encontrado',
        SERVER_ERROR: 'Error interno del servidor',
        UNEXPECTED: 'Ha ocurrido un error inesperado.'
    },
    LOADING: {
        LOGIN: 'Iniciando sesión...',
        REGISTER: 'Creando cuenta...',
        PLAYERS: 'Cargando jugadores...',
        CREATING: 'Creando jugador...',
        UPDATING: 'Actualizando jugador...',
        DELETING: 'Eliminando jugador...'
    }
};