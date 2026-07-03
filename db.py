import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "datos", "reclamos.db")


def conectar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conexion = sqlite3.connect(DB_PATH)
    return conexion


def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_reclamos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comentario TEXT,
            categoria TEXT,
            prioridad TEXT
        )
    """)
    conexion.commit()
    conexion.close()
    print("Base creada correctamente")


def insertar(comentario, categoria, prioridad):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO historial_reclamos(comentario, categoria, prioridad)
        VALUES(?, ?, ?)
    """, (comentario, categoria, prioridad))
    conexion.commit()
    conexion.close()


def obtener_todos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM historial_reclamos")
    registros = cursor.fetchall()
    conexion.close()
    return registros


def mostrar_historial():
    return obtener_todos()


def guardar_reclamo(comentario, categoria, prioridad):
    insertar(comentario, categoria, prioridad)


def crear_base():
    crear_tabla()


def obtener_por_id(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM historial_reclamos WHERE id = ?", (id,))
    registro = cursor.fetchone()
    conexion.close()
    return registro


def actualizar(id, comentario, categoria, prioridad):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE historial_reclamos
        SET comentario = ?, categoria = ?, prioridad = ?
        WHERE id = ?
    """, (comentario, categoria, prioridad, id))
    conexion.commit()
    conexion.close()


def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM historial_reclamos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()


def obtener_por_categoria(categoria):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM historial_reclamos WHERE categoria = ?", (categoria,)
    )
    registros = cursor.fetchall()
    conexion.close()
    return registros


if __name__ == "__main__":
    crear_tabla()
