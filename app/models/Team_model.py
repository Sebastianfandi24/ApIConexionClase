"""
Modelo de datos para equipos NBA
Define la estructura de la tabla 'teams' en la base de datos
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.config.NBA_database import Base


class Team(Base):
    """
    Modelo que representa un equipo NBA en la base de datos.
    
    Attributes:
        id (int): Identificador único del equipo
        name (str): Nombre completo del equipo (ej: "Los Angeles Lakers")
        city (str): Ciudad donde juega el equipo
        state (str): Estado/Provincia donde juega el equipo
        stadium (str): Nombre del estadio
        latitude (float): Latitud de la ubicación del estadio
        longitude (float): Longitud de la ubicación del estadio
        conference (str): Conferencia (East/West)
        division (str): División dentro de la conferencia
        created_at (datetime): Fecha de creación del registro
        updated_at (datetime): Fecha de última actualización
    """
    
    __tablename__ = "teams"
    
    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    stadium = Column(String(150), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    conference = Column(String(20), nullable=False)  # "East" o "West"
    division = Column(String(50), nullable=False)    # "Atlantic", "Central", etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        """Representación en string del equipo"""
        return f"<Team(id={self.id}, name='{self.name}', city='{self.city}')>"
    
    def to_dict(self):
        """
        Convierte el equipo a diccionario para serialización
        
        Returns:
            dict: Diccionario con los datos del equipo
        """
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "stadium": self.stadium,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "conference": self.conference,
            "division": self.division,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
