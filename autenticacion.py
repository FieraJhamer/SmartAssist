import os

ADMIN_USUARIO = os.environ.get("SMARTASSIST_ADMIN_USUARIO", "admin")
ADMIN_CLAVE = os.environ.get("SMARTASSIST_ADMIN_CLAVE", "admin123")


def autenticar(usuario, clave):
    """Valida las credenciales de administrador.

    Las credenciales se leen de las variables de entorno
    SMARTASSIST_ADMIN_USUARIO y SMARTASSIST_ADMIN_CLAVE, con valores
    por defecto solo para desarrollo.
    """
    return usuario.strip() == ADMIN_USUARIO and clave == ADMIN_CLAVE
