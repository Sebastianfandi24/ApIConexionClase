# 🏀 NBA Players Frontend

Frontend web básico para la NBA Players API. Permite gestionar jugadores de la NBA a través de una interfaz moderna y responsive.

## 🚀 Características

- **Autenticación completa**: Login y registro de usuarios
- **Gestión de jugadores**: Crear, ver, editar y eliminar jugadores
- **Interfaz responsive**: Funciona en desktop y móvil
- **Validaciones en tiempo real**: Formularios con validación automática
- **Notificaciones**: Mensajes de éxito y error
- **Paginación**: Navegación por páginas de jugadores
- **Persistencia de sesión**: Mantiene la sesión activa

## 📁 Estructura de archivos (MODULAR)

```
Front/
├── index.html              # Estructura principal de la aplicación
├── serve.py                # Servidor simple para desarrollo
├── README.md               # Esta documentación
│
├── assets/                 # Recursos de la aplicación
│   ├── css/               # Estilos modulares
│   │   ├── variables.css  # Variables CSS y configuración base
│   │   ├── layout.css     # Header, footer, layout general
│   │   ├── buttons.css    # Estilos de botones
│   │   ├── forms.css      # Estilos de formularios
│   │   ├── auth.css       # Estilos de autenticación
│   │   ├── players.css    # Estilos de jugadores
│   │   ├── components.css # Modal, notificaciones
│   │   └── animations.css # Animaciones y transiciones
│   │
│   └── js/                # JavaScript modular
│       ├── app.js         # Aplicación principal e inicialización
│       ├── config.js      # Configuración y constantes
│       ├── utils.js       # Utilidades generales
│       ├── api.js         # Manejo de llamadas a la API
│       ├── ui.js          # Gestión de interfaz de usuario
│       ├── auth.js        # Manejo de autenticación
│       └── players.js     # Gestión de jugadores
│
├── components/             # Componentes reutilizables (futuro)
├── pages/                  # Páginas separadas (futuro)
│
└── [archivos_antiguos]     # Versiones anteriores como respaldo
    ├── index_old.html
    ├── script_old.js
    └── styles_old.css
```

## 🛠️ Instalación y uso

### 1. Iniciar el backend (API)

Primero asegúrate de que tu API esté ejecutándose:

```bash
# En el directorio raíz del proyecto
cd /Users/pechi/Desktop/U/ApIConexionClase
fastapi dev app/main.py
```

La API debe estar disponible en: `http://localhost:8000`

### 2. Iniciar el frontend

Opción A: **Usando el servidor Python incluido (Recomendado)**
```bash
# En el directorio Front
cd Front
python3 serve.py
```

Opción B: **Usando cualquier servidor web**
```bash
# Opción con Python (puerto 8080)
cd Front
python3 -m http.server 8080

# Opción con Node.js (si tienes npx)
cd Front
npx serve -s . -l 3000
```

### 3. Abrir en el navegador

Ve a: `http://localhost:3000` (o el puerto que hayas elegido)

## 🎯 Cómo usar la aplicación

### 1. **Registro/Login**
- Al abrir la aplicación, verás la pantalla de autenticación
- **Registrarse**: Crea una cuenta nueva con usuario y contraseña
- **Iniciar sesión**: Usa tus credenciales para acceder

### 2. **Ver jugadores**
- Una vez autenticado, verás la lista de jugadores
- Usa los botones de paginación para navegar
- Click en "Actualizar" para recargar la lista

### 3. **Agregar jugador**
- Click en "Agregar Jugador"
- Completa todos los campos requeridos:
  - Nombre completo
  - Equipo
  - Posición (selecciona del dropdown)
  - Altura en metros (1.0 - 3.0)
  - Peso en kg (50 - 200)
  - Fecha de nacimiento
- Click en "Guardar Jugador"

### 4. **Editar jugador**
- Click en el ícono de editar (lápiz) en cualquier tarjeta de jugador
- Modifica los campos necesarios
- Click en "Guardar Jugador"

### 5. **Eliminar jugador**
- Click en el ícono de eliminar (papelera) en cualquier tarjeta
- Confirma la eliminación en el modal

### 6. **Cerrar sesión**
- Click en "Cerrar Sesión" en la parte superior derecha

## 🔧 Configuración

### Cambiar URL de la API

Si tu API está en una URL diferente, edita el archivo `assets/js/config.js`:

```javascript
// En config.js
export const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api/v1', // Cambiar aquí
    PLAYERS_PER_PAGE: 10,
    // ...
};
```

### Personalizar estilos

Los estilos están organizados modularmente en `assets/css/variables.css`:

```css
:root {
    --primary-color: #1a73e8;    /* Color principal */
    --success-color: #34a853;    /* Color de éxito */
    --danger-color: #ea4335;     /* Color de peligro */
    /* ... más variables ... */
}
```

### Estructura modular

- **CSS**: Dividido por responsabilidades (layout, buttons, forms, etc.)
- **JavaScript**: Módulos ES6 con responsabilidades específicas
- **Configuración**: Centralizada en `config.js`
- **Utilidades**: Funciones reutilizables en `utils.js`

## 🌐 Endpoints utilizados

El frontend consume estos endpoints de la API:

- `POST /auth/login` - Iniciar sesión
- `POST /auth/register` - Registrarse
- `GET /players/` - Listar jugadores (con paginación)
- `POST /players/` - Crear jugador
- `PUT /players/{id}` - Actualizar jugador
- `DELETE /players/{id}` - Eliminar jugador

## 📱 Características responsive

- **Desktop**: Layout completo con grid de 2-3 columnas
- **Tablet**: Layout adaptado con grid de 2 columnas
- **Móvil**: Layout en una columna, navegación optimizada

## 🔒 Seguridad

- **Tokens JWT**: Autenticación mediante tokens seguros
- **Validación de formularios**: Validación en frontend y backend
- **Sanitización**: Escape de caracteres HTML para prevenir XSS
- **Sesión persistente**: Token guardado de forma segura en localStorage

## 🐛 Solución de problemas

### Error de conexión
- Verifica que la API esté ejecutándose en `http://localhost:8000`
- Comprueba que no haya firewalls bloqueando los puertos

### Error de CORS
- Ya está configurado en el backend, pero si tienes problemas:
- Verifica que el archivo `main.py` tenga CORS habilitado

### Sesión expirada
- Los tokens JWT tienen expiración
- Si ves "Sesión expirada", simplemente inicia sesión nuevamente

### Problemas de permisos
- Asegúrate de estar autenticado
- Todos los endpoints de jugadores requieren JWT

## 🚀 Próximas mejoras

Ideas para mejorar el frontend:

- [x] **Arquitectura modular** - CSS y JS organizados en módulos
- [x] **Validación en tiempo real** - Formularios con validación automática
- [x] **Manejo de errores mejorado** - Mensajes específicos y manejo de excepciones
- [ ] Búsqueda y filtros de jugadores
- [ ] Ordenamiento por diferentes campos
- [ ] Subida de imágenes de jugadores
- [ ] Dashboard con estadísticas
- [ ] Modo oscuro/claro
- [ ] Notificaciones push
- [ ] Cache offline
- [ ] Tests unitarios para módulos JavaScript
- [ ] Componentes web reutilizables

## 📞 Soporte

Si encuentras problemas:

1. Verifica que el backend esté ejecutándose
2. Revisa la consola del navegador (F12)
3. Comprueba los logs del servidor API

¡Disfruta gestionando tu base de datos de jugadores NBA! 🏀