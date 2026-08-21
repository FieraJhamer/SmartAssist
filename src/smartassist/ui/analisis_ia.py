"""Página web: Análisis Inteligente con IA local (Ollama)."""
import streamlit as st

from smartassist import base_datos, ia
from smartassist.pandas_analisis import estadisticas_a_texto
from smartassist.ui.estilos import encabezado, footer


def _inicializar_chat():
    if "ia_chat_historial" not in st.session_state:
        st.session_state.ia_chat_historial = []


def _mostrar_chat():
    for mensaje in st.session_state.ia_chat_historial:
        with st.chat_message(mensaje["rol"]):
            st.markdown(mensaje["contenido"])


def _enviar_consulta(consulta):
    """Registra el mensaje del usuario; la respuesta se genera en el rerun."""
    st.session_state.ia_chat_historial.append({"rol": "user", "contenido": consulta})


def _generar_respuesta_pendiente(estadisticas):
    """Si el último mensaje es del usuario, genera y muestra la respuesta del asistente.

    El spinner es visible durante la espera real de Ollama porque la llamada
    ocurre dentro del render de la burbuja del asistente.
    """
    historial = st.session_state.ia_chat_historial
    if not historial or historial[-1]["rol"] != "user":
        return
    consulta = historial[-1]["contenido"]
    prompt = f"{consulta}\n\nDatos actuales del sistema:\n{estadisticas}"
    with st.chat_message("assistant"):
        try:
            with st.spinner("Consultando al modelo…"):
                respuesta = ia.consultar_ia(prompt)
        except Exception as e:
            respuesta = f"⚠️ Error al conectar con Ollama: {e}"
        st.markdown(respuesta)
    historial.append({"rol": "assistant", "contenido": respuesta})


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
    st.caption("Preguntá sobre los reclamos, pedí resúmenes, recomendaciones, etc. El contexto incluye las estadísticas actuales.")

    _inicializar_chat()
    _mostrar_chat()

    # Genera la respuesta pendiente ANTES del formulario para que el spinner
    # y la burbuja del asistente aparezcan por encima del input.
    _generar_respuesta_pendiente(estadisticas)

    # Formulario dentro del contenedor principal (no fijo al pie como chat_input)
    with st.form("ia_chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([6, 1])
        with col_input:
            consulta = st.text_input(
                "Tu mensaje",
                placeholder="Escribí tu pregunta…",
                label_visibility="collapsed",
                key="ia_chat_input",
            )
        with col_btn:
            enviado = st.form_submit_button("Enviar", type="primary", width="stretch")

    if enviado and consulta.strip():
        _enviar_consulta(consulta)
        st.rerun()

    footer()