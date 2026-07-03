import db
import analizador
import respuestas


def mostrar_historial():
    registros = db.mostrar_historial()
    if not registros:
        print("No hay registros en el historial.")
        return
    print(f"\n{'ID':<4} {'Comentario':<40} {'Categoría':<15} {'Prioridad':<10}")
    print("-" * 75)
    for r in registros:
        print(f"{r[0]:<4} {r[1][:38]:<40} {r[2]:<15} {r[3]:<10}")
    print()


def menu():
    print("\n=== SMARTASSIST AI ANALYST ===")
    print("1. Analizar un comentario")
    print("2. Ver historial completo")
    print("3. Ver por categoría")
    print("4. Editar reclamo")
    print("5. Eliminar reclamo")
    print("6. Salir \n")
    return input("Seleccione una opción: ").strip()


def main():
    db.crear_tabla()

    while True:
        opcion = menu()

        if opcion == "1":
            comentario = input("\nIngrese el comentario: ").strip()
            if not comentario:
                print("Comentario vacío, intente de nuevo.")
                continue

            categoria, prioridad = analizador.clasificar(comentario)
            respuesta = respuestas.generar_respuesta(categoria)

            db.insertar(comentario, categoria, prioridad)

            print(f"\n--- Resultado ---")
            print(f"Comentario:  {comentario}")
            print(f"Categoría:   {categoria}")
            print(f"Prioridad:   {prioridad}")
            print(f"Respuesta:   {respuesta}")
            print("------------------")

        elif opcion == "2":
            mostrar_historial()

        elif opcion == "3":
            categoria = input("\nCategoría (ACCESO, CONSULTA, DOCUMENTACION, OTRO): ").strip().upper()
            registros = db.obtener_por_categoria(categoria)
            if not registros:
                print(f"No hay registros en la categoría '{categoria}'.")
                continue
            print(f"\n{'ID':<4} {'Comentario':<40} {'Prioridad':<10}")
            print("-" * 60)
            for r in registros:
                print(f"{r[0]:<4} {r[1][:38]:<40} {r[3]:<10}")
            print()

        elif opcion == "4":
            mostrar_historial()
            id_editar = input("\nID del reclamo a editar: ").strip()
            if not id_editar.isdigit():
                print("ID inválido.")
                continue
            registro = db.obtener_por_id(int(id_editar))
            if not registro:
                print("No se encontró un reclamo con ese ID.")
                continue
            print(f"Editando: {registro[1][:40]} | {registro[2]} | {registro[3]}")
            nuevo_comentario = input("Nuevo comentario (Enter para mantener): ").strip()
            if not nuevo_comentario:
                nuevo_comentario = registro[1]
            nueva_categoria = input(f"Nueva categoría (Enter para mantener '{registro[2]}'): ").strip().upper()
            if not nueva_categoria:
                nueva_categoria = registro[2]
            nueva_prioridad = input(f"Nueva prioridad (Enter para mantener '{registro[3]}'): ").strip().upper()
            if not nueva_prioridad:
                nueva_prioridad = registro[3]
            db.actualizar(int(id_editar), nuevo_comentario, nueva_categoria, nueva_prioridad)
            print("Reclamo actualizado correctamente.")

        elif opcion == "5":
            mostrar_historial()
            id_eliminar = input("\nID del reclamo a eliminar: ").strip()
            if not id_eliminar.isdigit():
                print("ID inválido.")
                continue
            registro = db.obtener_por_id(int(id_eliminar))
            if not registro:
                print("No se encontró un reclamo con ese ID.")
                continue
            print(f"Reclamo: {registro[1][:40]} | {registro[2]} | {registro[3]}")
            confirmar = input("¿Eliminar este reclamo? (s/n): ").strip().lower()
            if confirmar == "s":
                db.eliminar(int(id_eliminar))
                print("Reclamo eliminado correctamente.")
            else:
                print("Eliminación cancelada.")

        elif opcion == "6":
            print("Saliendo de SmartAssist...")
            break

        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()
