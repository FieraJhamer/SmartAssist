# SmartAssist AI Analyst — Explicación del Proyecto

## ¿Qué es SmartAssist?

SmartAssist es una aplicación de consola (CLI) en Python que recibe comentarios de usuarios,
los clasifica automáticamente por categoría y prioridad, genera una respuesta automática y
almacena todo en una base de datos SQLite para mantener un historial permanente.

---

## Estructura del Proyecto

```
SmartAssist/
├── main.py              → Punto de entrada (menú interactivo)
├── analizador.py        → Wrapper que delega la clasificación
├── example.py           → Motor de clasificación por palabras clave
├── respuestas.py        → Plantillas de respuestas por categoría
├── db.py                → Capa de persistencia con SQLite
├── api_client.py        → Cliente HTTP para API externa (no utilizado aún)
├── datos/
│   └── reclamos.db      → Base de datos SQLite con el historial
├── markdowns/
│   ├── clase_9.md       → Material de la clase 9
│   ├── especificaciones.md
│   └── consigna.md
└── explicacion.md       → Este archivo
```

---

## Flujo de Ejecución

```
Usuario ingresa comentario
         ↓
   main.py (menú)
         ↓
   analizador.py → example.py (clasifica por palabras clave)
         ↓
   respuestas.py (genera respuesta automática)
         ↓
   db.py (guarda en SQLite)
         ↓
   Muestra resultado en pantalla
```

---

## Módulo por Módulo

### 1. `main.py` — Controlador principal

Importa los demás módulos y presenta un menú con 4 opciones:

1. **Analizar un comentario** — pide texto, lo clasifica, muestra categoría/prioridad/respuesta y lo guarda.
2. **Ver historial completo** — muestra todos los registros almacenados.
3. **Ver por categoría** — filtra el historial por una categoría específica.
4. **Salir** — finaliza el programa.

Al iniciar, ejecuta `db.crear_tabla()` para asegurarse de que la base de datos y la tabla existen.

---

### 2. `analizador.py` — Clasificador (wrapper)

Importa la función `analizar_comentario()` desde `example.py` y expone `clasificar(comentario)`,
que retorna una tupla `(categoria, prioridad)`.

Cuando se ejecuta directamente, corre una batería de 8 pruebas con comentarios de ejemplo.

---

### 3. `example.py` — Motor de clasificación

Contiene la lógica central de clasificación mediante detección de palabras clave
(case-insensitive). Evalúa el texto con `if/elif` y retorna un diccionario con:

| Palabras clave                     | Categoría       | Prioridad |
|------------------------------------|-----------------|-----------|
| `ingresar`                         | ERROR_ACCESO    | ALTA      |
| `lento`, `demora`, `lenta`         | RENDIMIENTO     | MEDIA     |
| `factura`, `cobro`, `pago`, etc.   | FACTURACION     | ALTA      |
| `dañado`, `equivocado`, etc.       | DEVOLUCION      | ALTA      |
| `baja`, `liquidar`, etc.           | CANCELACION     | ALTA      |
| (ninguna de las anteriores)        | CONSULTA        | BAJA      |

---

### 4. `respuestas.py` — Respuestas automáticas

Define un diccionario `RESPUESTAS` que mapea cada categoría a un texto de respuesta
predefinido. La función `generar_respuesta(categoria)` busca la respuesta y si la categoría
no existe, usa `"OTRO"` como valor por defecto.

Ejemplos:

- `ERROR_ACCESO` → "Verifique sus credenciales o solicite un reinicio de contraseña..."
- `FACTURACION` → "Su consulta de facturación ha sido derivada al área contable..."
- `DEVOLUCION` → "Generamos un turno para devolución..."

---

### 5. `db.py` — Persistencia con SQLite

Maneja toda la interacción con la base de datos SQLite (`datos/reclamos.db`).

La tabla `historial_reclamos` tiene 4 columnas:

| Columna     | Tipo    | Descripción                      |
|-------------|---------|----------------------------------|
| id          | INTEGER | Clave primaria (autoincremental) |
| comentario  | TEXT    | Texto original del usuario       |
| categoria   | TEXT    | Categoría asignada               |
| prioridad   | TEXT    | Prioridad asignada               |

**Funciones principales:**

| Función                     | Descripción                                    |
|-----------------------------|------------------------------------------------|
| `conectar()`                | Abre conexión a la BD (crea carpeta si falta) |
| `crear_tabla()`             | Crea la tabla si no existe                     |
| `insertar(c, cat, pri)`     | Inserta un nuevo registro                      |
| `obtener_todos()`           | Retorna todos los registros                    |
| `obtener_por_categoria(c)`  | Filtra registros por categoría                 |
| `mostrar_historial()`       | Alias de `obtener_todos()`                     |
| `guardar_reclamo(c,cat,pri)`| Alias de `insertar()`                          |
| `crear_base()`              | Alias de `crear_tabla()`                       |

---

### 6. `api_client.py` — Cliente HTTP (futuro)

Módulo independiente que envía el comentario a una API externa (`https://api.example.com/analyze`)
vía POST y espera un JSON con `categoria` y `prioridad`. Incluye manejo de errores.
Actualmente no se usa en el flujo principal, pero está preparado para una futura integración
con un servicio de inteligencia artificial.

---

## Datos

La base de datos se almacena en `datos/reclamos.db` y persiste entre ejecuciones del programa.
Esto le da a SmartAssist "memoria permanente" — a diferencia de usar listas o diccionarios en
memoria que se pierden al cerrar la aplicación.

---

## Cómo ejecutar

```bash
python main.py
```

Luego seleccionar una opción del menú:

```
=== SMARTASSIST AI ANALYST ===
1. Analizar un comentario
2. Ver historial completo
3. Ver por categoría
4. Salir
Seleccione una opción:
```

---

## Resumen de conceptos aprendidos

| Concepto                     | Aplicación en SmartAssist                        |
|------------------------------|--------------------------------------------------|
| Módulos en Python            | Separación en `main.py`, `db.py`, `respuestas.py`, etc. |
| SQLite                       | Base de datos liviana para persistencia local    |
| Palabras clave               | Clasificación de comentarios por coincidencia    |
| Menú interactivo             | Loop `while` con `input()` para navegar opciones |
| Persistencia de datos        | Los reclamos sobreviven al cierre del programa   |
| Parámetros SQL (?, ?, ?)     | Inserción segura evitando inyección SQL          |
