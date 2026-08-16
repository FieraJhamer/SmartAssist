"""SmartAssist — Interfaz web (punto de entrada principal).

Orquesta la navegación y delega cada sección en ``smartassist.ui``.
"""
import base64
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st

from smartassist import autenticacion, base_datos
from smartassist.config import CATEGORIAS, COLOR_CATEGORIA, FAVICON, LOGO_MUNICIPIO
from smartassist.ui import administradores, analisis_ia, estadisticas, historial, nuevo_reclamo, sesion
from smartassist.ui.estilos import inyectar_css

st.set_page_config(
    page_title="Reclamos Ciudadanos · La Rioja",
    page_icon=FAVICON if os.path.exists(FAVICON) else "🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _navegar_a(nombre):
    st.session_state.pagina_actual = nombre


def main():
    base_datos.crear_tabla()
    autenticacion.crear_admin_inicial()
    inyectar_css()

    if "logueado" not in st.session_state:
        st.session_state.logueado = False
    if "pagina_actual" not in st.session_state:
        st.session_state.pagina_actual = "Nuevo reclamo"

    # Restaurar sesión desde el token en la URL (persiste al recargar la página)
    if not st.session_state.logueado:
        try:
            token_usuario = sesion.leer_sesion_token()
        except Exception:
            token_usuario = None
        if token_usuario:
            st.session_state.logueado = True
            st.session_state.usuario = token_usuario
            st.session_state.pagina_actual = "Historial"

    if os.path.exists(LOGO_MUNICIPIO):
        with open(LOGO_MUNICIPIO, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        st.sidebar.markdown(
            f"""
            <div class="sidebar-brand">
                <img src="data:image/png;base64,{logo_b64}" alt="Marca La Rioja">
                <p class="sidebar-muni">Municipalidad de La Rioja</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown("## La Rioja")
        st.sidebar.markdown("#### Reclamos Ciudadanos")
    st.sidebar.markdown("---")

    # Login de administrador
    if not st.session_state.logueado:
        st.sidebar.markdown("### Acceso administrador")
        st.sidebar.text_input("Usuario", key="login_usuario")
        st.sidebar.text_input("Contraseña", type="password", key="login_clave")
        if st.sidebar.button(
            "Ingresar", type="primary", width="stretch", key="btn_login",
            on_click=sesion.login_callback,
        ):
            pass
        if st.session_state.get("login_error"):
            st.sidebar.error("Usuario o contraseña incorrectos.")
            st.session_state.login_error = False
    else:
        st.sidebar.markdown(f"#### Sesión: **{st.session_state.get('usuario', 'admin')}**")
        if st.sidebar.button(
            "Cerrar sesión", width="stretch", key="btn_logout",
            on_click=sesion.logout_callback,
        ):
            pass
    st.sidebar.markdown("---")

    # Secciones (los usuarios sin sesión solo ven "Nuevo reclamo")
    secciones = ["Nuevo reclamo"] if not st.session_state.logueado else [
        "Nuevo reclamo", "Historial", "Estadísticas", "Análisis Inteligente",
        "Administradores",
    ]
    for nombre in secciones:
        activo = st.session_state.pagina_actual == nombre
        st.sidebar.button(
            nombre,
            key=f"nav_{nombre}",
            type="primary" if activo else "secondary",
            width="stretch",
            on_click=_navegar_a,
            args=(nombre,),
        )

    if not st.session_state.logueado and st.session_state.pagina_actual != "Nuevo reclamo":
        st.session_state.pagina_actual = "Nuevo reclamo"

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Categorías del municipio**")
    for cat in CATEGORIAS:
        color = COLOR_CATEGORIA[cat]
        st.sidebar.markdown(
            f'<span class="badge badge-cat" style="border-color:{color};">{cat}</span>',
            unsafe_allow_html=True,
        )
    st.sidebar.caption("Clasificador inteligente de reclamos · v1.0")

    pagina = st.session_state.pagina_actual
    if pagina == "Nuevo reclamo":
        nuevo_reclamo.pagina()
    elif pagina == "Historial":
        historial.pagina()
    elif pagina == "Estadísticas":
        estadisticas.pagina()
    elif pagina == "Análisis Inteligente":
        analisis_ia.pagina()
    else:
        administradores.pagina()


if __name__ == "__main__":
    main()