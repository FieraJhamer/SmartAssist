"""Autenticación de administradores: login, hashing y token de sesión."""
import base64
import hashlib
import hmac
import json
import os
import time

import bcrypt

from smartassist import base_datos
from smartassist import config  # noqa: F401  (índice: garantiza la carga de .env)

ADMIN_USUARIO = os.environ.get("SMARTASSIST_ADMIN_USUARIO", "admin")
ADMIN_CLAVE = os.environ.get("SMARTASSIST_ADMIN_CLAVE", "admin123")

# Duración de la sesión (en horas y segundos)
SESSION_HORAS = int(os.environ.get("SMARTASSIST_SESSION_HORAS", "8"))
SESSION_SEGUNDOS = SESSION_HORAS * 3600
# Secreto para firmar el token de sesión (idealmente distinto en producción)
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


def _firmar(payload):
    """Firma el payload base64 con SESION_SECRETO (HMAC-SHA256)."""
    mensaje = payload.encode("utf-8")
    firma = hmac.new(SESION_SECRETO.encode("utf-8"), mensaje, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(firma).decode("ascii")


def _payload_urlsafe(payload_bytes):
    return base64.urlsafe_b64encode(payload_bytes).decode("ascii")


def _decodificar_payload(payload_b64):
    try:
        return base64.urlsafe_b64decode(payload_b64.encode("ascii"))
    except (ValueError, TypeError):
        return None


def crear_token_sesion(usuario):
    """Genera un token de sesión firmado con expiración (SESSION_HORAS).

    Formato: <payload_b64>.<firma>, donde payload = {"usuario", "exp"}
    """
    exp = int(time.time()) + SESSION_SEGUNDOS
    payload_json = json.dumps({"usuario": usuario, "exp": exp}, separators=(",", ":")).encode("utf-8")
    payload_b64 = _payload_urlsafe(payload_json)
    firma = _firmar(payload_b64)
    return f"{payload_b64}.{firma}"


def verificar_token_sesion(token):
    """Valida firma y expiración del token. Devuelve el usuario o None."""
    if not token or "." not in token:
        return None
    payload_b64, _, firma = token.rpartition(".")
    if not hmac.compare_digest(firma, _firmar(payload_b64)):
        return None
    payload_bytes = _decodificar_payload(payload_b64)
    if payload_bytes is None:
        return None
    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except (ValueError, TypeError):
        return None
    usuario = payload.get("usuario")
    exp = payload.get("exp")
    if not usuario or not isinstance(exp, (int, float)) or exp < time.time():
        return None
    return usuario