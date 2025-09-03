from datetime import date
from sqlalchemy.orm import Session
from app.repositories.NBA_repository import PlayerRepository
from app.models.NBA_model import Player


"""
Librerías utilizadas:
- repositories.NBA_repository: Proporciona la clase PlayerRepository para la gestión de jugadores en la base de datos.
- models.NBA_model: Define el modelo Player que representa a un jugador de la NBA.
- sqlalchemy.orm.Session: Permite manejar la sesión de la base de datos para realizar operaciones transaccionales.
"""


class PlayerService:
    """
    Capa de servicios para la gestión de jugadores NBA.
    Contiene la lógica de negocio y validaciones, delegando las operaciones de persistencia al repositorio.
    """

    def __init__(self, db_session: Session):
        """
        Inicializa el servicio de jugadores con una sesión de base de datos y un repositorio de jugadores.
        """
        self.repository = PlayerRepository(db_session)

    def listar_jugadores(self, skip: int = 0, limit: int = 100):
        """
        Recupera y retorna todos los jugadores con soporte para paginación.
        Útil para catálogos, listados o vistas generales.
        """
        return self.repository.get_all_players(skip=skip, limit=limit)

    def obtener_jugador(self, player_id: int):
        """
        Busca y retorna un jugador específico por su ID alfanumérico.
        Retorna None si no se encuentra.
        """
        return self.repository.get_player_by_id(player_id)

    def crear_jugador(self, name: str, team: str, position: str, height_m: float, weight_kg: float, birth_date: date):
        """
        Crea un nuevo jugador de la NBA con validaciones de negocio:
        - ID único.
        - Nombre no vacío.
        - Altura y peso válidos (>0).
        - Fecha de nacimiento no futura.
        """
        # Validaciones de negocio
        if not name or name.strip() == "":
            raise ValueError("El nombre del jugador no puede estar vacío")

        if not team or team.strip() == "":
            raise ValueError("El equipo no puede estar vacío")

        if height_m <= 0 or weight_kg <= 0:
            raise ValueError("La altura y el peso deben ser mayores a 0")

        # Convertir birth_date a date si es datetime
        if hasattr(birth_date, 'date'):
            birth_date_date = birth_date.date()
        else:
            birth_date_date = birth_date
        if birth_date_date > date.today():
            raise ValueError("La fecha de nacimiento no puede estar en el futuro")

        # Crear jugador
        new_player = Player(
            name=name,
            team=team,
            position=position,
            height_m=height_m,
            weight_kg=weight_kg,
            birth_date=birth_date
        )

        return self.repository.create_player(new_player)

    def actualizar_jugador(self, player_id: int, **kwargs):
        """
        Actualiza los datos de un jugador existente.
        Aplica validaciones de negocio según los campos recibidos.
        """
        player = self.repository.get_player_by_id(player_id)
        if not player:
            raise ValueError(f"No se encontró un jugador con ID {player_id}")

        if "name" in kwargs and not kwargs["name"].strip():
            raise ValueError("El nombre del jugador no puede estar vacío")
        if "team" in kwargs and not kwargs["team"].strip():
            raise ValueError("El equipo no puede estar vacío")
        if "height_m" in kwargs and kwargs["height_m"] <= 0:
            raise ValueError("La altura debe ser mayor a 0")
        if "weight_kg" in kwargs and kwargs["weight_kg"] <= 0:
            raise ValueError("El peso debe ser mayor a 0")
            if "birth_date" in kwargs:
                birth_date = kwargs["birth_date"]
                if hasattr(birth_date, "date"):
                    birth_date = birth_date.date()
                if birth_date > date.today():
                    raise ValueError("La fecha de nacimiento no puede estar en el futuro")
                kwargs["birth_date"] = birth_date

        # Aplicar cambios
        for key, value in kwargs.items():
            setattr(player, key, value)

        return self.repository.update_player(player)

    def eliminar_jugador(self, player_id: str):
        """
        Elimina un jugador existente según su ID.
        Lanza un error si no se encuentra.
        """
        player = self.repository.get_player_by_id(player_id)
        if not player:
            raise ValueError(f"No se encontró un jugador con ID {player_id}")

        return self.repository.delete_player(player)

# Funciones globales para exponer los métodos de PlayerService
def listar_jugadores(db, skip=0, limit=100):
    return PlayerService(db).listar_jugadores(skip, limit)

def obtener_jugador(db, player_id: int):
    return PlayerService(db).obtener_jugador(player_id)

def crear_jugador(db, player):
    return PlayerService(db).crear_jugador(
        name=player.name,
        team=player.team,
        position=player.position,
        height_m=player.height_m,
        weight_kg=player.weight_kg,
        birth_date=player.birth_date
    )

def actualizar_jugador(db, player_id: int, player):
    return PlayerService(db).actualizar_jugador(
        player_id,
        name=player.name,
        team=player.team,
        position=player.position,
        height_m=player.height_m,
        weight_kg=player.weight_kg,
        birth_date=player.birth_date
    )

def eliminar_jugador(db, player_id: int):
    return PlayerService(db).eliminar_jugador(player_id)
