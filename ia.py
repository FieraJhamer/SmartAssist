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


def resumir_comentario_ia(comentario):
    prompt = f"""
Resume el siguiente reclamo ciudadano en una o dos frases:

"{comentario}"
"""
    return consultar_ia(prompt)


def redactar_respuesta_ia(comentario, categoria):
    prompt = f"""
Un ciudadano realizo el siguiente reclamo municipal clasificado como {categoria}:

"{comentario}"

Redacta una respuesta cordial y profesional dirigida al ciudadano, en español,
sin saludo formal de cierre largo.
"""
    return consultar_ia(prompt)


if __name__ == "__main__":
    print(consultar_ia("Hola, decis hola."))
