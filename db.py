import sqlite3
import os

def crear_base():
    os.makedirs("datos", exist_ok=True)
    conexion = sqlite3.connect("datos/reclamos.db")
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

def guardar_reclamo(comentario, categoria, prioridad):
    conexion = sqlite3.connect("datos/reclamos.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO historial_reclamos(comentario, categoria, prioridad)
        VALUES (?, ?, ?)
    """, (comentario, categoria, prioridad))
    conexion.commit()
    conexion.close()

def mostrar_historial():
    conexion = sqlite3.connect("datos/reclamos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM historial_reclamos")
    registros = cursor.fetchall()
    conexion.close()
    return registros
