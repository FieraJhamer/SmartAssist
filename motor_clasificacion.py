import unicodedata


def _normalizar(texto):
    texto = texto.lower()
    sin_acentos = unicodedata.normalize("NFD", texto)
    sin_acentos = "".join(c for c in sin_acentos if unicodedata.category(c) != "Mn")
    return sin_acentos


def analizar_comentario(texto):
    texto_normalizado = _normalizar(texto)

    if any(p in texto_normalizado for p in ("agua", "cloaca", "perdida", "filtra", "sipotencia", "corte de agua")):
        categoria = "AGUA_CLOACAS"
        prioridad = "ALTA"

    elif any(p in texto_normalizado for p in ("basura", "basural", "residuo", "contenedor", "recoleccion")):
        categoria = "RECOLECCION_RESIDUOS"
        prioridad = "ALTA"

    elif any(p in texto_normalizado for p in ("alumbrado", "luminaria", "farol", "luz", "iluminacion", "sin luz", "apagad")):
        categoria = "ALUMBRADO"
        prioridad = "ALTA"

    elif any(p in texto_normalizado for p in ("seguridad", "robo", "peligro", "defensa civil", "inseguridad", "crimen")):
        categoria = "SEGURIDAD"
        prioridad = "ALTA"

    elif any(p in texto_normalizado for p in ("bache", "vereda", "calle", "asfalto", "senalizacion", "senal", "camino", "riploid")):
        categoria = "MANTENIMIENTO_VIAL"
        prioridad = "MEDIA"

    elif any(p in texto_normalizado for p in ("colectivo", "transporte", "micro", "omnibus", "parada", "recorrido", "buses")):
        categoria = "TRANSPORTE_PUBLICO"
        prioridad = "MEDIA"

    elif any(p in texto_normalizado for p in ("poda", "limpieza", "desmalezar", "hierba", "baldio", "escombro", "maleza")):
        categoria = "LIMPIEZA"
        prioridad = "MEDIA"

    else:
        categoria = "CONSULTA"
        prioridad = "BAJA"

    return {
        "comentario": texto,
        "categoria": categoria,
        "prioridad": prioridad,
    }