<p align="center">
  <img src="assets/cover.png" alt="slide-maker — design, redesign &amp; critique presentation-grade decks" width="100%">
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <b>Español</b>
</p>

# slide-maker — guía de diseño y operación

Este documento explica cómo está construida la skill y cómo razonar sobre ella, tanto para el usuario
(tú) como para cualquier persona que la mantenga. El modelo que *ejecuta* la skill lee `SKILL.md`
y la carpeta `references/`; este README es el mapa que está por encima de ellos.

---

## 1. Qué es

Una skill que construye, rediseña y critica presentaciones `.pptx` de calidad profesional para cualquier
audiencia, en cualquier idioma, con o sin plantilla, con o sin material de origen.
Su única convicción: **una diapositiva es una ayuda visual para quien expone, no un documento para leerse** —
de modo que cada decisión se optimiza para que se "entienda en segundos".

Es deliberadamente **interview-first** y **critic-gated**: pregunta antes de asumir,
y no confía en su propio resultado — un crítico independiente debe dar su consentimiento antes de que una presentación
se considere "terminada".

---

## 2. El pipeline principal (modo automático)

Cada presentación recorre siete pasos (`SKILL.md` es la especificación autoritativa):

| Paso | Qué ocurre | Por qué existe |
|---|---|---|
| **0 — Entrevista** | Un único lote de `AskUserQuestion`: plantilla, propósito y audiencia, material de origen, estilo. (+seguimientos: sede de la conferencia, nueva plantilla.) | Los requisitos del usuario son la fuente de verdad; tú los *aprendes*, nunca los heredas de una presentación previa. |
| **1 — Comprender** | Leer a fondo todo el material de origen; redactar un **informe de comprensión** (mensaje en una frase, contribuciones, esencia del método, para qué sirve *cada* figura/tabla, limitaciones). | Una presentación que se ve bien pero malinterpreta el trabajo no engaña a ningún experto. La fidelidad empieza aquí. |
| **2 — Lienzo** | Decidir la carpeta de salida (`~/Downloads/<deck>/`), cargar la plantilla *o* diseñar una apariencia adecuada al propósito; fijar paleta/fuentes (incluida la fuente CJK `EAFONT`). | La identidad de marca vive en los layouts; el diseño debe señalar el *tipo* de documento correcto antes de leer una sola palabra. |
| **3 — Planificar** | El número de diapositivas escala con el presupuesto de tiempo (~1/min): charla corta ~6–9, charla/clase/defensa/job-talk más larga ~10–20+. Una idea por diapositiva, conclusión primero, arco moldeado al propósito; ~15+ → despliegue por secciones (paso 4). | Es barato corregir un esquema; es caro corregir una presentación terminada. |
| **4 — Construir** | Un único script de construcción con los helpers de `deckkit`. Figuras de origen completas, márgenes, acentos rotatorios, ecuaciones reales, un solo idioma, builds/animación opcionales, notas del orador. | python-pptx es rápido; una ejecución del script, un único autor coherente. |
| **5 — Renderizar + bucle de crítica** | Renderizar a PNGs y *mirar*; luego un **subagente crítico independiente** devuelve JSON (consentimiento / revisar + correcciones por diapositiva). Repetir hasta el consentimiento. | python-pptx escribe a ciegas — los errores de desbordamiento/contraste/glifos solo aparecen en los píxeles. No eres el juez de tu propio trabajo. |
| **6 — Entrega + iteración** | Mostrar al usuario, dar la ruta de la carpeta, explicar la editabilidad + los dos carriles de cambio, integrar el feedback. | La presentación es suya para conservarla y seguir ajustándola — de forma segura. |

**El bucle actor–crítico es el motor de calidad.** Su *peso* escala con lo que está en juego (un
crítico para una reunión de laboratorio; un panel paralelo de 2–3 críticos con diferentes enfoques para una
conferencia/defensa/pitch), pero el bucle en sí no es negociable.

---

## 3. Dos modos

- **Automático (por defecto):** entrevista → construir → bucle de crítica hasta un listón alto → mostrar. El crítico
  captura la *calidad*.
- **Colaborativo (opt-in):** añade **puntos de aprobación** económicos — elegir una *dirección* (2–3
  diapositivas arquetipo reales renderizadas) → aprobar el *esquema* → construir el resto. Los puntos de aprobación
  capturan la *preferencia* (gusto), que un crítico no puede leer. El mismo motor por debajo;
  solo añade aprobaciones. (`references/collaborative-mode.md`, `scripts/archetypes.py`.)

---

## 4. Mapa de escenarios — qué camino toma una solicitud

La entrevista (paso 0, especialmente Q3) enruta la solicitud:

| El usuario quiere… | Camino |
|---|---|
| Una presentación a partir de su código/artículo/documento | Camino de construcción (pasos 1–6), rama de contenido |
| Una presentación sin material | Camino de construcción; redactar desde la experiencia + búsqueda web para fundamentar, confirmar el esquema |
| **Mejorar su propia** presentación | **Camino de rediseño** — diagnosticar primero, confirmar el alcance, reconstruir reutilizando su contenido/figuras (`references/redesign-existing-deck.md`) |
| Una presentación **con la apariencia de un ejemplo** | Imitación de estilo — redactar un informe de estilo, reproducir la apariencia (`references/style-analysis.md`) |
| Una charla de **conferencia** | Identificar + investigar en la web la sede (reglas, plantilla, audiencia), luego construir a la medida |
| Un **póster** | Acotado: un único lienzo grande; las reglas del oficio se mantienen, pero la skill está afinada para charlas — confirmar la especificación primero |
| Una presentación **no en inglés / CJK** | Fijar `EAFONT`, disciplina de un solo idioma, tipografía CJK (`references/multilingual.md`) |
| Una presentación **grande** (15+ diapositivas) | Despliegue opcional por secciones: `style.py` compartido, autores de sección en paralelo, `assemble.py`, panel de críticos (`references/large-deck-orchestration.md`) |
| **Ver opciones primero** | Puntos de aprobación del modo colaborativo |
| **Cambios tras la entrega** | Iterar de forma segura — nunca pisar las ediciones hechas a mano (`references/handoff-and-iteration.md`) |

---

## 5. Mapa de archivos

**Columna vertebral**
- `SKILL.md` — las instrucciones de operación que sigue el modelo (pasos 0–6, las reglas).

**Motor (`scripts/`)**
- `deckkit.py` — el kit de construcción: helpers de texto/forma/componente (`bullet`, `callout`,
  `chip`, `arrow`, `modbox`, `hrule`), ecuaciones (`eq_par`, `equation_png`),
  `speaker_notes`, comprobación de contraste, paleta/fuentes (incluida la fuente CJK `EAFONT`), reutilización de plantillas
  (`open_template`, `content_slide`) y el chrome sin plantilla (`blank_deck`,
  `title_bar`, `footer`). Impórtalo; no vuelvas a derivar las primitivas.
- `render_deck.sh` — `.pptx` → un PNG por diapositiva (LibreOffice → PDF → PNG). Multiplataforma;
  usa un perfil privado de LibreOffice para que los renders paralelos/coexistentes no colisionen.
- `check_env.sh` — preverificación única del toolchain.
- `anim.py` — inyecta el XML de timing de build/animación de PowerPoint que python-pptx no puede escribir.
- `assemble.py` — combina módulos de sección creados en paralelo en una sola presentación (sin fusiones frágiles).
- `archetypes.py` — construye las mismas diapositivas de vista previa por dirección para el punto de aprobación colaborativo.
- `inspect_template.py` — imprime los layouts/placeholders/logos de una plantilla.
- `extract_deck.py` — extrae texto/tablas/figuras *de* una presentación existente (rediseño + reconciliación).
- `export_notes.py` — exporta las notas del orador de una presentación a un guion de ensayo en texto plano.

**Juicio**
- `agents/critic.md` — el brief del crítico independiente + el esquema JSON.
- `references/review-rubrics.md` — rúbrica universal + capas por propósito (con respaldo en investigación).
- `references/design-principles.md` — el oficio y el "porqué".

**Referencias por escenario**
- `design-by-purpose.md` · `animation.md` · `multilingual.md` · `font-guidance.md` ·
  `style-analysis.md` · `redesign-existing-deck.md` · `collaborative-mode.md` ·
  `large-deck-orchestration.md` · `handoff-and-iteration.md`
- `examples/` — script de construcción resuelto, la convención de estilo compartido + módulo de sección.

**Externo (no forma parte de la skill)**
- `~/.claude/slide-templates/` — el registro personal de plantillas del usuario; léelo para las elecciones,
  escribe nuevos perfiles en él. Vacío para un usuario nuevo.

---

## 6. Principios de diseño integrados en la skill

1. **Los requisitos por encima de los artefactos.** Una plantilla, una presentación antigua o el gusto del modelo son
   *entradas*, no instrucciones. Cuando entran en conflicto con el requisito declarado, gana el
   requisito.
2. **Fidelidad estricta.** Cada afirmación/cifra/figura se remonta al material de origen. La única excepción
   es el contenido prospectivo claramente señalado.
3. **Crítica independiente.** Un agente aparte juzga los píxeles renderizados — su
   independencia es lo que hace que el "consentimiento" signifique algo.
4. **Paralelizar la recolección, nunca la comprensión.** Despliega la lectura/preparación de recursos; una sola mente
   sostiene el hilo conductor.
5. **Diseño adecuado al propósito.** Una defensa, un informe ejecutivo y una clase no deberían verse igual.
6. **Un solo idioma, mantenido de principio a fin.**
7. **El script es la fuente de verdad; el `.pptx` es un artefacto.** Reproducible, y
   seguro de iterar sin perder las ediciones del usuario.

---

## 7. Limitaciones conocidas (sé honesto sobre ellas)

- **La altura del texto se estima, no se mide.** python-pptx no puede conocer la altura del texto renderizado,
  por lo que las alturas de `bullet`/`callout` son estimaciones escaladas — el bucle de render (paso 5) es la forma de
  detectar el desbordamiento. Mira siempre los PNGs.
- **La animación no puede previsualizarse de forma estática.** Los renders muestran solo el estado final construido;
  el *orden* de build se verifica en PowerPoint real y se describe al usuario en la entrega.
- **Los scripts RTL (árabe/hebreo)** son un punto débil conocido — sin reflujo bidi.
- **Los pósters** se soportan solo de forma mínima; la skill está afinada para charlas.
- **Las fuentes no se incrustan** (limitación de python-pptx) — señala cualquier dependencia de fuente no estándar/CJK en la entrega.

---

## 8. Toolchain

`python-pptx`, `pymupdf` (render), `matplotlib` + `Pillow` (ecuaciones/gráficos) y
LibreOffice (`soffice`) para el renderizado. Ejecuta `bash scripts/check_env.sh` una vez en una máquina
nueva; imprime la corrección exacta para cualquier cosa que falte.
