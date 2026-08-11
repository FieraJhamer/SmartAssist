import re

MAX_LONGITUD_COMENTARIO = 500
MAX_LONGITUD_CALLE = 80
MAX_LONGITUD_NUMERO = 10

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

_PATRON_CALLE = re.compile(
    r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ\s.,'\"-]{2,80}$"
)


def validar_comentario(comentario):
    comentario = comentario.strip()
    if not comentario:
        return False, "Ingrese un comentario."
    if len(comentario) > MAX_LONGITUD_COMENTARIO:
        return (
            False,
            f"El comentario no puede superar los {MAX_LONGITUD_COMENTARIO} caracteres.",
        )
    return True, ""


def validar_calle(calle):
    calle = calle.strip()
    if not calle:
        return False, "Ingrese la calle."
    if not _PATRON_CALLE.fullmatch(calle):
        return (
            False,
            "La calle contiene caracteres no permitidos (solo letras, números, espacios y . , ' -).",
        )
    return True, ""


def validar_numero(numero):
    numero = numero.strip()
    if not numero:
        return False, "Ingrese el número de la dirección."
    if not numero.isdigit():
        return False, "El número de la calle debe ser numérico (sin letras)."
    if len(numero) > MAX_LONGITUD_NUMERO:
        return (
            False,
            f"El número no puede superar los {MAX_LONGITUD_NUMERO} dígitos.",
        )
    return True, ""


def validar_categoria(categoria):
    categoria = categoria.strip().upper()
    if categoria not in CATEGORIAS:
        return False, f"Categoría inválida. Válidas: {', '.join(CATEGORIAS)}."
    return True, ""


def validar_prioridad(prioridad):
    prioridad = prioridad.strip().upper()
    if prioridad not in PRIORIDADES:
        return False, f"Prioridad inválida. Válidas: {', '.join(PRIORIDADES)}."
    return True, ""
