from sqlalchemy.orm import Session
from app.repositories.User_repository import UserRepository
from app.models.User_model import User
import hashlib


"""
Librerías utilizadas:
- repositories.User_repository: Proporciona la clase UserRepository para la gestión de usuarios en la base de datos.
- models.User_model: Define el modelo User que representa a un usuario del sistema.
- sqlalchemy.orm.Session: Permite manejar la sesión de la base de datos para realizar operaciones transaccionales.
- hashlib: Para hashear contraseñas de forma segura.
"""


class UserService:
    """
    Capa de servicios para la gestión de usuarios.
    Contiene la lógica de negocio y validaciones, delegando las operaciones de persistencia al repositorio.
    """

    def __init__(self, db_session: Session):
        """
        Inicializa el servicio de usuarios con una sesión de base de datos y un repositorio de usuarios.
        """
        self.repository = UserRepository(db_session)

    def _hash_password(self, password: str) -> str:
        """Hashea una contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def listar_usuarios(self, skip: int = 0, limit: int = 100):
        """
        Recupera y retorna todos los usuarios con soporte para paginación.
        Útil para catálogos, listados o vistas generales.
        """
        return self.repository.get_all_users(skip=skip, limit=limit)

    def obtener_usuario(self, user_id: int):
        """
        Busca y retorna un usuario específico por su ID numérico.
        Retorna None si no se encuentra.
        """
        return self.repository.get_user_by_id(user_id)

    def obtener_usuario_por_username(self, username: str):
        """
        Busca y retorna un usuario específico por su nombre de usuario.
        Retorna None si no se encuentra.
        """
        return self.repository.get_user_by_username(username)

    def crear_usuario(self, username: str, password: str):
        """
        Crea un nuevo usuario con validaciones de negocio:
        - Username único y no vacío.
        - Password no vacío y con longitud mínima.
        - Password se hashea antes de almacenar.
        """
        # Validaciones de negocio
        if not username or username.strip() == "":
            raise ValueError("El nombre de usuario no puede estar vacío")
        
        if len(username) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        
        if len(username) > 50:
            raise ValueError("El nombre de usuario no puede tener más de 50 caracteres")
        
        if not password or password.strip() == "":
            raise ValueError("La contraseña no puede estar vacía")
        
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        # Verificar que el username sea único
        existing_user = self.repository.get_user_by_username(username)
        if existing_user:
            raise ValueError(f"El nombre de usuario '{username}' ya está en uso")

        # Hashear la contraseña
        hashed_password = self._hash_password(password)

        # Crear el usuario
        new_user = User(
            username=username,
            password=hashed_password
        )

        return self.repository.create_user(new_user)

    def actualizar_usuario(self, user_id: int, username: str = None, password: str = None):
        """
        Actualiza un usuario existente con validaciones:
        - Usuario debe existir.
        - Si se proporciona username, debe ser único.
        - Si se proporciona password, se hashea antes de almacenar.
        """
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

        # Validar y actualizar username si se proporciona
        if username is not None:
            if not username or username.strip() == "":
                raise ValueError("El nombre de usuario no puede estar vacío")
            
            if len(username) < 3:
                raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
            
            if len(username) > 50:
                raise ValueError("El nombre de usuario no puede tener más de 50 caracteres")

            # Verificar que el nuevo username sea único (excepto para el usuario actual)
            existing_user = self.repository.get_user_by_username(username)
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"El nombre de usuario '{username}' ya está en uso")
            
            user.username = username

        # Validar y actualizar password si se proporciona
        if password is not None:
            if not password or password.strip() == "":
                raise ValueError("La contraseña no puede estar vacía")
            
            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            
            # Hashear la nueva contraseña
            user.password = self._hash_password(password)

        return self.repository.update_user(user)

    def eliminar_usuario(self, user_id: int):
        """
        Elimina un usuario existente.
        Valida que el usuario exista antes de eliminarlo.
        """
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")
        
        self.repository.delete_user(user)
        return user


# Funciones helper para usar en los controladores (siguiendo el patrón existente)
def listar_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Función helper para listar usuarios"""
    service = UserService(db)
    return service.listar_usuarios(skip, limit)

def obtener_usuario(db: Session, user_id: int):
    """Función helper para obtener un usuario por ID"""
    service = UserService(db)
    return service.obtener_usuario(user_id)

def obtener_usuario_por_username(db: Session, username: str):
    """Función helper para obtener un usuario por username"""
    service = UserService(db)
    return service.obtener_usuario_por_username(username)

def crear_usuario(db: Session, username: str, password: str):
    """Función helper para crear un usuario"""
    service = UserService(db)
    return service.crear_usuario(username, password)

def actualizar_usuario(db: Session, user_id: int, username: str = None, password: str = None):
    """Función helper para actualizar un usuario"""
    service = UserService(db)
    return service.actualizar_usuario(user_id, username, password)

def eliminar_usuario(db: Session, user_id: int):
    """Función helper para eliminar un usuario"""
    service = UserService(db)
    return service.eliminar_usuario(user_id)