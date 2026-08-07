# CLASE 14

# SMARTASSIST AI ANALYST

# Integración de Inteligencia Artificial con

# Ollama

# Fundamentación

A lo largo del curso, los estudiantes desarrollaron un proyecto completo que evolucionó
progresivamente incorporando nuevos módulos y tecnologías. Inicialmente, SmartAssist
era una aplicación capaz de recibir información del usuario y organizar su código
mediante funciones y modularización. Posteriormente, incorporó una base de datos
SQLite para almacenar información de forma persistente, operaciones CRUD para
administrar los registros, análisis estadístico mediante Pandas e interfaz gráfica con
Streamlit.
Hasta este momento, el sistema era capaz de **capturar datos, almacenarlos,
analizarlos y visualizarlos** , pero seguía dependiendo de reglas programadas por el
desarrollador para generar respuestas.
En esta clase se incorpora **Ollama** , una plataforma que permite ejecutar modelos de
lenguaje de manera local, transformando a SmartAssist en un asistente capaz de
interpretar información y generar respuestas en lenguaje natural sin depender de servicios
externos.
La integración de Ollama permite comprender cómo la Inteligencia Artificial puede
convertirse en un componente más dentro de una arquitectura de software, donde cada
tecnología cumple una función específica y complementaria.

# Objetivos Generales

Al finalizar la clase, el estudiante será capaz de:

- Comprender el concepto de modelo de lenguaje.
- Explicar el funcionamiento general de Ollama.
- Integrar Inteligencia Artificial a un proyecto desarrollado en Python.
- Analizar información mediante un modelo de IA local.
- Comprender el flujo completo de SmartAssist desde el ingreso del dato hasta la
    generación de un informe inteligente.


# Objetivos Específicos

El estudiante será capaz de:

- Diferenciar una IA ejecutada localmente de un servicio basado en API.
- Instalar y ejecutar Ollama.
- Descargar un modelo adecuado para equipos con 8 GB de RAM.
- Crear un módulo independiente para la comunicación con la IA.
- Construir prompts efectivos.
- Integrar la IA con los datos obtenidos desde SQLite y Pandas.

# Recuperación de Saberes

Recordar la evolución del proyecto.
Clase 1
│ ▼
Python
│ ▼
Funciones
│ ▼
SQLite
│
▼CRUD

│
▼Pandas

│
▼Streamlit

│
▼Hoy

Inteligencia Artificial

# Problema Inicial

SmartAssist conoce los datos.

**¿Puede explicar qué significan?**
Ejemplo:
ERROR_ACCESO : 48


FACTURACION : 21
CONSULTA : 8

La pregunta es:
¿Dónde está el análisis?

Respuesta:
No existe. Solo existen números.

# Entonces...

_Necesitamos un modelo capaz de interpretar información._
Aquí aparece **Ollama**.

# ¿Qué es Ollama?

Ollama es un programa que permite ejecutar modelos de Inteligencia Artificial
directamente en nuestra computadora.
No utiliza Internet para responder una vez descargado el modelo.
No requiere API Keys.
No depende de servicios externos.

# Comparación

```
API en la nube Ollama
Requiere Internet Funciona localmente
API Key No
Puede tener costos Gratuito
Datos viajan a servidores
externos
```
```
Datos permanecen en la
PC
```
# ¿Qué es un modelo de Inteligencia

# Artificial?

Un **modelo de Inteligencia Artificial** es un programa que fue entrenado con millones o
miles de millones de textos para aprender patrones del lenguaje humano.
No memoriza todas las respuestas. Lo que hace es **predecir cuál es la siguiente
palabra más probable** según el contexto recibido.


Imaginen un estudiante que durante años leyó:

- libros.
- Artículos.
- Manuales.
- páginas web.
- conversaciones.
Después de leer todo ese material, ese estudiante puede responder preguntas, resumir
textos, redactar documentos o explicar conceptos.
Un modelo de IA funciona de forma parecida: aprende patrones a partir de una enorme
cantidad de información.

## ¿Qué hace un modelo?

Cuando escribimos:
¿Por qué hay muchos reclamos de acceso?
El modelo no busca esa respuesta en Internet.
En realidad hace algo similar a esto:
Palabra 1
↓
Palabra 2
↓
Palabra 3
↓
Palabra 4
↓
Respuesta completa
Va construyendo la respuesta palabra por palabra.

## ¿Qué sabe hacer un modelo?

Dependiendo de cómo fue entrenado puede:

- responder preguntas.
- resumir textos.
- traducir idiomas.
- generar código.
- corregir errores.
- clasificar información.
- redactar informes.
- explicar conceptos.


- analizar datos.
Eso es justamente lo que hará dentro de SmartAssist.

# Arquitectura del proyecto

Hasta ayer:
Usuario
↓
SmartAssist↓

SQLite
↓
Pandas

Ahora:
Usuario
↓
SmartAssist↓

SQLite
↓
Pandas↓

Ollama
↓
Respuesta Inteligente

# Instalación

Sitio oficial: https://ollama.com/

La instalación tiene **dos etapas** :

1. **Instalar Ollama** (el programa que ejecuta modelos).
2. **Descargar un modelo**
En windows:
Ingresar a: https://ai.google.dev/gemma/docs/integrations/ollama?
utm_source=chatgpt.com&hl=es-



Instalación según el sistema operativo.
En Linux:

curl -fsSL https://ollama.com/install.sh | sh

Verificar:
ollama --version


# Descargar el modelo

Para un estándar básico (8 GB de RAM), utilizar:
ollama pull gemma3:1b

**¿Por que se elige un modelo pequeño:**

- menor consumo de memoria;
- mejor velocidad de respuesta;
- suficiente para tareas educativas.

Si descargáramos un modelo de 12 mil millones de parámetros:

- tardaría mucho en responder;
- consumiría gran parte de la memoria;
- algunas computadoras podrían quedarse sin recursos.

# Probar el modelo

ollama run gemma3:1b

Estamos diciendo:

```
"Ollama, ejecutá el modelo Gemma 3 de 1 billón de parámetros."
```
# ¿Qué significa "1b"?

El número indica aproximadamente la cantidad de **parámetros** que posee el modelo.
Los parámetros son los valores internos que el modelo aprendió durante su entrenamiento
y que utiliza para generar respuestas.
Podemos pensar en ellos como la "experiencia" o el "conocimiento" que adquirió.

# Ejemplo

```
Modelo Parámetrosaproximados
Gemma3:1b 1.000 millones
Gemma3:4b 4.000 millones
Llama3:8b 8.000 millones
Gemma3:12b 12.000 millones
```

Cuantos más parámetros tiene un modelo:

- generalmente comprende mejor las preguntas;
- produce respuestas más elaboradas;
- puede resolver tareas más complejas.
Pero también consume más recursos.

Poner en práctica:
Hola.

Luego:
Resume el siguiente comentario...

# Comparación

```
Modelo RAM recomendada Velocidad Calidad
1B 4–8 GB Muy rápida Buena para tareas educativas
4B 8–12 GB Rápida Muy buena
8B 16 GB o más Media Excelente
12B+ 24 GB o más Más lenta Muy alta
```
# ¿Pierdo calidad por usar un modelo

# pequeño?

Sí, pero depende de la tarea.
En SmartAssist el modelo deberá:

- resumir comentarios;
- redactar respuestas;
- interpretar estadísticas;
- sugerir recomendaciones.
No le estamos pidiendo:
- escribir una tesis;
- resolver problemas científicos complejos;
- programar un sistema operativo.
Para este tipo de tareas, un modelo pequeño ofrece un equilibrio muy bueno entre calidad
y rendimiento.


# Relación con SmartAssist

Hasta ahora el sistema producía resultados como estos:
ERROR_ACCESO : 45
FACTURACION : 18
CONSULTA : 9

Eso son **datos**.
Con Ollama, el modelo recibe esos datos y genera una interpretación, por ejemplo:
_“La mayoría de los reclamos corresponden a problemas de acceso.
Se recomienda revisar el proceso de autenticación y reforzar la asistencia a los usuarios
durante el inicio de sesión”._
Es importante destacar que **el modelo no reemplaza a Pandas**. Pandas organiza y
resume la información; el modelo toma ese resumen y lo transforma en un texto
comprensible para una persona.

# SMARTASSIST

**SQLite**
▼
Guarda los datos

**Pandas**
▼
Los organiza y obtiene estadísticas

**Ollama**
▼
Interpreta esas estadísticas y redacta una conclusión

**Usuario**
▼


Lee un informe claro y comprensible
**Cada tecnología cumple un rol distinto** dentro del proyecto y que la Inteligencia Artificial
no aparece "por arte de magia": necesita datos bien almacenados y bien analizados para
generar respuestas útiles.

# Integración con Python

**Instalar:**
pip install ollama

**Crear un nuevo módulo:**
ia.py

## Código básico

import ollama
def consultar_ia(prompt):
respuesta = ollama.chat( model="gemma3:1b",
messages=[ {
"role": "user", "content": prompt
} ]
)
return respuesta["message"]["content"]

## Explicación

- import ollama: importa la biblioteca.
- consultar_ia(): función reutilizable.
    - model: modelo seleccionado.
    - messages: conversación enviada al modelo.
    - role: identifica al emisor.
    - content: texto del usuario.
    - return: devuelve únicamente la respuesta.

# Integración con SmartAssist

Agregar en app.py un nuevo bloque:
st.header(" Análisis Inteligente")
if st.button("Generar informe con IA"):


estadisticas = generar_estadisticas()
prompt = f"""
Estas son las estadísticas del sistema:
{estadisticas}

Elabora un informe indicando:

- categoría predominante;
- prioridad predominante;
- posibles causas;
- tres recomendaciones. """

respuesta = consultar_ia(prompt)
st.write(respuesta)

**El prompt utiliza los datos calculados por Pandas.**

# Flujo completo del sistema

Usuario
▼SmartAssist
▼SQLite
▼Pandas
▼Generación de estadísticas
▼Prompt
▼Ollama
▼Respuesta en lenguaje natural

# Actividad 1

Instalar Ollama y verificar su funcionamiento.

# Actividad 2

Descargar el modelo gemma3:1b y realizar tres consultas libres para comprobar que
responde correctamente.


# Actividad 3

Integrar el módulo ia.py al proyecto y enviar un prompt simple, por ejemplo:
Resume este comentario:
"No puedo acceder a mi cuenta desde ayer y necesito ingresar con urgencia."

Mostrar la respuesta en consola.

# Actividad 4 (Integración con SmartAssist)

Utilizar las estadísticas generadas por analisis.py y construir un prompt que solicite al
modelo un informe breve sobre el estado del sistema.
Comparar el resultado con las estadísticas numéricas obtenidas mediante Pandas.

# Desafíos

### Desafío 1

Modificar el prompt para que el informe tenga un máximo de cinco líneas.

### Desafío 2

Cambiar el rol del modelo:

- Supervisor técnico.
- Gerente.
- Responsable de atención al cliente.
Comparar las respuestas.

### Desafío 3

Pedir al modelo que redacte un correo electrónico dirigido a la gerencia explicando el
estado del sistema.

### Desafío 4

Modificar las estadísticas incorporando nuevos reclamos y analizar cómo cambia el
informe generado por la IA.

### Desafío 5 (Pensamiento crítico)

Ejecutar el mismo prompt dos veces.
Responder:

- ¿La respuesta fue exactamente igual?
- ¿Qué diferencias encontraron?
- ¿Por qué creen que sucede?


Este desafío introduce el concepto de variabilidad en los modelos generativos y la
importancia de validar las respuestas.

# Integración con el proyecto final

Explicar que, a partir de esta clase, cada estudiante incorporará Ollama al dominio elegido
para su proyecto individual:

- Biblioteca: resumir préstamos, devoluciones y sugerir acciones.
- Clínica: interpretar el estado de los turnos.
- Comercio: analizar ventas o reclamos.
- Escuela: resumir consultas de estudiantes.
- Hotel: interpretar reservas y cancelaciones.
La arquitectura será la misma; solo cambiarán los datos y el contexto del análisis.

# Cierre de la clase

Entrada de datos
▼
Funciones
▼
SQLite
▼
CRUD
▼
Pandas
▼
Streamlit
▼
Ollama
▼
Informe Inteligente

# Conclusión:

```
"La Inteligencia Artificial no reemplazó el trabajo que hicieron durante todo el
curso. Al contrario: pudo aportar valor porque primero construyeron una
aplicación bien organizada, con datos confiables y un análisis previo. La IA
necesita un buen software para ser realmente útil."
```

