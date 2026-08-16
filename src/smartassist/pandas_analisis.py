"""Análisis de reclamos con Pandas: construcción de DataFrames y resúmenes."""
import pandas as pd

from smartassist import base_datos
from smartassist.config import PRIORIDADES

COLUMNAS_DF = [
    "ID",
    "Comentario",
    "Categoría",
    "Prioridad",
    "Calle",
    "Número",
    "Fecha",
]


def dataframe_reclamos():
    """Devuelve un DataFrame con todos los reclamos y la fecha tipada."""
    registros = base_datos.obtener_todos_reclamos()
    df = pd.DataFrame(registros, columns=COLUMNAS_DF)
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    return df


def estadisticas_a_texto():
    """Genera un texto legible con las estadísticas para alimentar a la IA."""
    registros = base_datos.obtener_todos_reclamos()
    if not registros:
        return "No hay reclamos registrados todavia."
    df = dataframe_reclamos()
    lineas = [f"Total de reclamos: {len(df)}"]
    lineas.append("\nPor categoria:")
    for cat, cant in base_datos.contar_reclamos_por_categoria():
        lineas.append(f"  {cat}: {cant}")
    lineas.append("\nPor prioridad:")
    for pri in PRIORIDADES:
        numero = len(base_datos.obtener_reclamos_por_prioridad(pri))
        lineas.append(f"  {pri}: {numero}")
    return "\n".join(lineas)