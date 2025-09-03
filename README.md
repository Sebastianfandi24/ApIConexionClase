# API NBA Players

## Descripción General

Este proyecto es una API RESTful desarrollada con FastAPI y SQLAlchemy para gestionar jugadores de la NBA. Permite crear, consultar, actualizar y eliminar jugadores en una base de datos PostgreSQL. El sistema está estructurado en capas (controladores, servicios, repositorios, modelos y esquemas) siguiendo buenas prácticas de arquitectura.

## Estructura del Proyecto

```
app/
├── controllers/      # Endpoints y lógica de rutas
├── models/           # Modelos ORM (SQLAlchemy)
├── repositories/     # Acceso a datos
├── services/         # Lógica de negocio
├── Schema/           # Esquemas Pydantic (validación)
├── config/           # Configuración de la base de datos
├── main.py           # Punto de entrada de la app FastAPI
```

## Funcionalidades
- Crear jugadores con todos los datos relevantes.
- Consultar jugadores por id y listar todos.
- Actualizar jugadores (requiere todos los campos).
- Eliminar jugadores por id.
- Validaciones de negocio (fechas, campos obligatorios, etc).

## Instalación y ejecución

### Requisitos
- Python 3.13+
- PostgreSQL
- pip
- macOS o Windows

### 1. Clonar el repositorio
```sh
git clone <url-del-repo>
cd ApIConexionClase
```

### 2. Crear y activar entorno virtual
#### macOS
```sh
python3 -m venv .venv
source .venv/bin/activate
```
#### Windows
```sh
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias
```sh
pip install -r requirements.txt
```


### 4. Configurar la conexión a la base de datos
La conexión a la base de datos se realiza usando las credenciales almacenadas en el archivo `.env` en la raíz del proyecto. Este archivo debe contener las variables necesarias para conectarse a PostgreSQL, por ejemplo:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tu_basededatos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

El archivo `app/config/NBA_database.py` lee estas variables para establecer la conexión. Así se evita exponer credenciales en el código fuente y se facilita el cambio de entorno.

#### ¿Cómo se maneja la conexión para evitar caídas?
- El sistema utiliza SQLAlchemy, que gestiona automáticamente el pool de conexiones y la reconexión en caso de pérdida temporal.
- Si la conexión se pierde, SQLAlchemy intentará reestablecerla en la siguiente operación.
- Es importante mantener el archivo `.env` con los datos correctos y la base de datos activa para evitar errores de conexión.

**Nota:** Nunca subas el archivo `.env` a repositorios públicos.

### 5. Crear la base de datos y tablas
Asegúrate de que la base de datos existe. Las tablas se crean automáticamente al iniciar la app si no existen.

### 6. Ejecutar la API
```sh
fastapi dev app/main.py
```
O también:
```sh
uvicorn app.main:app --reload
```

## Ejemplos de uso con curl

### Crear un jugador
```sh
curl -X 'POST' \
   'http://127.0.0.1:8000/players/players/' \
   -H 'accept: application/json' \
   -H 'Content-Type: application/json' \
   -d '{
      "name": "LeBron James",
      "team": "Los Angeles Lakers",
      "position": "SF",
      "height_m": 2.06,
      "weight_kg": 113,
      "birth_date": "1984-12-30T00:00:00.000Z"
   }'
```

### Consultar todos los jugadores
```sh
curl -X 'GET' 'http://127.0.0.1:8000/players/players/' -H 'accept: application/json'
```

### Consultar jugador por id
```sh
curl -X 'GET' 'http://127.0.0.1:8000/players/players/1' -H 'accept: application/json'
```

### Actualizar jugador
```sh
curl -X 'PUT' \
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
