# 🐳 Resumen de Archivos Docker Creados

## 📁 Archivos Creados

| Archivo | Descripción |
|---------|-------------|
| `Dockerfile` | Imagen multi-stage optimizada para producción |
| `.dockerignore` | Excluye archivos innecesarios del build |
| `docker-compose.yml` | Orquestación para desarrollo local (API + PostgreSQL) |
| `docker-compose.prod.yml` | Configuración para producción |
| `railway.json` | Configuración para Railway |
| `DOCKER_GUIDE.md` | Guía completa de Docker (debugging, comandos, etc.) |
| `RAILWAY_QUICK_START.md` | Guía rápida para desplegar en Railway |
| `test-docker.sh` | Script para probar la imagen Docker localmente |
| `cleanup-docker.sh` | Script para limpiar contenedores e imágenes |

---

## 🚀 Inicio Rápido

### Opción 1: Desarrollo Local con Docker Compose

```bash
# 1. Asegúrate de tener Docker Desktop corriendo

# 2. Iniciar todos los servicios (API + PostgreSQL)
docker compose up --build

# 3. Acceder a la API
open http://localhost:8000/docs
```

### Opción 2: Probar Solo la Imagen Docker

```bash
# 1. Iniciar Docker Desktop

# 2. Ejecutar script de testing
./test-docker.sh

# 3. Acceder a la API
open http://localhost:8001/docs
```

### Opción 3: Desplegar en Railway

```bash
# 1. Lee RAILWAY_QUICK_START.md

# 2. Sube el código a GitHub
git add .
git commit -m "Add Docker configuration"
git push origin main

# 3. Conecta Railway a tu repositorio GitHub

# 4. Railway desplegará automáticamente
```

---

## 📋 Comandos Esenciales

### Docker Compose (Desarrollo Local)

```bash
# Iniciar servicios
docker compose up -d

# Ver logs
docker compose logs -f api

# Detener servicios
docker compose down

# Reconstruir imagen
docker compose up --build
```

### Docker Manual

```bash
# Construir imagen
docker build -t nba-api:latest .

# Ejecutar contenedor
docker run -d -p 8000:8000 --env-file .env nba-api:latest

# Ver logs
docker logs -f <container_id>

# Detener contenedor
docker stop <container_id>
```

### Scripts Útiles

```bash
# Probar imagen completa
./test-docker.sh

# Limpiar todo
./cleanup-docker.sh
```

---

## 🌐 URLs Importantes

### Desarrollo Local
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health
- **PgAdmin**: http://localhost:5050 (si usas `--profile tools`)

### Producción (Railway)
- **API**: https://tu-app.up.railway.app
- **Docs**: https://tu-app.up.railway.app/docs
- **Health**: https://tu-app.up.railway.app/health

---

## 📚 Documentación Completa

- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)**: Guía completa con debugging y troubleshooting
- **[RAILWAY_QUICK_START.md](RAILWAY_QUICK_START.md)**: Guía rápida para Railway

---

## ✅ Checklist Pre-Despliegue

- [ ] Docker Desktop instalado y corriendo
- [ ] Archivo `.env` configurado con variables correctas
- [ ] `./test-docker.sh` ejecutado sin errores
- [ ] PostgreSQL agregado en Railway
- [ ] Variables de entorno configuradas en Railway
- [ ] Código subido a GitHub

---

## 🔧 Características del Dockerfile

✅ **Multi-stage build** para imagen optimizada (~200MB)  
✅ **Usuario no-root** para seguridad  
✅ **Health check** integrado  
✅ **Compatible con Railway** (variable PORT dinámica)  
✅ **Cacheo de dependencias** para builds rápidos  
✅ **Optimizado para Python 3.13**  

---

## 🐛 Problemas Comunes

### "Docker daemon not running"
```bash
# Inicia Docker Desktop
open -a Docker
```

### "Port 8000 already in use"
```bash
# Cambia el puerto en docker-compose.yml o usa otro puerto
docker run -p 8001:8000 nba-api:latest
```

### Ver logs para debugging
```bash
docker compose logs -f api
# o
docker logs -f <container_id>
```

---

## 💡 Notas Importantes

1. **Variables de Entorno**: El archivo `.env` NO debe subirse a GitHub
2. **Railway**: Inyecta automáticamente la variable `PORT`, no la configures
3. **PostgreSQL**: En local usa docker-compose, en Railway usa su servicio
4. **Secrets**: Usa variables de entorno de Railway para producción

---

**¿Necesitas ayuda?** Lee [DOCKER_GUIDE.md](DOCKER_GUIDE.md) para documentación completa.

🚀 **¡Happy Deploying!**
