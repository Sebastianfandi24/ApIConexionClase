import { CONFIG, APP_STATE, MESSAGES } from './config.js';
import { api } from './api.js';
import { ui } from './ui.js';
import { Storage, Events } from './utils.js';

// Clase para manejar autenticación
export class AuthManager {
    constructor() {
        this.initializeAuth();
        this.setupEventListeners();
    }

    // Inicializar autenticación
    initializeAuth() {
        const savedToken = Storage.get(CONFIG.TOKEN_KEY);
        const savedUser = Storage.get(CONFIG.USER_KEY);
        
        if (savedToken && savedUser) {
            APP_STATE.authToken = savedToken;
            APP_STATE.currentUser = savedUser;
            ui.showPlayersSection();
            Events.dispatch('auth:login', { user: savedUser });
        } else {
            ui.showAuthSection();
        }
    }

    // Configurar event listeners
    setupEventListeners() {
        // Botones de navegación
        ui.elements.authBtn?.addEventListener('click', () => this.showLogin());
        ui.elements.logoutBtn?.addEventListener('click', () => this.logout());
        
        // Pestañas de autenticación
        ui.elements.loginTab?.addEventListener('click', () => ui.switchAuthTab('login'));
        ui.elements.registerTab?.addEventListener('click', () => ui.switchAuthTab('register'));
        
        // Formularios
        ui.elements.loginForm?.addEventListener('submit', (e) => this.handleLogin(e));
        ui.elements.registerForm?.addEventListener('submit', (e) => this.handleRegister(e));
    }

    // Mostrar pantalla de login
    showLogin() {
        ui.showAuthSection();
        ui.switchAuthTab('login');
    }

    // Manejar login
    async handleLogin(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const credentials = {
            username: formData.get('username'),
            password: formData.get('password')
        };

        // Validación básica
        if (!credentials.username || !credentials.password) {
            ui.showNotification('Por favor, completa todos los campos', 'error');
            return;
        }

        try {
            ui.showLoading(MESSAGES.LOADING.LOGIN);
            
            const response = await api.login(credentials);
            
            // Guardar datos de autenticación
            APP_STATE.authToken = response.access_token;
            APP_STATE.currentUser = { 
                username: credentials.username,
                token_type: response.token_type
            };
            
            Storage.set(CONFIG.TOKEN_KEY, APP_STATE.authToken);
            Storage.set(CONFIG.USER_KEY, APP_STATE.currentUser);
            
            // Mostrar éxito y cambiar vista
            ui.showNotification(MESSAGES.SUCCESS.LOGIN, 'success');
            ui.showPlayersSection();
            
            // Limpiar formulario
            e.target.reset();
            
            // Disparar evento
            Events.dispatch('auth:login', { user: APP_STATE.currentUser });
            
        } catch (error) {
            console.error('Error en login:', error);
            ui.showNotification(error.message || MESSAGES.ERROR.LOGIN_FAILED, 'error');
        } finally {
            ui.hideLoading();
        }
    }

    // Manejar registro
    async handleRegister(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const userData = {
            username: formData.get('username'),
            password: formData.get('password')
        };

        // Validación básica
        if (!userData.username || !userData.password) {
            ui.showNotification('Por favor, completa todos los campos', 'error');
            return;
        }

        if (userData.password.length < 6) {
            ui.showNotification('La contraseña debe tener al menos 6 caracteres', 'error');
            return;
        }

        try {
            ui.showLoading(MESSAGES.LOADING.REGISTER);
            
            await api.register(userData);
            
            ui.showNotification(MESSAGES.SUCCESS.REGISTER, 'success');
            ui.switchAuthTab('login');
            e.target.reset();
            
        } catch (error) {
            console.error('Error en registro:', error);
            ui.showNotification(error.message || MESSAGES.ERROR.REGISTER_FAILED, 'error');
        } finally {
            ui.hideLoading();
        }
    }

    // Cerrar sesión
    logout() {
        // Limpiar estado
        APP_STATE.authToken = null;
        APP_STATE.currentUser = null;
        APP_STATE.players = [];
        APP_STATE.editingPlayerId = null;
        APP_STATE.currentPage = 1;
        
        // Limpiar almacenamiento
        Storage.remove(CONFIG.TOKEN_KEY);
        Storage.remove(CONFIG.USER_KEY);
        
        // Cambiar vista
        ui.showAuthSection();
        ui.hidePlayerForm();
        
        // Mostrar mensaje
        ui.showNotification(MESSAGES.SUCCESS.LOGOUT, 'success');
        
        // Disparar evento
        Events.dispatch('auth:logout');
    }

    // Verificar si está autenticado
    isAuthenticated() {
        return !!(APP_STATE.authToken && APP_STATE.currentUser);
    }

    // Obtener usuario actual
    getCurrentUser() {
        return APP_STATE.currentUser;
    }

    // Obtener token
    getToken() {
        return APP_STATE.authToken;
    }
}

// Instancia singleton del Auth Manager
export const auth = new AuthManager();