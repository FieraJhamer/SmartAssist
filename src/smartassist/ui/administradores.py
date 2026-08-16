"""Página web: Gestión de administradores."""
import pandas as pd
import streamlit as st

from smartassist import autenticacion, base_datos
from smartassist.ui.estilos import encabezado, footer


def pagina():
    encabezado("Administradores", "Gestioná los usuarios con acceso al sistema")

    st.markdown("## Agregar administrador")
    col_u, col_c = st.columns(2)
    with col_u:
        nuevo_usuario = st.text_input("Usuario", key="adm_usuario")
    with col_c:
        nueva_clave = st.text_input("Contraseña", type="password", key="adm_clave")
    col_p, _ = st.columns(2)
    with col_p:
        confirmar_clave = st.text_input("Confirmar contraseña", type="password", key="adm_clave2")

    if st.button("Crear administrador", type="primary", key="btn_crear_admin"):
        nuevo_usuario = nuevo_usuario.strip()
        if len(nuevo_usuario) < 3:
            st.warning("El usuario debe tener al menos 3 caracteres.")
        elif len(nueva_clave) < 4:
            st.warning("La contraseña debe tener al menos 4 caracteres.")
        elif nueva_clave != confirmar_clave:
            st.warning("Las contraseñas no coinciden.")
        elif autenticacion.usuario_existe(nuevo_usuario):
            st.warning("Ese usuario ya existe.")
        else:
            autenticacion.crear_usuario(nuevo_usuario, nueva_clave)
            st.success(f"Administrador '{nuevo_usuario}' creado correctamente.")

    st.markdown("## Administradores existentes")
    usuarios = base_datos.obtener_usuarios()
    if not usuarios:
        st.info("No hay administradores registrados.")
    else:
        st.dataframe(
            pd.DataFrame(usuarios, columns=["Usuario", "Creado el"]),
            width="stretch",
            hide_index=True,
        )

    st.markdown("## Eliminar administrador")
    nombres = [u[0] for u in usuarios]
    if nombres:
        id_borrar = st.selectbox("Seleccionar administrador", nombres, key="adm_borrar")
        if st.button("Eliminar administrador", key="btn_eliminar_admin"):
            if id_borrar == st.session_state.get("usuario", "admin"):
                st.error("No podés eliminar tu propia cuenta.")
            elif id_borrar == autenticacion.ADMIN_USUARIO and len(nombres) == 1:
                st.error("No se puede eliminar el único administrador.")
            else:
                base_datos.eliminar_usuario(id_borrar)
                st.success(f"Administrador '{id_borrar}' eliminado.")
    footer()