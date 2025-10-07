// Configuración de la API
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Estado de la aplicación
let currentUser = null;
let authToken = null;
let currentPage = 1;
const playersPerPage = 10;
let players = [];
let editingPlayerId = null;

// Elementos del DOM
const elements = {
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

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Verificar si hay un token guardado
    const savedToken = localStorage.getItem('auth_token');
    const savedUser = localStorage.getItem('current_user');
    
    if (savedToken && savedUser) {
        authToken = savedToken;
        currentUser = JSON.parse(savedUser);
        showPlayersSection();
        loadPlayers();
    } else {
        showAuthSection();
    }
}

function setupEventListeners() {
    // Eventos de autenticación
    elements.authBtn.addEventListener('click', showAuthSection);
    elements.logoutBtn.addEventListener('click', logout);
    elements.loginTab.addEventListener('click', () => switchAuthTab('login'));
    elements.registerTab.addEventListener('click', () => switchAuthTab('register'));
    elements.loginForm.addEventListener('submit', handleLogin);
    elements.registerForm.addEventListener('submit', handleRegister);
    
    // Eventos de jugadores
    elements.addPlayerBtn.addEventListener('click', showAddPlayerForm);
    elements.playerForm.addEventListener('submit', handlePlayerForm);
    elements.cancelFormBtn.addEventListener('click', hidePlayerForm);
    elements.refreshBtn.addEventListener('click', () => loadPlayers());
    
    // Eventos de paginación
    elements.prevPageBtn.addEventListener('click', () => changePage(currentPage - 1));
    elements.nextPageBtn.addEventListener('click', () => changePage(currentPage + 1));
    
    // Eventos del modal
    elements.modalClose.addEventListener('click', hideModal);
    elements.modalCancel.addEventListener('click', hideModal);
    
    // Eventos de notificaciones
    elements.notificationClose.addEventListener('click', hideNotification);
    
    // Cerrar modal al hacer clic fuera
    elements.modal.addEventListener('click', (e) => {
        if (e.target === elements.modal) {
            hideModal();
        }
    });
}

// === AUTENTICACIÓN ===

function switchAuthTab(tab) {
    if (tab === 'login') {
        elements.loginTab.classList.add('active');
        elements.registerTab.classList.remove('active');
        elements.loginForm.style.display = 'block';
        elements.registerForm.style.display = 'none';
    } else {
        elements.registerTab.classList.add('active');
        elements.loginTab.classList.remove('active');
        elements.registerForm.style.display = 'block';
        elements.loginForm.style.display = 'none';
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const loginData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    try {
        showLoading('Iniciando sesión...');
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            authToken = data.access_token;
            currentUser = { username: loginData.username };
            
            // Guardar en localStorage
            localStorage.setItem('auth_token', authToken);
            localStorage.setItem('current_user', JSON.stringify(currentUser));
            
            showNotification('¡Bienvenido! Sesión iniciada correctamente.', 'success');
            showPlayersSection();
            loadPlayers();
            
            // Limpiar formulario
            e.target.reset();
        } else {
            showNotification(data.detail || 'Error al iniciar sesión', 'error');
        }
    } catch (error) {
        console.error('Error en login:', error);
        showNotification('Error de conexión. Verifica que el servidor esté ejecutándose.', 'error');
    } finally {
        hideLoading();
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const registerData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    try {
        showLoading('Creando cuenta...');
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registerData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success');
            switchAuthTab('login');
            e.target.reset();
        } else {
            showNotification(data.detail || 'Error al crear la cuenta', 'error');
        }
    } catch (error) {
        console.error('Error en registro:', error);
        showNotification('Error de conexión. Verifica que el servidor esté ejecutándose.', 'error');
    } finally {
        hideLoading();
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('current_user');
    
    showNotification('Sesión cerrada correctamente.', 'success');
    showAuthSection();
    hidePlayerForm();
}

function showAuthSection() {
    elements.authSection.style.display = 'block';
    elements.playersSection.style.display = 'none';
    elements.authBtn.style.display = 'block';
    elements.logoutBtn.style.display = 'none';
}

function showPlayersSection() {
    elements.authSection.style.display = 'none';
    elements.playersSection.style.display = 'block';
    elements.authBtn.style.display = 'none';
    elements.logoutBtn.style.display = 'block';
}

// === GESTIÓN DE JUGADORES ===

async function loadPlayers() {
    if (!authToken) {
        showNotification('Debes iniciar sesión para ver los jugadores.', 'error');
        return;
    }
    
    try {
        showLoading('Cargando jugadores...');
        const skip = (currentPage - 1) * playersPerPage;
        
        const response = await fetch(`${API_BASE_URL}/players/?skip=${skip}&limit=${playersPerPage}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            players = await response.json();
            renderPlayers();
            updatePagination();
        } else if (response.status === 401) {
            showNotification('Sesión expirada. Por favor, inicia sesión nuevamente.', 'error');
            logout();
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Error al cargar jugadores', 'error');
        }
    } catch (error) {
        console.error('Error al cargar jugadores:', error);
        showNotification('Error de conexión. Verifica que el servidor esté ejecutándose.', 'error');
    } finally {
        hideLoading();
    }
}

function renderPlayers() {
    if (players.length === 0) {
        elements.playersList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-basketball-ball"></i>
                <h3>No hay jugadores registrados</h3>
                <p>Agrega el primer jugador para comenzar.</p>
            </div>
        `;
        return;
    }
    
    elements.playersList.innerHTML = players.map(player => `
        <div class="player-card" data-player-id="${player.id}">
            <div class="player-header">
                <div>
                    <div class="player-name">${escapeHtml(player.name)}</div>
                    <div class="player-team">${escapeHtml(player.team)}</div>
                </div>
                <div class="player-actions">
                    <button class="btn btn-secondary btn-icon" onclick="editPlayer(${player.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-danger btn-icon" onclick="confirmDeletePlayer(${player.id})" title="Eliminar">
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
                    <span>${formatDate(player.birth_date)}</span>
                </div>
                <div class="player-detail">
                    <i class="fas fa-clock"></i>
                    <span>Agregado: ${formatDate(player.created_at)}</span>
                </div>
            </div>
            <div class="player-position">${escapeHtml(player.position)}</div>
        </div>
    `).join('');
}

function showAddPlayerForm() {
    editingPlayerId = null;
    elements.formTitle.textContent = 'Agregar Nuevo Jugador';
    elements.playerForm.reset();
    elements.playerFormSection.style.display = 'block';
    elements.playerFormSection.scrollIntoView({ behavior: 'smooth' });
}

function hidePlayerForm() {
    elements.playerFormSection.style.display = 'none';
    elements.playerForm.reset();
    editingPlayerId = null;
}

async function handlePlayerForm(e) {
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
    
    try {
        showLoading(editingPlayerId ? 'Actualizando jugador...' : 'Creando jugador...');
        
        const url = editingPlayerId 
            ? `${API_BASE_URL}/players/${editingPlayerId}`
            : `${API_BASE_URL}/players/`;
        
        const method = editingPlayerId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(playerData)
        });
        
        if (response.ok) {
            const message = editingPlayerId 
                ? 'Jugador actualizado correctamente' 
                : 'Jugador creado correctamente';
            showNotification(message, 'success');
            hidePlayerForm();
            loadPlayers();
        } else if (response.status === 401) {
            showNotification('Sesión expirada. Por favor, inicia sesión nuevamente.', 'error');
            logout();
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Error al guardar jugador', 'error');
        }
    } catch (error) {
        console.error('Error al guardar jugador:', error);
        showNotification('Error de conexión. Verifica que el servidor esté ejecutándose.', 'error');
    } finally {
        hideLoading();
    }
}

async function editPlayer(playerId) {
    editingPlayerId = playerId;
    const player = players.find(p => p.id === playerId);
    
    if (!player) {
        showNotification('Jugador no encontrado', 'error');
        return;
    }
    
    // Llenar el formulario con los datos del jugador
    elements.formTitle.textContent = 'Editar Jugador';
    document.getElementById('player-name').value = player.name;
    document.getElementById('player-team').value = player.team;
    document.getElementById('player-position').value = player.position;
    document.getElementById('player-height').value = player.height_m;
    document.getElementById('player-weight').value = player.weight_kg;
    document.getElementById('player-birthdate').value = player.birth_date.split('T')[0];
    
    elements.playerFormSection.style.display = 'block';
    elements.playerFormSection.scrollIntoView({ behavior: 'smooth' });
}

function confirmDeletePlayer(playerId) {
    const player = players.find(p => p.id === playerId);
    if (!player) return;
    
    elements.modalTitle.textContent = 'Confirmar Eliminación';
    elements.modalMessage.textContent = `¿Estás seguro de que quieres eliminar al jugador "${player.name}"? Esta acción no se puede deshacer.`;
    
    elements.modalConfirm.onclick = () => deletePlayer(playerId);
    showModal();
}

async function deletePlayer(playerId) {
    try {
        hideModal();
        showLoading('Eliminando jugador...');
        
        const response = await fetch(`${API_BASE_URL}/players/${playerId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            showNotification('Jugador eliminado correctamente', 'success');
            loadPlayers();
        } else if (response.status === 401) {
            showNotification('Sesión expirada. Por favor, inicia sesión nuevamente.', 'error');
            logout();
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Error al eliminar jugador', 'error');
        }
    } catch (error) {
        console.error('Error al eliminar jugador:', error);
        showNotification('Error de conexión. Verifica que el servidor esté ejecutándose.', 'error');
    } finally {
        hideLoading();
    }
}

// === PAGINACIÓN ===

function changePage(page) {
    if (page < 1) return;
    currentPage = page;
    loadPlayers();
}

function updatePagination() {
    elements.pageInfo.textContent = `Página ${currentPage}`;
    elements.prevPageBtn.disabled = currentPage === 1;
    elements.nextPageBtn.disabled = players.length < playersPerPage;
}

// === UTILIDADES DE UI ===

function showModal() {
    elements.modal.style.display = 'flex';
}

function hideModal() {
    elements.modal.style.display = 'none';
}

function showNotification(message, type = 'info') {
    elements.notificationMessage.textContent = message;
    elements.notification.className = `notification ${type}`;
    elements.notification.style.display = 'block';
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        hideNotification();
    }, 5000);
}

function hideNotification() {
    elements.notification.style.display = 'none';
}

function showLoading(message = 'Cargando...') {
    if (elements.loading) {
        elements.loading.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            ${message}
        `;
        elements.loading.style.display = 'block';
    }
}

function hideLoading() {
    if (elements.loading) {
        elements.loading.style.display = 'none';
    }
}

// === UTILIDADES GENERALES ===

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Función global para manejar errores no capturados
window.addEventListener('error', function(e) {
    console.error('Error no capturado:', e.error);
    showNotification('Ha ocurrido un error inesperado.', 'error');
});

// Función global para manejar promesas rechazadas
window.addEventListener('unhandledrejection', function(e) {
    console.error('Promesa rechazada no manejada:', e.reason);
    showNotification('Error de conexión con el servidor.', 'error');
    e.preventDefault();
});

// Función para verificar el estado del servidor
async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);
        return response.ok;
    } catch (error) {
        return false;
    }
}

// Verificar estado del servidor cada 30 segundos
setInterval(async () => {
    if (authToken) {
        const isServerUp = await checkServerStatus();
        if (!isServerUp) {
            showNotification('Conexión con el servidor perdida. Verifica que el servidor esté ejecutándose.', 'warning');
        }
    }
}, 30000);