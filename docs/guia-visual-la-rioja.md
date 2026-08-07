# Guía de Diseño Web y Sistema de Estilos: Marca La Rioja

Esta guía define los lineamientos UI/UX y el sistema de diseño para el desarrollo de interfaces web basadas en la identidad visual oficial de **LA RIOJA - Argentina**. Está optimizada para consumo directo por **Claude Code** y desarrolladores frontend.

---

## 1. Análisis Visual del Logo

### 1.1. Geometría y Morfología
- **Composición Isométrica / Tangram:** El isotipo está construido mediante triángulos rectángulos con **vértices redondeados** (soft corners). Las formas representan abstracciones dinámicas de la topografía montañosa (cordillera/cerros), arquitectura regional y dinamismo cultural.
- **Ritmo y Dirección:** El juego de triángulos alternados crea una sensación de avance, innovación y estructura limpia.
- **Tipografía del Logo:** 
  - **"LA RIOJA":** Sans-serif geométrica, en mayúsculas sostenidas, de peso ultra-bold/heavy, trazado limpio y compacto.
  - **"- Argentina":** Sans-serif humanista/geométrica en caja baja/alta, peso medium, generando equilibrio formal.

### 1.2. ADN de la Marca
- **Personalidad:** Vital, moderna, institucional pero cercana, cálida, estructurada y de alto impacto visual.
- **Enfoque Digital:** Minimalismo con presencia fuerte del color rojo, priorizando espacios en blanco amplia respiración visual y legibilidad.

---

## 2. Paleta de Colores

De acuerdo con el requerimiento expreso, el esquema cromático base utiliza **Blanco Puro** como lienzo y el **Rojo Oficial de la Marca** como color identitario primario. Para asegurar accesibilidad (WCAG 2.1), jerarquía visual y funcionalidad UI, se establecen los siguientes matices y tonos neutros derivados:

### 2.1. Colores Principales
| Rol de Color | Nombre | HEX | RGB | HSL | Uso Principal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primario Marca** | Rojo La Rioja | `#E61B36` | `rgb(230, 27, 54)` | `352°, 81%, 50%` | Botones primarios, acentos clave, marcas de identidad, estados activos. |
| **Fondo Base** | Blanco Puro | `#FFFFFF` | `rgb(255, 255, 255)` | `0°, 0%, 100%` | Fondo principal de la web, contenedores primarios, tarjetas destacadas. |

### 2.2. Acentos y Escala Funcional Derivada
| Rol de Color | Nombre | HEX | RGB | Uso Principal |
| :--- | :--- | :--- | :--- | :--- |
| **Texto Principal** | Neutro Oscuro | `#1A0B0E` | `rgb(26, 11, 14)` | Títulos y texto de lectura. Aporta contraste extremo (17.5:1) sin ser negro puro. |
| **Texto Secundario**| Neutro Medio | `#524346` | `rgb(82, 67, 70)` | Subtítulos, descripciones secundarias, metadatos y labels de apoyo. |
| **Hover / Active** | Rojo Profundo | `#C4102A` | `rgb(196, 16, 42)` | Estados hover/press de botones rojos y enlaces activos. |
| **Superficie Suave**| Rojo Subtilo | `#FFF0F2` | `rgb(255, 240, 242)` | Fondos de banners, cards secundarias, badges y highlighting. |
| **Borde / Separador**| Neutro Borde | `#E5D8DA` | `rgb(229, 216, 218)` | Líneas divisorias, bordes de inputs y tarjetería. |

---

## 3. Sistema Tipográfico

Para reflejar la geometría del logo y garantizar la máxima legibilidad en dispositivos digitales:

### 3.1. Tipografías Recomendadas (Google Fonts)
- **Titulares y Display:** `Montserrat` o `Outfit` (Sans-serif geométrica con gran peso visual).
- **Cuerpo de Texto y UI:** `Plus Jakarta Sans` o `Inter` (Sans-serif con excelente legibilidad en pantallas).

### 3.2. Escala Tipográfica y Pesos

```css
/* Escala tipográfica recomendada */
--font-sans: 'Plus Jakarta Sans', system-ui, sans-serif;
--font-heading: 'Montserrat', system-ui, sans-serif;

/* Jerarquía */
h1 { font-family: var(--font-heading); font-weight: 800; font-size: 2.75rem; line-height: 1.15; letter-spacing: -0.02em; }
h2 { font-family: var(--font-heading); font-weight: 700; font-size: 2.00rem; line-height: 1.20; letter-spacing: -0.01em; }
h3 { font-family: var(--font-heading); font-weight: 700; font-size: 1.50rem; line-height: 1.30; }
h4 { font-family: var(--font-heading); font-weight: 600; font-size: 1.25rem; line-height: 1.40; }
body { font-family: var(--font-sans); font-weight: 400; font-size: 1.00rem; line-height: 1.60; color: #1A0B0E; }
small { font-family: var(--font-sans); font-weight: 500; font-size: 0.875rem; color: #524346; }
```

---

## 4. Lenguaje de Diseño y Estética UI

### 4.1. Radios de Borde (Border Radius)
Inspirados en las esquinas suavizadas de los triángulos del logo:
- **Botones e Inputs:** `8px` (`rounded-md`)
- **Tarjetas / Cards:** `16px` (`rounded-2xl`)
- **Modales y Hero Banners:** `24px` (`rounded-3xl`)
- **Badges / Pills:** `9999px` (`rounded-full`)

### 4.2. Sombras y Elevación
Se evitan sombras pesadas. Las elevaciones deben ser limpias con una ligera infusión cálida/roja en la sombra:
- **Card Shadow (Rest):** `0px 4px 20px rgba(26, 11, 14, 0.04)`
- **Card Shadow (Hover):** `0px 12px 32px rgba(230, 27, 54, 0.12)`
- **Modal Shadow:** `0px 20px 40px rgba(26, 11, 14, 0.15)`

### 4.3. Elementos Geométricos Decorativos
- **Motivo Triangulado (Pattern):** Utilizar patrones geométricos basados en triángulos con opacidad ultraligera (`rgba(230, 27, 54, 0.04)`) en hero sections o divisores.
- **Cortes Diagonales / Accents:** Accent bars horizontales de `4px` de grosor con `background-color: #E61B36` y esquinas redondeadas para subrayar títulos principales o destacar secciones.

---

## 5. Componentes de UI Básicos

### 5.1. Botones
```html
<!-- Botón Primario -->
<button class="btn-primary">
  Explorar
</button>

<!-- Botón Secundario / Outline -->
<button class="btn-outline">
  Saber más
</button>
```

```css
.btn-primary {
  background-color: #E61B36;
  color: #FFFFFF;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 4px 14px rgba(230, 27, 54, 0.25);
}

.btn-primary:hover {
  background-color: #C4102A;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(230, 27, 54, 0.35);
}

.btn-outline {
  background-color: #FFFFFF;
  color: #E61B36;
  border: 2px solid #E61B36;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.2s ease-in-out;
}

.btn-outline:hover {
  background-color: #FFF0F2;
  border-color: #C4102A;
  color: #C4102A;
}
```

### 5.2. Tarjetas (Cards)
```css
.card {
  background-color: #FFFFFF;
  border: 1px solid #E5D8DA;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 20px rgba(26, 11, 14, 0.04);
}

.card:hover {
  border-color: #E61B36;
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(230, 27, 54, 0.12);
}
```

---

## 6. Archivos de Configuración para Proyectos

### 6.1. Variables CSS (`styles/variables.css`)
```css
:root {
  /* Marca Primaria */
  --color-primary: #E61B36;
  --color-primary-hover: #C4102A;
  --color-primary-light: #FFF0F2;
  
  /* Superficie y Neutros */
  --color-bg-main: #FFFFFF;
  --color-surface: #FFFFFF;
  --color-text-main: #1A0B0E;
  --color-text-muted: #524346;
  --color-border: #E5D8DA;

  /* Geometría */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  /* Sombras */
  --shadow-sm: 0 2px 8px rgba(26, 11, 14, 0.04);
  --shadow-md: 0 6px 20px rgba(26, 11, 14, 0.06);
  --shadow-brand: 0 8px 24px rgba(230, 27, 54, 0.18);
}
```

### 6.2. Configuración de Tailwind CSS (`tailwind.config.js`)
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#E61B36',
          dark: '#C4102A',
          light: '#FFF0F2',
        },
        neutral: {
          dark: '#1A0B0E',
          muted: '#524346',
          border: '#E5D8DA',
        }
      },
      fontFamily: {
        heading: ['Montserrat', 'Outfit', 'sans-serif'],
        body: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
      },
      borderRadius: {
        'brand-card': '16px',
        'brand-btn': '8px',
      },
      boxShadow: {
        'brand': '0 8px 24px rgba(230, 27, 54, 0.18)',
        'card-hover': '0 12px 32px rgba(230, 27, 54, 0.12)',
      }
    },
  },
  plugins: [],
}
```

---

## 7. Reglas para Agentes de IA (Claude Code / Cursor)

Si estás utilizando **Claude Code** para generar código en este proyecto, adjunta o haz referencia a este archivo `.md` y añade el siguiente prompt de instrucción:

> **Instrucciones para Claude Code:**
> 1. Utiliza la paleta especificada en este documento. El color primario **debe** ser `#E61B36` y el fondo principal blanco `#FFFFFF`.
> 2. Mantén un diseño limpio, moderno, con abundante espacio blanco (*whitespaces*) y alta legibilidad.
> 3. Utiliza esquinas suavizadas (`8px` en botones, `16px` en tarjetas).
> 4. Asegura que los textos mantengan un alto contraste usando `#1A0B0E` para títulos sobre fondo blanco, o `#FFFFFF` para texto sobre botones o contenedores `#E61B36`.
> 5. Incorpora detalles geométricos suaves o bordes acentuados en color `#E61B36` para evocar la estética del logo.
