def generar_respuesta(categoria):
    respuestas = {
        "ERROR_ACCESO": "Verifique usuario y contraseña.",
        "RENDIMIENTO": "El problema de rendimiento será analizado por nuestro equipo.",
        "FACTURACION": "Su consulta fue enviada al área administrativa.",
        "DEVOLUCION": "Su solicitud de devolución ha sido registrada.",
        "CANCELACION": "Su solicitud de cancelación ha sido registrada. Un agente procesará su caso.",
        "CONSULTA": "Gracias por comunicarse con nosotros."
    }
    return respuestas[categoria]
