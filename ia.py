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

    Devuelve (es_valido, motivo) donde es_valido es un bool y motivo un texto
    explicativo. Ante cualquier error (por ejemplo, sin Ollama) devuelve
    (True, "") para no bloquear reclamos legítimos.
    """
    prompt = f"""
Eres un moderador de reclamos de la Municipalidad de la Ciudad de La Rioja.
Tu tarea es decidir si el siguiente comentario de un ciudadano describe un
problema municipal válido o si se trata de SPAM, publicidad, caracteres sin
sentido (gibberish) o mensajes incoherentes.

Comentario del ciudadano:
"{comentario}"

Respondí SOLO con "VALIDO" o "SPAM". No agregues ninguna otra palabra.
"""
    try:
        respuesta = consultar_ia(prompt).strip().upper()
        if "VALIDO" in respuesta:
            return True, ""
        if "SPAM" in respuesta:
            return False, "El comentario fue detectado como spam o sin sentido."
        return True, ""
    except Exception:
        return True, ""
