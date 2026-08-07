import os
import shutil
from datetime import datetime

import base_datos

RUTA_STORAGE = os.path.join(os.path.dirname(__file__), "storage", "fotos")
FORMATOS_PERMITIDOS = {"png", "jpg", "jpeg", "gif", "webp"}
TAMANIO_MAXIMO_MB = 15
TAMANIO_MAXIMO_BYTES = TAMANIO_MAXIMO_MB * 1024 * 1024


def _carpeta_reclamo(reclamo_id):
    return os.path.join(RUTA_STORAGE, str(reclamo_id))


def ruta_archivo(reclamo_id, nombre):
    return os.path.join(_carpeta_reclamo(reclamo_id), nombre)


def validar_archivo(uploaded_file):
    nombre = uploaded_file.name.lower()
    ext = nombre.rsplit(".", 1)[-1] if "." in nombre else ""
    if ext not in FORMATOS_PERMITIDOS:
        return (
            False,
            f"'{nombre}': formato no válido. Se permiten {', '.join(sorted(FORMATOS_PERMITIDOS))}.",
        )
    if uploaded_file.size > TAMANIO_MAXIMO_BYTES:
        return False, f"'{nombre}' supera el tamaño máximo de {TAMANIO_MAXIMO_MB} MB."
    return True, ""


def guardar_imagenes(uploaded_files, reclamo_id):
    """Guarda las imágenes subidas para un reclamo y registra sus rutas.

    Devuelve (guardadas, rechazadas) donde guardadas es un int y rechazadas
    una lista de (nombre, motivo).
    """
    guardadas = 0
    rechazadas = []
    if not uploaded_files:
        return guardadas, rechazadas

    carpeta = _carpeta_reclamo(reclamo_id)
    os.makedirs(carpeta, exist_ok=True)

    for archivo in uploaded_files:
        ok, motivo = validar_archivo(archivo)
        if not ok:
            rechazadas.append((archivo.name, motivo))
            continue

        ext = archivo.name.rsplit(".", 1)[-1].lower()
        marca = datetime.now().strftime("%Y%m%d%H%M%S%f")
        nombre = f"{marca}_{guardadas + 1}.{ext}"

        ruta = os.path.join(carpeta, nombre)
        with open(ruta, "wb") as f:
            f.write(archivo.getbuffer())
        base_datos.insertar_imagen(reclamo_id, nombre)
        guardadas += 1

    return guardadas, rechazadas


def eliminar_fotos_reclamo(reclamo_id):
    carpeta = _carpeta_reclamo(reclamo_id)
    if os.path.isdir(carpeta):
        shutil.rmtree(carpeta, ignore_errors=True)