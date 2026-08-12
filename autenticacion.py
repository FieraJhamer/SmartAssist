import os

import bcrypt
from dotenv import load_dotenv

import base_datos

load_dotenv()

ADMIN_USUARIO = os.environ.get("SMARTASSIST_ADMIN_USUARIO", "admin")
ADMIN_CLAVE = os.environ.get("SMARTASSIST_ADMIN_CLAVE", "admin123")

# Duración de la sesión por cookies (en horas y segundos)
SESSION_HORAS = int(os.environ.get("SMARTASSIST_SESSION_HORAS", "8"))
SESSION_SEGUNDOS = SESSION_HORAS * 3600
# Secreto para cifrar las cookies de sesión (idealmente distinto en producción)
SESION_SECRETO = os.environ.get("SMARTASSIST_SESSION_SECRET", "clave-cookies-dev")


def hash_clave(clave):
    """Genera un hash bcrypt para una contraseña."""
    return bcrypt.hashpw(clave.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_clave(clave, clave_hash):
    """Compara una contraseña en claro contra su hash bcrypt."""
    try:
        return bcrypt.checkpw(clave.encode("utf-8"), clave_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def crear_admin_inicial():
    """Crea el administrador inicial a partir de las variables de entorno.

    Devuelve True si creó el usuario, False si el usuario ya existía.
    """
    if base_datos.existe_usuario(ADMIN_USUARIO):
        return False
    base_datos.crear_usuario(ADMIN_USUARIO, hash_clave(ADMIN_CLAVE))
    return True


def autenticar(usuario, clave):
    """Valida las credenciales de un usuario contra la base de datos."""
    if not usuario or not clave:
        return False
    clave_hash = base_datos.obtener_clave_hash(usuario.strip())
    if not clave_hash:
        return False
    return verificar_clave(clave, clave_hash)


def usuario_existe(usuario):
    """Indica si un nombre de usuario ya está registrado."""
    return base_datos.existe_usuario(usuario.strip())


def crear_usuario(usuario, clave):
    """Crea un nuevo usuario con su contraseña hasheada."""
    return base_datos.crear_usuario(usuario.strip(), hash_clave(clave))