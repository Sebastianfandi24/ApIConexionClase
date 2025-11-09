import { auth } from './auth.js';
import { players } from './players.js';
import { api } from './api.js';
import { ui } from './ui.js';
import { CONFIG, MESSAGES } from './config.js';

// Clase principal de la aplicación
class App {
    constructor() {
        this.initializeApp();
        this.setupGlobalErrorHandling();
        this.startHealthCheck();
    }

    // Inicializar la aplicación
    async initializeApp() {
        try {
            console.log('🏀 Iniciando NBA Players App...');
            
            // Los managers ya se inicializan en sus constructores
            // auth, players, ui están disponibles
            
            console.log('✅ App inicializada correctamente');
            
        } catch (error) {
            console.error('❌ Error al inicializar la app:', error);
            ui.showNotification('Error al inicializar la aplicación', 'error');
        }
    }

    // Configurar manejo global de errores
    setupGlobalErrorHandling() {
        // Errores no capturados
        window.addEventListener('error', (e) => {
            console.error('Error no capturado:', e.error);
            ui.showNotification(MESSAGES.ERROR.UNEXPECTED, 'error');
        });

        // Promesas rechazadas no manejadas
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Promesa rechazada no manejada:', e.reason);
            ui.showNotification(MESSAGES.ERROR.CONNECTION, 'error');
            e.preventDefault();
        });
    }

    // Verificar estado del servidor periódicamente
    startHealthCheck() {
        // Verificar inmediatamente
        this.checkServerHealth();
        
        // Verificar cada 30 segundos
        setInterval(() => {
            if (auth.isAuthenticated()) {
                this.checkServerHealth();
            }
        }, 30000);
    }

    // Verificar salud del servidor
    async checkServerHealth() {
        try {
            const isHealthy = await api.checkHealth();
            if (!isHealthy && auth.isAuthenticated()) {
                ui.showNotification(
                    'Conexión con el servidor perdida. Verifica que el servidor esté ejecutándose.',
                    'warning'
                );
            }
        } catch (error) {
            // Ignorar errores de health check para no ser molesto
            console.warn('Health check failed:', error);
        }
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});

// Exportar instancias para uso global si es necesario
export { auth, players, ui, api };