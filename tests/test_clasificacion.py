"""Pruebas de la clasificación de reclamos."""
import pytest

from smartassist import clasificador


@pytest.mark.parametrize(
    "texto,categoria_esperada,prioridad_esperada",
    [
        ("No hay agua en mi barrio desde hace dos días", "AGUA_CLOACAS", "ALTA"),
        ("La plaza está llena de basura y contenedores desbordados", "RECOLECCION_RESIDUOS", "ALTA"),
        ("Se cortó el alumbrado público en toda la cuadra", "ALUMBRADO", "ALTA"),
        ("Hubo un robo y hay árboles en peligro de caerse", "SEGURIDAD", "ALTA"),
        ("La calle tiene baches y la señalización está borrada", "MANTENIMIENTO_VIAL", "MEDIA"),
        ("El colectivo de la línea 3 tarda una hora en pasar", "TRANSPORTE_PUBLICO", "MEDIA"),
        ("El terreno baldío tiene maleza y escombros acumulados", "LIMPIEZA", "MEDIA"),
        ("Quiero información sobre los turnos municipales", "CONSULTA", "BAJA"),
    ],
)
def test_clasificacion_basica(texto, categoria_esperada, prioridad_esperada):
    categoria, prioridad = clasificador.clasificar_comentario(texto)
    assert categoria == categoria_esperada
    assert prioridad == prioridad_esperada


@pytest.mark.parametrize(
    "texto,categoria_esperada",
    [
        ("NO HAY AGUA EN MI BARRIO", "AGUA_CLOACAS"),
        ("se filtra agua por la vereda", "AGUA_CLOACAS"),
        ("CorTaron el aLUMbrado", "ALUMBRADO"),
        ("háy báches en la calle", "MANTENIMIENTO_VIAL"),
        ("BASURA en los contenedores", "RECOLECCION_RESIDUOS"),
        ("colectivo con demora", "TRANSPORTE_PUBLICO"),
    ],
)
def test_clasificacion_case_y_acentos(texto, categoria_esperada):
    """La clasificación no distingue mayúsculas ni acentos."""
    categoria, _ = clasificador.clasificar_comentario(texto)
    assert categoria == categoria_esperada


def test_comentario_sin_coincidencias_es_consulta():
    categoria, prioridad = clasificador.clasificar_comentario("Hola, cómo estás")
    assert categoria == "CONSULTA"
    assert prioridad == "BAJA"