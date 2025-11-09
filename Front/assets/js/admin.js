const API_URL = 'http://localhost:8000/api/v1';
let allPlayers = [];
let editingPlayerId = null;

// Verificar autenticación
function checkAuth() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        window.location.href = '../../login.html';
        return null;
    }

    const userData = JSON.parse(user);
    
    // Verificar que es admin
    if (userData.role_id !== 1) {
        // Si no es admin, redirigir a la página de usuario
        window.location.href = './user.html';
        return null;
    }

    return { token, user: userData };
}

// Cargar jugadores
async function loadPlayers() {
    const auth = checkAuth();
    if (!auth) return;

    const loading = document.getElementById('loading');
    const playersGrid = document.getElementById('players-grid');
    const errorMessage = document.getElementById('error-message');
    const emptyState = document.getElementById('empty-state');

    loading.style.display = 'flex';
    errorMessage.style.display = 'none';
    playersGrid.innerHTML = '';
    emptyState.style.display = 'none';

    try {
        const response = await fetch(`${API_URL}/players/?skip=0&limit=100`, {
            headers: {
                'Authorization': `Bearer ${auth.token}`
            }
        });

        if (!response.ok) {
            throw new Error('Error al cargar jugadores');
        }

        allPlayers = await response.json();
        displayPlayers(allPlayers);
        updateStats(allPlayers);

    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
}

// Mostrar jugadores
function displayPlayers(players) {
    const playersGrid = document.getElementById('players-grid');
    const emptyState = document.getElementById('empty-state');

    if (players.length === 0) {
        emptyState.style.display = 'flex';
        return;
    }

    playersGrid.innerHTML = players.map(player => `
        <div class="player-card admin-card">
            <div class="player-header">
                <div class="player-number">#${player.id}</div>
                <div class="player-position">${player.position}</div>
            </div>
            <div class="player-avatar">
                <i class="fas fa-user-circle"></i>
            </div>
            <h3 class="player-name">${player.name}</h3>
            <p class="player-team">
                <i class="fas fa-basketball-ball"></i>
                ${player.team}
            </p>
            <div class="player-stats">
                <div class="stat">
                    <i class="fas fa-ruler-vertical"></i>
                    <span>${player.height_m}m</span>
                </div>
                <div class="stat">
                    <i class="fas fa-weight"></i>
                    <span>${player.weight_kg}kg</span>
                </div>
            </div>
            <div class="player-actions">
                <button class="btn-edit" onclick="editPlayer(${player.id})">
                    <i class="fas fa-edit"></i>
                    Editar
                </button>
                <button class="btn-delete" onclick="deletePlayer(${player.id}, '${player.name}')">
                    <i class="fas fa-trash"></i>
                    Eliminar
                </button>
            </div>
        </div>
    `).join('');
}

// Actualizar estadísticas
function updateStats(players) {
    document.getElementById('total-players').textContent = players.length;
    const uniqueTeams = [...new Set(players.map(p => p.team))];
    document.getElementById('total-teams').textContent = uniqueTeams.length;
}

// Abrir modal de crear jugador
document.getElementById('add-player-btn').addEventListener('click', () => {
    editingPlayerId = null;
    document.getElementById('modal-title').textContent = 'Nuevo Jugador';
    document.getElementById('player-form').reset();
    document.getElementById('player-id').value = '';
    document.getElementById('player-modal').style.display = 'flex';
});

// Editar jugador
window.editPlayer = async function(playerId) {
    const auth = checkAuth();
    if (!auth) return;

    try {
        const response = await fetch(`${API_URL}/players/${playerId}`, {
            headers: {
                'Authorization': `Bearer ${auth.token}`
            }
        });

        const player = await response.json();

        editingPlayerId = playerId;
        document.getElementById('modal-title').textContent = 'Editar Jugador';
        document.getElementById('player-id').value = player.id;
        document.getElementById('player-name').value = player.name;
        document.getElementById('player-team').value = player.team;
        document.getElementById('player-position').value = player.position;
        document.getElementById('player-height').value = player.height_m;
        document.getElementById('player-weight').value = player.weight_kg;
        document.getElementById('player-birthdate').value = player.birth_date.split('T')[0];
        document.getElementById('player-modal').style.display = 'flex';

    } catch (error) {
        alert('Error al cargar jugador: ' + error.message);
    }
};

// Eliminar jugador
window.deletePlayer = async function(playerId, playerName) {
    if (!confirm(`¿Estás seguro de eliminar a ${playerName}?`)) {
        return;
    }

    const auth = checkAuth();
    if (!auth) return;

    try {
        const response = await fetch(`${API_URL}/players/${playerId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${auth.token}`
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al eliminar jugador');
        }

        alert('Jugador eliminado exitosamente');
        loadPlayers();

    } catch (error) {
        alert('Error: ' + error.message);
    }
};

// Guardar jugador (crear o actualizar)
document.getElementById('player-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const auth = checkAuth();
    if (!auth) return;

    const playerData = {
        name: document.getElementById('player-name').value,
        team: document.getElementById('player-team').value,
        position: document.getElementById('player-position').value,
        height_m: parseFloat(document.getElementById('player-height').value),
        weight_kg: parseFloat(document.getElementById('player-weight').value),
        birth_date: document.getElementById('player-birthdate').value
    };

    try {
        let response;
        
        if (editingPlayerId) {
            // Actualizar
            response = await fetch(`${API_URL}/players/${editingPlayerId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${auth.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(playerData)
            });
        } else {
            // Crear
            response = await fetch(`${API_URL}/players/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${auth.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(playerData)
            });
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al guardar jugador');
        }

        alert(editingPlayerId ? 'Jugador actualizado exitosamente' : 'Jugador creado exitosamente');
        document.getElementById('player-modal').style.display = 'none';
        loadPlayers();

    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Buscar jugadores
document.getElementById('search-input').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filtered = allPlayers.filter(player => 
        player.name.toLowerCase().includes(searchTerm) ||
        player.team.toLowerCase().includes(searchTerm) ||
        player.position.toLowerCase().includes(searchTerm)
    );
    displayPlayers(filtered);
});

// Cerrar modales
document.getElementById('close-player-modal').addEventListener('click', () => {
    document.getElementById('player-modal').style.display = 'none';
});

document.getElementById('cancel-btn').addEventListener('click', () => {
    document.getElementById('player-modal').style.display = 'none';
});

document.getElementById('close-profile').addEventListener('click', () => {
    document.getElementById('profile-modal').style.display = 'none';
});

// Mostrar perfil
document.getElementById('profile-link').addEventListener('click', (e) => {
    e.preventDefault();
    const auth = checkAuth();
    if (auth) {
        document.getElementById('profile-username').textContent = auth.user.username;
        document.getElementById('profile-modal').style.display = 'flex';
    }
});

// Cerrar sesión
document.getElementById('logout-btn').addEventListener('click', () => {
    if (confirm('¿Estás seguro de cerrar sesión?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '../../login.html';
    }
});

// ========================================
// GESTIÓN DE USUARIOS
// ========================================
let allUsers = [];
let currentView = 'players'; // 'players' o 'users'

// Cargar todos los usuarios
async function loadUsers() {
    const auth = checkAuth();
    if (!auth) return;

    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');

    loading.style.display = 'flex';
    errorMessage.style.display = 'none';

    try {
        const response = await fetch(`${API_URL}/users/all`, {
            headers: {
                'Authorization': `Bearer ${auth.token}`
            }
        });

        if (!response.ok) {
            throw new Error('Error al cargar usuarios');
        }

        allUsers = await response.json();
        displayUsers(allUsers);

    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
}

// Mostrar usuarios en tabla
function displayUsers(users) {
    const mainContent = document.querySelector('.main-content');
    
    mainContent.innerHTML = `
        <header class="content-header">
            <div class="header-left">
                <h1>👥 Gestión de Usuarios</h1>
                <p>Total de usuarios: ${users.length}</p>
            </div>
        </header>

        <div class="users-table-container">
            <table class="users-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Usuario</th>
                        <th>Contraseña (Hash)</th>
                        <th>Rol</th>
                        <th>Estado</th>
                        <th>Fecha Creación</th>
                    </tr>
                </thead>
                <tbody>
                    ${users.map(user => `
                        <tr>
                            <td>${user.id}</td>
                            <td><strong>${user.username}</strong></td>
                            <td><code class="password-hash">${user.password.substring(0, 30)}...</code></td>
                            <td>
                                <span class="role-badge ${user.role_id === 1 ? 'admin' : 'user'}">
                                    ${user.role?.name || (user.role_id === 1 ? 'Admin' : 'User')}
                                </span>
                            </td>
                            <td>
                                <span class="status-badge ${user.is_active ? 'active' : 'inactive'}">
                                    ${user.is_active ? 'Activo' : 'Inactivo'}
                                </span>
                            </td>
                            <td>${new Date(user.created_at).toLocaleDateString('es-ES')}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>

        <style>
            .users-table-container {
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                overflow-x: auto;
                margin-top: 20px;
            }

            .users-table {
                width: 100%;
                border-collapse: collapse;
            }

            .users-table thead {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }

            .users-table th {
                padding: 15px;
                text-align: left;
                font-weight: 600;
                font-size: 14px;
            }

            .users-table tbody tr {
                border-bottom: 1px solid #e5e7eb;
                transition: background 0.2s;
            }

            .users-table tbody tr:hover {
                background: #f9fafb;
            }

            .users-table td {
                padding: 15px;
                font-size: 14px;
            }

            .password-hash {
                background: #f3f4f6;
                padding: 4px 8px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color: #6b7280;
            }

            .role-badge {
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }

            .role-badge.admin {
                background: #fee2e2;
                color: #dc2626;
            }

            .role-badge.user {
                background: #dbeafe;
                color: #2563eb;
            }

            .status-badge {
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }

            .status-badge.active {
                background: #d1fae5;
                color: #059669;
            }

            .status-badge.inactive {
                background: #fee2e2;
                color: #dc2626;
            }
        </style>
    `;
}

// Volver a vista de jugadores
function showPlayersView() {
    currentView = 'players';
    const mainContent = document.querySelector('.main-content');
    
    // Restaurar el HTML original de jugadores
    mainContent.innerHTML = `
        <header class="content-header">
            <div class="header-left">
                <h1>🏀 Jugadores NBA</h1>
                <div class="search-box">
                    <i class="fas fa-search"></i>
                    <input type="text" id="search-input" placeholder="Buscar jugadores...">
                </div>
            </div>
            <div class="header-right">
                <button class="btn-primary" id="new-player-btn">
                    <i class="fas fa-plus"></i>
                    Nuevo Jugador
                </button>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card admin">
                <i class="fas fa-users"></i>
                <div>
                    <h3 id="total-players">0</h3>
                    <p>Total Jugadores</p>
                </div>
            </div>
            <div class="stat-card admin">
                <i class="fas fa-user-plus"></i>
                <div>
                    <h3>CRUD</h3>
                    <p>Control Total</p>
                </div>
            </div>
        </div>

        <div id="loading" class="loading" style="display: none;">
            <i class="fas fa-spinner fa-spin"></i>
            Cargando jugadores...
        </div>

        <div id="error-message" class="error-message" style="display: none;"></div>

        <div id="players-grid" class="players-grid"></div>

        <div id="empty-state" class="empty-state" style="display: none;">
            <i class="fas fa-basketball-ball"></i>
            <p>No hay jugadores registrados</p>
        </div>
    `;
    
    // Re-bind event listeners
    document.getElementById('new-player-btn').addEventListener('click', () => {
        editingPlayerId = null;
        document.getElementById('modal-title').textContent = 'Nuevo Jugador';
        document.getElementById('player-form').reset();
        document.getElementById('player-modal').style.display = 'flex';
    });

    document.getElementById('search-input').addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filtered = allPlayers.filter(player =>
            player.name.toLowerCase().includes(searchTerm) ||
            player.team.toLowerCase().includes(searchTerm) ||
            player.position.toLowerCase().includes(searchTerm)
        );
        displayPlayers(filtered);
    });

    loadPlayers();
}

// Event listener para navegación
document.getElementById('users-link').addEventListener('click', (e) => {
    e.preventDefault();
    
    // Actualizar navegación activa
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    e.currentTarget.classList.add('active');
    
    currentView = 'users';
    loadUsers();
});

document.querySelector('.nav-item').addEventListener('click', (e) => {
    e.preventDefault();
    
    // Actualizar navegación activa
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    e.currentTarget.classList.add('active');
    
    showPlayersView();
});

// Inicializar
window.addEventListener('DOMContentLoaded', () => {
    const auth = checkAuth();
    if (auth) {
        document.getElementById('username-display').textContent = auth.user.username;
        loadPlayers();
    }
});
