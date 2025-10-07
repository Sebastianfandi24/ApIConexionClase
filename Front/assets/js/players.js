import { CONFIG, APP_STATE, MESSAGES } from './config.js';
import { api } from './api.js';
import { ui } from './ui.js';
import { auth } from './auth.js';
import { Utils, Events } from './utils.js';

// Clase para manejar jugadores
export class PlayersManager {
    constructor() {
        this.setupEventListeners();
        this.setupValidation();
    }

    // Configurar event listeners
    setupEventListeners() {
        // Botones principales
        ui.elements.addPlayerBtn?.addEventListener('click', () => this.showAddForm());
        ui.elements.refreshBtn?.addEventListener('click', () => this.loadPlayers());
        ui.elements.cancelFormBtn?.addEventListener('click', () => this.hideForm());
        
        // Formulario
        ui.elements.playerForm?.addEventListener('submit', (e) => this.handlePlayerForm(e));
        
        // Paginación
        ui.elements.prevPageBtn?.addEventListener('click', () => this.changePage(APP_STATE.currentPage - 1));
        ui.elements.nextPageBtn?.addEventListener('click', () => this.changePage(APP_STATE.currentPage + 1));
        
        // Event listeners personalizados
        Events.on('auth:login', () => this.loadPlayers());
        Events.on('auth:logout', () => this.clearPlayers());
    }

    // Configurar validación en tiempo real
    setupValidation() {
        const form = ui.elements.playerForm;
        if (!form) return;

        const fields = {
            'player-name': { required: true, minLength: 2, maxLength: 100, label: 'Nombre' },
            'player-team': { required: true, minLength: 2, maxLength: 50, label: 'Equipo' },
            'player-position': { required: true, label: 'Posición' },
            'player-height': { required: true, min: 1.0, max: 3.0, label: 'Altura' },
            'player-weight': { required: true, min: 40, max: 200, label: 'Peso' },
            'player-birthdate': { required: true, label: 'Fecha de nacimiento' }
        };

        Object.entries(fields).forEach(([fieldId, rules]) => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('blur', () => ui.validateField(field, rules));
                field.addEventListener('input', Utils.debounce(() => ui.validateField(field, rules), 300));
            }
        });
    }

    // Cargar jugadores
    async loadPlayers() {
        if (!auth.isAuthenticated()) {
            ui.showNotification('Debes iniciar sesión para ver los jugadores.', 'error');
            return;
        }

        try {
            ui.showLoading(MESSAGES.LOADING.PLAYERS);
            
            const skip = (APP_STATE.currentPage - 1) * CONFIG.PLAYERS_PER_PAGE;
            const players = await api.getPlayers(skip, CONFIG.PLAYERS_PER_PAGE);
            
            APP_STATE.players = players;
            this.renderPlayers();
            this.updatePagination();
            
        } catch (error) {
            console.error('Error al cargar jugadores:', error);
            
            if (error.message.includes('expirada')) {
                auth.logout();
            } else {
                ui.showNotification(error.message || MESSAGES.ERROR.CONNECTION, 'error');
            }
        } finally {
            ui.hideLoading();
        }
    }

    // Renderizar jugadores
    renderPlayers() {
        if (!APP_STATE.players || APP_STATE.players.length === 0) {
            ui.elements.playersList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-basketball-ball"></i>
                    <h3>No hay jugadores registrados</h3>
                    <p>Agrega el primer jugador para comenzar.</p>
                </div>
            `;
            return;
        }

        ui.elements.playersList.innerHTML = APP_STATE.players.map(player => this.createPlayerCard(player)).join('');
    }

    // Crear tarjeta de jugador
    createPlayerCard(player) {
        return `
            <div class="player-card" data-player-id="${player.id}">
                <div class="player-header">
                    <div>
                        <div class="player-name">${Utils.escapeHtml(player.name)}</div>
                        <div class="player-team">${Utils.escapeHtml(player.team)}</div>
                    </div>
                    <div class="player-actions">
                        <button class="btn btn-secondary btn-icon" onclick="players.editPlayer(${player.id})" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-danger btn-icon" onclick="players.confirmDeletePlayer(${player.id})" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="player-details">
                    <div class="player-detail">
                        <i class="fas fa-ruler-vertical"></i>
                        <span>${player.height_m}m</span>
                    </div>
                    <div class="player-detail">
                        <i class="fas fa-weight"></i>
                        <span>${player.weight_kg}kg</span>
                    </div>
                    <div class="player-detail">
                        <i class="fas fa-calendar"></i>
                        <span>${Utils.formatDate(player.birth_date)}</span>
                    </div>
                    <div class="player-detail">
                        <i class="fas fa-clock"></i>
                        <span>Agregado: ${Utils.formatDate(player.created_at)}</span>
                    </div>
                </div>
                <div class="player-position">${Utils.escapeHtml(player.position)}</div>
            </div>
        `;
    }

    // Mostrar formulario para agregar
    showAddForm() {
        APP_STATE.editingPlayerId = null;
        ui.showPlayerForm(false);
    }

    // Mostrar formulario para editar
    async editPlayer(playerId) {
        const player = APP_STATE.players.find(p => p.id === playerId);
        
        if (!player) {
            ui.showNotification('Jugador no encontrado', 'error');
            return;
        }

        APP_STATE.editingPlayerId = playerId;
        ui.showPlayerForm(true, player);
    }

    // Ocultar formulario
    hideForm() {
        ui.hidePlayerForm();
        APP_STATE.editingPlayerId = null;
    }

    // Manejar envío de formulario
    async handlePlayerForm(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const playerData = {
            name: formData.get('name'),
            team: formData.get('team'),
            position: formData.get('position'),
            height_m: parseFloat(formData.get('height_m')),
            weight_kg: parseFloat(formData.get('weight_kg')),
            birth_date: formData.get('birth_date')
        };

        // Validación básica
        if (!this.validatePlayerData(playerData)) {
            return;
        }

        try {
            const isEdit = APP_STATE.editingPlayerId !== null;
            const loadingMessage = isEdit ? MESSAGES.LOADING.UPDATING : MESSAGES.LOADING.CREATING;
            
            ui.showLoading(loadingMessage);
            
            let result;
            if (isEdit) {
                result = await api.updatePlayer(APP_STATE.editingPlayerId, playerData);
            } else {
                result = await api.createPlayer(playerData);
            }
            
            const successMessage = isEdit ? MESSAGES.SUCCESS.PLAYER_UPDATED : MESSAGES.SUCCESS.PLAYER_CREATED;
            ui.showNotification(successMessage, 'success');
            
            this.hideForm();
            await this.loadPlayers();
            
        } catch (error) {
            console.error('Error al guardar jugador:', error);
            
            if (error.message.includes('expirada')) {
                auth.logout();
            } else {
                ui.showNotification(error.message || 'Error al guardar jugador', 'error');
            }
        } finally {
            ui.hideLoading();
        }
    }

    // Validar datos del jugador
    validatePlayerData(data) {
        const errors = [];

        if (!data.name || data.name.trim().length < 2) {
            errors.push('El nombre debe tener al menos 2 caracteres');
        }

        if (!data.team || data.team.trim().length < 2) {
            errors.push('El equipo debe tener al menos 2 caracteres');
        }

        if (!data.position) {
            errors.push('Debe seleccionar una posición');
        }

        if (!data.height_m || data.height_m < 1.0 || data.height_m > 3.0) {
            errors.push('La altura debe estar entre 1.0 y 3.0 metros');
        }

        if (!data.weight_kg || data.weight_kg < 40 || data.weight_kg > 200) {
            errors.push('El peso debe estar entre 40 y 200 kg');
        }

        if (!data.birth_date) {
            errors.push('Debe seleccionar una fecha de nacimiento');
        } else {
            const birthDate = new Date(data.birth_date);
            const today = new Date();
            if (birthDate >= today) {
                errors.push('La fecha de nacimiento debe ser anterior a hoy');
            }
        }

        if (errors.length > 0) {
            ui.showNotification(errors[0], 'error');
            return false;
        }

        return true;
    }

    // Confirmar eliminación
    confirmDeletePlayer(playerId) {
        const player = APP_STATE.players.find(p => p.id === playerId);
        if (!player) return;

        ui.showModal(
            'Confirmar Eliminación',
            `¿Estás seguro de que quieres eliminar al jugador "${player.name}"? Esta acción no se puede deshacer.`,
            () => this.deletePlayer(playerId)
        );
    }

    // Eliminar jugador
    async deletePlayer(playerId) {
        try {
            ui.showLoading(MESSAGES.LOADING.DELETING);
            
            await api.deletePlayer(playerId);
            
            ui.showNotification(MESSAGES.SUCCESS.PLAYER_DELETED, 'success');
            await this.loadPlayers();
            
        } catch (error) {
            console.error('Error al eliminar jugador:', error);
            
            if (error.message.includes('expirada')) {
                auth.logout();
            } else {
                ui.showNotification(error.message || 'Error al eliminar jugador', 'error');
            }
        } finally {
            ui.hideLoading();
        }
    }

    // Cambiar página
    changePage(page) {
        if (page < 1) return;
        APP_STATE.currentPage = page;
        this.loadPlayers();
    }

    // Actualizar paginación
    updatePagination() {
        const hasMore = APP_STATE.players.length === CONFIG.PLAYERS_PER_PAGE;
        ui.updatePagination(APP_STATE.currentPage, hasMore);
    }

    // Limpiar jugadores
    clearPlayers() {
        APP_STATE.players = [];
        APP_STATE.currentPage = 1;
        APP_STATE.editingPlayerId = null;
        
        if (ui.elements.playersList) {
            ui.elements.playersList.innerHTML = '';
        }
    }
}

// Instancia global para funciones onclick
export const players = new PlayersManager();

// Hacer disponible globalmente para los onclick del HTML
window.players = players;