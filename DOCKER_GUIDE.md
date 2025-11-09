# 🐳 Guía de Docker - NBA Players API

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Estructura de Archivos Docker](#estructura-de-archivos-docker)
- [Desarrollo Local](#desarrollo-local)
- [Construcción de Imagen](#construcción-de-imagen)
- [Despliegue en Railway](#despliegue-en-railway)
- [Comandos Útiles](#comandos-útiles)
- [Debugging](#debugging)
- [Troubleshooting](#troubleshooting)

---

## 📦 Requisitos Previos

### Software Necesario
- ✅ **Docker Desktop** >= 20.10
- ✅ **Docker Compose** >= 2.0
- ✅ **Git** (para clonar el repositorio)
- ✅ **Cuenta en Railway** (para despliegue en producción)

### Verificar Instalación
```bash
# Verificar versión de Docker
docker --version
# Salida esperada: Docker version 24.x.x o superior

# Verificar Docker Compose
docker compose version
# Salida esperada: Docker Compose version v2.x.x o superior

# Verificar que Docker está corriendo
docker ps
# Debe mostrar una tabla (aunque esté vacía)
```

---

## 🗂️ Estructura de Archivos Docker

```
ApIConexionClase/
├── Dockerfile              # Imagen multi-stage optimizada para producción
├── .dockerignore          # Archivos excluidos del contexto de Docker
├── docker-compose.yml     # Orquestación para desarrollo local
├── docker-compose.prod.yml # Configuración para producción
├── .env                   # Variables de entorno (NO versionar)
└── DOCKER_GUIDE.md        # Esta guía
```

### Descripción de Archivos

| Archivo | Propósito |
|---------|-----------|
| `Dockerfile` | Define la imagen de la aplicación (multi-stage para optimización) |
| `.dockerignore` | Excluye archivos innecesarios del contexto de construcción |
| `docker-compose.yml` | Configuración para desarrollo local (incluye PostgreSQL) |
| `docker-compose.prod.yml` | Configuración simplificada para producción |

---

## 🛠️ Desarrollo Local

### 1. Configurar Variables de Entorno

Asegúrate de tener tu archivo `.env` configurado:

```bash
# .env
user=postgres
password=tu_password_seguro
host=db  # 'db' es el nombre del servicio en docker-compose
db_port=5432
dbname=postgres
JWT_SECRET_KEY=tu_clave_secreta_jwt
```

### 2. Iniciar Todos los Servicios

```bash
# Construir e iniciar todos los servicios (API + PostgreSQL)
docker compose up --build

# En modo background (detached)
docker compose up -d --build

# Solo construir sin iniciar
docker compose build
```

### 3. Verificar que Todo Funciona

```bash
# Ver logs en tiempo real
docker compose logs -f api

# Verificar estado de los contenedores
docker compose ps

# Probar la API
curl http://localhost:8000/health
# Respuesta esperada: {"status":"healthy",...}

# Probar endpoint de documentación
open http://localhost:8000/docs  # macOS
# o visitar: http://localhost:8000/docs en el navegador
```

### 4. Acceder a la Base de Datos (Opcional)

Si necesitas administrar la base de datos localmente:

```bash
# Iniciar con PgAdmin
docker compose --profile tools up -d

# Acceder a PgAdmin
# URL: http://localhost:5050
# Email: admin@admin.com
# Password: admin
```

### 5. Detener los Servicios

```bash
# Detener contenedores (mantiene datos)
docker compose stop

# Detener y eliminar contenedores
docker compose down

# Eliminar todo (incluyendo volúmenes de BD)
docker compose down -v
```

---

## 🏗️ Construcción de Imagen

### Construcción Manual

```bash
# Construir imagen con tag específico
docker build -t nba-api:latest .

# Construir para una plataforma específica (útil para M1/M2 Mac)
docker build --platform linux/amd64 -t nba-api:latest .

# Ver imágenes creadas
docker images | grep nba-api
```

### Probar la Imagen Localmente

```bash
# Ejecutar contenedor desde la imagen
docker run -d \
  --name nba-api-test \
  -p 8000:8000 \
  -e PORT=8000 \
  -e user=postgres \
  -e password=tu_password \
  -e host=tu_host_db \
  -e db_port=5432 \
  -e dbname=postgres \
  -e JWT_SECRET_KEY=tu_clave_jwt \
  nba-api:latest

# Ver logs
docker logs -f nba-api-test

# Probar la API
curl http://localhost:8000/health

# Detener y eliminar
docker stop nba-api-test
docker rm nba-api-test
```

---

## 🚀 Despliegue en Railway

### Método 1: Despliegue Automático (Recomendado)

#### Paso 1: Conectar Repositorio a Railway

1. **Ir a [Railway.app](https://railway.app)** y hacer login
2. Click en **"New Project"**
3. Seleccionar **"Deploy from GitHub repo"**
4. Autorizar Railway para acceder a tu repositorio
5. Seleccionar el repositorio `ApIConexionClase`

#### Paso 2: Configurar Servicio

Railway detectará automáticamente el `Dockerfile` y configurará el servicio.

#### Paso 3: Agregar Base de Datos PostgreSQL

1. En tu proyecto de Railway, click en **"New"**
2. Seleccionar **"Database"** → **"Add PostgreSQL"**
3. Railway creará automáticamente una base de datos PostgreSQL

#### Paso 4: Configurar Variables de Entorno

En la sección de **Variables** del servicio de la API, agregar:

```bash
# Railway inyecta automáticamente PORT
# Solo necesitas configurar estas:

user=${{Postgres.PGUSER}}
password=${{Postgres.PGPASSWORD}}
host=${{Postgres.PGHOST}}
db_port=${{Postgres.PGPORT}}
dbname=${{Postgres.PGDATABASE}}
JWT_SECRET_KEY=tu_clave_secreta_jwt_produccion
```

💡 **Tip**: Railway permite referenciar variables de otros servicios usando `${{ServiceName.VARIABLE}}`

#### Paso 5: Desplegar

```bash
# Railway desplegará automáticamente al hacer push al repositorio
git add .
git commit -m "Deploy to Railway"
git push origin main

# Railway construirá la imagen y desplegará
```

### Método 2: Despliegue Manual con Railway CLI

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Link a proyecto existente (opcional)
railway link

# Desplegar
railway up

# Ver logs
railway logs

# Abrir en browser
railway open
```

### Verificar Despliegue en Railway

```bash
# Railway asignará una URL pública, ejemplo:
# https://tu-app.up.railway.app

# Probar health check
curl https://tu-app.up.railway.app/health

# Probar documentación
open https://tu-app.up.railway.app/docs
```

---

## 🔧 Comandos Útiles

### Docker

```bash
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores (incluyendo detenidos)
docker ps -a

# Ver logs de un contenedor específico
docker logs <container_id_o_nombre>

# Logs en tiempo real
docker logs -f <container_id_o_nombre>

# Ejecutar comando dentro del contenedor
docker exec -it nba-api bash

# Ver uso de recursos
docker stats

# Limpiar imágenes no usadas
docker image prune

# Limpiar todo (CUIDADO: elimina todo lo no usado)
docker system prune -a --volumes
```

### Docker Compose

```bash
# Ver logs de todos los servicios
docker compose logs

# Logs de un servicio específico
docker compose logs api

# Reiniciar un servicio
docker compose restart api

# Reconstruir un servicio específico
docker compose up -d --build api

# Ver variables de entorno de un servicio
docker compose config

# Ejecutar comando en servicio
docker compose exec api python -m pytest
```

### Inspección y Debugging

```bash
# Inspeccionar imagen
docker inspect nba-api:latest

# Ver historial de capas
docker history nba-api:latest

# Tamaño de la imagen
docker images nba-api:latest --format "{{.Size}}"

# Entrar al contenedor para debugging
docker compose exec api /bin/bash

# Ver redes
docker network ls

# Inspeccionar red
docker network inspect nba_network
```

---

## 🐛 Debugging

### Problemas Comunes y Soluciones

#### 1. Error: "Cannot connect to PostgreSQL"

**Síntoma**: La API no puede conectarse a la base de datos

**Solución**:
```bash
# Verificar que PostgreSQL está corriendo
docker compose ps db

# Ver logs de PostgreSQL
docker compose logs db

# Verificar variables de entorno
docker compose exec api env | grep -E 'user|password|host|dbname'

# Reiniciar servicios en orden
docker compose down
docker compose up -d db
# Esperar 10 segundos
docker compose up -d api
```

#### 2. Error: "Port already in use"

**Síntoma**: `Error starting userland proxy: listen tcp4 0.0.0.0:8000: bind: address already in use`

**Solución**:
```bash
# Encontrar qué está usando el puerto
lsof -i :8000

# Matar el proceso (reemplazar PID con el número real)
kill -9 <PID>

# O cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"  # Mapear puerto local 8001 al 8000 del contenedor
```

#### 3. Error: "Build failed - No space left on device"

**Síntoma**: Docker se queda sin espacio

**Solución**:
```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes no usadas
docker image prune -a

# Limpiar volúmenes no usados
docker volume prune

# Limpiar todo
docker system prune -a --volumes
```

#### 4. Cambios en código no se reflejan

**Síntoma**: Modificas el código pero el contenedor sigue usando el código viejo

**Solución**:
```bash
# Reconstruir la imagen
docker compose up -d --build

# O forzar recreación completa
docker compose down
docker compose up --build
```

#### 5. Logs para Debugging Profundo

```bash
# Ver todos los logs con timestamps
docker compose logs -f --timestamps

# Ver solo errores
docker compose logs api 2>&1 | grep -i error

# Exportar logs a archivo
docker compose logs > debug.log

# Ver logs de la última hora
docker compose logs --since 1h
```

### Debugging Interactivo

```bash
# Acceder al contenedor
docker compose exec api bash

# Verificar Python y paquetes
python --version
pip list

# Probar importaciones manualmente
python -c "from app.main import app; print('OK')"

# Ver estructura de archivos
ls -la /app

# Ver variables de entorno
env

# Probar conectividad a base de datos
python -c "
from app.config.NBA_database import engine
with engine.connect() as conn:
    print('✅ DB Connected')
"
```

---

## 🔍 Troubleshooting

### Health Check Failures

Si el health check falla:

```bash
# Verificar el endpoint de health manualmente
docker compose exec api curl http://localhost:8000/health

# Si curl no está instalado en el contenedor
docker compose exec api python -c "
import requests
resp = requests.get('http://localhost:8000/health')
print(resp.json())
"
```

### Performance Issues

```bash
# Monitorear uso de recursos
docker stats nba-api

# Ver procesos dentro del contenedor
docker compose exec api ps aux

# Ajustar workers de uvicorn en Dockerfile
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4
```

### Networking Issues

```bash
# Ver red del proyecto
docker network inspect nba_network

# Probar conectividad entre contenedores
docker compose exec api ping db

# Verificar DNS interno
docker compose exec api nslookup db
```

---

## 📊 Mejores Prácticas

### Seguridad

- ✅ Nunca incluir `.env` en el repositorio
- ✅ Usar usuario no-root en el contenedor
- ✅ Mantener dependencias actualizadas
- ✅ Usar secrets de Railway para producción
- ✅ Implementar rate limiting en producción

### Performance

- ✅ Usar multi-stage builds (ya implementado)
- ✅ Minimizar capas en Dockerfile
- ✅ Usar `.dockerignore` para reducir contexto
- ✅ Ajustar workers según CPUs disponibles
- ✅ Implementar caching de dependencias

### Monitoreo

```bash
# En Railway, ver métricas
railway logs --tail 100

# Configurar alertas en Railway
# Settings → Monitoring → Alerts
```

---

## 📚 Recursos Adicionales

- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de Railway](https://docs.railway.app/)
- [FastAPI en Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

---

## 🎯 Checklist de Despliegue

Antes de desplegar a producción:

- [ ] Variables de entorno configuradas en Railway
- [ ] Base de datos PostgreSQL creada en Railway
- [ ] JWT_SECRET_KEY es diferente al de desarrollo
- [ ] Health check responde correctamente
- [ ] Documentación accesible en `/docs`
- [ ] Logs no muestran errores
- [ ] Probar endpoints principales
- [ ] Configurar dominio personalizado (opcional)
- [ ] Implementar monitoreo y alertas

---

## 💡 Tips Finales

1. **Desarrollo Local**: Usa `docker-compose.yml` con PostgreSQL local
2. **Producción**: Railway maneja la base de datos, solo despliegas la API
3. **Secrets**: Usa variables de entorno de Railway, nunca hardcodees
4. **Logs**: Railway guarda logs automáticamente por 7 días
5. **Escalado**: Railway permite escalar horizontalmente fácilmente

---

**¿Preguntas o problemas?** Revisa la sección de [Troubleshooting](#troubleshooting) o crea un issue en GitHub.

🚀 **¡Happy Deploying!**
