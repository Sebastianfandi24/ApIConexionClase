import { CONFIG, ENDPOINTS, MESSAGES } from './config.js';
import { Storage } from './utils.js';

// Clase para manejar las llamadas a la API
export class ApiService {
    constructor() {
        this.baseURL = CONFIG.API_BASE_URL;
    }

    // Obtener headers con autenticación
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (includeAuth) {
            const token = Storage.get(CONFIG.TOKEN_KEY);
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }

        return headers;
    }

    // Manejar respuestas de la API
    async handleResponse(response) {
        if (response.ok) {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            return response;
        }

        const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
        
        if (response.status === 401) {
            // Token expirado o inválido
            Storage.remove(CONFIG.TOKEN_KEY);
            Storage.remove(CONFIG.USER_KEY);
            throw new Error(MESSAGES.ERROR.UNAUTHORIZED);
        }

        throw new Error(error.detail || MESSAGES.ERROR.SERVER_ERROR);
    }

    // Realizar petición HTTP
    async request(endpoint, options = {}) {
        try {
            const url = `${this.baseURL}${endpoint}`;
            const config = {
                ...options,
                headers: {
                    ...this.getHeaders(options.auth !== false),
                    ...options.headers
                }
            };

            const response = await fetch(url, config);
            return await this.handleResponse(response);
        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error(MESSAGES.ERROR.CONNECTION);
            }
            throw error;
        }
    }

    // Métodos de autenticación
    async login(credentials) {
        return await this.request(ENDPOINTS.AUTH.LOGIN, {
            method: 'POST',
            body: JSON.stringify(credentials),
            auth: false
        });
    }

    async register(userData) {
        return await this.request(ENDPOINTS.AUTH.REGISTER, {
            method: 'POST',
            body: JSON.stringify(userData),
            auth: false
        });
    }

    async getProfile() {
        return await this.request(ENDPOINTS.AUTH.PROFILE);
    }

    // Métodos de jugadores
    async getPlayers(skip = 0, limit = CONFIG.PLAYERS_PER_PAGE) {
        return await this.request(`${ENDPOINTS.PLAYERS.LIST}?skip=${skip}&limit=${limit}`);
    }

    async getPlayer(id) {
        return await this.request(ENDPOINTS.PLAYERS.GET(id));
    }

    async createPlayer(playerData) {
        return await this.request(ENDPOINTS.PLAYERS.CREATE, {
            method: 'POST',
            body: JSON.stringify(playerData)
        });
    }

    async updatePlayer(id, playerData) {
        return await this.request(ENDPOINTS.PLAYERS.UPDATE(id), {
            method: 'PUT',
            body: JSON.stringify(playerData)
        });
    }

    async deletePlayer(id) {
        return await this.request(ENDPOINTS.PLAYERS.DELETE(id), {
            method: 'DELETE'
        });
    }

    // Verificar estado del servidor
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL.replace('/api/v1', '')}/health`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}

// Instancia singleton de la API
export const api = new ApiService();