"""Ubicación aproximada de los reclamos en Google Maps."""
from urllib.parse import quote

import streamlit as st


def url_mapa_reclamo(calle, numero):
    direccion = f"{calle} {numero}".strip()
    if not direccion:
        return None
    consulta = f"{direccion}, La Rioja, Argentina"
    return "https://maps.google.com/maps?q=" + quote(consulta) + "&output=embed&z=17"


def mostrar_mapa(calle, numero, altura=360):
    url = url_mapa_reclamo(calle, numero)
    if not url:
        st.info("Este reclamo no tiene dirección cargada.")
        return
    st.caption(f"{calle} {numero}".strip() + " · La Rioja, Argentina")
    with st.container(border=True):
        st.iframe(url, width="stretch", height=altura)