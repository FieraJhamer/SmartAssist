from analizador import analizar_comentario
from respuestas import generar_respuesta
from db import crear_base, guardar_reclamo, mostrar_historial

crear_base()

while True:
    print("\n=== MENU PRINCIPAL ===")
    print("1 - Nuevo reclamo")
    print("2 - Ver historial")
    print("0 - Salir")

    opcion = input("\nSeleccione una opción: ")

    if opcion == "1":
        comentario = input("Ingrese comentario: ")
        resultado = analizar_comentario(comentario)
        respuesta = generar_respuesta(resultado["categoria"])
        guardar_reclamo(comentario, resultado["categoria"], resultado["prioridad"])

        print()
        print("Categoría:", resultado["categoria"])
        print("Prioridad:", resultado["prioridad"])
        print("Respuesta:", respuesta)

    elif opcion == "2":
        historial = mostrar_historial()
        print("\n=== HISTORIAL ===")
        print(f"{'ID':<4} {'Comentario':<40} {'Categoría':<16} {'Prioridad':<10}")
        print("-------------------      -----------------------------------------------------")
        for fila in historial:
            print(f"{fila[0]:<4} {fila[1]:<40} {fila[2]:<16} {fila[3]:<10}")
        print("\n")

    elif opcion == "0":
        print("Saliendo de SmartAssist.")
        break

    else:
        print("Opción no válida.")
