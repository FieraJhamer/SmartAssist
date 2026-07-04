## **CLASE 12** 

## **SMARTASSIST AI ANALYST** 

## **Análisis Inteligente de Datos con Pandas** 

## **Fundamentación** 

Durante las clases anteriores, SmartAssist fue incorporando capacidades fundamentales para el desarrollo de un sistema inteligente. Inicialmente clasificó comentarios mediante reglas programadas, posteriormente comenzó a almacenar información en una base de datos SQLite y, finalmente, adquirió la capacidad de administrar esos registros mediante operaciones de consulta, modificación y eliminación. 

Sin  embargo,  una  aplicación  moderna  no  obtiene  valor  únicamente  por  almacenar información. El verdadero potencial aparece cuando los datos pueden ser analizados para descubrir patrones, generar estadísticas y facilitar la toma de decisiones. 

En esta clase se incorpora **Pandas** , una de las bibliotecas más utilizadas en Ciencia de Datos, Inteligencia Artificial y análisis estadístico. A diferencia del trabajo manual realizado hasta el momento mediante listas y consultas individuales, Pandas permite organizar grandes volúmenes de información en estructuras tabulares denominadas **DataFrames** , simplificando  el  análisis  de  datos  y  preparando  la  información  para  ser  utilizada posteriormente por modelos de Inteligencia Artificial. 

La incorporación de Pandas representa un cambio importante en el proyecto SmartAssist: el sistema deja de limitarse a registrar información para comenzar a interpretarla. Este paso  constituye  el  puente  entre  la  programación  tradicional  y  el  análisis  de  datos, acercando  a  los  estudiantes  al  modo  en  que  trabajan  actualmente  los  sistemas inteligentes. 

## **Objetivos Generales** 

Al finalizar la clase el estudiante será capaz de: 

- Comprender el propósito de Pandas dentro de un proyecto de software. 

- Analizar información almacenada en SQLite utilizando DataFrames. 

- Obtener estadísticas básicas a partir de datos reales. 

- Interpretar resultados obtenidos mediante Pandas. 

- Integrar un nuevo módulo al proyecto SmartAssist. 

- Preparar la información para su utilización en modelos de Inteligencia Artificial. 

## **Objetivos Específicos** 

El estudiante podrá: 

- Instalar la biblioteca Pandas. 

- Importar datos desde SQLite. 

- Crear un DataFrame. 

- Explorar la información almacenada. 

- Obtener estadísticas mediante funciones propias de Pandas. 

- Generar reportes automáticos. 

- Comprender la diferencia entre datos e información. 

## **Saberes Previos** 

Recordar el estado actual del proyecto. 

Usuario 

↓ 

SmartAssist 

↓ 

SQLite 

↓ 

Guardar 

Consultar 

Modificar 

Eliminar 

Pregunta: 

**¿Puede SmartAssist responder cuál es la categoría con mayor cantidad de reclamos?** 

Respuesta esperada: 

"No de forma sencilla." 

## **Problema Inicial** 

Base de Datos 

## **1200 reclamos** 

Pregunta: 

## **¿Quién los analiza?** 

Posibles respuesta: 

- nosotros 

- el programa 

- una consulta SQL 

Planteo: 

## **¿Y si hubiera 100.000 reclamos?** 

## **¿Qué es Pandas?** 

Pandas es una biblioteca de Python diseñada para trabajar con grandes cantidades de datos de manera rápida y organizada. 

Su estructura principal recibe el nombre de **DataFrame** . 

**Puede pensarse como una hoja de cálculo de Excel, pero controlada completamente desde Python.** 

## **¿Qué es un DataFrame?** 

SQLite 

↓ 

Tabla 

↓ 

Pandas 

↓ 

DataFrame 

Un DataFrame permite: 

- ordenar información; 

- buscar registros; 

- obtener estadísticas; 

- filtrar datos; 

- agrupar información; 

- preparar datos para IA. 

## **Instalación** 

## **pip install pandas** 

Verificación: 

**import pandas as pd** 

## **Integración con SmartAssist** 

Crear un nuevo archivo. 

## **analisis.py** 

Continuamos con la modularización del proyecto. 

No mezclaremos análisis con: 

- db.py 

- main.py 

## **Primer código** 

import sqlite3 import pandas as pd 

conexion = sqlite3.connect( "datos/reclamos.db" ) df = pd.read_sql_query( "SELECT * FROM historial_reclamos", conexion ) 

conexion.close() 

## **Explicación línea por línea** 

## **sqlite3.connect()** 

Conecta con la base. 

## **pd.read_sql_query()** 

Ejecuta la consulta SQL. Pero ahora devuelve un: 

## **DataFrame** 

## **Visualización** 

print(df) 

## Mostrar: 

id comentario categoria prioridad 

1 ... 2 ... 

3 ... 

Aquí ya no estamos trabajando con: 

## **fetchall()** 

Ahora toda la información está dentro del **DataFrame** . 

## **Explorando el DataFrame** 

## **Primeras filas** 

print(df.head()) 

## **Últimas filas** 

print(df.tail()) 

## **Cantidad de registros** 

print(len(df)) 

## **Información del DataFrame** 

print(df.info()) 

**`dtypes: int64(1), str(3)`** : Tienes **1 columna** con números enteros de 64 bits ( `int64` ) y **3 columnas** con texto ( `str` ). 

**`memory usage: 580.0 bytes`** : Apenas consume 580 bytes de memoria RAM. 

**`None`** , algunas interfaces lo muestran explícitamente al final de la impresión. No es un error ni significa que pase algo malo; simplemente es Pandas diciéndote _"ya imprimí todo, mi trabajo aquí terminó y mi valor de retorno es vacío"_ . 

## **Estadísticas** 

print(df.describe()) 

describe() resulta especialmente útil cuando existen columnas numéricas y que luego podrá utilizarse en proyectos más complejos. 

## **Analizando SmartAssist** 

¿Cuántos reclamos existen? 

print(len(df)) 

¿Cuántos ERROR_ACCESO? 

print( df["categoria"].value_counts() ) 

## **Prioridades** 

print( df["prioridad"].value_counts() ) 

## **Filtrar** 

print( df[ df["categoria"]=="ERROR_ACCESO" ] ) 

## **Filtrar prioridades** 

print( df[ df["prioridad"]=="ALTA" ] ) 

## **Creando el módulo analisis.py** 

import sqlite3 import pandas as pd 

def cargar_datos(): 

conexion = sqlite3.connect("datos/reclamos.db") 

df = pd.read_sql_query( "SELECT * FROM historial_reclamos", conexion ) conexion.close() return df 

def generar_estadisticas(): 

df = cargar_datos() 

return { "total": len(df), "categorias": df["categoria"].value_counts(), "prioridades": df["prioridad"].value_counts() } 

## **Integración con main.py** 

Agregar: 

## **Estadísticas con Pandas** 

Cuando el usuario seleccione esa opción: 

generar_estadisticas() 

estadisticas = generar_estadisticas() 

print("\n===== SMARTASSIST ANALYTICS =====") 

print(f"\nTotal de reclamos: {estadisticas['total']}") 

print("\nCategorías:") 

print(estadisticas["categorias"]) 

print("\nPrioridades:") 

print(estadisticas["prioridades"]) 

## **Actividad 1** 

Registrar veinte reclamos diferentes. 

Ejecutar el análisis. Interpretar los resultados. 

## **Actividad 2** 

Responder: 

- ¿Cuál es la categoría predominante? 

- ¿Qué prioridad aparece con mayor frecuencia? 

- ¿Cuántos reclamos existen? 

## **Actividad 3** 

Modificar varios registros mediante CRUD. 

Volver a ejecutar Pandas. 

Comparar los resultados. 

## **Actividad Avanzada** 

Agregar una nueva categoría. 

Registrar varios reclamos. 

Comprobar cómo cambia automáticamente el análisis. 

## **Desafío 1** 

Mostrar solamente: 

## **Prioridad ALTA** 

utilizando Pandas. 

## **Desafío 2** 

Ordenar los reclamos por categoría. 

Investigar: 

**sort_values()** 

## **Desafío 3** 

Exportar el DataFrame a un archivo CSV. 

**df.to_csv( "reporte.csv", index=False )** 

Abrir el archivo y verificar su contenido. 

## **Desafío Integrador** 

Cada estudiante deberá adaptar el módulo analisis.py a su proyecto final. 

Por ejemplo: 

- Biblioteca: analizar préstamos por tipo. 

- Clínica: analizar turnos por especialidad. 

- Comercio: analizar productos por categoría. 

- Escuela: analizar consultas por curso. 

- Hotel: analizar reservas por estado. 

El objetivo es que el análisis responda preguntas relevantes para el dominio elegido, utilizando la misma estructura del proyecto SmartAssist. 

## **Cierre Conceptual** 

Hasta ayer... 

SmartAssist almacenaba información. 

↓ 

Hoy... 

SmartAssist descubre patrones. 

↓ 

Próxima clase... 

SmartAssist tendrá una interfaz gráfica mediante Streamlit. 

↓ 

Luego... 

Un modelo de IA (Ollama) interpretará esos patrones y generará conclusiones automáticas. 

