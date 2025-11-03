# 🏀 NBA Manager - Frontend

Interfaz web moderna y responsive para la gestión de jugadores NBA con sistema de roles.

## 🎨 Características

### ✨ Diseño Moderno
- 🎯 **Interfaz limpia y profesional** con gradientes y animaciones
- 📱 **Totalmente responsive** (móvil, tablet, desktop)
- 🌈 **Esquema de colores NBA** (rojo, azul, gris)
- ⚡ **Animaciones suaves** y transiciones fluidas

### 🔐 Sistema de Autenticación
- **Login seguro** con JWT
- **Redirección automática** según rol (admin/user)
- **Sesión persistente** con localStorage
- **Credenciales de prueba** visibles en login

### 👥 Dos Interfaces Diferentes

#### 🟢 Vista de Usuario (user.html)
- ✅ Ver lista de jugadores
- ✅ Buscar jugadores
- ✅ Ver detalles completos
- ❌ Sin permisos de edición
- 📊 Estadísticas de solo lectura

#### 🔴 Vista de Administrador (admin.html)
- ✅ Ver todos los jugadores
- ✅ Crear nuevos jugadores
- ✅ Editar jugadores existentes
- ✅ Eliminar jugadores
- ✅ Gestión completa del sistema
- 📊 Dashboard con estadísticas

## 📁 Estructura de Archivos

```
Front/
├── login.html              # Página de inicio de sesión
├── src/
│   └── pages/
│       ├── user.html       # Dashboard para usuarios
│       └── admin.html      # Dashboard para administradores
├── assets/
│   ├── css/
│   │   ├── login.css       # Estilos del login
│   │   └── dashboard.css   # Estilos compartidos admin/user
│   └── js/
│       └── admin.js        # Lógica del panel admin
```

## 🚀 Uso

### 1. Iniciar Backend
```bash
cd /Users/pechi/Desktop/U/ApIConexionClase
source .venv/bin/activate
python3 -m fastapi dev app/main.py
```

### 2. Abrir Frontend
Abre en tu navegador:
```
file:///Users/pechi/Desktop/U/ApIConexionClase/Front/login.html
```

O usa un servidor HTTP:
```bash
cd Front
python3 -m http.server 8080
```
Luego ve a: `http://localhost:8080/login.html`

### 3. Iniciar Sesión

**Administrador:**
- Usuario: `admin123`
- Contraseña: `admin123`
- Acceso: Panel completo con CRUD

**Usuario Regular:**
- Usuario: `user123`
- Contraseña: `user123`
- Acceso: Solo lectura

## 🎯 Flujo de Navegación

```
┌─────────────┐
│ login.html  │  ← Página de inicio
└──────┬──────┘
       │
       ├─ role_id = 1 (admin)
       │  └─→ admin.html (Panel de Admin)
       │      ├─ Ver jugadores
       │      ├─ Crear jugador
       │      ├─ Editar jugador
       │      └─ Eliminar jugador
       │
       └─ role_id = 2 (user)
          └─→ user.html (Vista de Usuario)
              ├─ Ver jugadores
              └─ Ver detalles
```

## 🎨 Componentes UI

### Login
- ✅ Formulario centrado con animación
- ✅ Validación en tiempo real
- ✅ Mensajes de error claros
- ✅ Loading spinner
- ✅ Credenciales de prueba visibles
- ✅ Fondo animado con basketballs

### Dashboard
- ✅ Sidebar con navegación
- ✅ Header con búsqueda
- ✅ Tarjetas de estadísticas
- ✅ Grid de jugadores responsive
- ✅ Modales para crear/editar
- ✅ Perfil de usuario

### Tarjetas de Jugador
- ✅ Avatar con icono
- ✅ Número de jugador
- ✅ Posición destacada
- ✅ Nombre y equipo
- ✅ Altura y peso
- ✅ Botones de acción según rol

## 🔧 Funcionalidades

### Vista Usuario
```javascript
✅ Listar jugadores (paginado)
✅ Buscar por nombre/equipo/posición
✅ Ver detalles en modal
✅ Estadísticas totales
✅ Ver mi perfil
✅ Cerrar sesión
```

### Vista Admin
```javascript
✅ Todo lo de usuario +
✅ Crear jugador (modal con formulario)
✅ Editar jugador (modal precargado)
✅ Eliminar jugador (con confirmación)
✅ Validaciones de formulario
✅ Gestión completa CRUD
```

## 🎨 Paleta de Colores

```css
--primary: #e74c3c        /* Rojo NBA */
--primary-dark: #c0392b   /* Rojo oscuro */
--secondary: #3498db      /* Azul */
--success: #2ecc71        /* Verde */
--warning: #f39c12        /* Naranja */
--danger: #e74c3c         /* Rojo */
--dark: #2c3e50          /* Gris oscuro */
--gray: #95a5a6          /* Gris */
--light: #ecf0f1         /* Gris claro */
--white: #ffffff         /* Blanco */
```

## 📱 Responsive Design

### Desktop (>1024px)
- Sidebar de 280px
- Grid de 3-4 columnas
- Todas las funcionalidades

### Tablet (768px - 1024px)
- Sidebar de 240px
- Grid de 2-3 columnas
- Funcionalidades completas

### Mobile (<768px)
- Sidebar oculta (hamburger menu)
- Grid de 1 columna
- Optimizado para touch

## 🔐 Seguridad

1. **Token JWT**: Almacenado en localStorage
2. **Verificación en cada página**: checkAuth()
3. **Redirección automática**: Si no hay token → login
4. **Protección por rol**: Admin solo admin.html, User solo user.html
5. **Headers de autorización**: En todas las peticiones

## 🎭 Diferencias Admin vs User

| Característica | Admin | User |
|----------------|-------|------|
| **Sidebar** | Rojo degradado | Azul oscuro |
| **Botón "Nuevo"** | ✅ Visible | ❌ Oculto |
| **Editar jugador** | ✅ Permitido | ❌ Bloqueado |
| **Eliminar jugador** | ✅ Permitido | ❌ Bloqueado |
| **Ver jugadores** | ✅ Permitido | ✅ Permitido |
| **Ver detalles** | ✅ Permitido | ✅ Permitido |
| **Estadísticas** | "Acceso Total" | "Solo Lectura" |
| **Avatar perfil** | 🛡️ Shield | 👤 User |
| **Color tema** | Rojo (#e74c3c) | Azul (#3498db) |

## 🚀 Mejoras Futuras

- [ ] Menu hamburger para móvil
- [ ] Filtros avanzados
- [ ] Ordenamiento de columnas
- [ ] Exportar a PDF/Excel
- [ ] Gestión de usuarios (admin)
- [ ] Gestión de roles (admin)
- [ ] Modo oscuro
- [ ] Notificaciones toast
- [ ] Paginación mejorada
- [ ] Gráficas y estadísticas
- [ ] Subida de fotos de jugadores
- [ ] Historial de cambios

## 💡 Notas Técnicas

- **Sin framework**: Vanilla JavaScript puro
- **Sin compilación**: HTML/CSS/JS directo
- **API REST**: Fetch API nativa
- **Módulos ES6**: import/export
- **localStorage**: Persistencia de sesión
- **Font Awesome**: Iconos
- **CSS Grid/Flexbox**: Layout responsive

## 🎯 Próximos Pasos

1. Probar ambas interfaces
2. Verificar permisos funcionan
3. Ajustar estilos según preferencias
4. Agregar más funcionalidades
5. Mejorar UX/UI
