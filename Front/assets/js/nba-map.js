/**
 * 🗺️ NBA MAP MODULE
 * 
 * Módulo para gestionar el mapa interactivo de equipos NBA
 * Utiliza Leaflet.js para renderizar mapas y marcadores
 * 
 * Funcionalidades:
 * - Cargar ubicaciones de equipos desde la API
 * - Mostrar marcadores en el mapa
 * - Popups con información de equipos
 * - Estadísticas de jugadores por equipo
 * 
 * Autor: NBA API Team
 * Fecha: 2025-11-02
 */

// ========================================
// CONFIGURACIÓN Y CONSTANTES
// ========================================

/**
 * URL base de la API
 * @constant {string}
 */
const API_URL = 'http://localhost:8000/api/v1';

/**
 * Referencia al mapa de Leaflet
 * @type {L.Map|null}
 */
let nbaMap = null;

/**
 * Array con todas las ubicaciones de equipos
 * @type {Array}
 */
let teamsLocations = [];

/**
 * Capa de marcadores para controlar visibilidad
 * @type {L.LayerGroup|null}
 */
let markersLayer = null;

// ========================================
// FUNCIONES DE AUTENTICACIÓN
// ========================================

/**
 * Verifica si el usuario está autenticado
 * Lee el token y datos del usuario desde localStorage
 * 
 * @returns {Object|null} - Objeto con token y usuario, o null si no está autenticado
 */
function checkAuth() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        console.warn('⚠️ Usuario no autenticado');
        return null;
    }

    try {
        const userData = JSON.parse(user);
        return { token, user: userData };
    } catch (error) {
        console.error('❌ Error al parsear datos del usuario:', error);
        return null;
    }
}

// ========================================
// FUNCIONES DE CARGA DE DATOS
// ========================================

/**
 * Carga las ubicaciones de los equipos NBA desde la API
 * Requiere autenticación JWT
 * 
 * @async
 * @returns {Promise<Array>} - Array con las ubicaciones de equipos
 * @throws {Error} - Si falla la petición a la API
 */
async function loadTeamsLocations() {
    const auth = checkAuth();
    if (!auth) {
        console.error('❌ No se puede cargar ubicaciones sin autenticación');
        throw new Error('No hay autenticación válida');
    }

    try {
        console.log('🔄 Cargando ubicaciones de equipos NBA...');
        console.log('🔑 Token:', auth.token.substring(0, 20) + '...');
        
        const url = `${API_URL}/nba-map/teams-locations`;
        console.log('🌐 URL:', url);
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${auth.token}`,
                'Content-Type': 'application/json'
            }
        });

        console.log('📡 Response status:', response.status);
        console.log('📡 Response ok:', response.ok);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Error response:', errorText);
            throw new Error(`Error HTTP: ${response.status} - ${errorText}`);
        }

        const locations = await response.json();
        console.log(`✅ ${locations.length} equipos cargados exitosamente`);
        console.log('📦 Primer equipo:', locations[0]);
        
        return locations;

    } catch (error) {
        console.error('❌ Error al cargar ubicaciones:', error);
        throw error;
    }
}

// ========================================
// FUNCIONES DE MAPA
// ========================================

/**
 * Inicializa el mapa de Leaflet
 * Centra el mapa en Estados Unidos y configura opciones básicas
 * 
 * @param {string} containerId - ID del contenedor HTML donde se renderiza el mapa
 * @returns {L.Map} - Instancia del mapa de Leaflet
 */
function initializeMap(containerId = 'nba-map') {
    console.log('🗺️ Inicializando mapa NBA...');
    
    // Crear mapa centrado en Estados Unidos
    const map = L.map(containerId).setView([39.8283, -98.5795], 4);

    // Agregar capa de tiles (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
        minZoom: 3
    }).addTo(map);

    // Crear capa de marcadores
    markersLayer = L.layerGroup().addTo(map);

    console.log('✅ Mapa inicializado correctamente');
    return map;
}

/**
 * Crea el contenido HTML del popup para un equipo
 * Muestra información del equipo, clima y lista de jugadores
 * 
 * @param {Object} team - Objeto con datos del equipo
 * @param {string} team.team - Nombre del equipo
 * @param {string} team.city - Ciudad del equipo
 * @param {string} team.state - Estado del equipo
 * @param {string} team.stadium - Estadio del equipo
 * @param {number} team.players_count - Cantidad de jugadores
 * @param {Array<string>} team.players - Lista de nombres de jugadores
 * @param {Object} team.weather - Información del clima
 * @returns {string} - HTML del popup
 */
function createPopupContent(team) {
    // HTML de jugadores
    const playersHTML = team.players && team.players.length > 0
        ? `<ul class="players-list">
            ${team.players.slice(0, 5).map(player => `
                <li><i class="fas fa-basketball-ball"></i> ${player}</li>
            `).join('')}
            ${team.players.length > 5 ? `
                <li class="more-players">
                    <i class="fas fa-plus-circle"></i>
                    ...y ${team.players.length - 5} jugadores más
                </li>
            ` : ''}
           </ul>`
        : '<p class="no-players"><em>No hay jugadores registrados</em></p>';

    // HTML del clima (si está disponible)
    let weatherHTML = '';
    if (team.weather) {
        const w = team.weather;
        const iconUrl = `https://openweathermap.org/img/wn/${w.icon}@2x.png`;
        
        // Emoji según temperatura
        let tempEmoji = '🌡️';
        if (w.temperature > 30) tempEmoji = '🥵';
        else if (w.temperature > 25) tempEmoji = '☀️';
        else if (w.temperature > 15) tempEmoji = '🌤️';
        else if (w.temperature > 5) tempEmoji = '🌥️';
        else tempEmoji = '🥶';
        
        weatherHTML = `
            <div class="weather-info">
                <h4><i class="fas fa-cloud-sun"></i> Clima Actual</h4>
                <div class="weather-content">
                    <div class="weather-main">
                        <img src="${iconUrl}" alt="${w.description}" class="weather-icon">
                        <div class="weather-temp">
                            <span class="temp-value">${tempEmoji} ${w.temperature}°C</span>
                            <span class="temp-description">${w.description}</span>
                        </div>
                    </div>
                    <div class="weather-details">
                        <div class="weather-item">
                            <i class="fas fa-temperature-high"></i>
                            <span>Sensación: ${w.feels_like}°C</span>
                        </div>
                        <div class="weather-item">
                            <i class="fas fa-tint"></i>
                            <span>Humedad: ${w.humidity}%</span>
                        </div>
                        <div class="weather-item">
                            <i class="fas fa-wind"></i>
                            <span>Viento: ${w.wind_speed} km/h</span>
                        </div>
                        <div class="weather-item">
                            <i class="fas fa-cloud"></i>
                            <span>Nubes: ${w.clouds}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    return `
        <div class="team-popup">
            <div class="team-popup-header">
                <h3 class="team-name">
                    <i class="fas fa-basketball-ball"></i>
                    ${team.team}
                </h3>
                <div class="team-location">
                    <i class="fas fa-map-marker-alt"></i>
                    ${team.city}, ${team.state}
                </div>
            </div>
            <div class="team-popup-body">
                <div class="team-stadium">
                    <strong><i class="fas fa-building"></i> Estadio:</strong>
                    <span>${team.stadium}</span>
                </div>
                
                ${weatherHTML}
                
                <div class="players-count">
                    <i class="fas fa-users"></i>
                    ${team.players_count} jugador${team.players_count !== 1 ? 'es' : ''}:
                </div>
                <div class="team-players">
                    ${playersHTML}
                </div>
            </div>
        </div>
    `;
}

/**
 * Determina el color del marcador según la cantidad de jugadores
 * 
 * @param {number} playersCount - Cantidad de jugadores en el equipo
 * @returns {string} - Color del marcador ('red', 'orange', 'green', 'blue')
 */
function getMarkerColor(playersCount) {
    if (playersCount >= 5) return 'red';      // 5+ jugadores
    if (playersCount >= 3) return 'orange';   // 3-4 jugadores
    if (playersCount >= 1) return 'green';    // 1-2 jugadores
    return 'blue';                            // Sin jugadores
}

/**
 * Agrega marcadores al mapa para cada equipo
 * Crea popups con información del equipo
 * 
 * @param {Array} locations - Array de ubicaciones de equipos
 */
function addMarkersToMap(locations) {
    console.log(`📍 Agregando ${locations.length} marcadores al mapa...`);
    console.log('📦 Datos recibidos:', locations);
    
    // Limpiar marcadores previos
    if (markersLayer) {
        markersLayer.clearLayers();
    }

    // Verificar que tenemos datos válidos
    if (!locations || locations.length === 0) {
        console.warn('⚠️ No hay ubicaciones para mostrar');
        return;
    }

    // Agregar un marcador por cada equipo
    locations.forEach((team, index) => {
        console.log(`🏀 Procesando equipo ${index + 1}:`, team.team);
        console.log(`   📍 Coordenadas: [${team.latitude}, ${team.longitude}]`);
        console.log(`   👥 Jugadores: ${team.players_count}`);
        
        // Validar coordenadas
        if (!team.latitude || !team.longitude) {
            console.error(`❌ Coordenadas inválidas para ${team.team}`);
            return;
        }
        
        // Crear ícono personalizado según cantidad de jugadores
        const markerColor = getMarkerColor(team.players_count);
        console.log(`   🎨 Color del marcador: ${markerColor}`);
        
        const customIcon = L.AwesomeMarkers.icon({
            icon: 'basketball-ball',
            prefix: 'fa',
            markerColor: markerColor,
            iconColor: 'white'
        });

        // Crear marcador
        const marker = L.marker(
            [team.latitude, team.longitude],
            { icon: customIcon }
        );

        // Agregar popup con información del equipo
        const popupContent = createPopupContent(team);
        marker.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'nba-team-popup'
        });

        // Agregar marcador a la capa
        marker.addTo(markersLayer);
        console.log(`   ✅ Marcador agregado para ${team.team}`);
    });

    console.log('✅ Todos los marcadores agregados exitosamente');
}

// ========================================
// FUNCIONES DE ESTADÍSTICAS
// ========================================

/**
 * Actualiza las estadísticas en la interfaz
 * Muestra total de equipos y total de jugadores
 * 
 * @param {Array} locations - Array de ubicaciones de equipos
 */
function updateMapStats(locations) {
    const totalTeams = locations.length;
    const totalPlayers = locations.reduce((sum, team) => sum + team.players_count, 0);

    // Actualizar elementos en el DOM - usar IDs correctos
    const teamsElement = document.getElementById('map-total-teams');
    const playersElement = document.getElementById('map-total-players');

    if (teamsElement) {
        teamsElement.textContent = totalTeams;
    }

    if (playersElement) {
        playersElement.textContent = totalPlayers;
    }

    console.log(`📊 Estadísticas: ${totalTeams} equipos, ${totalPlayers} jugadores`);
}

// ========================================
// FUNCIÓN PRINCIPAL DE INICIALIZACIÓN
// ========================================

/**
 * Inicializa el mapa completo
 * 1. Verifica autenticación
 * 2. Inicializa el mapa de Leaflet
 * 3. Carga ubicaciones desde la API
 * 4. Agrega marcadores
 * 5. Actualiza estadísticas
 * 
 * @async
 */
async function initNBAMap() {
    try {
        console.log('🚀 Iniciando NBA Map...');

        // Verificar autenticación
        const auth = checkAuth();
        if (!auth) {
            console.error('❌ Autenticación requerida');
            showError('Por favor, inicia sesión para ver el mapa');
            return;
        }

        // Mostrar loading
        const loadingElement = document.getElementById('map-loading');
        const errorElement = document.getElementById('map-error-message');
        
        if (loadingElement) {
            loadingElement.style.display = 'flex';
        }
        if (errorElement) {
            errorElement.style.display = 'none';
        }

        // Inicializar mapa solo si no existe
        if (!nbaMap) {
            console.log('🗺️ Creando nuevo mapa...');
            nbaMap = initializeMap('nba-map');
        } else {
            console.log('🗺️ Mapa ya existe, reutilizando...');
        }

        // Cargar ubicaciones
        console.log('📡 Cargando ubicaciones desde API...');
        teamsLocations = await loadTeamsLocations();
        console.log('📊 Ubicaciones cargadas:', teamsLocations.length);

        // Ocultar loading
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }

        // Verificar que tenemos datos
        if (!teamsLocations || teamsLocations.length === 0) {
            console.warn('⚠️ No se encontraron equipos');
            showError('No se encontraron equipos para mostrar en el mapa');
            return;
        }

        // Agregar marcadores al mapa
        console.log('📍 Agregando marcadores...');
        addMarkersToMap(teamsLocations);

        // Actualizar estadísticas
        console.log('📊 Actualizando estadísticas...');
        updateMapStats(teamsLocations);

        console.log('✅ NBA Map inicializado completamente');

    } catch (error) {
        console.error('❌ Error al inicializar mapa:', error);
        console.error('Stack trace:', error.stack);
        
        // Ocultar loading
        const loadingElement = document.getElementById('map-loading');
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        
        // Mostrar error en la interfaz
        showError(`Error al cargar el mapa: ${error.message}`);
    }
}

/**
 * Muestra un mensaje de error en la interfaz
 * 
 * @param {string} message - Mensaje de error a mostrar
 */
function showError(message) {
    const errorElement = document.getElementById('map-error-message');
    if (errorElement) {
        errorElement.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            ${message}
        `;
        errorElement.style.display = 'block';
    }
}

// ========================================
// EXPORTS (si se usa como módulo ES6)
// ========================================

// Si estás usando módulos ES6, descomenta esto:
// export { initNBAMap, loadTeamsLocations, checkAuth };
