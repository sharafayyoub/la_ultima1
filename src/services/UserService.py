import hashlib
import os
import uuid
from src.repositories.UsuarioRepository import UsuarioRepository

class UserService:
    def __init__(self):
        self.user_repo = UsuarioRepository()

    def register(self, username: str, password: str) -> bool:
        # Validar que el nombre no exista
        if self.user_repo.exists(username):
            return False
        # Generar salt y hash
        salt = os.urandom(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        # Guardar usuario con hash y salt
        self.user_repo.save(username, password_hash, salt)
        return True

    def login(self, username: str, password: str):
        user = self.user_repo.get(username)
        if not user:
            return None
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            user['salt'],
            100000
        )
        if password_hash == user['password_hash']:
            session_token = str(uuid.uuid4())
            # Opcional: guardar sesión en memoria o marcar usuario como logueado
            # No se implementa persistencia de sesión ni "recordarme". Las credenciales se almacenan, pero la sesión solo vive en memoria.
            return session_token
        return None
