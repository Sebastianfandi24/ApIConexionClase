"""
Servicio para obtener información del clima usando OpenWeatherMap API
Similar al notebook de referencia con Folium y clima
"""
import httpx
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger('nba_api.services.weather')


class WeatherService:
    """
    Servicio para consultar información meteorológica de ciudades.
    Usa la API de OpenWeatherMap (gratuita).
    """
    
    # API Key de OpenWeatherMap
    API_KEY = "3d4ed16bf828ee79b0b0fa9176dd9a12"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self):
        """Inicializa el servicio de clima"""
        self.api_key = self.API_KEY
        self.base_url = self.BASE_URL
    
    async def get_weather(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Obtiene el clima actual para unas coordenadas específicas.
        
        Args:
            latitude: Latitud de la ubicación
            longitude: Longitud de la ubicación
            
        Returns:
            Dict con información del clima o None si falla
            
        Example:
            {
                "temperature": 25.5,
                "feels_like": 26.0,
                "temp_min": 24.0,
                "temp_max": 27.0,
                "humidity": 60,
                "pressure": 1013,
                "description": "cielo claro",
                "icon": "01d",
                "wind_speed": 5.2,
                "clouds": 0
            }
        """
        try:
            # Parámetros para la API
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
                "units": "metric",  # Para obtener temperatura en Celsius
                "lang": "es"  # Descripciones en español
            }
            
            # Hacer petición asíncrona
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.base_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extraer información relevante
                    weather_info = {
                        "temperature": round(data["main"]["temp"], 1),
                        "feels_like": round(data["main"]["feels_like"], 1),
                        "temp_min": round(data["main"]["temp_min"], 1),
                        "temp_max": round(data["main"]["temp_max"], 1),
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"],
                        "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s a km/h
                        "clouds": data["clouds"]["all"],
                        "visibility": data.get("visibility", 0) / 1000,  # metros a km
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    logger.info(f"🌤️ Clima obtenido: {weather_info['temperature']}°C - {weather_info['description']}")
                    return weather_info
                    
                elif response.status_code == 401:
                    logger.error("❌ API Key inválida para OpenWeatherMap")
                    return None
                    
                else:
                    logger.error(f"❌ Error en API de clima: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("⏱️ Timeout al consultar API de clima")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error al obtener clima: {str(e)}")
            return None
    
    async def get_weather_by_city(self, city: str, country_code: str = "US") -> Optional[Dict]:
        """
        Obtiene el clima para una ciudad específica.
        
        Args:
            city: Nombre de la ciudad
            country_code: Código ISO del país (default: US)
            
        Returns:
            Dict con información del clima o None si falla
        """
        try:
            params = {
                "q": f"{city},{country_code}",
                "appid": self.api_key,
                "units": "metric",
                "lang": "es"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.base_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    weather_info = {
                        "temperature": round(data["main"]["temp"], 1),
                        "feels_like": round(data["main"]["feels_like"], 1),
                        "temp_min": round(data["main"]["temp_min"], 1),
                        "temp_max": round(data["main"]["temp_max"], 1),
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"],
                        "wind_speed": round(data["wind"]["speed"] * 3.6, 1),
                        "clouds": data["clouds"]["all"],
                        "visibility": data.get("visibility", 0) / 1000,
                        "city_name": data["name"],
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    logger.info(f"🌤️ Clima en {city}: {weather_info['temperature']}°C")
                    return weather_info
                    
                else:
                    logger.error(f"❌ Ciudad no encontrada: {city}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Error al obtener clima de {city}: {str(e)}")
            return None
    
    def get_weather_icon_url(self, icon_code: str) -> str:
        """
        Obtiene la URL del ícono del clima.
        
        Args:
            icon_code: Código del ícono (ej: "01d", "10n")
            
        Returns:
            URL completa del ícono
        """
        return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
