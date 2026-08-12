import ollama

MODELO = "gemma3:1b"


def consultar_ia(prompt, modelo=MODELO):
    respuesta = ollama.chat(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
    )
    return respuesta["message"]["content"]


def generar_informe_ia(estadisticas_texto, rol="analista de datos", max_lineas=None):
    extra = f" El informe debe tener como maximo {max_lineas} lineas." if max_lineas else ""
    prompt = f"""
Actuas como {rol} de la Municipalidad de la Ciudad de La Rioja.

Estas son las estadisticas de reclamos ciudadanos:
{estadisticas_texto}

Elabora un informe indicando:
- reclamo predominante;
- prioridad predominante;
- posibles causas;
- tres recomendaciones.{extra}
"""
    return consultar_ia(prompt)


def generar_email_ia(estadisticas_texto):
    prompt = f"""
Actuas como analista de la Municipalidad de la Ciudad de La Rioja.
Redacta un correo electronico dirigido a la gerencia municipal explicando el
estado de los reclamos ciudadanos basandote en estas estadisticas:

{estadisticas_texto}

Incluye asunto, saludo, cuerpo y despedida.
"""
    return consultar_ia(prompt)


def verificar_comentario_ia(comentario):
    """Analiza si un comentario de reclamo es válido o es spam/sin sentido.

    El criterio es permisivo: se acepta cualquier problema real que pueda
    tener una ciudad.
    Solo se rechaza si es inequívocamente SPAM, publicidad sin relación con
    el municipio, o caracteres sin sentido (gibberish).

    Devuelve (es_valido, motivo) donde es_valido es un bool y motivo un texto
    explicativo. Ante cualquier error (por ejemplo, sin Ollama) devuelve
    (True, "") para no bloquear reclamos legítimos.
    """
    prompt = f"""
Eres un moderador permisivo de reclamos de la Municipalidad de la Ciudad.
Solo marcás como SPAM un mensaje que sean 
CLARAMENTE enlaces promocionales o caracteres sin sentido (gibberish).

Todo lo demás se considera VALIDO, aunque el problema esté mal redactado,
falten signos de puntuación o la categoría no se entienda bien. Aceptá
cualquier problema real de una ciudad.

Comentario del ciudadano:
"{comentario}"

¿Es SPAM inequívoco o caracteres sin sentido? Respondé SOLO con "VALIDO" o
"SPAM". Cuando tengas dudas, respondé "VALIDO". No agregues ninguna otra
palabra.
"""
    try:
        respuesta = consultar_ia(prompt).strip().upper()
        if "NO ES SPAM" in respuesta or "NO SPAM" in respuesta or "NO ES UN SPAM" in respuesta:
            return True, ""
        if "VALIDO" in respuesta:
            return True, ""
        if "SPAM" in respuesta:
            return False, "El comentario fue detectado como spam o sin sentido."
        return True, ""
    except Exception:
        return True, ""


def sugerir_prioridad_ia(comentario):
    """Pide a la IA una prioridad sugerida para un reclamo.

    Devuelve (prioridad, detalle) donde prioridad es "ALTA", "MEDIA", "BAJA"
    o None si la IA no responde algo interpretable (por ejemplo, sin Ollama).
    """
    prompt = f"""
Eres un evaluador de reclamos de la Municipalidad de la Ciudad de La Rioja.
Dado el siguiente comentario de un ciudadano, indicá qué tan urgente es
atender el problema.

Comentario:
"{comentario}"

Considerá riesgo a personas, daño a la propiedad, corte de servicios
esenciales (agua, luz, gas) y gravedad del problema.

Respondé SOLO con una palabra: ALTA, MEDIA o BAJA.
"""
    try:
        respuesta = consultar_ia(prompt).strip().upper()
        for nivel in ("ALTA", "MEDIA", "BAJA"):
            if nivel in respuesta:
                return nivel, ""
        return None, "La IA no devolvió un nivel de prioridad válido."
    except Exception as e:
        return None, f"Ollama no disponible: {e}"


def combinar_prioridades(prioridad_reglas, prioridad_ia):
    """Combina la prioridad de las reglas con la sugerida por IA.

    Devuelve (prioridad_final, origen) donde origen indica qué fuente
    determinó el valor ("reglas", "ia" o "ambas"). Se toma siempre el nivel
    de mayor severidad para no subestimar un reclamo grave.
    """
    severidad = {"ALTA": 3, "MEDIA": 2, "BAJA": 1}
    if prioridad_ia is None:
        return prioridad_reglas, "reglas"

    if severidad.get(prioridad_ia, 0) > severidad.get(prioridad_reglas, 0):
        return prioridad_ia, "ia"
    if severidad.get(prioridad_ia, 0) < severidad.get(prioridad_reglas, 0):
        return prioridad_reglas, "reglas"
    return prioridad_reglas, "ambas"
