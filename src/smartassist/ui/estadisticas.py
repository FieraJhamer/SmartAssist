"""Página web: Estadísticas y reportes con Pandas."""
import pandas as pd
import streamlit as st

from smartassist import base_datos
from smartassist.pandas_analisis import dataframe_reclamos
from smartassist.ui.estilos import encabezado, footer


def pagina():
    encabezado("Estadísticas", "Visión general de los reclamos de la ciudad")

    total = base_datos.contar_total_reclamos()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de reclamos", total)
    c2.metric(
        "Prioridad ALTA",
        len(base_datos.obtener_reclamos_por_prioridad("ALTA")),
    )
    c3.metric(
        "Prioridad BAJA",
        len(base_datos.obtener_reclamos_por_prioridad("BAJA")),
    )

    if total == 0:
        st.info("Aún no hay reclamos para mostrar estadísticas.")
        footer()
        return

    col_graf, col_tabla = st.columns(2)

    datos_cat = base_datos.contar_reclamos_por_categoria()
    df_cat = pd.DataFrame(datos_cat, columns=["Categoría", "Cantidad"])
    df_cat = df_cat.set_index("Categoría")

    with col_graf:
        st.markdown("### Por categoría")
        st.bar_chart(df_cat, color=["#E61B36"])
    with col_tabla:
        st.markdown("### Detalle")
        st.dataframe(df_cat.reset_index(), width="stretch", hide_index=True)

    st.markdown("### Por prioridad")
    serie = {
        "ALTA": len(base_datos.obtener_reclamos_por_prioridad("ALTA")),
        "MEDIA": len(base_datos.obtener_reclamos_por_prioridad("MEDIA")),
        "BAJA": len(base_datos.obtener_reclamos_por_prioridad("BAJA")),
    }
    df_pri = pd.DataFrame([{"Prioridad": k, "Cantidad": v} for k, v in serie.items()])
    st.bar_chart(df_pri.set_index("Prioridad"), color=["#E61B36"])

    st.markdown("## Resumen general")
    df_total = dataframe_reclamos()
    st.dataframe(df_total, width="stretch", hide_index=True)
    footer()