CLASE 11
SmartAssist AI Analyst
Consultas Inteligentes y Estadísticas con SQLite
Fundamentación

Hasta este momento SmartAssist ya es capaz de clasificar comentarios, generar
respuestas automáticas y administrar su historial mediante SQLite. Sin embargo, disponer
de una base de datos no aporta valor por sí sola; la verdadera utilidad surge cuando la
información almacenada puede convertirse en conocimiento.
En esta clase los estudiantes aprenderán a realizar consultas específicas sobre la base
de datos y a obtener estadísticas básicas utilizando únicamente SQLite y Python. Este
proceso constituye el primer acercamiento al análisis de datos, preparando el camino para
el uso de herramientas como Pandas y, posteriormente, para la incorporación de modelos
de Inteligencia Artificial.
La clase busca que el estudiante comprenda que un sistema inteligente no solo almacena
datos, sino que también puede responder preguntas sobre ellos.
Objetivos

Al finalizar la clase el estudiante será capaz de:

    Realizar consultas específicas sobre SQLite.
    Obtener información mediante filtros.
    Utilizar funciones SQL de agregación.
    Interpretar resultados obtenidos de una base de datos.
    Integrar nuevas funciones al proyecto SmartAssist.
    Comprender la importancia del análisis de datos en sistemas inteligentes.

Nuevas funciones en db.py

contar_reclamos()
def contar_reclamos():
conexion = sqlite3.connect("datos/reclamos.db")
cursor = conexion.cursor()
cursor.execute("""
SELECT COUNT(*)

FROM historial_reclamos
""")
cantidad = cursor.fetchone()[0]
conexion.close()
return cantidad

buscar_categoria()
def buscar_categoria(categoria):
conexion = sqlite3.connect("datos/reclamos.db")
cursor = conexion.cursor()
cursor.execute("""
SELECT *
FROM historial_reclamos
WHERE categoria =?
""",
(categoria,))
registros = cursor.fetchall()
conexion.close()
return registros

contar_por_categoria()
def contar_por_categoria():
conexion = sqlite3.connect("datos/reclamos.db")
cursor = conexion.cursor()
cursor.execute("""
SELECT categoria,
COUNT(*)

FROM historial_reclamos
GROUP BY categoria
""")
datos = cursor.fetchall()
conexion.close()
return datos
Modificaciones en main.py

Agregar opciones:
6 - Buscar por categoría
7 – Estadísticas

Opción 6
Mostrar únicamente la categoría solicitada.

Opción 7
Mostrar:
Cantidad total: 25
ERROR_ACCESO : 12
FACTURACION : 7
CONSULTA : 6
Actividades
Actividad 1

Buscar únicamente los reclamos:
ERROR_ACCESO
Actividad 2

Mostrar la cantidad total de reclamos.
Actividad 3

Determinar cuál es la categoría predominante.
No hacerlo "a ojo".
Debe obtenerse desde SQLite.
Desafío

Crear una función:
buscar_prioridad(prioridad)
Desafío Avanzado

Mostrar:
====================ESTADO DEL SISTEMA
Reclamos registrados : 18Categoría más frecuente :
ERROR_ACCESO====================
Reportes Automáticos y Preparación para la IA
Fundamentación

Una vez obtenidas consultas y estadísticas básicas, el siguiente paso consiste en
transformar esos datos en información útil para la toma de decisiones.
En esta clase SmartAssist dejará de mostrar únicamente registros almacenados para
comenzar a generar reportes automáticos sobre el estado del sistema.
Esta etapa representa la transición entre la administración de datos y el análisis
inteligente, preparando la incorporación de modelos de Inteligencia Artificial capaces de
interpretar dichos reportes.
Objetivos

    Generar reportes automáticos.
    Organizar información para su interpretación.
    Desarrollar funciones reutilizables.
    Comprender la diferencia entre dato e información.
    Preparar SmartAssist para la futura integración con Ollama.

Nueva función

def generar_reporte():
def generar_reporte():
total = contar_reclamos()
categorias = contar_por_categoria()
print()
print("========================")
print("REPORTE SMARTASSIST")
print("========================")
print()
print(
"Total de reclamos:", total
)

print()
for categoria, cantidad in categorias:
print(
categoria,
":",
cantidad
)

main.py

Agregar:
8 - Generar reporte

Actividad
Ejecutar SmartAssist.
Ingresar:
15 reclamos.
Luego generar el reporte.

Desafío 1
Crear un reporte con el siguiente formato:
==========================
SMARTASSIST REPORT
==========================
Total:
25
Categorías
ERROR_ACCESO 10
FACTURACION 8
CONSULTA 7
==========================

Desafío 2
Agregar al reporte:

Fecha:
Hora:
(utilizando el módulo datetime).
Integración con el Proyecto Principal
Usuario
│
▼
Ingreso del comentario
│ ▼
Analizador (Python)
│
▼
Clasificación │
▼
Respuesta automática
│
▼SQLite
│
├── Guardar reclamo
├── Consultar historial
├── Modificar registros ├── Eliminar registros
├── Buscar información
├── Obtener estadísticas
└── Generar reportes