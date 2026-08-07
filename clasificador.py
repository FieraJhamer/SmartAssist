from motor_clasificacion import analizar_comentario


def clasificar_comentario(comentario):
    resultado = analizar_comentario(comentario)
    return resultado["categoria"], resultado["prioridad"]


if __name__ == "__main__":
    tests = [
        "No hay agua en mi barrio desde hace dos días",
        "La plaza está llena de basura y contenedores desbordados",
        "Se cortó el alumbrado público en la cuadra",
        "Hubo un robo y hay árboles en peligro de caerse",
        "La calle tiene baches y la señalización está borrada",
        "El colectivo de la línea 3 tarda una hora en pasar",
        "El terreno baldío tiene maleza y escombros",
        "Quiero información sobre turnos municipales",
    ]
    for t in tests:
        cat, pri = clasificar_comentario(t)
        print(f"'{t}' -> {cat} / {pri}")
