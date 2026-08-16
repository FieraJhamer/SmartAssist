"""Página web: Análisis Inteligente con IA local (Ollama)."""
import streamlit as st

from smartassist import base_datos, ia
from smartassist.pandas_analisis import estadisticas_a_texto
from smartassist.ui.estilos import encabezado, footer


def pagina():
    encabezado("Análisis Inteligente", "Interpretación automática de los reclamos con IA local (Ollama)")

    if base_datos.contar_total_reclamos() == 0:
        st.info("No hay reclamos registrados. Ingrese reclamos en la sección 'Nuevo reclamo' para poder analizarlos.")
        return

    estadisticas = estadisticas_a_texto()

    with st.expander("Ver estadísticas que alimentan al modelo"):
        st.code(estadisticas)

    st.markdown("## Generar informe")
    col_rol, col_lineas = st.columns(2)
    with col_rol:
        rol = st.selectbox(
            "Rol del modelo",
            ["Analista de datos", "Supervisor técnico", "Gerente municipal", "Responsable de atención al ciudadano"],
            key="ia_rol",
        )
    with col_lineas:
        max_lineas = st.slider("Máximo de líneas del informe", 3, 10, 5, key="ia_lineas")

    if st.button("Generar informe con IA", type="primary", key="btn_ia_informe"):
        with st.spinner("El modelo está analizando las estadísticas…"):
            try:
                respuesta = ia.generar_informe_ia(estadisticas, rol=rol, max_lineas=max_lineas)
                st.markdown(respuesta)
            except Exception as e:
                st.error(f"No se pudo conectar con Ollama: {e}")

    st.markdown("---")
    st.markdown("## Chat libre con la IA")
    consulta = st.text_input("Escriba una pregunta sobre el sistema o los datos", key="ia_consulta")
    if consulta.strip() and st.button("Enviar consulta", key="btn_ia_chat"):
        with st.spinner("Consultando al modelo…"):
            try:
                prompt = f"{consulta}\n\nDatos actuales del sistema:\n{estadisticas}"
                st.markdown(ia.consultar_ia(prompt))
            except Exception as e:
                st.error(f"No se pudo conectar con Ollama: {e}")
    footer()