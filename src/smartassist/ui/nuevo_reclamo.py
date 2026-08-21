"""Página web: Nuevo reclamo (acceso libre para ciudadanos)."""
from datetime import datetime

import streamlit as st

from smartassist import base_datos, clasificador, ia, plantillas_respuestas, storage_imagenes, validaciones
from smartassist.ui.estilos import encabezado, footer, tarjeta_resultado
from smartassist.ui.mapa import mostrar_mapa


def pagina():
    encabezado("Reclamos Ciudadanos", "Reporta un problema del municipio y nosotros lo gestionamos")

    st.markdown("## Nuevo reclamo")
    st.caption("Contanos qué está pasando y el sistema lo clasificará por categoría y prioridad.")
    if not st.session_state.logueado:
        st.caption("Las secciones de Historial, Estadísticas y Análisis Inteligente requieren acceso de administrador.")

    comentario = st.text_area(
        "Comentario del usuario",
        placeholder="Ej.: No hay alumbrado público en la calle Alberdi…",
        height=130,
        label_visibility="collapsed",
    )

    col_calle, col_num = st.columns(2)
    with col_calle:
        calle = st.text_input("Calle")
    with col_num:
        numero = st.text_input("Número")

    fotos = st.file_uploader(
        "Fotos del problema (opcional)",
        type=["png", "jpg", "jpeg", "gif", "webp"],
        accept_multiple_files=True,
        help=f"Máximo {storage_imagenes.TAMANIO_MAXIMO_MB} MB por foto.",
    )

    if calle.strip():
        with st.expander(f"Ubicación (aproximada) — {calle.strip()} {numero.strip()}",
                          expanded=True):
            mostrar_mapa(calle.strip(), numero.strip(), altura=280)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        analizar = st.button("Clasificar y guardar", type="primary", width="stretch")

    if analizar:
        ok, motivo = validaciones.validar_comentario(comentario)
        if not ok:
            st.warning(motivo)
            return
        comentario = comentario.strip()
        ok, motivo = validaciones.validar_calle(calle)
        if not ok:
            st.warning(motivo)
            return
        calle = calle.strip()
        ok, motivo = validaciones.validar_numero(numero)
        if not ok:
            st.warning(motivo)
            return
        numero = numero.strip()
        categoria, prioridad_reglas = clasificador.clasificar_comentario(comentario)
        with st.spinner("Consultando a la IA por la prioridad…"):
            prioridad_ia, detalle_ia = ia.sugerir_prioridad_ia(comentario)
        prioridad, origen_prioridad = ia.combinar_prioridades(prioridad_reglas, prioridad_ia)
        respuesta = plantillas_respuestas.generar_respuesta(categoria)
        fecha_ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id_reclamo = base_datos.insertar_reclamo(
            comentario, categoria, prioridad, calle, numero, fecha=fecha_ahora
        )

        guardadas, rechazadas = storage_imagenes.guardar_imagenes(fotos, id_reclamo)

        st.markdown("### Resultado")
        tarjeta_resultado(categoria, prioridad, respuesta)
        st.caption(f"Prioridad asignada: reglas → **{prioridad_reglas}**, IA → "
                   f"**{prioridad_ia or 'no disponible'}**. Determinó el valor: **{origen_prioridad}**.")
        if detalle_ia:
            st.caption(detalle_ia)
        if guardadas:
            st.success(
                f"Reclamo #{id_reclamo} registrado el {fecha_ahora} con {guardadas} foto(s)."
            )
        else:
            st.success(f"Reclamo #{id_reclamo} registrado el {fecha_ahora}.")
        for nombre, motivo in rechazadas:
            st.warning(f"{nombre}: {motivo}")
    footer()