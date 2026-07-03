RESPUESTAS = {
    "ERROR_ACCESO": "Verifique sus credenciales o solicite un reinicio de contraseña al administrador.",
    "RENDIMIENTO": "Estamos revisando los reportes de lentitud. Le informaremos cuando esté solucionado.",
    "FACTURACION": "Su consulta de facturación ha sido derivada al área contable. Recibirá novedades en breve.",
    "DEVOLUCION": "Generamos un turno para devolución. Un asesor se comunicará para coordinar el proceso.",
    "CANCELACION": "Su solicitud de cancelación fue registrada. Un operador lo contactará para finalizar el trámite.",
    "CONSULTA": "Un asistente se comunicará pronto para brindarle la información solicitada.",
    "OTRO": "Su comentario ha sido registrado. Un operador lo revisará a la brevedad.",
}


def generar_respuesta(categoria):
    return RESPUESTAS.get(categoria, RESPUESTAS["OTRO"])


if __name__ == "__main__":
    for cat in RESPUESTAS:
        print(f"{cat}: {generar_respuesta(cat)}")
