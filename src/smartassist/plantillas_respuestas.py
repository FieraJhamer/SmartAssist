"""Respuestas automáticas por categoría de reclamo."""

RESPUESTAS = {
    "AGUA_CLOACAS": "Su reclamo sobre el servicio de agua está siendo derivado a la Secretaría de Obras y Servicios. Una cuadrilla se comunicará para coordinar la revisión.",
    "RECOLECCION_RESIDUOS": "Registramos su pedido sobre recolección de residuos y lo derivamos a la Secretaría de Ambiente. La zona será atendida lo antes posible.",
    "ALUMBRADO": "Su reclamo por alumbrado público fue registrado. Se lo derivó al área eléctrica municipal para su reemplazo o reparación.",
    "SEGURIDAD": "Su reclamo de seguridad fue derivado a Defensa Civil y a la policía local. Se priorizará la asistencia en la zona.",
    "MANTENIMIENTO_VIAL": "Registramos el problema vial indicado. Se lo enviamos a la Dirección de Vialidad Municipal para su intervención.",
    "TRANSPORTE_PUBLICO": "Su reclamo sobre el transporte público fue enviado a la dirección de tránsito. Analizaremos frecuencias y recorridos.",
    "LIMPIEZA": "Registramos su solicitud de limpieza. Se coordinará con la cuadrilla de mantenimiento correspondiente.",
    "CONSULTA": "Gracias por su mensaje. Un agente municipal se comunicará pronto con la información solicitada.",
    "OTRO": "Su reclamo fue registrado. Un operador municipal lo revisará a la brevedad.",
}


def generar_respuesta(categoria):
    return RESPUESTAS.get(categoria, RESPUESTAS["OTRO"])