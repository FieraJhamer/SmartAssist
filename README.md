# SmartAssist AI Analyst

CLI en Python que clasifica comentarios de usuarios por categoría y prioridad, genera respuestas automáticas y persiste todo en SQLite.

## Requisitos

- Python 3.x

## Instalación

```bash
git clone <repo>
cd SmartAssist
```

## Uso

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
8. Salir
```

## Estructura

| Archivo | Rol |
|---------|-----|
| `menu_principal.py` | Punto de entrada, menú interactivo |
| `clasificador.py` | Wrapper que delega la clasificación |
| `motor_clasificacion.py` | Motor de clasificación por palabras clave |
| `plantillas_respuestas.py` | Plantillas de respuesta por categoría |
| `base_datos.py` | Capa de persistencia SQLite |
| `cliente_api.py` | Cliente HTTP para API externa (no integrado) |
| `datos/reclamos.db` | Base de datos SQLite |

## Módulos

### `menu_principal.py`

Funciones:
- `mostrar_historial()` — imprime todos los registros
- `generar_reporte()` — imprime reporte con total, desglose, categoría más frecuente y fecha/hora
- `mostrar_menu()` — muestra opciones y captura input
- `iniciar()` — bucle principal del programa

### `clasificador.py`

- `clasificar_comentario(comentario)` → `(categoria, prioridad)`

Ejecución directa: `python clasificador.py` — corre 8 tests de ejemplo.

### `motor_clasificacion.py`

- `analizar_comentario(texto)` → `{comentario, categoria, prioridad}`

Reglas de clasificación (case-insensitive):

| Palabras clave | Categoría | Prioridad |
|----------------|-----------|-----------|
| `ingresar` | ERROR_ACCESO | ALTA |
| `lento`, `demora`, `lenta` | RENDIMIENTO | MEDIA |
| `factura`, `cobro`, `pago`, `tarjeta`, `compra` | FACTURACION | ALTA |
| `dañado`, `equivocado`, `incompleto`, `faltante`, `destruido` | DEVOLUCION | ALTA |
| `baja`, `liquidar`, `saldar`, `rescindir` | CANCELACION | ALTA |
| (ninguna) | CONSULTA | BAJA |

### `plantillas_respuestas.py`

- `generar_respuesta(categoria)` → `str`

Variables: `RESPUESTAS` — dict que mapea categoría a texto de respuesta. Fallback a `"OTRO"`.

### `base_datos.py`

Esquema SQLite (`historial_reclamos`):

| Columna | Tipo |
|---------|------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT |
| `comentario` | TEXT |
| `categoria` | TEXT |
| `prioridad` | TEXT |

Funciones principales:
- `crear_tabla()` — crea la tabla si no existe
- `insertar_reclamo(comentario, categoria, prioridad)`
- `obtener_todos_reclamos()` → `list[tuple]`
- `obtener_reclamo_por_id(id)` → `tuple | None`
- `actualizar_reclamo(id, comentario, categoria, prioridad)`
- `eliminar_reclamo(id)`
- `obtener_reclamos_por_categoria(categoria)` → `list[tuple]`
- `contar_total_reclamos()` → `int`
- `contar_reclamos_por_categoria()` → `list[(str, int)]`
- `obtener_reclamos_por_prioridad(prioridad)` → `list[tuple]`
- `mostrar_historial()` → alias de `obtener_todos_reclamos()`
- `guardar_reclamo(c, cat, pri)` → alias de `insertar_reclamo()`
- `crear_base()` → alias de `crear_tabla()`

### `cliente_api.py`

- `analizar_comentario_con_api(comentario)` → `(categoria, prioridad)`

Envía POST a `URL_API_EXTERNA` con `{"texto": comentario}`. No integrado en el flujo principal.
