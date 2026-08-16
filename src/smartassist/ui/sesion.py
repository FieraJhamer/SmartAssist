"""Gestión de la sesión del administrador en la interfaz web."""
import streamlit as st

from smartassist import autenticacion


def leer_sesion_token():
    """Devuelve el usuario autenticado desde el token en la URL, o None."""
    try:
        token = st.query_params.get("sesion_admin", [None])
    except Exception:
        return None
    if isinstance(token, list):
        token = token[0] if token else None
    if not token:
        return None
    usuario = autenticacion.verificar_token_sesion(token)
    if usuario:
        return usuario
    return None


def guardar_sesion_token(usuario):
    st.query_params["sesion_admin"] = autenticacion.crear_token_sesion(usuario)


def limpiar_sesion_token():
    try:
        del st.query_params["sesion_admin"]
    except Exception:
        pass


def cerrar_sesion():
    st.session_state.logueado = False
    st.session_state.pagina_actual = "Nuevo reclamo"
    limpiar_sesion_token()


def login_callback():
    usuario = st.session_state.get("login_usuario", "")
    clave = st.session_state.get("login_clave", "")
    if autenticacion.autenticar(usuario, clave):
        st.session_state.logueado = True
        st.session_state.usuario = usuario.strip()
        st.session_state.pagina_actual = "Historial"
        try:
            guardar_sesion_token(usuario.strip())
        except Exception:
            pass
        st.session_state.login_error = False
    else:
        st.session_state.login_error = True


def logout_callback():
    cerrar_sesion()