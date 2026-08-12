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

# 3. Configurar credenciales (opcional, con valores por defecto no hace falta)
cp .env.example .env
# editar .env con usuario y contraseña del administrador
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

**Acceso por roles:**

- **Ciudadano (sin login)** — ve solo la sección **Nuevo reclamo** para reportar un problema. No necesita registrarse.
- **Administrador (con login)** — ve todas las secciones. Iniciá sesión desde el sidebar. Las contraseñas se guardan **hasheadas con bcrypt** en la base de datos `datos/reclamos.db` (tabla `usuarios`), nunca en texto plano. Los administradores se gestionan en la sección **Administradores** (agregar nuevos admins o eliminarlos).

**Configuración del administrador inicial (`.env`):**

1. Copiá `.env.example` → `.env`.
2. Editá usuario y contraseña **antes de la primera ejecución**:
   ```
   SMARTASSIST_ADMIN_USUARIO=admin
   SMARTASSIST_ADMIN_CLAVE=tu_clave_segura
   ```
3. `streamlit run app.py`. El admin se crea **solo la primera vez**; si ya existe en la base (`.db`) y querés regenerarlo, eliminá ese usuario desde la sección Administradores o borrá la fila en la tabla `usuarios`.

Secciones (administrador):

- **Nuevo reclamo** — ingresá el comentario del ciudadano y el sistema lo clasifica. Muestra una **vista previa del mapa** de la dirección apenas cargás la calle.
- **Historial** — consultá, filtrá, editá, eliminá, analizá con IA y **verificá la ubicación aproximada en Google Maps** de cada reclamo.
- **Estadísticas** — métricas y gráficos por categoría y prioridad.
- **Análisis Inteligente** — generá informe con IA, correo a gerencia y chat libre.
- **Administradores** — creá o eliminá usuarios con acceso al sistema.
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
├── autenticacion.py          # Autenticación de administradores (login)
├── validaciones.py           # Validación de datos de entrada (web y CLI)
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

- `url_mapa_reclamo(calle, numero)` → URL del embed de Google Maps para la dirección del reclamo (aproximada, sin API key).
- `mostrar_mapa(calle, numero, altura)` → renderiza el mapa dentro de un marco con `st.iframe`.

### `motor_clasificacion.py`

- `analizar_comentario(texto)` → `{"comentario", "categoria", "prioridad"}`

Normaliza el texto (minúsculas y sin acentos) y aplica reglas de palabras clave. Define la **prioridad por reglas** (primera palabra clave que coincida).

### `clasificador.py`

- `clasificar_comentario(comentario)` → `(categoria, prioridad)`

Ejecución directa: `python clasificador.py` — corre 8 tests de ejemplo.

> **Asignación final de prioridad:** en el alta web la prioridad por reglas se combina con una **segunda opinión de la IA** (`sugerir_prioridad_ia` + `combinar_prioridades`). Se toma siempre el nivel de mayor severidad (ALTA > MEDIA > BAJA), de modo que la IA puede escalar reclamos que las reglas no detectan bien. La CLI por ahora usa solo las reglas.

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
| `fecha` | TEXT (YYYY-MM-DD HH:MM:SS) |

La dirección (calle y número) se guarda con cada reclamo y por ahora **no participa del análisis con IA**.

Tabla `reclamo_imagenes` (fotos por reclamo):

| Columna | Tipo |
|---------|------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `reclamo_id` | INTEGER (ref. `historial_reclamos.id`) |
| `ruta` | TEXT |

Tabla `usuarios` (login de administradores):

| Columna | Tipo |
|---------|------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `usuario` | TEXT UNIQUE NOT NULL |
| `clave_hash` | TEXT (hash bcrypt) |
| `creado_en` | TEXT |

Funciones: `crear_tabla()`, `insertar_reclamo(..., fecha=None)` (devuelve el `id` creado; si `fecha` se omite registra la actual), `insertar_imagen()`, `obtener_imagenes_reclamo()`, `obtener_todos_reclamos()`, `obtener_reclamo_por_id()`, `actualizar_reclamo()`, `eliminar_reclamo()`, `obtener_reclamos_por_categoria()`, `contar_total_reclamos()`, `contar_reclamos_por_categoria()`, `obtener_reclamos_por_prioridad()`, `crear_usuario()`, `obtener_clave_hash()`, `existe_usuario()`, `eliminar_usuario()`, `obtener_usuarios()`. Para bases existentes, `crear_tabla()` agrega las columnas/tablas faltantes con `ALTER TABLE` / `CREATE TABLE` automáticos.

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
- `verificar_comentario_ia(comentario)` → `(bool, str)` — detecta spam/gibberish antes de guardar.
- `sugerir_prioridad_ia(comentario)` → `(prioridad|None, detalle)` — segunda opinión de prioridad con IA.
- `combinar_prioridades(prioridad_reglas, prioridad_ia)` → `(prioridad, origen)` — combina reglas e IA tomando la de mayor severidad.

### `pandas_analisis.py`

Lee la base de datos y muestra las estadísticas con Pandas.

### `autenticacion.py`

Backend de login con contraseñas hasheadas:

- `hash_clave(clave)` → `str` — genera un hash **bcrypt** para una contraseña.
- `verificar_clave(clave, clave_hash)` → `bool` — compara la contraseña en claro contra su hash.
- `crear_admin_inicial()` → `bool` — crea el administrador inicial (si no existe) a partir de las variables de entorno.
- `autenticar(usuario, clave)` → `bool` — valida las credenciales contra la base de datos.
- `usuario_existe(usuario)` → `bool` — indica si el usuario ya está registrado.
- `crear_usuario(usuario, clave)` — crea un usuario nuevo con su contraseña hasheada.

Usa `python-dotenv` para cargar `.env` (si existe) al importar, dando prioridad a las variables de entorno del sistema. Los usuarios se guardan en la tabla `usuarios` de `datos/reclamos.db` con la clave **hasheada con bcrypt** (nunca en texto plano).

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
