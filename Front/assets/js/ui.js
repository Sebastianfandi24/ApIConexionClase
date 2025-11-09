import { CONFIG, MESSAGES } from './config.js';
import { Storage, Events } from './utils.js';

// Clase para manejar elementos de UI
export class UIManager {
    constructor() {
        this.elements = this.initializeElements();
        this.initializeEventListeners();
    }

    // Inicializar referencias a elementos del DOM
    initializeElements() {
        return {
            // Autenticación
            authSection: document.getElementById('auth-section'),
            playersSection: document.getElementById('players-section'),
            authBtn: document.getElementById('auth-btn'),
            logoutBtn: document.getElementById('logout-btn'),
            loginTab: document.getElementById('login-tab'),
            registerTab: document.getElementById('register-tab'),
            loginForm: document.getElementById('login-form'),
            registerForm: document.getElementById('register-form'),
            
            // Formulario de jugadores
            playerFormSection: document.getElementById('player-form-section'),
            addPlayerBtn: document.getElementById('add-player-btn'),
            playerForm: document.getElementById('player-form'),
            formTitle: document.getElementById('form-title'),
            cancelFormBtn: document.getElementById('cancel-form-btn'),
            
            // Lista de jugadores
            playersList: document.getElementById('players-list'),
            loading: document.getElementById('loading'),
            refreshBtn: document.getElementById('refresh-btn'),
            
            // Paginación
            prevPageBtn: document.getElementById('prev-page'),
            nextPageBtn: document.getElementById('next-page'),
            pageInfo: document.getElementById('page-info'),
            
            // Modal
            modal: document.getElementById('modal'),
            modalTitle: document.getElementById('modal-title'),
            modalMessage: document.getElementById('modal-message'),
            modalConfirm: document.getElementById('modal-confirm'),
            modalCancel: document.getElementById('modal-cancel'),
            modalClose: document.getElementById('modal-close'),
            
            // Notificaciones
            notification: document.getElementById('notification'),
            notificationMessage: document.getElementById('notification-message'),
            notificationClose: document.getElementById('notification-close')
        };
    }

    // Inicializar event listeners de UI
    initializeEventListeners() {
        // Modal
        if (this.elements.modalClose) {
            this.elements.modalClose.addEventListener('click', () => this.hideModal());
        }
        if (this.elements.modalCancel) {
            this.elements.modalCancel.addEventListener('click', () => this.hideModal());
        }
        
        // Notificaciones
        if (this.elements.notificationClose) {
            this.elements.notificationClose.addEventListener('click', () => this.hideNotification());
        }
        
        // Cerrar modal al hacer clic fuera
        if (this.elements.modal) {
            this.elements.modal.addEventListener('click', (e) => {
                if (e.target === this.elements.modal) {
                    this.hideModal();
                }
            });
        }
    }

    // Mostrar sección de autenticación
    showAuthSection() {
        this.elements.authSection.style.display = 'block';
        this.elements.playersSection.style.display = 'none';
        this.elements.authBtn.style.display = 'block';
        this.elements.logoutBtn.style.display = 'none';
    }

    // Mostrar sección de jugadores
    showPlayersSection() {
        this.elements.authSection.style.display = 'none';
        this.elements.playersSection.style.display = 'block';
        this.elements.authBtn.style.display = 'none';
        this.elements.logoutBtn.style.display = 'block';
    }

    // Cambiar pestañas de autenticación
    switchAuthTab(tab) {
        if (tab === 'login') {
            this.elements.loginTab.classList.add('active');
            this.elements.registerTab.classList.remove('active');
            this.elements.loginForm.style.display = 'block';
            this.elements.registerForm.style.display = 'none';
        } else {
            this.elements.registerTab.classList.add('active');
            this.elements.loginTab.classList.remove('active');
            this.elements.registerForm.style.display = 'block';
            this.elements.loginForm.style.display = 'none';
        }
    }

    // Mostrar formulario de jugador
    showPlayerForm(isEdit = false, playerData = null) {
        if (isEdit && playerData) {
            this.elements.formTitle.textContent = 'Editar Jugador';
            this.fillPlayerForm(playerData);
        } else {
            this.elements.formTitle.textContent = 'Agregar Nuevo Jugador';
            this.elements.playerForm.reset();
        }
        
        this.elements.playerFormSection.style.display = 'block';
        this.elements.playerFormSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Ocultar formulario de jugador
    hidePlayerForm() {
        this.elements.playerFormSection.style.display = 'none';
        this.elements.playerForm.reset();
    }

    // Llenar formulario con datos del jugador
    fillPlayerForm(player) {
        document.getElementById('player-name').value = player.name || '';
        document.getElementById('player-team').value = player.team || '';
        document.getElementById('player-position').value = player.position || '';
        document.getElementById('player-height').value = player.height_m || '';
        document.getElementById('player-weight').value = player.weight_kg || '';
        
        if (player.birth_date) {
            document.getElementById('player-birthdate').value = player.birth_date.split('T')[0];
        }
    }

    // Mostrar/ocultar carga
    showLoading(message = MESSAGES.LOADING.PLAYERS) {
        if (this.elements.loading) {
            this.elements.loading.innerHTML = `
                <i class="fas fa-spinner fa-spin"></i>
                ${message}
            `;
            this.elements.loading.style.display = 'block';
        }
    }

    hideLoading() {
        if (this.elements.loading) {
            this.elements.loading.style.display = 'none';
        }
    }

    // Actualizar información de paginación
    updatePagination(currentPage, hasMore) {
        if (this.elements.pageInfo) {
            this.elements.pageInfo.textContent = `Página ${currentPage}`;
        }
        if (this.elements.prevPageBtn) {
            this.elements.prevPageBtn.disabled = currentPage === 1;
        }
        if (this.elements.nextPageBtn) {
            this.elements.nextPageBtn.disabled = !hasMore;
        }
    }

    // Modal
    showModal(title, message, onConfirm) {
        this.elements.modalTitle.textContent = title;
        this.elements.modalMessage.textContent = message;
        
        // Limpiar event listeners anteriores
        const newConfirmBtn = this.elements.modalConfirm.cloneNode(true);
        this.elements.modalConfirm.parentNode.replaceChild(newConfirmBtn, this.elements.modalConfirm);
        this.elements.modalConfirm = newConfirmBtn;
        
        // Agregar nuevo event listener
        this.elements.modalConfirm.addEventListener('click', () => {
            this.hideModal();
            if (onConfirm) onConfirm();
        });
        
        this.elements.modal.style.display = 'flex';
    }

    hideModal() {
        this.elements.modal.style.display = 'none';
    }

    // Notificaciones
    showNotification(message, type = 'info', duration = 5000) {
        this.elements.notificationMessage.textContent = message;
        this.elements.notification.className = `notification ${type}`;
        this.elements.notification.style.display = 'block';
        
        // Auto-ocultar
        setTimeout(() => {
            this.hideNotification();
        }, duration);
    }

    hideNotification() {
        this.elements.notification.style.display = 'none';
    }

    // Validar formulario en tiempo real
    validateField(field, rules) {
        const value = field.value;
        const errors = [];

        if (rules.required && !value.trim()) {
            errors.push(`${rules.label} es requerido`);
        }

        if (value && rules.minLength && value.length < rules.minLength) {
            errors.push(`${rules.label} debe tener al menos ${rules.minLength} caracteres`);
        }

        if (value && rules.maxLength && value.length > rules.maxLength) {
            errors.push(`${rules.label} no puede tener más de ${rules.maxLength} caracteres`);
        }

        if (value && rules.min && parseFloat(value) < rules.min) {
            errors.push(`${rules.label} debe ser mayor a ${rules.min}`);
        }

        if (value && rules.max && parseFloat(value) > rules.max) {
            errors.push(`${rules.label} debe ser menor a ${rules.max}`);
        }

        // Mostrar/ocultar errores
        this.showFieldErrors(field, errors);
        
        return errors.length === 0;
    }

    showFieldErrors(field, errors) {
        // Remover errores anteriores
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }

        if (errors.length > 0) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.style.color = 'var(--danger-color)';
            errorDiv.style.fontSize = '0.875rem';
            errorDiv.style.marginTop = 'var(--spacing-xs)';
            errorDiv.textContent = errors[0];
            
            field.parentNode.appendChild(errorDiv);
            field.style.borderColor = 'var(--danger-color)';
        } else {
            field.style.borderColor = 'var(--border-color)';
        }
    }
}

// Instancia singleton del UI Manager
export const ui = new UIManager();