import sqlite3
import pandas as pd

conexion = sqlite3.connect(
    "datos/reclamos.db"
)

df = pd.read_sql_query(
    "SELECT * FROM historial_reclamos",
    conexion
)

conexion.close()

print(df)