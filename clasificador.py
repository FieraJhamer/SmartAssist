from motor_clasificacion import analizar_comentario


def clasificar_comentario(comentario):
    resultado = analizar_comentario(comentario)
    return resultado["categoria"], resultado["prioridad"]


if __name__ == "__main__":
    tests = [
        "No puedo ingresar al sistema",
        "La página está lenta",
        "Necesito un certificado",
        "Olvidé mi contraseña",
        "Quiero información sobre cursos",
        "La factura no coincide",
        "El producto llegó dañado",
        "Quiero dar de baja el servicio",
    ]
    for t in tests:
        cat, pri = clasificar_comentario(t)
        print(f"'{t}' -> {cat} / {pri}")
