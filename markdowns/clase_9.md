# CLASE 9 – SMARTASSIST AI ANALYST

## Integración del Sistema con SQLite: La Memoria

## Permanente de SmartAssist

# Fundamentación

## Hasta el momento SmartAssist puede recibir comentarios, clasificarlos según categorías y

## generar respuestas automáticas. Sin embargo, existe una limitación importante: toda la

## información procesada desaparece cuando el programa finaliza.

## Los sistemas inteligentes reales necesitan almacenar información para construir

## historiales, analizar comportamientos, detectar patrones y generar reportes. Por ello,

## resulta necesario incorporar una base de datos que permita conservar los datos

## procesados por el sistema.

## En esta clase se integrará SQLite al proyecto SmartAssist, transformando al asistente en

## un sistema capaz de recordar cada reclamo recibido. Esta incorporación representa la

## construcción de la memoria permanente del sistema y constituye el paso previo al análisis

## de datos y la futura integración con Inteligencia Artificial.

# Objetivos

- Comprender la función de una base de datos dentro de una aplicación.
- Integrar SQLite a un proyecto modular en Python.
- Crear funciones para almacenar y recuperar información.
- Relacionar la persistencia de datos con el funcionamiento de SmartAssist.
- Comprender el flujo completo de almacenamiento de reclamos.
- Diferenciar memoria temporal (variables, listas, diccionarios) de memoria

## permanente (SQLite).

# Recuperación de Saberes Previos

## Pregunta inicial:

## ¿Qué sucede cuando cerramos SmartAssist?


## Problema a Resolver

## Necesitamos que SmartAssist recuerde los reclamos procesados.

## Para ello incorporamos:

SQLite

# Evolución del Proyecto

## Antes

Usuario ↓
Comentario ↓
Analizador ↓
Clasificación ↓
Respuesta

## Toda la información desaparece.

## Ahora

Usuario ↓
Comentario ↓
Analizador ↓
Clasificación ↓
Respuesta ↓
SQLite

## La información queda almacenada.

# Estructura Final del Proyecto

SmartAssist/│
├── main.py├── analizador.py
├── respuestas.py├── db.py
│└── datos/
└── reclamos.db


# Paso 1 – Transformar db.py en un módulo

## Hasta la clase anterior utilizamos:

insertar_prueba.py
consultar_prueba.py

## Ahora SmartAssist realizará esas tareas automáticamente.

# Código Completo de db.py

import sqlite3import os

def crear_base():
os.makedirs( "datos",
exist_ok=True )

conexion = sqlite3.connect(
"datos/reclamos.db" )

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

def guardar_reclamo(
comentario, categoria,
prioridad):

conexion = sqlite3.connect(
"datos/reclamos.db" )

cursor = conexion.cursor()


cursor.execute("""
INSERT INTO historial_reclamos( comentario,
categoria, prioridad
)
VALUES (?, ?, ?)
""",
( comentario,
categoria, prioridad
))
conexion.commit() conexion.close()

def mostrar_historial():
conexion = sqlite3.connect( "datos/reclamos.db"
)
cursor = conexion.cursor()
cursor.execute( "SELECT * FROM historial_reclamos"
)
registros = cursor.fetchall()
conexion.close()
return registros

# Explicación del Código

## crear_base()

## Responsabilidad:

**Crear la memoria permanente de SmartAssist.**

## Esta función:

- Verifica si existe la carpeta datos.
- Verifica si existe la base.
- Verifica si existe la tabla.
- Si no existen, las crea.


## Importante:

## La base se crea físicamente una sola vez.

## Sin embargo:

crear_base()

## se ejecuta cada vez que inicia SmartAssist para verificar que todo esté disponible.

## guardar_reclamo()

## Responsabilidad:

Guardar un nuevo reclamo.

## Ejemplo:

Comentario:
No puedo ingresar
Categoría:ERROR_ACCESO

Prioridad:
ALTA

## Se almacena automáticamente.

## mostrar_historial()

## Responsabilidad:

Recuperar los reclamos almacenados.

## ¿Qué hace fetchall()?

registros = cursor.fetchall()

## Obtiene todos los registros encontrados por la consulta.

## Ejemplo:

### [

(1, 'No puedo ingresar', 'ERROR_ACCESO', 'ALTA'), (2, 'Factura incorrecta', 'FACTURACION', 'ALTA')
]

# Paso 2 – Revisar analizador.py

def analizar_comentario(
comentario):


comentario = comentario.lower()
if "ingresar" in comentario:
return {
"categoria":
"ERROR_ACCESO",
"prioridad": "ALTA"

}
elif "factura" in comentario:
return {
"categoria":
"FACTURACION",
"prioridad": "ALTA"

}
else:
return {
"categoria":
"CONSULTA",
"prioridad": "MEDIA"

}

# Paso 3 – Revisar respuestas.py

def generar_respuesta( categoria
):
respuestas = {
"ERROR_ACCESO": "Verifique usuario y contraseña.",

"FACTURACION":
"Su consulta fue enviada al área administrativa.",
"CONSULTA": "Gracias por comunicarse con nosotros."

}
return respuestas[categoria]


# Paso 4 – Modificar main.py

## Código Completo

from analizador import analizar_comentario
from respuestas import generar_respuesta
from db import ( crear_base,
guardar_reclamo)

crear_base()
comentario = input(
"Ingrese comentario: ")

resultado = analizar_comentario(
comentario)

respuesta = generar_respuesta(
resultado["categoria"])

guardar_reclamo(
comentario,
resultado["categoria"],
resultado["prioridad"]
)
print()
print(
"Categoría:", resultado["categoria"]
)
print( "Prioridad:",
resultado["prioridad"])

print(
"Respuesta:", respuesta
)


# Flujo Completo de Ejecución

## Cuando ejecutamos:

python main.py

## ocurre lo siguiente:

## Paso 1

Se verifica la base de datos.

## Paso 2

El usuario escribe un comentario.

## Paso 3

analizador.py clasifica.

## Paso 4

respuestas.py genera una respuesta.

## Paso 5

db.py almacena el reclamo.

## Paso 6

SQLite guarda permanentemente la información.

# Esquema Visual

Usuario ↓
main.py ↓
analizador.py ↓
Categoría ↓
respuestas.py ↓
Respuesta ↓
db.py ↓
SQLite


# Actividad Práctica 1

## Ejecutar SmartAssist utilizando los siguientes comentarios:

No puedo ingresar al sistema

Tengo problemas con mi factura (tienen que haber realizado la actualización propuesta en la actividad de la
clase anterior)

Necesito ayuda

## Completar:

## Comentario Categoría Prioridad

# Actividad Práctica 2

## Modificar el código para agregar una nueva categoría.

## Ejemplo:

### DEVOLUCION

## Agregar la condición correspondiente en:

analizador.py

## y la respuesta correspondiente en:

respuestas.py

## Probar el funcionamiento.

# Actividad Práctica 3

## Importar en main.py:

from db import mostrar_historial

## Agregar al final:

historial = mostrar_historial()
print("\nHISTORIAL")
for fila in historial: print(fila)

## ¿Qué observan?

## Responder:

## 1.¿Dónde se almacenan los reclamos?


## 2.¿Qué sucede si cerramos el programa y volvemos a ejecutarlo?

## 3.¿Qué diferencia existe entre una lista de Python y SQLite?

# Actividad Desafío

## Crear un menú:

### SMARTASSIST

1 - Nuevo reclamo
2 - Ver historial

## Si el usuario selecciona:

### 2

## mostrar todos los registros almacenados utilizando:

mostrar_historial()

# Cierre de la Clase

## Hasta la Clase 8:

SmartAssist entendía reclamos.

## Ahora:

SmartAssist entiende reclamos
y recuerda reclamos.

## Camino hacia la IA

## ✅ SmartAssist clasifica información.

## ✅ SmartAssist genera respuestas.

## ✅ SmartAssist almacena historial.