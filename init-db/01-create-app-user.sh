#!/bin/bash
# ================================
# Script de inicialización de PostgreSQL
# Crea un usuario de aplicación no-root con permisos limitados
# ================================

set -e

echo "🔧 Iniciando configuración de base de datos..."

# Variables de entorno (proporcionadas por docker-compose)
APP_USER="${APP_USER:-appuser}"
APP_PASSWORD="${APP_PASSWORD:-apppassword}"
APP_DB="${APP_DB:-railway}"

echo "📊 Base de datos: $APP_DB"
echo "👤 Usuario de aplicación: $APP_USER"

# Crear usuario de aplicación si no existe
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Crear usuario si no existe
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$APP_USER') THEN
            CREATE ROLE $APP_USER WITH LOGIN PASSWORD '$APP_PASSWORD';
            RAISE NOTICE 'Usuario % creado exitosamente', '$APP_USER';
        ELSE
            RAISE NOTICE 'Usuario % ya existe', '$APP_USER';
        END IF;
    END
    \$\$;

    -- Otorgar permisos al usuario en la base de datos
    GRANT CONNECT ON DATABASE $APP_DB TO $APP_USER;
    GRANT USAGE ON SCHEMA public TO $APP_USER;
    GRANT CREATE ON SCHEMA public TO $APP_USER;
    
    -- Permisos para tablas existentes y futuras
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO $APP_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO $APP_USER;
    
    -- Permisos para secuencias (para IDs auto-incrementales)
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO $APP_USER;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO $APP_USER;

    -- Confirmación
    \echo '✅ Usuario de aplicación configurado correctamente'
EOSQL

echo "✅ Configuración completada exitosamente"
echo "📝 Usuario '$APP_USER' tiene acceso a la base de datos '$APP_DB'"
