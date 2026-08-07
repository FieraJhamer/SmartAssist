# 🏙️ SmartAssist — Reclamos Ciudadanos de La Rioja

Sistema web + CLI para que los ciudadanos de **La Rioja (Argentina)** registren reclamos municipales. Clasifica automáticamente cada reclamo por **categoría y prioridad**, genera respuestas, persiste todo en **SQLite**, lo analiza con **Pandas** y lo interpreta con un **modelo de IA local (Ollama)**.

---

## ✨ Funcionalidades

- 📝 Carga de reclamos ciudadanos con clasificación automática (8 categorías municipales).
- 📊 Historial con filtros por categoría y prioridad, edición y eliminación.
- 🗂️ Estadísticas y reportes con Pandas.
- 🤖 Análisis inteligente con IA local (Ollama): informe del estado, correo a gerencia, resumen y respuesta por reclamo.
- 🎨 Interfaz web responsive con la identidad visual de la Marca La Rioja.

## 🧠 Categorías de reclamos

| Categoría | Prioridad | Palabras clave (ej.) |
|-----------|-----------|----------------------|
| AGUA_CLOACAS | ALTA | agua, cloaca, pérdida, filtra, corte de agua |
| RECOLECCION_RESIDUOS | ALTA | basura, residuo, contenedor, basural |
| ALUMBRADO | ALTA | alumbrado, luminaria, farol, luz, apagado |
| SEGURIDAD | ALTA | seguridad, robo, peligro, defensa civil |
| MANTENIMIENTO_VIAL | MEDIA | bache, vereda, calle, asfalto, señalización |
| TRANSPORTE_PUBLICO | MEDIA | colectivo, transporte, micro, ómnibus, parada |
| LIMPIEZA | MEDIA | poda, limpieza, maleza, baldío, escombro |
| CONSULTA | BAJA | cualquier consulta general |

La clasificación es **case-insensitive** y no distingue acentos (se normalizan).

---

## 🚀 Instalación (desde cero)

Requisitos: **Python 3.10+** y **git**.

```bash
git clone <URL-DEL-REPOSITORIO>
cd SmartAssist

# 1. Entorno virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS

# 2. Instalar dependencias
pip install -r requirements.txt
```

### 🤖 Configurar Ollama (para la IA)

1. Instalar [Ollama](https://ollama.com/) y descargar el modelo:

   ```bash
   ollama pull gemma3:1b
   ```

2. Verificar que responde:

   ```bash
   ollama run gemma3:1b
   ```

> La app usa el modelo `gemma3:1b` (definido en `ia.py`). Si querés otro modelo, cambiá la constante `MODELO` en ese archivo.

---

## ▶️ Uso

### Interfaz web (recomendada)

```bash
streamlit run app.py
```

Secciones:

- **Nuevo reclamo** — ingresá el comentario del ciudadano y el sistema lo clasifica.
- **Historial** — consultá, filtrá, editá, eliminá y analizá con IA cada reclamo.
- **Estadísticas** — métricas y gráficos por categoría y prioridad.
- **Análisis Inteligente** — generá informe con IA, correo a gerencia y chat libre.

### Consola CLI

```bash
python menu_principal.py
```

```
=== SMARTASSIST AI ANALYST ===
1. Analizar un comentario
2. Ver historial completo
3. Ver por categoría
4. Editar reclamo
5. Eliminar reclamo
6. Estadísticas
7. Generar reporte
0. Salir
```

---

## 📁 Estructura del proyecto

```
SmartAssist/
├── app.py                    # Interfaz web Streamlit (punto de entrada principal)
├── menu_principal.py         # Menú interactivo de consola
├── clasificador.py           # Wrapper de clasificación + tests de ejemplo
├── motor_clasificacion.py    # Motor de clasificación por palabras clave
├── plantillas_respuestas.py  # Respuestas automáticas por categoría
├── base_datos.py             # Capa de persistencia SQLite (CRUD)
├── storage_imagenes.py       # Almacenamiento y validación de fotos de reclamos
├── ia.py                     # Integración con Ollama (IA local)
├── pandas_analisis.py        # Estadísticas con Pandas
├── cliente_api.py            # Cliente HTTP para API externa (no integrado)
├── assets/                   # Imágenes y recursos (logo de La Rioja, favicon)
├── docs/                     # Documentación de diseño y especificación
├── markdowns/                # Material de las clases del curso
├── datos/                    # Base de datos SQLite (se crea sola, no se versiona)
├── storage/                  # Fotos subidas por los usuarios (no se versionan)
├── requirements.txt          # Dependencias de Python
└── README.md
```

---

## 🔍 Detalle de módulos

### `app.py`

Interfaz web con Streamlit. Configura `layout="wide"`, inyecta el CSS de la marca (paleta La Rioja, Montserrat + Plus Jakarta Sans) y organiza la navegación en el sidebar con el logo del municipio.

### `motor_clasificacion.py`

- `analizar_comentario(texto)` → `{"comentario", "categoria", "prioridad"}`

Normaliza el texto (minúsculas y sin acentos) y aplica reglas de palabras clave.

### `clasificador.py`

- `clasificar_comentario(comentario)` → `(categoria, prioridad)`

Ejecución directa: `python clasificador.py` — corre 8 tests de ejemplo.

### `plantillas_respuestas.py`

- `generar_respuesta(categoria)` → `str`

`RESPUESTAS` mapea cada categoría a una respuesta oficial. Fallback a `"OTRO"`.

### `base_datos.py`

Base de datos SQLite en `datos/reclamos.db`. Esquema `historial_reclamos`:

| Columna | Tipo |
|---------|------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `comentario` | TEXT |
| `categoria` | TEXT |
| `prioridad` | TEXT |
| `calle` | TEXT |
| `numero` | TEXT |

La dirección (calle y número) se guarda con cada reclamo y por ahora **no participa del análisis con IA**.

Tabla `reclamo_imagenes` (fotos por reclamo):

| Columna | Tipo |
|---------|------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `reclamo_id` | INTEGER (ref. `historial_reclamos.id`) |
| `ruta` | TEXT |

Funciones: `crear_tabla()`, `insertar_reclamo()` (devuelve el `id` creado), `insertar_imagen()`, `obtener_imagenes_reclamo()`, `obtener_todos_reclamos()`, `obtener_reclamo_por_id()`, `actualizar_reclamo()`, `eliminar_reclamo()`, `obtener_reclamos_por_categoria()`, `contar_total_reclamos()`, `contar_reclamos_por_categoria()`, `obtener_reclamos_por_prioridad()`.

### `storage_imagenes.py`

Almacena las fotos de los reclamos en `storage/fotos/{id_reclamo}/` (archivos) y guarda la referencia en la tabla `reclamo_imagenes`.

- `guardar_imagenes(uploaded_files, reclamo_id)` → `(guardadas, rechazadas)`
- `validar_archivo(uploaded_file)` → `(ok, motivo)` — valida formato (PNG/JPG/JPEG/GIF/WEBP) y tamaño máximo (15 MB).
- `eliminar_fotos_reclamo(reclamo_id)` — borra la carpeta de fotos del reclamo.
- `ruta_archivo(reclamo_id, nombre)` → ruta absoluta para visualizar la foto.

> La carpeta `storage/` **no se versiona** (está en `.gitignore`).

### `ia.py`

- `consultar_ia(prompt)` → `str`
- `generar_informe_ia(estadisticas_texto, rol, max_lineas)` → `str`
- `generar_email_ia(estadisticas_texto)` → `str`
- `resumir_comentario_ia(comentario)` → `str`
- `redactar_respuesta_ia(comentario, categoria)` → `str`

### `pandas_analisis.py`

Lee la base de datos y muestra las estadísticas con Pandas.

### `cliente_api.py`

Cliente HTTP para una API externa. **No integrado** en el flujo principal.

---

## 🗂️ Base de datos

La base `datos/reclamos.db` se **crea automáticamente** al ejecutar la app (primera corrida). No está versionada en git; en una PC nueva se regenera sola.

---

## 🧪 Verificación rápida

```bash
python clasificador.py   # ejecuta 8 tests de clasificación
python -m py_compile app.py ia.py base_datos.py  # chequea sintaxis
```

---

## 📚 Documentación adicional

- `docs/guia-visual-la-rioja.md` — guía de diseño de la Marca La Rioja.
- `docs/new_features.md` — especificación de la integración con Ollama.
- `markdowns/` — material de las clases (consigna, especificaciones, pandas, etc.).
