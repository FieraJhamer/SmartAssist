from datetime import datetime

import streamlit as st
import pandas as pd

import base_datos
import clasificador
import plantillas_respuestas
import ia
import storage_imagenes
import validaciones

import os

logo_municipio = os.path.join(os.path.dirname(__file__), "assets", "Marca_LaRioja_Color.png")
favicon = os.path.join(os.path.dirname(__file__), "assets", "favicon.png")

st.set_page_config(
    page_title="Reclamos Ciudadanos · La Rioja",
    page_icon=favicon if os.path.exists(favicon) else "🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CATEGORIAS = [
    "AGUA_CLOACAS",
    "RECOLECCION_RESIDUOS",
    "ALUMBRADO",
    "SEGURIDAD",
    "MANTENIMIENTO_VIAL",
    "TRANSPORTE_PUBLICO",
    "LIMPIEZA",
    "CONSULTA",
]

PRIORIDADES = ["ALTA", "MEDIA", "BAJA"]

COLOR_PRIORIDAD = {
    "ALTA": "#ef4444",
    "MEDIA": "#f59e0b",
    "BAJA": "#10b981",
}

COLOR_CATEGORIA = {
    "AGUA_CLOACAS": "#0ea5e9",
    "RECOLECCION_RESIDUOS": "#84cc16",
    "ALUMBRADO": "#facc15",
    "SEGURIDAD": "#f43f5e",
    "MANTENIMIENTO_VIAL": "#f97316",
    "TRANSPORTE_PUBLICO": "#8b5cf6",
    "LIMPIEZA": "#14b8a6",
    "CONSULTA": "#94a3b8",
}


def inyectar_css():
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )


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


def dataframe_reclamos():
    registros = base_datos.obtener_todos_reclamos()
    df = pd.DataFrame(
        registros,
        columns=["ID", "Comentario", "Categoría", "Prioridad", "Calle", "Número"],
    )
    return df


def etiqueta_reclamo(fila):
    comentario = fila["Comentario"]
    if len(comentario) > 45:
        comentario = comentario[:45] + "…"
    return f"#{int(fila['ID'])} · {comentario}"


def estadisticas_a_texto():
    registros = base_datos.obtener_todos_reclamos()
    if not registros:
        return "No hay reclamos registrados todavia."
    df = dataframe_reclamos()
    lineas = [f"Total de reclamos: {len(df)}"]
    lineas.append("\nPor categoria:")
    for cat, cant in base_datos.contar_reclamos_por_categoria():
        lineas.append(f"  {cat}: {cant}")
    lineas.append("\nPor prioridad:")
    for pri in PRIORIDADES:
        numero = len(base_datos.obtener_reclamos_por_prioridad(pri))
        lineas.append(f"  {pri}: {numero}")
    return "\n".join(lineas)


def pagina_nuevo_reclamo():
    encabezado("Reclamos Ciudadanos", "Reporta un problema del municipio y nosotros lo gestionamos")

    st.markdown("## Nuevo reclamo")
    st.caption("Contanos qué está pasando y el sistema lo clasificará por categoría y prioridad.")

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
        with st.spinner("Verificando que el reclamo sea válido…"):
            es_valido, motivo = ia.verificar_comentario_ia(comentario)
        if not es_valido:
            st.error(f"Reclamo no registrado: {motivo}")
            return
        categoria, prioridad = clasificador.clasificar_comentario(comentario)
        respuesta = plantillas_respuestas.generar_respuesta(categoria)
        id_reclamo = base_datos.insertar_reclamo(
            comentario, categoria, prioridad, calle, numero
        )

        guardadas, rechazadas = storage_imagenes.guardar_imagenes(fotos, id_reclamo)

        st.markdown("### Resultado")
        tarjeta_resultado(categoria, prioridad, respuesta)
        if guardadas:
            st.success(
                f"Reclamo registrado correctamente con {guardadas} foto(s)."
            )
        else:
            st.success("Reclamo registrado correctamente en la base de datos.")
        for nombre, motivo in rechazadas:
            st.warning(f"{nombre}: {motivo}")
    footer()


def pagina_historial():
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

    st.dataframe(df, width="stretch", hide_index=True)

    st.markdown("## Fotos del reclamo")
    st.caption("Imágenes subidas en el reclamo seleccionado.")
    ids = [int(i) for i in df["ID"]]
    etiquetas = {fila["ID"]: etiqueta_reclamo(fila) for _, fila in df.iterrows()}
    id_fotos = st.selectbox(
        "Seleccionar reclamo para ver fotos",
        ids,
        key="fotos_reclamo",
        format_func=lambda i: etiquetas[i],
    )
    nombres_fotos = base_datos.obtener_imagenes_reclamo(int(id_fotos))
    if nombres_fotos:
        columnas = st.columns(min(len(nombres_fotos), 3))
        for i, nombre in enumerate(nombres_fotos):
            ruta = storage_imagenes.ruta_archivo(int(id_fotos), nombre)
            with columnas[i % 3]:
                st.image(ruta, width="stretch")
    else:
        st.info("Este reclamo no tiene fotos adjuntas.")

    st.markdown("## Editar reclamo")
    id_editar = st.selectbox(
        "Seleccionar reclamo",
        ids,
        key="editar_id",
        format_func=lambda i: etiquetas[i],
    )
    registro = base_datos.obtener_reclamo_por_id(int(id_editar))
    if registro:
        nuevo_comentario = st.text_input("Comentario", value=registro[1], key="edit_com")
        nueva_categoria = st.selectbox(
            "Categoría",
            CATEGORIAS,
            index=CATEGORIAS.index(registro[2]) if registro[2] in CATEGORIAS else 0,
            key="edit_cat",
        )
        nueva_prioridad = st.selectbox(
            "Prioridad",
            PRIORIDADES,
            index=PRIORIDADES.index(registro[3]) if registro[3] in PRIORIDADES else 0,
            key="edit_pri",
        )
        nueva_calle = st.text_input("Calle", value=registro[4] or "", key="edit_calle")
        nuevo_numero = st.text_input("Número", value=registro[5] or "", key="edit_num")
        if st.button("Guardar cambios", key="btn_editar"):
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
                int(id_editar),
                nuevo_comentario.strip(),
                nueva_categoria,
                nueva_prioridad,
                nueva_calle.strip(),
                nuevo_numero.strip(),
            )
            st.success("Reclamo actualizado correctamente.")

    st.markdown("## Eliminar reclamo")
    id_eliminar = st.selectbox(
        "Seleccionar reclamo a eliminar",
        ids,
        key="borrar_id",
        format_func=lambda i: etiquetas[i],
    )
    if st.button("Eliminar reclamo", type="primary", key="btn_eliminar"):
        storage_imagenes.eliminar_fotos_reclamo(int(id_eliminar))
        base_datos.eliminar_reclamo(int(id_eliminar))
        st.success(f"Reclamo #{id_eliminar} eliminado (junto con sus fotos).")
    footer()


def pagina_estadisticas():
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


def pagina_analisis_ia():
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


def _navegar_a(nombre):
    st.session_state.pagina_actual = nombre


def main():
    base_datos.crear_tabla()
    inyectar_css()

    if os.path.exists(logo_municipio):
        with open(logo_municipio, "rb") as f:
            import base64
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

    if "pagina_actual" not in st.session_state:
        st.session_state.pagina_actual = "Nuevo reclamo"

    # Secciones
    for nombre in ["Nuevo reclamo", "Historial", "Estadísticas", "Análisis Inteligente"]:
        activo = st.session_state.pagina_actual == nombre
        st.sidebar.button(
            nombre,
            key=f"nav_{nombre}",
            type="primary" if activo else "secondary",
            width="stretch",
            on_click=_navegar_a,
            args=(nombre,),
        )

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
        pagina_nuevo_reclamo()
    elif pagina == "Historial":
        pagina_historial()
    elif pagina == "Estadísticas":
        pagina_estadisticas()
    else:
        pagina_analisis_ia()


if __name__ == "__main__":
    main()
