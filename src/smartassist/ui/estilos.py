"""Estilos y helpers visuales de la interfaz web (Marca La Rioja)."""
from datetime import datetime

import streamlit as st

from smartassist.config import COLOR_CATEGORIA, COLOR_PRIORIDAD

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --color-primary: #E61B36;
    --color-primary-hover: #C4102A;
    --color-primary-light: #FFF0F2;
    --color-bg-main: #FFFFFF;
    --color-surface: #FFFFFF;
    --color-text-main: #1A0B0E;
    --color-text-muted: #524346;
    --color-border: #E5D8DA;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --shadow-sm: 0 2px 8px rgba(26, 11, 14, 0.04);
    --shadow-md: 0 6px 20px rgba(26, 11, 14, 0.06);
    --shadow-brand: 0 8px 24px rgba(230, 27, 54, 0.18);
}

.stApp {
    background: var(--color-bg-main);
    color: var(--color-text-main);
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}

[data-testid="stHeader"] { background: transparent; }

[data-testid="stSidebar"] {
    background: #FFFDFD;
    border-right: 1px solid var(--color-border);
}
[data-testid="stSidebar"] [data-testid="stMarkdown"] p {
    color: var(--color-text-muted);
}

.sidebar-brand { text-align: center; padding: 0.25rem 0 0.5rem 0; }
.sidebar-brand img { display: block; margin: 0 auto; margin-bottom: 1rem; width: 280px; height: auto; }
.sidebar-nombre {
    font-family: 'Montserrat', system-ui, sans-serif;
    font-weight: 800;
    font-size: 1.2rem;
    color: var(--color-text-main);
    margin: 0.6rem 0 0.1rem 0;
    letter-spacing: -0.01em;
}
.sidebar-sub {
    font-family: 'Montserrat', system-ui, sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--color-primary);
    margin: 0;
    letter-spacing: 0.02em;
}
.sidebar-muni {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    font-weight: 500;
    font-size: 0.72rem;
    color: var(--color-text-muted);
    margin: 0.15rem 0 0 0;
}

.block-container { padding-top: 2rem; padding-bottom: 3rem; }

h1, h2, h3, h4 {
    font-family: 'Montserrat', system-ui, sans-serif;
    color: var(--color-text-main) !important;
    letter-spacing: -0.02em;
}

h1 { font-weight: 800; font-size: 2.4rem; line-height: 1.15; }

h2 {
    font-weight: 700;
    font-size: 1.7rem;
    border-bottom: 4px solid var(--color-primary);
    border-radius: 2px;
    padding-bottom: 0.4rem;
    width: fit-content;
}

h3 { font-weight: 700; font-size: 1.25rem; }

.stMarkdown p, .stCaption, .stText { color: var(--color-text-main); }

.tarjeta {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.4rem;
    margin: 0.5rem 0 1rem 0;
    box-shadow: var(--shadow-sm);
}

.tarjeta-titulo {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--color-text-muted);
    margin: -0.5rem 0 1.5rem 0;
}

.brand-accent {
    width: 4px;
    height: 36px;
    background: var(--color-primary);
    border-radius: 2px;
    margin-right: 0.75rem;
    flex: none;
}

.brand-title-row { display: flex; align-items: center; margin-bottom: 0.25rem; }
.brand-title-row h1 { margin: 0; }

.badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}

.badge-pri { color: #fff; box-shadow: var(--shadow-sm); }
.badge-cat {
    background: var(--color-primary-light);
    color: var(--color-primary-hover);
    border: 1px solid rgba(230, 27, 54, 0.25);
}

.muted { color: var(--color-text-muted); }

div[data-testid="stMetric"] {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: 1rem 1.2rem;
    box-shadow: var(--shadow-sm);
}
div[data-testid="stMetricValue"] { color: var(--color-text-main); font-weight: 800; }
div[data-testid="stMetricLabel"] {
    color: var(--color-text-muted);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stButton > button {
    border: 2px solid var(--color-primary);
    background: var(--color-surface);
    color: var(--color-primary);
    border-radius: var(--radius-sm);
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    background: var(--color-primary-light);
    border-color: var(--color-primary-hover);
    color: var(--color-primary-hover);
}
.stButton > button[kind="primary"] {
    background: var(--color-primary);
    color: #fff;
    border: none;
    box-shadow: 0 4px 14px rgba(230, 27, 54, 0.25);
}
.stButton > button[kind="primary"]:hover {
    background: var(--color-primary-hover);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(230, 27, 54, 0.35);
}

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
}

.stTextArea textarea,
.stTextInput input,
.stSelectbox [data-baseweb="select"] > div {
    background-color: var(--color-surface);
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-sm);
    color: var(--color-text-main);
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.respuesta {
    border-left: 4px solid var(--color-primary);
    background: var(--color-primary-light);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    padding: 0.9rem 1.1rem;
}
.respuesta p { margin: 0; color: var(--color-text-main); }

hr { border-color: var(--color-border) !important; }

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: 999px; }
::-webkit-scrollbar-track { background: transparent; }
</style>
"""

_MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def inyectar_css():
    st.markdown(CSS, unsafe_allow_html=True)


def footer():
    st.markdown("---")
    st.caption(
        f"Municipalidad de La Rioja · Plataforma de Reclamos Ciudadanos · {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )


def encabezado(titulo, subtitulo):
    st.markdown(
        f"""
        <div class="brand-title-row">
            <div class="brand-accent"></div>
            <h1>{titulo}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="tarjeta-titulo">{subtitulo}</div>', unsafe_allow_html=True)


def tarjeta_resultado(categoria, prioridad, respuesta):
    pri_color = COLOR_PRIORIDAD.get(prioridad, "#94a3b8")
    st.markdown(
        f"""
        <div class="tarjeta">
            <span class="badge badge-pri" style="background:{pri_color};">{prioridad}</span>
            &nbsp;
            <span class="badge badge-cat">{categoria}</span>
            <div style="margin-top:1rem;"></div>
            <div class="respuesta"><p>{respuesta}</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def fecha_formateada(fecha):
    """Convierte 'YYYY-MM-DD HH:MM:SS' a '12 de Julio de 2026 | 20:45 hs'."""
    try:
        dt = datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return fecha or ""
    return f"{dt.day} de {_MESES[dt.month - 1]} de {dt.year} | {dt.strftime('%H:%M')} hs"


def etiqueta_prioridad_html(prioridad):
    color = COLOR_PRIORIDAD.get(prioridad, "#94a3b8")
    return f'<span class="badge badge-pri" style="background:{color};">{prioridad}</span>'


def etiqueta_categoria_html(categoria):
    color = COLOR_CATEGORIA.get(categoria, "#94a3b8")
    return (
        f'<span class="badge badge-cat" style="background:{color};color:#fff;'
        f'border-color:transparent;">{categoria}</span>'
    )