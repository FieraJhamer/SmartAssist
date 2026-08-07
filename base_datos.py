import sqlite3
import os

RUTA_BASE_DATOS = os.path.join(os.path.dirname(__file__), "datos", "reclamos.db")


def conectar():
    os.makedirs(os.path.dirname(RUTA_BASE_DATOS), exist_ok=True)
    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    return conexion


def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_reclamos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comentario TEXT,
            categoria TEXT,
            prioridad TEXT,
            calle TEXT,
            numero TEXT
        )
    """)
    columnas = [fila[1] for fila in cursor.execute("PRAGMA table_info(historial_reclamos)")]
    if "calle" not in columnas:
        cursor.execute("ALTER TABLE historial_reclamos ADD COLUMN calle TEXT")
    if "numero" not in columnas:
        cursor.execute("ALTER TABLE historial_reclamos ADD COLUMN numero TEXT")
    conexion.commit()
    conexion.close()
    print("Base creada correctamente")


def insertar_reclamo(comentario, categoria, prioridad, calle="", numero=""):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO historial_reclamos(comentario, categoria, prioridad, calle, numero)
        VALUES(?, ?, ?, ?, ?)
    """, (comentario, categoria, prioridad, calle, numero))
    conexion.commit()
    conexion.close()


def obtener_todos_reclamos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM historial_reclamos")
    registros = cursor.fetchall()
    conexion.close()
    return registros


def mostrar_historial():
    return obtener_todos_reclamos()


def guardar_reclamo(comentario, categoria, prioridad):
    insertar_reclamo(comentario, categoria, prioridad)


def crear_base():
    crear_tabla()


def obtener_reclamo_por_id(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM historial_reclamos WHERE id = ?", (id,))
    registro = cursor.fetchone()
    conexion.close()
    return registro


def actualizar_reclamo(id, comentario, categoria, prioridad, calle="", numero=""):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE historial_reclamos
        SET comentario = ?, categoria = ?, prioridad = ?, calle = ?, numero = ?
        WHERE id = ?
    """, (comentario, categoria, prioridad, calle, numero, id))
    conexion.commit()
    conexion.close()


def eliminar_reclamo(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM historial_reclamos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()


def obtener_reclamos_por_categoria(categoria):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM historial_reclamos WHERE categoria = ?", (categoria,)
    )
    registros = cursor.fetchall()
    conexion.close()
    return registros


def contar_total_reclamos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM historial_reclamos")
    cantidad = cursor.fetchone()[0]
    conexion.close()
    return cantidad


def contar_reclamos_por_categoria():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT categoria, COUNT(*)
        FROM historial_reclamos
        GROUP BY categoria
    """)
    datos = cursor.fetchall()
    conexion.close()
    return datos


def obtener_reclamos_por_prioridad(prioridad):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM historial_reclamos WHERE prioridad = ?", (prioridad,)
    )
    registros = cursor.fetchall()
    conexion.close()
    return registros


if __name__ == "__main__":
    crear_tabla()
