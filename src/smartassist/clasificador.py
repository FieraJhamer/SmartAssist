"""Wrapper del clasificador: expone una función simple (categoria, prioridad)."""
from smartassist.motor_clasificacion import analizar_comentario


def clasificar_comentario(comentario):
    resultado = analizar_comentario(comentario)
    return resultado["categoria"], resultado["prioridad"]