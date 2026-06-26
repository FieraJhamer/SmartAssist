# SMARTASSIST AI ANALYST

# CLASE 8

## Persistencia de Datos con SQLite

# Fundamentación

### Las aplicaciones modernas requieren almacenar información para su posterior

### recuperación, análisis y generación de conocimiento. Los asistentes inteligentes no sólo

### deben procesar datos, sino también conservarlos para construir historiales y estadísticas.

### En esta clase los estudiantes incorporarán una base de datos SQLite al proyecto

### SmartAssist, permitiendo registrar cada comentario analizado junto con su clasificación y

### prioridad. Este proceso constituye el primer paso hacia la construcción de sistemas

### capaces de generar reportes y análisis automatizados.

# Objetivos

### Al finalizar la clase los estudiantes serán capaces de:

- Comprender el concepto de persistencia de datos.
- Crear bases de datos SQLite desde Python.
- Diseñar tablas simples.
- Insertar información en una base de datos.
- Consultar registros almacenados.
- Integrar SQLite dentro del proyecto SmartAssist.

# Contenidos

- Persistencia.
- SQLite.
- Bases de datos relacionales.
- CREATE TABLE.
- INSERT.
- SELECT.
- Integración Python-SQLite.


# Estructura del Proyecto

### SmartAssist/

### │

### ├── main.py

### ├── api_client.py

### ├── analizador.py

### ├── respuestas.py

### ├── db.py

### │

### └── datos/

### └── reclamos.db

# Desarrollo Central

## Paso 1

### Crear:

## db.py

import sqlite
conexion = sqlite3.connect(
"datos/reclamos.db")

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


## Paso 2

### Ejecutar:

python db.py
**Este archivo se ejecuta una sola vez para crear la estructura.**

### Verificar que se genere:

reclamos.db

## Paso 3

### Insertar registros.

cursor.execute("""
INSERT INTO historial_reclamos(
comentario,categoria,
prioridad
)
VALUES(
?,?,
?
)
""",
(
"No puedo ingresar",
"ERROR_ACCESO",
"ALTA"
)
)

## Paso 4

### Consultar información.

cursor.execute(
"SELECT * FROM historial_reclamos"


#### )

registros = cursor.fetchall()
for fila in registros:
print(fila)

# Actividad Práctica 1

### Crear tres registros manuales.

### Ejemplo:

No puedo ingresar

La página está lenta

Necesito ayuda

# Actividad Práctica 2

### Consultar todos los registros almacenados.

### Mostrar:

- ID
- Comentario
- Categoría
- Prioridad

# Actividad Práctica 3

### Consultar únicamente:

SELECT * FROM historial_reclamosWHERE categoria='ERROR_ACCESO';

### Interpretar resultados.

# Actividad Integradora

### Integrar:

Comentario ↓
analizador.py ↓
resultado ↓
SQLite


### Guardar automáticamente el resultado obtenido.

# Producto Final de la Clase

### SmartAssist será capaz de:

Comentario ↓
Clasificación ↓
Prioridad ↓
Respuesta automática ↓
SQLite ↓
Historial permanente

# Estado Final del Proyecto

SmartAssist/│
├── main.py├── api_client.py
├── analizador.py├── respuestas.py
├── db.py│
└── datos/ └── reclamos.db


