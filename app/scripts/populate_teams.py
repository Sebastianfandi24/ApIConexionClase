"""
Script para poblar la tabla de equipos NBA
Inserta los 30 equipos de la NBA con sus ubicaciones
"""
from sqlalchemy.orm import Session
from app.config.NBA_database import SessionLocal, engine, Base
from app.models.Team_model import Team
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Datos de los 30 equipos NBA
NBA_TEAMS_DATA = [
    # Conferencia Este - División Atlántico
    {
        "name": "Boston Celtics",
        "city": "Boston",
        "state": "Massachusetts",
        "stadium": "TD Garden",
        "latitude": 42.3601,
        "longitude": -71.0589,
        "conference": "East",
        "division": "Atlantic"
    },
    {
        "name": "Brooklyn Nets",
        "city": "Brooklyn",
        "state": "New York",
        "stadium": "Barclays Center",
        "latitude": 40.6782,
        "longitude": -73.9442,
        "conference": "East",
        "division": "Atlantic"
    },
    {
        "name": "New York Knicks",
        "city": "New York",
        "state": "New York",
        "stadium": "Madison Square Garden",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "conference": "East",
        "division": "Atlantic"
    },
    {
        "name": "Philadelphia 76ers",
        "city": "Philadelphia",
        "state": "Pennsylvania",
        "stadium": "Wells Fargo Center",
        "latitude": 39.9526,
        "longitude": -75.1652,
        "conference": "East",
        "division": "Atlantic"
    },
    {
        "name": "Toronto Raptors",
        "city": "Toronto",
        "state": "Ontario",
        "stadium": "Scotiabank Arena",
        "latitude": 43.6532,
        "longitude": -79.3832,
        "conference": "East",
        "division": "Atlantic"
    },
    
    # Conferencia Este - División Central
    {
        "name": "Chicago Bulls",
        "city": "Chicago",
        "state": "Illinois",
        "stadium": "United Center",
        "latitude": 41.8781,
        "longitude": -87.6298,
        "conference": "East",
        "division": "Central"
    },
    {
        "name": "Cleveland Cavaliers",
        "city": "Cleveland",
        "state": "Ohio",
        "stadium": "Rocket Mortgage FieldHouse",
        "latitude": 41.4993,
        "longitude": -81.6944,
        "conference": "East",
        "division": "Central"
    },
    {
        "name": "Detroit Pistons",
        "city": "Detroit",
        "state": "Michigan",
        "stadium": "Little Caesars Arena",
        "latitude": 42.3314,
        "longitude": -83.0458,
        "conference": "East",
        "division": "Central"
    },
    {
        "name": "Indiana Pacers",
        "city": "Indianapolis",
        "state": "Indiana",
        "stadium": "Gainbridge Fieldhouse",
        "latitude": 39.7684,
        "longitude": -86.1581,
        "conference": "East",
        "division": "Central"
    },
    {
        "name": "Milwaukee Bucks",
        "city": "Milwaukee",
        "state": "Wisconsin",
        "stadium": "Fiserv Forum",
        "latitude": 43.0389,
        "longitude": -87.9065,
        "conference": "East",
        "division": "Central"
    },
    
    # Conferencia Este - División Sureste
    {
        "name": "Atlanta Hawks",
        "city": "Atlanta",
        "state": "Georgia",
        "stadium": "State Farm Arena",
        "latitude": 33.7490,
        "longitude": -84.3880,
        "conference": "East",
        "division": "Southeast"
    },
    {
        "name": "Charlotte Hornets",
        "city": "Charlotte",
        "state": "North Carolina",
        "stadium": "Spectrum Center",
        "latitude": 35.2271,
        "longitude": -80.8431,
        "conference": "East",
        "division": "Southeast"
    },
    {
        "name": "Miami Heat",
        "city": "Miami",
        "state": "Florida",
        "stadium": "Kaseya Center",
        "latitude": 25.7617,
        "longitude": -80.1918,
        "conference": "East",
        "division": "Southeast"
    },
    {
        "name": "Orlando Magic",
        "city": "Orlando",
        "state": "Florida",
        "stadium": "Amway Center",
        "latitude": 28.5383,
        "longitude": -81.3792,
        "conference": "East",
        "division": "Southeast"
    },
    {
        "name": "Washington Wizards",
        "city": "Washington",
        "state": "D.C.",
        "stadium": "Capital One Arena",
        "latitude": 38.9072,
        "longitude": -77.0369,
        "conference": "East",
        "division": "Southeast"
    },
    
    # Conferencia Oeste - División Noroeste
    {
        "name": "Denver Nuggets",
        "city": "Denver",
        "state": "Colorado",
        "stadium": "Ball Arena",
        "latitude": 39.7392,
        "longitude": -104.9903,
        "conference": "West",
        "division": "Northwest"
    },
    {
        "name": "Minnesota Timberwolves",
        "city": "Minneapolis",
        "state": "Minnesota",
        "stadium": "Target Center",
        "latitude": 44.9778,
        "longitude": -93.2650,
        "conference": "West",
        "division": "Northwest"
    },
    {
        "name": "Oklahoma City Thunder",
        "city": "Oklahoma City",
        "state": "Oklahoma",
        "stadium": "Paycom Center",
        "latitude": 35.4676,
        "longitude": -97.5164,
        "conference": "West",
        "division": "Northwest"
    },
    {
        "name": "Portland Trail Blazers",
        "city": "Portland",
        "state": "Oregon",
        "stadium": "Moda Center",
        "latitude": 45.5152,
        "longitude": -122.6784,
        "conference": "West",
        "division": "Northwest"
    },
    {
        "name": "Utah Jazz",
        "city": "Salt Lake City",
        "state": "Utah",
        "stadium": "Delta Center",
        "latitude": 40.7608,
        "longitude": -111.8910,
        "conference": "West",
        "division": "Northwest"
    },
    
    # Conferencia Oeste - División Pacífico
    {
        "name": "Golden State Warriors",
        "city": "San Francisco",
        "state": "California",
        "stadium": "Chase Center",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "conference": "West",
        "division": "Pacific"
    },
    {
        "name": "Los Angeles Clippers",
        "city": "Los Angeles",
        "state": "California",
        "stadium": "Intuit Dome",
        "latitude": 34.0522,
        "longitude": -118.2437,
        "conference": "West",
        "division": "Pacific"
    },
    {
        "name": "Los Angeles Lakers",
        "city": "Los Angeles",
        "state": "California",
        "stadium": "Crypto.com Arena",
        "latitude": 34.0522,
        "longitude": -118.2437,
        "conference": "West",
        "division": "Pacific"
    },
    {
        "name": "Phoenix Suns",
        "city": "Phoenix",
        "state": "Arizona",
        "stadium": "Footprint Center",
        "latitude": 33.4484,
        "longitude": -112.0740,
        "conference": "West",
        "division": "Pacific"
    },
    {
        "name": "Sacramento Kings",
        "city": "Sacramento",
        "state": "California",
        "stadium": "Golden 1 Center",
        "latitude": 38.5816,
        "longitude": -121.4944,
        "conference": "West",
        "division": "Pacific"
    },
    
    # Conferencia Oeste - División Suroeste
    {
        "name": "Dallas Mavericks",
        "city": "Dallas",
        "state": "Texas",
        "stadium": "American Airlines Center",
        "latitude": 32.7767,
        "longitude": -96.7970,
        "conference": "West",
        "division": "Southwest"
    },
    {
        "name": "Houston Rockets",
        "city": "Houston",
        "state": "Texas",
        "stadium": "Toyota Center",
        "latitude": 29.7604,
        "longitude": -95.3698,
        "conference": "West",
        "division": "Southwest"
    },
    {
        "name": "Memphis Grizzlies",
        "city": "Memphis",
        "state": "Tennessee",
        "stadium": "FedExForum",
        "latitude": 35.1495,
        "longitude": -90.0490,
        "conference": "West",
        "division": "Southwest"
    },
    {
        "name": "New Orleans Pelicans",
        "city": "New Orleans",
        "state": "Louisiana",
        "stadium": "Smoothie King Center",
        "latitude": 29.9511,
        "longitude": -90.0715,
        "conference": "West",
        "division": "Southwest"
    },
    {
        "name": "San Antonio Spurs",
        "city": "San Antonio",
        "state": "Texas",
        "stadium": "AT&T Center",
        "latitude": 29.4241,
        "longitude": -98.4936,
        "conference": "West",
        "division": "Southwest"
    }
]


def create_tables():
    """Crea todas las tablas en la base de datos"""
    logger.info("🔧 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas creadas exitosamente")


def populate_teams(db: Session):
    """
    Pobla la tabla de equipos con los 30 equipos NBA.
    
    Args:
        db: Sesión de base de datos
    """
    logger.info("🏀 Poblando tabla de equipos NBA...")
    
    teams_created = 0
    teams_skipped = 0
    
    for team_data in NBA_TEAMS_DATA:
        # Verificar si el equipo ya existe
        existing_team = db.query(Team).filter(Team.name == team_data["name"]).first()
        
        if existing_team:
            logger.info(f"⏭️  Equipo ya existe: {team_data['name']}")
            teams_skipped += 1
            continue
        
        # Crear nuevo equipo
        team = Team(**team_data)
        db.add(team)
        teams_created += 1
        logger.info(f"✅ Equipo creado: {team_data['name']} ({team_data['city']}, {team_data['state']})")
    
    # Commit de todos los cambios
    db.commit()
    
    logger.info(f"\n📊 Resumen:")
    logger.info(f"   ✅ Equipos creados: {teams_created}")
    logger.info(f"   ⏭️  Equipos omitidos (ya existían): {teams_skipped}")
    logger.info(f"   🏀 Total equipos en BD: {db.query(Team).count()}")


def main():
    """Función principal"""
    logger.info("🚀 Iniciando script de población de equipos NBA\n")
    
    # Crear tablas
    create_tables()
    
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # Poblar equipos
        populate_teams(db)
        logger.info("\n✅ Script completado exitosamente")
        
    except Exception as e:
        logger.error(f"\n❌ Error durante la ejecución: {str(e)}")
        db.rollback()
        raise
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
