# 🏀 NBA Players API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-00C7B7?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?style=flat&logo=postgresql)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 📋 Descripción General

**NBA Players API** es una API RESTful moderna y robusta desarrollada con **FastAPI** y **SQLAlchemy** para gestionar información completa de jugadores de la NBA. El sistema implementa operaciones CRUD completas con validaciones avanzadas, documentación interactiva automática y una arquitectura escalable en capas.

### ✨ Características principales

- 🚀 **API ultra-rápida** con FastAPI y validaciones automáticas
- 🗄️ **Base de datos PostgreSQL** con ORM SQLAlchemy
- 📊 **Paginación inteligente** para grandes conjuntos de datos
- 🔍 **Documentación interactiva** con Swagger UI, ReDoc y Scalar
- ✅ **Validaciones robustas** de datos de entrada
- 🏗️ **Arquitectura en capas** bien estructurada
- 🌐 **CORS configurado** para integración con frontend
- 🔧 **Health checks** para monitoreo del sistema

## 🏗️ Arquitectura del Proyecto

```
app/
├── 📂 controllers/      # 🎯 Endpoints y lógica de rutas (FastAPI)
│   ├── NBA_controller.py
│   └── CONTROLLER.md
├── 📂 models/          # 🗃️ Modelos ORM SQLAlchemy 
│   ├── NBA_model.py
│   └── MODELS.md
├── 📂 repositories/    # 💾 Capa de acceso a datos
│   ├── NBA_repository.py
│   └── REPOSITORY.md  
├── 📂 services/        # 🔧 Lógica de negocio
│   ├── NBA_service.py
│   └── SERVICES.md
├── 📂 Schema/          # 📋 Esquemas Pydantic (validación/serialización)
│   └── NBA_Schema.py
├── 📂 config/          # ⚙️ Configuración de base de datos
│   └── NBA_database.py
├── 📄 main.py          # 🚀 Punto de entrada de la aplicación
└── 📄 __init__.py
```

### 🧠 Patrón de Arquitectura

La aplicación sigue el **patrón de capas** para mantener separación de responsabilidades:

1. **Controllers (Presentación)**: Manejo de HTTP requests/responses
2. **Services (Lógica de Negocio)**: Reglas de negocio y validaciones
3. **Repositories (Acceso a Datos)**: Interacción con la base de datos
4. **Models (Entidades)**: Definición de estructura de datos
5. **Schemas (Validación)**: Validación y serialización con Pydantic

## 🚀 Instalación y Configuración
### 📋 Requisitos del Sistema

- 🐍 **Python 3.13+**
- 🐘 **PostgreSQL 12+**
- 📦 **pip** (gestor de paquetes)
- 💻 **macOS/Windows/Linux**

### 1️⃣ Clonar el repositorio

```bash
git clone <url-del-repo>
cd ApIConexionClase
```

### 2️⃣ Crear y activar entorno virtual

#### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configuración de Base de Datos

Crea un archivo `.env` en la raíz del proyecto con las credenciales de PostgreSQL:

```env
# Configuración de Base de Datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nba_players_db
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña

# Configuración de la aplicación
DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui
```

> ⚠️ **Importante**: Nunca subas el archivo `.env` a repositorios públicos

### 5️⃣ Crear base de datos

```sql
-- Conectar a PostgreSQL y crear la base de datos
CREATE DATABASE nba_players_db;
```

Las tablas se crean automáticamente al iniciar la aplicación.

### 6️⃣ Ejecutar la aplicación

```bash
# Modo desarrollo (recomendado)
fastapi dev app/main.py

# Modo alternativo
uvicorn app.main:app --reload
```

## 📊 Endpoints de la API

| Método | Endpoint | Descripción | Estado |
|--------|----------|-------------|---------|
| `GET` | `/` | Página de inicio con información de la API | ✅ |
| `GET` | `/health` | Estado de la aplicación y base de datos | ✅ |
| `GET` | `/api/v1/players/` | Lista todos los jugadores (paginado) | ✅ |
| `GET` | `/api/v1/players/{id}` | Obtiene un jugador específico | ✅ |
| `POST` | `/api/v1/players/` | Crea un nuevo jugador | ✅ |
| `PUT` | `/api/v1/players/{id}` | Actualiza un jugador existente | ✅ |
| `DELETE` | `/api/v1/players/{id}` | Elimina un jugador | ✅ |

## 📚 Documentación Interactiva

Una vez que la aplicación esté ejecutándose, puedes acceder a la documentación interactiva:

| Interfaz | URL | Descripción |
|----------|-----|-------------|
| 🔵 **Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interfaz clásica e interactiva |
| 📘 **ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Documentación elegante y responsive |
| ⚡ **Scalar** | [http://localhost:8000/scalar](http://localhost:8000/scalar) | Interfaz moderna y avanzada |

## 🔧 Ejemplos de Uso

### 🏀 Crear un nuevo jugador

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/players/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "LeBron James",
    "team": "Los Angeles Lakers", 
    "position": "Small Forward",
    "height_m": 2.06,
    "weight_kg": 113.4,
    "birth_date": "1984-12-30T00:00:00"
  }'
```

### 📋 Listar todos los jugadores

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/players/?skip=0&limit=10' \
  -H 'accept: application/json'
```

### 🔍 Obtener jugador por ID

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/players/1' \
  -H 'accept: application/json'
```

### ✏️ Actualizar jugador

```bash
curl -X 'PUT' \
  'http://localhost:8000/api/v1/players/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "team": "Miami Heat"
  }'
```

### 🗑️ Eliminar jugador

```bash
curl -X 'DELETE' \
  'http://localhost:8000/api/v1/players/1' \
  -H 'accept: application/json'
```

## 📝 Esquema de Datos

### Jugador (Player)

```json
{
  "id": 1,
  "name": "LeBron James",
  "team": "Los Angeles Lakers",
  "position": "Small Forward", 
  "height_m": 2.06,
  "weight_kg": 113.4,
  "birth_date": "1984-12-30T00:00:00",
  "created_at": "2025-09-04T00:00:00"
}
```

### Validaciones

- **name**: 2-100 caracteres
- **team**: 2-50 caracteres  
- **position**: 1-20 caracteres
- **height_m**: 1.0 - 3.0 metros
- **weight_kg**: 50 - 200 kilogramos
- **birth_date**: Formato ISO datetime

## 🧪 Testing

### Ejecutar tests

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest tests/ -v
```

### Health Check

Verifica que la aplicación esté funcionando:

```bash
curl http://localhost:8000/health
```

## 🚀 Deployment

### Con Docker

```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables de Entorno para Producción

```env
# Producción
DB_HOST=your-production-db-host
DB_PORT=5432
DB_NAME=nba_players_prod
DB_USER=prod_user
DB_PASSWORD=secure_password
DEBUG=False
```

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **FastAPI** | 0.104+ | Framework web principal |
| **SQLAlchemy** | 2.0+ | ORM para base de datos |
| **PostgreSQL** | 12+ | Base de datos relacional |
| **Pydantic** | 2.0+ | Validación de datos |
| **Uvicorn** | 0.24+ | Servidor ASGI |
| **Python** | 3.13+ | Lenguaje de programación |

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- **FastAPI** por proporcionar un framework excepcional
- **SQLAlchemy** por el excelente ORM
- **Pydantic** por las validaciones robustas
- **Comunidad Open Source** por las herramientas increíbles

---

<div align="center">

**🏀 NBA Players API v1.2.0**

[📖 Documentación](http://localhost:8000/docs) • [🔧 API Reference](http://localhost:8000/scalar) • [📊 Health Check](http://localhost:8000/health)

</div>
   'http://127.0.0.1:8000/players/players/1' \
   -H 'accept: application/json' \
   -H 'Content-Type: application/json' \
   -d '{
      "name": "sebas",
      "team": "Celtics",
      "position": "PG",
      "height_m": 1.85,
      "weight_kg": 80,
      "birth_date": "2000-01-01T00:00:00.000Z"
   }'
```

### Eliminar jugador
```sh
curl -X 'DELETE' 'http://127.0.0.1:8000/players/players/1' -H 'accept: application/json'
```

## Notas importantes
- En macOS, los comandos de activación de entorno virtual y ejecución pueden diferir de Windows.
- Si cambias el modelo, elimina la tabla en la base de datos para que se cree correctamente.
- La API valida que la fecha de nacimiento no sea mayor a la fecha actual.
- Todos los endpoints requieren los campos obligatorios definidos en los esquemas.

## Autor
Sebastian Fandiño
