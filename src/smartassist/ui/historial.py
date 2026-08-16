"""Página web: Historial de reclamos (consulta, edición y eliminación)."""
import streamlit as st

from smartassist import base_datos, storage_imagenes, validaciones
from smartassist.config import CATEGORIAS, COLOR_CATEGORIA, COLOR_PRIORIDAD, PRIORIDADES
from smartassist.pandas_analisis import dataframe_reclamos
from smartassist.ui.estilos import (
    encabezado,
    etiqueta_categoria_html,
    etiqueta_prioridad_html,
    fecha_formateada,
    footer,
)
from smartassist.ui.mapa import mostrar_mapa


def _etiqueta_reclamo(fila):
    comentario = fila["Comentario"]
    if len(comentario) > 45:
        comentario = comentario[:45] + "…"
    return f"#{int(fila['ID'])} · {comentario}"


def _formulario_editar(registro):
    st.markdown("#### Editar reclamo")
    nuevo_comentario = st.text_area(
        "Comentario", value=registro[1], key="edit_com", height=110
    )
    col_a, col_b = st.columns(2)
    with col_a:
        nueva_categoria = st.selectbox(
            "Categoría",
            CATEGORIAS,
            index=CATEGORIAS.index(registro[2]) if registro[2] in CATEGORIAS else 0,
            key="edit_cat",
        )
    with col_b:
        nueva_prioridad = st.selectbox(
            "Prioridad",
            PRIORIDADES,
            index=PRIORIDADES.index(registro[3]) if registro[3] in PRIORIDADES else 0,
            key="edit_pri",
        )
    col_x, col_y = st.columns(2)
    with col_x:
        nueva_calle = st.text_input("Calle", value=registro[4] or "", key="edit_calle")
    with col_y:
        nuevo_numero = st.text_input("Número", value=registro[5] or "", key="edit_num")

    if st.button("Guardar cambios", key="btn_editar", type="primary"):
        ok, motivo = validaciones.validar_comentario(nuevo_comentario)
        if not ok:
            st.warning(motivo)
            return
        ok, motivo = validaciones.validar_calle(nueva_calle)
        if not ok:
            st.warning(motivo)
            return
        ok, motivo = validaciones.validar_numero(nuevo_numero)
        if not ok:
            st.warning(motivo)
            return
        base_datos.actualizar_reclamo(
            int(registro[0]),
            nuevo_comentario.strip(),
            nueva_categoria,
            nueva_prioridad,
            nueva_calle.strip(),
            nuevo_numero.strip(),
        )
        st.success("Reclamo actualizado correctamente.")


@st.dialog("Eliminar reclamo", width="small")
def _dialogo_eliminar(id_reclamo, etiqueta):
    st.markdown(f"¿Seguro que querés eliminar el reclamo **{etiqueta}** y todas sus fotos?")
    st.caption("Esta acción no se puede deshacer.")
    col_ok, col_cancel = st.columns(2)
    with col_ok:
        if st.button("Sí, eliminar", type="primary", key="conf_eliminar"):
            storage_imagenes.eliminar_fotos_reclamo(int(id_reclamo))
            base_datos.eliminar_reclamo(int(id_reclamo))
            st.session_state.pop("historial_seleccion", None)
            st.rerun()
    with col_cancel:
        if st.button("Cancelar", key="cancelar_eliminar"):
            st.rerun()


def _detalle_reclamo(ids, etiquetas):
    st.markdown("## Detalle del reclamo")
    st.caption("Seleccioná un reclamo de la lista para ver su ficha completa.")
    id_seleccion = st.selectbox(
        "Reclamo",
        ids,
        key="historial_seleccion",
        format_func=lambda i: etiquetas[i],
    )
    if id_seleccion is None:
        return

    registro = base_datos.obtener_reclamo_por_id(int(id_seleccion))
    if not registro:
        st.warning("Ese reclamo ya no existe. Se actualizó la lista.")
        return

    id_reclamo, comentario, categoria, prioridad, calle, numero, fecha = registro

    st.markdown(
        f"""
        <div class="tarjeta">
            <div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;">
                {etiqueta_prioridad_html(prioridad)}
                {etiqueta_categoria_html(categoria)}
                <span class="muted" style="margin-left:auto;">🗓️ {fecha_formateada(fecha)}</span>
            </div>
            <div style="margin-top:0.8rem;font-size:1.05rem;">{comentario}</div>
            <div class="muted" style="margin-top:0.6rem;">
                📍 {calle or "—"} {numero or ""} · La Rioja, Argentina
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Fotos")
    nombres_fotos = base_datos.obtener_imagenes_reclamo(int(id_reclamo))
    if nombres_fotos:
        columnas = st.columns(min(len(nombres_fotos), 3))
        for i, nombre in enumerate(nombres_fotos):
            ruta = storage_imagenes.ruta_archivo(int(id_reclamo), nombre)
            with columnas[i % 3]:
                st.image(ruta, width="stretch")
    else:
        st.info("Este reclamo no tiene fotos adjuntas.")

    st.markdown("### Ubicación (aproximada)")
    if calle or numero:
        mostrar_mapa(calle or "", numero or "", altura=320)
    else:
        st.info("Este reclamo no tiene dirección cargada.")

    _formulario_editar(registro)

    st.markdown("### Eliminar reclamo")
    if st.button("Eliminar reclamo", key="btn_eliminar"):
        _dialogo_eliminar(int(id_reclamo), etiquetas.get(int(id_reclamo), f"#{id_reclamo}"))


def pagina():
    encabezado("Historial de reclamos", "Consulta, analiza y gestiona los reclamos registrados")

    if not base_datos.obtener_todos_reclamos():
        st.info("Todavía no hay reclamos registrados.")
        footer()
        return

    col_cat, col_pri = st.columns(2)
    with col_cat:
        filtro_cat = st.selectbox("Filtrar por categoría", ["Todas"] + CATEGORIAS)
    with col_pri:
        filtro_pri = st.selectbox("Filtrar por prioridad", ["Todas"] + PRIORIDADES)

    df = dataframe_reclamos()
    if filtro_cat != "Todas":
        df = df[df["Categoría"] == filtro_cat]
    if filtro_pri != "Todas":
        df = df[df["Prioridad"] == filtro_pri]

    if df.empty:
        st.warning("No hay reclamos que coincidan con los filtros seleccionados.")
        footer()
        return

    df = df.sort_values("ID", ascending=False).reset_index(drop=True)

    st.markdown("## Lista de reclamos")
    df_tabla = df.copy()
    df_tabla["Comentario"] = df_tabla["Comentario"].apply(
        lambda c: c if len(c) <= 50 else c[:50] + "…"
    )
    df_tabla = df_tabla[["ID", "Comentario", "Categoría", "Prioridad", "Calle", "Fecha"]]

    def _color_prioridad(val):
        color = COLOR_PRIORIDAD.get(val, "#94a3b8")
        return f"color: #fff; background-color: {color}; font-weight: 700; text-align: center;"

    def _color_categoria(val):
        color = COLOR_CATEGORIA.get(val, "#94a3b8")
        return f"color: #fff; background-color: {color}; text-align: center;"

    df_estilizado = df_tabla.style.map(_color_prioridad, subset=["Prioridad"]).map(
        _color_categoria, subset=["Categoría"]
    )
    st.dataframe(df_estilizado, width="stretch", hide_index=True)

    ids = [int(i) for i in df["ID"]]
    etiquetas = {fila["ID"]: _etiqueta_reclamo(fila) for _, fila in df.iterrows()}

    _detalle_reclamo(ids, etiquetas)
    footer()