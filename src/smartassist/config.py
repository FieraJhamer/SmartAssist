"""Configuración central de SmartAssist.

Concentra rutas del proyecto, constantes del dominio (categorías, prioridades,
colores) y la carga de variables de entorno desde ``.env``.

Las rutas se resuelven en base a la ubicación de este módulo para que la app
funcione independientemente del directorio de trabajo (``cwd``).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent.parent

# --- Rutas del proyecto -----------------------------------------------------
RUTA_DATOS = RAIZ_PROYECTO / "datos"
RUTA_BASE_DATOS = RUTA_DATOS / "reclamos.db"
RUTA_STORAGE = RAIZ_PROYECTO / "storage" / "fotos"
RUTA_ASSETS = RAIZ_PROYECTO / "assets"
RUTA_ENV = RAIZ_PROYECTO / ".env"
LOGO_MUNICIPIO = RUTA_ASSETS / "Marca_LaRioja_Color.png"
FAVICON = RUTA_ASSETS / "favicon.png"

# --- Constantes del dominio -------------------------------------------------
CATEGORIAS = [
    "AGUA_CLOACAS",
    "RECOLECCION_RESIDUOS",
    "ALUMBRADO",
    "SEGURIDAD",
    "MANTENIMIENTO_VIAL",
    "TRANSPORTE_PUBLICO",
    "LIMPIEZA",
    "CONSULTA",
]

PRIORIDADES = ["ALTA", "MEDIA", "BAJA"]

COLOR_PRIORIDAD = {
    "ALTA": "#ef4444",
    "MEDIA": "#f59e0b",
    "BAJA": "#10b981",
}

COLOR_CATEGORIA = {
    "AGUA_CLOACAS": "#0ea5e9",
    "RECOLECCION_RESIDUOS": "#84cc16",
    "ALUMBRADO": "#facc15",
    "SEGURIDAD": "#f43f5e",
    "MANTENIMIENTO_VIAL": "#f97316",
    "TRANSPORTE_PUBLICO": "#8b5cf6",
    "LIMPIEZA": "#14b8a6",
    "CONSULTA": "#94a3b8",
}

# --- Variables de entorno ---------------------------------------------------
# Se cargan una sola vez al importar este módulo, garantizando que
# `os.environ` esté completo antes de que la autenticación lea sus valores.
load_dotenv(RUTA_ENV)