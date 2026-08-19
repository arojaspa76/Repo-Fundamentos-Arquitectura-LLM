/**
 * create_presentation.js
 * Sesión 1 — Fundamentos de Arquitectura LLM
 * Genera presentación profesional con pptxgenjs
 *
 * Ejecutar: node create_presentation.js
 */

const pptxgen = require("pptxgenjs");

// ── Paleta de colores ────────────────────────────────────────────────────
const C = {
  // Fondos
  bgDark:    "0D1117",   // Fondo principal oscuro
  bgCard:    "161B22",   // Cards / bloques de contenido
  bgMid:     "21262D",   // Superficies secundarias
  bgLight:   "30363D",   // Bordes, divisores

  // Acentos
  cyan:      "58A6FF",   // Azul eléctrico — acento principal
  green:     "3FB950",   // Verde — éxito, capacidades
  coral:     "FF7B72",   // Coral — limitaciones, alertas
  purple:    "D2A8FF",   // Morado — embeddings, vectores
  yellow:    "E3B341",   // Amarillo — advertencias, notas

  // Texto
  textPri:   "E6EDF3",   // Texto principal (off-white)
  textSec:   "8B949E",   // Texto secundario (gris)
  textDim:   "484F58",   // Texto terciario (muy oscuro)

  // Fondos claros (para slides de tema)
  bgTheme1:  "0A1628",   // Transformer — azul muy oscuro
  bgTheme2:  "0F0A1E",   // Embeddings — morado muy oscuro
  bgTheme3:  "0A1A0A",   // Capacidades — verde muy oscuro
};

// ── Tipografía ────────────────────────────────────────────────────────────
const F = {
  title:  "Calibri",
  body:   "Calibri",
  mono:   "Courier New",
};

// ── Helper: fondo oscuro uniforme para todos los slides ──────────────────
function setDarkBg(slide, bgColor = C.bgDark) {
  slide.addShape("RECTANGLE", {
    x: 0, y: 0, w: "100%", h: "100%",
    fill: { color: bgColor },
    line: { color: bgColor },
  });
}

// ── Helper: badge de tema (pill colorido) ─────────────────────────────────
function addThemeBadge(slide, label, color, x = 0.4, y = 0.25) {
  slide.addShape("ROUNDED_RECTANGLE", {
    x, y, w: 2.2, h: 0.30,
    fill: { color },
    line: { color },
    rectRadius: 0.08,
  });
  slide.addText(label, {
    x, y, w: 2.2, h: 0.30,
    fontSize: 9, bold: true, color: C.bgDark,
    align: "center", valign: "middle",
    fontFace: F.body, margin: 0,
  });
}

// ── Helper: tarjeta oscura ────────────────────────────────────────────────
function addCard(slide, x, y, w, h, color = C.bgCard, lineColor = C.bgLight) {
  slide.addShape("ROUNDED_RECTANGLE", {
    x, y, w, h,
    fill: { color },
    line: { color: lineColor, width: 1 },
    rectRadius: 0.10,
  });
}

// ── Helper: título de sección ─────────────────────────────────────────────
function addSectionTitle(slide, text, subtitle = "") {
  slide.addText(text, {
    x: 0.4, y: 0.75, w: 9.2, h: 0.65,
    fontSize: 34, bold: true, color: C.textPri,
    fontFace: F.title, align: "left",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.4, y: 1.35, w: 9.2, h: 0.30,
      fontSize: 14, color: C.textSec,
      fontFace: F.body, align: "left",
    });
  }
}

// ── Helper: ícono en círculo ──────────────────────────────────────────────
function addIconCircle(slide, emoji, x, y, size = 0.55, bgColor = C.cyan) {
  slide.addShape("OVAL", {
    x, y, w: size, h: size,
    fill: { color: bgColor },
    line: { color: bgColor },
  });
  slide.addText(emoji, {
    x: x - 0.02, y: y + 0.01, w: size + 0.04, h: size,
    fontSize: size * 20, align: "center", valign: "middle",
    margin: 0,
  });
}

// ── Helper: stat callout grande ───────────────────────────────────────────
function addStatCallout(slide, number, label, x, y, accentColor = C.cyan) {
  addCard(slide, x, y, 2.1, 1.3, C.bgCard, accentColor);
  slide.addText(number, {
    x, y: y + 0.10, w: 2.1, h: 0.75,
    fontSize: 40, bold: true, color: accentColor,
    fontFace: F.title, align: "center", margin: 0,
  });
  slide.addText(label, {
    x, y: y + 0.85, w: 2.1, h: 0.35,
    fontSize: 10, color: C.textSec,
    fontFace: F.body, align: "center", margin: 0,
  });
}

// ─────────────────────────────────────────────────────────────────────────
// INICIAR PRESENTACIÓN
// ─────────────────────────────────────────────────────────────────────────

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 inches

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 01 — PORTADA
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s, "080D14");

  // Líneas decorativas tipo "circuito" — rectángulos sutiles
  s.addShape("RECTANGLE", { x: 0, y: 0, w: 0.04, h: "100%", fill: { color: C.cyan }, line: { color: C.cyan } });
  s.addShape("RECTANGLE", { x: 0.06, y: 0, w: 0.015, h: "100%", fill: { color: "1A3A5C" }, line: { color: "1A3A5C" } });

  // Etiqueta del curso
  s.addShape("ROUNDED_RECTANGLE", {
    x: 0.55, y: 0.55, w: 3.8, h: 0.35,
    fill: { color: "112233" },
    line: { color: C.cyan, width: 1 },
    rectRadius: 0.08,
  });
  s.addText("FUNDAMENTOS DE ARQUITECTURA LLM", {
    x: 0.55, y: 0.55, w: 3.8, h: 0.35,
    fontSize: 9, bold: true, color: C.cyan,
    fontFace: F.body, align: "center", valign: "middle", margin: 0,
  });

  // Título principal
  s.addText("Sesión 1", {
    x: 0.55, y: 1.15, w: 9.0, h: 0.45,
    fontSize: 20, color: C.textSec, fontFace: F.body, align: "left",
  });
  s.addText("Arquitectura y\nComponentes\nEsenciales de los LLM", {
    x: 0.55, y: 1.52, w: 8.5, h: 2.0,
    fontSize: 42, bold: true, color: C.textPri,
    fontFace: F.title, align: "left",
  });

  // Línea separadora
  s.addShape("RECTANGLE", { x: 0.55, y: 3.55, w: 4.5, h: 0.025, fill: { color: C.cyan }, line: { color: C.cyan } });

  // Subtítulo / descripción
  s.addText("Capítulo 1 · Conceptos Fundamentales de LLM", {
    x: 0.55, y: 3.70, w: 7.0, h: 0.30,
    fontSize: 13, color: C.textSec, fontFace: F.body, align: "left",
  });

  // Temas a cubrir
  const temas = [
    "Arquitectura Transformer: atención y tokens",
    "Embeddings, contexto y ventanas de contexto",
    "Capacidades y limitaciones típicas",
  ];
  temas.forEach((t, i) => {
    const colors = [C.cyan, C.purple, C.green];
    s.addShape("OVAL", {
      x: 0.55, y: 4.10 + i * 0.33, w: 0.18, h: 0.18,
      fill: { color: colors[i] }, line: { color: colors[i] },
    });
    s.addText(t, {
      x: 0.82, y: 4.08 + i * 0.33, w: 6.5, h: 0.22,
      fontSize: 11, color: C.textSec, fontFace: F.body, align: "left",
    });
  });

  // Decoración — gran círculo translúcido
  s.addShape("OVAL", {
    x: 6.8, y: 0.6, w: 4.5, h: 4.5,
    fill: { color: "0A1E35" },
    line: { color: "1A3A5C", width: 1.5 },
  });
  s.addShape("OVAL", {
    x: 7.5, y: 1.2, w: 3.1, h: 3.1,
    fill: { color: "061220" },
    line: { color: C.cyan, width: 1 },
  });
  s.addText("🤖", { x: 7.6, y: 1.5, w: 3.0, h: 2.5, fontSize: 80, align: "center", valign: "middle" });

  s.addNotes("Slide de portada. Presenta el curso y los 3 temas de la sesión. Tiempo estimado de la sesión: 2-3 horas con ejercicios prácticos.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 02 — AGENDA
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);

  s.addText("Agenda de la Sesión", {
    x: 0.4, y: 0.30, w: 9.2, h: 0.55,
    fontSize: 32, bold: true, color: C.textPri, fontFace: F.title,
  });

  const blocks = [
    { num: "01", title: "Arquitectura Transformer", items: ["¿Qué es un Transformer?", "Mecanismo de auto-atención", "Tokens y tokenización", "Encoder-Decoder vs Decoder-Only"], color: C.cyan, emoji: "🔧", x: 0.4 },
    { num: "02", title: "Embeddings y Contexto", items: ["¿Qué son los embeddings?", "Espacio vectorial semántico", "Ventana de contexto", "Estrategias para contextos largos"], color: C.purple, emoji: "🧭", x: 3.55 },
    { num: "03", title: "Capacidades y Límites", items: ["¿Qué hacen bien los LLM?", "Limitaciones conocidas", "El problema de las alucinaciones", "Comparativa de modelos"], color: C.green, emoji: "⚖️", x: 6.70 },
  ];

  blocks.forEach(b => {
    addCard(s, b.x, 0.95, 2.95, 4.30, C.bgCard, b.color);
    // Header del bloque
    s.addShape("ROUNDED_RECTANGLE", {
      x: b.x, y: 0.95, w: 2.95, h: 0.85,
      fill: { color: C.bgMid },
      line: { color: b.color, width: 1 },
      rectRadius: 0.10,
    });
    s.addText(b.emoji + "  " + b.num, {
      x: b.x + 0.1, y: 0.98, w: 1.5, h: 0.40,
      fontSize: 16, bold: true, color: b.color, fontFace: F.title, margin: 0,
    });
    s.addText(b.title, {
      x: b.x + 0.1, y: 1.38, w: 2.75, h: 0.30,
      fontSize: 11, bold: true, color: C.textPri, fontFace: F.body, margin: 0,
    });

    b.items.forEach((item, i) => {
      s.addShape("OVAL", {
        x: b.x + 0.15, y: 2.00 + i * 0.70, w: 0.12, h: 0.12,
        fill: { color: b.color }, line: { color: b.color },
      });
      s.addText(item, {
        x: b.x + 0.33, y: 1.93 + i * 0.70, w: 2.5, h: 0.60,
        fontSize: 11, color: C.textPri, fontFace: F.body,
        align: "left", valign: "middle",
      });
    });
  });

  // Demo bar al fondo
  addCard(s, 0.4, 5.28, 9.2, 0.25, "0A1E35", C.cyan);
  s.addText("🛠️  Práctica en vivo: Ollama + FastAPI + React · Ejemplos en Python · Ejercicios guiados", {
    x: 0.4, y: 5.28, w: 9.2, h: 0.25,
    fontSize: 10, color: C.cyan, fontFace: F.body, align: "center", valign: "middle", margin: 0,
  });

  s.addNotes("Presenta la agenda de la sesión. Explica que cada tema tiene teoría + demo en vivo + ejercicio práctico. La sesión incluye configuración de Ollama si los estudiantes no lo tienen.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 03 — SEPARADOR TEMA 1
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s, C.bgTheme1);

  s.addShape("RECTANGLE", { x: 0, y: 0, w: "100%", h: "100%", fill: { color: C.bgTheme1 }, line: { color: C.bgTheme1 } });

  s.addText("TEMA 01", {
    x: 0.5, y: 1.1, w: 9.0, h: 0.45,
    fontSize: 13, bold: true, color: C.cyan, fontFace: F.body, align: "center",
    charSpacing: 8,
  });
  s.addText("Arquitectura\nTransformer", {
    x: 0.5, y: 1.55, w: 9.0, h: 1.8,
    fontSize: 60, bold: true, color: C.textPri, fontFace: F.title, align: "center",
  });
  s.addText("Atención · Tokens · Arquitectura", {
    x: 0.5, y: 3.45, w: 9.0, h: 0.40,
    fontSize: 16, color: C.textSec, fontFace: F.body, align: "center",
  });

  s.addShape("RECTANGLE", { x: 3.5, y: 4.0, w: 3.0, h: 0.03, fill: { color: C.cyan }, line: { color: C.cyan } });

  s.addNotes("TEMA 1 — Arquitectura Transformer. Este tema cubre los fundamentos técnicos de la arquitectura que impulsa los LLMs modernos. Paper de referencia: 'Attention is All You Need' (Vaswani et al., 2017).");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 04 — ¿QUÉ ES UN LLM?
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 1 · TRANSFORMERS", C.cyan);

  addSectionTitle(s, "¿Qué es un LLM?", "Large Language Model — Modelo de Lenguaje Extenso");

  // Definición principal
  addCard(s, 0.4, 1.75, 9.2, 1.05, "0A1E35", C.cyan);
  s.addText("\"Un LLM es un modelo de IA entrenado con enormes volúmenes de texto que aprende a predecir\nla siguiente palabra (token) dada una secuencia de entrada — y lo hace tan bien que emula la comprensión.\"", {
    x: 0.6, y: 1.82, w: 8.8, h: 0.90,
    fontSize: 13, color: C.textPri, fontFace: F.body, align: "center", valign: "middle",
    italic: true,
  });

  // 4 características clave
  const facts = [
    { icon: "📚", title: "Preentrenados", desc: "Trillones de tokens de texto (libros, web, código)", color: C.cyan },
    { icon: "🧠", title: "Redes Neuronales", desc: "Millones o billones de parámetros ajustables", color: C.purple },
    { icon: "🔮", title: "Generativos", desc: "Producen texto nuevo, no recuperan texto guardado", color: C.green },
    { icon: "🎯", title: "Few-shot Learning", desc: "Aprenden tareas nuevas con pocos ejemplos", color: C.yellow },
  ];
  facts.forEach((f, i) => {
    const x = 0.4 + i * 2.35;
    addCard(s, x, 2.90, 2.25, 2.55, C.bgCard, f.color);
    s.addText(f.icon, { x, y: 3.00, w: 2.25, h: 0.60, fontSize: 28, align: "center" });
    s.addText(f.title, {
      x: x + 0.08, y: 3.58, w: 2.09, h: 0.35,
      fontSize: 12, bold: true, color: f.color, fontFace: F.body, align: "center", margin: 0,
    });
    s.addText(f.desc, {
      x: x + 0.08, y: 3.92, w: 2.09, h: 1.35,
      fontSize: 10.5, color: C.textSec, fontFace: F.body, align: "center",
    });
  });

  s.addNotes("Definición de LLM. Puntos clave a resaltar:\n- 'Predecir el siguiente token' es la tarea central, todo lo demás emerge de ella\n- GPT-4 tiene ~1.8 TRILLONES de parámetros (estimado)\n- El entrenamiento se hace en clusters de miles de GPUs durante semanas\n- Los modelos no 'saben' cosas - capturan patrones estadísticos de texto");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 05 — ARQUITECTURA TRANSFORMER
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 1 · TRANSFORMERS", C.cyan);

  addSectionTitle(s, "La Arquitectura Transformer", "Vaswani et al. — 'Attention Is All You Need' (2017)");

  // Panel izquierdo: diagrama simplificado
  addCard(s, 0.4, 1.75, 4.5, 3.70, C.bgCard, C.cyan);

  // Diagrama visual del transformer
  const blocks_t = [
    { label: "📤 Output Tokens", y: 1.90, color: C.green },
    { label: "🔤 Linear + Softmax", y: 2.35, color: C.bgMid },
    { label: "🎯 Nx × Decoder Block", y: 2.80, color: C.cyan },
    { label: "🔄 Nx × Encoder Block", y: 3.25, color: C.purple },
    { label: "📐 Positional Encoding", y: 3.70, color: C.bgMid },
    { label: "📥 Input Tokens", y: 4.15, color: C.yellow },
  ];
  blocks_t.forEach(b => {
    addCard(s, 0.65, b.y, 4.0, 0.38, C.bgMid, b.color);
    s.addText(b.label, {
      x: 0.65, y: b.y, w: 4.0, h: 0.38,
      fontSize: 11, color: C.textPri, fontFace: F.body, align: "center", valign: "middle", margin: 0,
    });
    if (b.y < 4.15) {
      s.addShape("RECTANGLE", { x: 2.45, y: b.y + 0.38, w: 0.1, h: 0.07, fill: { color: C.textDim }, line: { color: C.textDim } });
    }
  });

  // Panel derecho: conceptos clave
  const concepts = [
    { icon: "👁️", title: "Self-Attention", desc: "Cada token puede 'ver' y relacionarse con TODOS los demás tokens a la vez. Esto permite capturar dependencias de largo alcance.", color: C.cyan },
    { icon: "📍", title: "Positional Encoding", desc: "Los transformers no procesan tokens en secuencia — un vector de posición les indica el orden de cada token.", color: C.purple },
    { icon: "🔁", title: "Bloques Nx", desc: "Se apilan múltiples capas idénticas (6-96 o más en modelos grandes). Cada capa refina la representación del texto.", color: C.green },
    { icon: "⚡", title: "Paralelismo", desc: "A diferencia de RNNs, todos los tokens se procesan en paralelo durante el entrenamiento = mucho más rápido.", color: C.yellow },
  ];

  concepts.forEach((c, i) => {
    const y = 1.75 + i * 0.93;
    addCard(s, 5.1, y, 4.5, 0.85, C.bgCard, C.bgLight);
    s.addText(c.icon, { x: 5.15, y: y + 0.10, w: 0.55, h: 0.55, fontSize: 22, align: "center" });
    s.addText(c.title, {
      x: 5.75, y: y + 0.05, w: 3.75, h: 0.28,
      fontSize: 12, bold: true, color: c.color, fontFace: F.body, margin: 0,
    });
    s.addText(c.desc, {
      x: 5.75, y: y + 0.30, w: 3.75, h: 0.50,
      fontSize: 10, color: C.textSec, fontFace: F.body,
    });
  });

  s.addNotes("Arquitectura Transformer.\n\nPuntos clave:\n- Antes de los transformers existían RNNs/LSTMs que procesaban tokens UNO a la vez, de izquierda a derecha\n- El self-attention fue la innovación clave: cada token 'presta atención' a todos los demás\n- En GPT-4 hay estimados ~120 capas (Nx). En llama3.2 3B hay 28 capas\n- El positional encoding es necesario porque sin él el transformer no sabría el orden de las palabras\n\nAnálogia: imagina que tienes 10 personas (tokens) en una sala. Las RNNs les hacen pasar el mensaje de uno a uno. Los Transformers hacen que todos se hablen entre sí al mismo tiempo.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 06 — MECANISMO DE ATENCIÓN
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 1 · TRANSFORMERS", C.cyan);

  addSectionTitle(s, "Mecanismo de Self-Attention", "¿Cómo cada token 'decide' qué importa?");

  // Ejemplo visual con frase
  addCard(s, 0.4, 1.70, 9.2, 0.60, "0A1E35", C.cyan);
  s.addText("Ejemplo: \"El banco financiero procesó la transacción\"", {
    x: 0.6, y: 1.78, w: 8.8, h: 0.42,
    fontSize: 15, bold: true, color: C.textPri, fontFace: F.title, align: "center",
  });

  // Tokens como cajas
  const tokens = ["El", "banco", "financiero", "procesó", "la", "transacción"];
  const tokenColors = [C.bgMid, C.cyan, C.green, C.bgMid, C.bgMid, C.yellow];
  const tw = 1.42;
  tokens.forEach((tok, i) => {
    addCard(s, 0.4 + i * tw, 2.40, 1.32, 0.45, tokenColors[i] === C.bgMid ? C.bgCard : "0A1420", tokenColors[i]);
    s.addText(tok, {
      x: 0.4 + i * tw, y: 2.40, w: 1.32, h: 0.45,
      fontSize: 13, bold: tokenColors[i] !== C.bgMid, color: tokenColors[i] === C.bgMid ? C.textSec : tokenColors[i],
      fontFace: F.mono, align: "center", valign: "middle", margin: 0,
    });
  });

  // Línea de atención (banco → financiero, banco → transacción)
  s.addText("↗ atención alta", { x: 1.15, y: 2.90, w: 2.5, h: 0.25, fontSize: 9, color: C.cyan, fontFace: F.body, italic: true });
  s.addText("↗ atención alta", { x: 5.6, y: 2.90, w: 2.5, h: 0.25, fontSize: 9, color: C.yellow, fontFace: F.body, italic: true });

  // Explicación QKV
  const qkv = [
    { letter: "Q", name: "Query", desc: "¿Qué estoy buscando?", color: C.cyan },
    { letter: "K", name: "Key",   desc: "¿Qué tengo yo para ofrecer?", color: C.purple },
    { letter: "V", name: "Value", desc: "¿Qué información entrego si soy relevante?", color: C.green },
  ];

  addCard(s, 0.4, 3.25, 5.9, 2.15, C.bgCard, C.bgLight);
  s.addText("Matrices Q · K · V (Query, Key, Value)", {
    x: 0.55, y: 3.32, w: 5.6, h: 0.30,
    fontSize: 12, bold: true, color: C.textPri, fontFace: F.body, margin: 0,
  });
  qkv.forEach((q, i) => {
    const y = 3.68 + i * 0.55;
    s.addShape("ROUNDED_RECTANGLE", {
      x: 0.55, y, w: 0.35, h: 0.35,
      fill: { color: q.color }, line: { color: q.color }, rectRadius: 0.05,
    });
    s.addText(q.letter, { x: 0.55, y, w: 0.35, h: 0.35, fontSize: 14, bold: true, color: C.bgDark, align: "center", valign: "middle", margin: 0 });
    s.addText(q.name + "  —  " + q.desc, {
      x: 0.98, y: y + 0.03, w: 5.2, h: 0.30,
      fontSize: 11, color: C.textSec, fontFace: F.body, align: "left",
    });
  });

  // Formula simplificada
  addCard(s, 0.4, 5.12, 5.9, 0.38, "030810", C.cyan);
  s.addText("Attention(Q,K,V) = softmax( Q·Kᵀ / √dk ) · V", {
    x: 0.5, y: 5.14, w: 5.7, h: 0.34,
    fontSize: 13, color: C.cyan, fontFace: F.mono, align: "center", valign: "middle", margin: 0,
  });

  // Panel derecho: Multi-Head Attention
  addCard(s, 6.5, 3.25, 3.1, 2.25, C.bgCard, C.bgLight);
  s.addText("Multi-Head Attention", {
    x: 6.6, y: 3.32, w: 2.9, h: 0.30,
    fontSize: 12, bold: true, color: C.textPri, fontFace: F.body, margin: 0,
  });
  s.addText("GPT-4 tiene 96 'cabezas' de atención en paralelo, cada una aprende diferentes tipos de relaciones:", {
    x: 6.6, y: 3.65, w: 2.9, h: 0.65,
    fontSize: 10, color: C.textSec, fontFace: F.body,
  });
  ["Sintaxis gramatical", "Referencia pronombres", "Relaciones semánticas", "Patrones de código"].forEach((h, i) => {
    s.addShape("OVAL", { x: 6.6, y: 4.35 + i * 0.25, w: 0.12, h: 0.12, fill: { color: C.cyan }, line: { color: C.cyan } });
    s.addText(h, { x: 6.78, y: 4.32 + i * 0.25, w: 2.7, h: 0.22, fontSize: 10, color: C.textPri, fontFace: F.body });
  });

  s.addNotes("Self-Attention:\n\nConcepto clave: El token 'banco' necesita saber si significa institución financiera o asiento físico. El mecanismo de atención le permite mirar el resto de la oración ('financiero', 'transacción') y decidir el contexto.\n\nLa fórmula Q·Kᵀ / √dk:\n- Q·Kᵀ = cuánto 'coincide' mi búsqueda con lo que ofrece cada token\n- / √dk = normalizamos para evitar que los valores sean muy grandes\n- softmax = convertir los scores en probabilidades que suman 1\n- × V = ponderar los valores por esas probabilidades\n\nAnálogía del buscador: si haces una búsqueda (Query), los documentos tienen palabras clave (Keys), y el resultado es la información (Values) de los documentos más relevantes.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 07 — TOKENS
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 1 · TRANSFORMERS", C.cyan);

  addSectionTitle(s, "Tokens: la Unidad Mínima del LLM", "El LLM no ve palabras — ve tokens");

  // Ejemplo de tokenización visual
  addCard(s, 0.4, 1.75, 9.2, 1.35, C.bgCard, C.bgLight);
  s.addText("¿Cómo tokeniza el modelo esta frase?", {
    x: 0.6, y: 1.82, w: 9.0, h: 0.28,
    fontSize: 11, color: C.textSec, fontFace: F.body,
  });
  // Tokens de la frase
  const tokenPairs = [
    ["trans", C.cyan], ["form", C.purple], ["ers", C.green], [" are", C.yellow],
    [" amazing", C.coral], [".", C.bgLight],
  ];
  tokenPairs.forEach((tp, i) => {
    const x = 0.6 + i * 1.52;
    s.addShape("ROUNDED_RECTANGLE", {
      x, y: 2.20, w: 1.40, h: 0.42,
      fill: { color: "0A0E1A" },
      line: { color: tp[1], width: 1.5 },
      rectRadius: 0.06,
    });
    s.addText(`"${tp[0]}"`, {
      x, y: 2.20, w: 1.40, h: 0.42,
      fontSize: 13, bold: true, color: tp[1],
      fontFace: F.mono, align: "center", valign: "middle", margin: 0,
    });
  });
  s.addText("\"transformers are amazing.\"  →  6 tokens (no 3 palabras)", {
    x: 0.6, y: 2.72, w: 9.0, h: 0.28,
    fontSize: 11, color: C.textSec, fontFace: F.body, italic: true,
  });

  // 3 stats grandes
  addStatCallout(s, "~0.75", "palabras / token\n(inglés)", 0.40, 3.15, C.cyan);
  addStatCallout(s, "~0.60", "palabras / token\n(español)", 2.60, 3.15, C.purple);
  addStatCallout(s, "100K", "tokens = vocabulario\n(tiktoken cl100k)", 4.80, 3.15, C.green);
  addStatCallout(s, "BPE", "Byte-Pair Encoding\nalgo. tokenizador", 7.00, 3.15, C.yellow);

  // Tabla de ejemplos
  addCard(s, 0.4, 4.55, 9.2, 0.95, C.bgCard, C.bgLight);
  s.addText("Palabras que se convierten en más de 1 token:", {
    x: 0.6, y: 4.62, w: 6.0, h: 0.25, fontSize: 11, bold: true, color: C.textPri, fontFace: F.body, margin: 0,
  });
  const tokEx = ["extraordinario → [extra][ordin][ario]", "tokenization → [token][ization]", "🤖 → [<0x1F916>] (emoji=varios tokens)", "12345 → [1][2][3][4][5]"];
  tokEx.forEach((ex, i) => {
    s.addText(ex, {
      x: 0.6 + (i % 2) * 4.6, y: 4.90 + Math.floor(i / 2) * 0.25, w: 4.4, h: 0.24,
      fontSize: 10.5, color: C.textSec, fontFace: F.mono,
    });
  });

  s.addNotes("Tokens — conceptos importantes para los estudiantes:\n\n1. Los LLMs NO leen palabras — leen tokens (subpalabras)\n2. El vocabulario se construye con BPE (Byte-Pair Encoding): se empieza con caracteres individuales y se fusionan los pares más frecuentes\n3. IMPORTANCIA PARA EL NEGOCIO: las APIs cloud cobran por token, no por palabra\n4. El español usa más tokens que el inglés = es más caro en APIs cloud\n\nDemo en vivo: abrir https://platform.openai.com/tokenizer y mostrar cómo se colorean los tokens.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 08 — TIPOS DE ARQUITECTURA (Encoder/Decoder)
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 1 · TRANSFORMERS", C.cyan);

  addSectionTitle(s, "Tipos de Arquitectura Transformer", "No todos los LLMs son iguales por dentro");

  const archs = [
    {
      title: "Encoder-Only",
      model: "BERT, RoBERTa",
      color: C.purple,
      emoji: "🔍",
      desc: "Procesa texto en AMBAS direcciones (izquierda ↔ derecha). Ideal para entender texto, no para generarlo.",
      uses: ["Clasificación de texto", "NER (Extracción de entidades)", "Análisis de sentimientos", "Búsqueda semántica"],
      x: 0.4,
    },
    {
      title: "Decoder-Only",
      model: "GPT-4, Llama, Mistral",
      color: C.cyan,
      emoji: "✍️",
      desc: "Solo mira hacia ATRÁS (izquierda → derecha). Predice el siguiente token. Base de ChatGPT y la mayoría de LLMs actuales.",
      uses: ["Generación de texto", "Chat / Asistentes", "Completado de código", "Razonamiento"],
      x: 3.55,
    },
    {
      title: "Encoder-Decoder",
      model: "T5, BART, Gemini",
      color: C.green,
      emoji: "🔄",
      desc: "Combina ambos. El encoder entiende el input, el decoder genera el output. Más complejo pero versátil.",
      uses: ["Traducción automática", "Resumen de texto", "Preguntas y respuestas", "Tareas seq2seq"],
      x: 6.70,
    },
  ];

  archs.forEach(a => {
    addCard(s, a.x, 1.65, 3.05, 3.85, C.bgCard, a.color);
    s.addText(a.emoji, { x: a.x + 0.1, y: 1.75, w: 0.6, h: 0.6, fontSize: 28, align: "center" });
    s.addText(a.title, {
      x: a.x + 0.1, y: 1.73, w: 2.85, h: 0.40,
      fontSize: 15, bold: true, color: a.color, fontFace: F.title, align: "right", margin: 0,
    });
    addCard(s, a.x + 0.1, 2.18, 2.85, 0.30, "0A0E1A", a.color);
    s.addText(a.model, {
      x: a.x + 0.1, y: 2.18, w: 2.85, h: 0.30,
      fontSize: 10, color: C.textSec, fontFace: F.mono, align: "center", valign: "middle", margin: 0,
    });
    s.addText(a.desc, {
      x: a.x + 0.1, y: 2.55, w: 2.85, h: 0.80,
      fontSize: 10.5, color: C.textSec, fontFace: F.body,
    });
    a.uses.forEach((u, i) => {
      s.addShape("OVAL", { x: a.x + 0.15, y: 3.40 + i * 0.28, w: 0.10, h: 0.10, fill: { color: a.color }, line: { color: a.color } });
      s.addText(u, { x: a.x + 0.30, y: 3.36 + i * 0.28, w: 2.65, h: 0.24, fontSize: 10, color: C.textPri, fontFace: F.body });
    });
  });

  // Footer
  addCard(s, 0.4, 5.62, 9.2, 0.28, "0A1228", C.cyan);
  s.addText("💡 Para este curso nos enfocamos en Decoder-Only (GPT, Llama, Mistral) — la base de los asistentes modernos", {
    x: 0.5, y: 5.64, w: 9.0, h: 0.24, fontSize: 10.5, color: C.cyan, fontFace: F.body, align: "center", valign: "middle", margin: 0,
  });

  s.addNotes("Arquitecturas:\n- Encoder-Only: BERT fue revolucionario en 2018. Entiende texto bidireccional. NO genera texto libre.\n- Decoder-Only: GPT (Generative Pre-trained Transformer) = genera texto de izquierda a derecha. Es la arquitectura dominante hoy en asistentes.\n- Encoder-Decoder: T5 y modelos de traducción. Más flexible pero más complejo.\n\nPregunta para la clase: '¿Para qué tarea usarían cada tipo?' — análisis de documentos (encoder), chatbot (decoder), traducción (enc-dec).");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 09 — SEPARADOR TEMA 2
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s, C.bgTheme2);

  s.addText("TEMA 02", {
    x: 0.5, y: 1.1, w: 9.0, h: 0.45,
    fontSize: 13, bold: true, color: C.purple, fontFace: F.body, align: "center",
    charSpacing: 8,
  });
  s.addText("Embeddings,\nContexto y Ventanas", {
    x: 0.5, y: 1.55, w: 9.0, h: 1.8,
    fontSize: 52, bold: true, color: C.textPri, fontFace: F.title, align: "center",
  });
  s.addText("Representación vectorial · Similitud semántica · Límites del modelo", {
    x: 0.5, y: 3.50, w: 9.0, h: 0.40,
    fontSize: 14, color: C.textSec, fontFace: F.body, align: "center",
  });
  s.addShape("RECTANGLE", { x: 3.5, y: 4.05, w: 3.0, h: 0.03, fill: { color: C.purple }, line: { color: C.purple } });

  s.addNotes("TEMA 2 — Embeddings, Contexto y Ventanas de Contexto. Este tema es fundamental para entender RAG y búsqueda semántica.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 10 — QUÉ SON LOS EMBEDDINGS
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 2 · EMBEDDINGS", C.purple);

  addSectionTitle(s, "¿Qué son los Embeddings?", "Convirtiendo significado en coordenadas");

  // Panel izquierdo — concepto
  addCard(s, 0.4, 1.75, 4.7, 3.70, C.bgCard, C.bgLight);

  s.addText("\"Un embedding es la representación numérica del SIGNIFICADO de un texto como un vector en un espacio de alta dimensión.\"", {
    x: 0.55, y: 1.85, w: 4.4, h: 0.90,
    fontSize: 11.5, color: C.textPri, fontFace: F.body, italic: true,
  });

  // Fórmula visual
  addCard(s, 0.55, 2.85, 4.3, 0.45, "080812", C.purple);
  s.addText('"inteligencia artificial"  →  [-0.32, 0.81, 0.14, ..., 0.27]  (768 dimensiones)', {
    x: 0.6, y: 2.88, w: 4.2, h: 0.38,
    fontSize: 9, color: C.purple, fontFace: F.mono, align: "center", valign: "middle", margin: 0,
  });

  s.addText("¿Para qué sirven?", {
    x: 0.55, y: 3.38, w: 4.4, h: 0.30,
    fontSize: 12, bold: true, color: C.textPri, fontFace: F.body, margin: 0,
  });
  const uses = [
    ["🔍", "Búsqueda semántica — encontrar documentos por significado"],
    ["🤖", "Base de RAG — enriquecer LLMs con conocimiento externo"],
    ["📊", "Clasificación — agrupar textos similares"],
    ["🎯", "Recomendación — sugerir contenido relacionado"],
    ["🔗", "Detección de duplicados semánticos"],
  ];
  uses.forEach((u, i) => {
    s.addText(u[0], { x: 0.55, y: 3.72 + i * 0.32, w: 0.35, h: 0.28, fontSize: 14, align: "center" });
    s.addText(u[1], { x: 0.93, y: 3.73 + i * 0.32, w: 3.9, h: 0.26, fontSize: 10.5, color: C.textSec, fontFace: F.body });
  });

  // Panel derecho — visualización de espacio vectorial
  addCard(s, 5.3, 1.75, 4.3, 3.70, C.bgCard, C.bgLight);
  s.addText("Espacio Vectorial 2D (simplificado)", {
    x: 5.45, y: 1.82, w: 4.0, h: 0.28,
    fontSize: 11, bold: true, color: C.textPri, fontFace: F.body, margin: 0,
  });

  // Ejes del mapa
  const ox = 5.7, oy = 4.6, ew = 3.5, eh = 2.5;
  s.addShape("RECTANGLE", { x: ox, y: oy - eh + 0.3, w: 0.02, h: eh, fill: { color: C.textDim }, line: { color: C.textDim } });
  s.addShape("RECTANGLE", { x: ox, y: oy, w: ew, h: 0.02, fill: { color: C.textDim }, line: { color: C.textDim } });

  // Puntos en el espacio vectorial
  const points = [
    { label: "🐶 perro",          x: ox + 0.5,  y: oy - 1.7, color: C.yellow  },
    { label: "🐱 gato",           x: ox + 0.9,  y: oy - 1.5, color: C.yellow  },
    { label: "🐟 pez",            x: ox + 0.3,  y: oy - 0.9, color: C.yellow  },
    { label: "🤖 IA",             x: ox + 2.5,  y: oy - 2.1, color: C.cyan    },
    { label: "💻 ML",             x: ox + 2.8,  y: oy - 1.9, color: C.cyan    },
    { label: "🧠 neuronal",       x: ox + 2.3,  y: oy - 1.5, color: C.cyan    },
    { label: "🍕 pizza",          x: ox + 1.5,  y: oy - 0.45, color: C.coral  },
    { label: "🍣 sushi",          x: ox + 1.9,  y: oy - 0.35, color: C.coral  },
  ];
  points.forEach(p => {
    s.addShape("OVAL", { x: p.x - 0.06, y: p.y - 0.06, w: 0.12, h: 0.12, fill: { color: p.color }, line: { color: p.color } });
    s.addText(p.label, {
      x: p.x + 0.06, y: p.y - 0.12, w: 1.5, h: 0.25,
      fontSize: 9, color: p.color, fontFace: F.body, margin: 0,
    });
  });

  s.addText("Animales", { x: ox + 0.1, y: oy - 2.1, w: 1.2, h: 0.22, fontSize: 9, color: C.yellow, fontFace: F.body, italic: true });
  s.addText("Tecnología IA", { x: ox + 2.0, y: oy - 2.38, w: 1.5, h: 0.22, fontSize: 9, color: C.cyan, fontFace: F.body, italic: true });
  s.addText("Comida", { x: ox + 1.3, y: oy - 0.15, w: 1.0, h: 0.22, fontSize: 9, color: C.coral, fontFace: F.body, italic: true });

  s.addNotes("Embeddings:\n\nAnálogía clave: Imagina un mapa donde las palabras son ciudades. Ciudades cercanas = conceptos relacionados. 'Perro' y 'gato' están cerca. 'Pizza' está lejos de 'inteligencia artificial'.\n\nDato real: nomic-embed-text usa 768 dimensiones. OpenAI text-embedding-3-large usa 3,072 dimensiones. Los humanos solo podemos visualizar 2-3 dimensiones pero el modelo trabaja con cientos.\n\nDemo en vivo: Usar la pestaña 'Embeddings' de la app para mostrar similitudes en tiempo real.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 11 — SIMILITUD COSENO
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 2 · EMBEDDINGS", C.purple);

  addSectionTitle(s, "Similitud Coseno: Midiendo el Significado", "La matemática detrás de la búsqueda semántica");

  addCard(s, 0.4, 1.75, 5.0, 3.72, C.bgCard, C.bgLight);

  // Fórmula
  addCard(s, 0.55, 1.88, 4.7, 0.50, "080812", C.purple);
  s.addText("cos(θ) = (A · B) / (|A| × |B|)   ∈ [-1, 1]", {
    x: 0.55, y: 1.88, w: 4.7, h: 0.50,
    fontSize: 14, bold: true, color: C.purple, fontFace: F.mono, align: "center", valign: "middle", margin: 0,
  });

  s.addText("Interpretación del score:", {
    x: 0.60, y: 2.45, w: 4.6, h: 0.28, fontSize: 11, bold: true, color: C.textPri, fontFace: F.body, margin: 0,
  });

  const scores = [
    { range: "≥ 0.95", color: C.green,  label: "Casi idénticos (sinónimos exactos)" },
    { range: "0.85–0.95", color: "6FD68C",label: "Muy similares (mismo concepto)" },
    { range: "0.70–0.85", color: C.yellow,label: "Relacionados (mismo dominio)" },
    { range: "0.50–0.70", color: C.coral, label: "Vaguamente relacionados" },
    { range: "< 0.50",   color: "FF4444", label: "Sin relación semántica" },
  ];
  scores.forEach((sc, i) => {
    const y = 2.78 + i * 0.50;
    addCard(s, 0.60, y, 1.1, 0.38, "0A0E1A", sc.color);
    s.addText(sc.range, { x: 0.60, y, w: 1.1, h: 0.38, fontSize: 10, bold: true, color: sc.color, fontFace: F.mono, align: "center", valign: "middle", margin: 0 });
    s.addText(sc.label, { x: 1.80, y: y + 0.06, w: 3.2, h: 0.26, fontSize: 10.5, color: C.textSec, fontFace: F.body });
  });

  // Panel derecho: ejemplos reales
  addCard(s, 5.55, 1.75, 4.05, 3.72, C.bgCard, C.bgLight);
  s.addText("Ejemplos reales (nomic-embed-text)", {
    x: 5.70, y: 1.82, w: 3.8, h: 0.28, fontSize: 11, bold: true, color: C.textPri, fontFace: F.body, margin: 0,
  });

  const examples = [
    { t1: "automóvil", t2: "carro",            sim: 0.94, color: C.green   },
    { t1: "IA",        t2: "inteligencia art.", sim: 0.91, color: C.green   },
    { t1: "perro",     t2: "gato",             sim: 0.83, color: "6FD68C"  },
    { t1: "IA",        t2: "artificial intel.", sim: 0.89, color: C.green   },
    { t1: "amor",      t2: "odio",             sim: 0.72, color: C.yellow   },
    { t1: "pizza",     t2: "cuántica",         sim: 0.31, color: "FF4444"   },
  ];
  examples.forEach((ex, i) => {
    const y = 2.18 + i * 0.52;
    s.addText(`"${ex.t1}" ↔ "${ex.t2}"`, {
      x: 5.70, y, w: 3.8, h: 0.22,
      fontSize: 10, color: C.textSec, fontFace: F.body, margin: 0,
    });
    const barW = ex.sim * 3.0;
    s.addShape("ROUNDED_RECTANGLE", { x: 5.70, y: y + 0.24, w: 3.0, h: 0.16, fill: { color: C.bgLight }, line: { color: C.bgLight }, rectRadius: 0.04 });
    s.addShape("ROUNDED_RECTANGLE", { x: 5.70, y: y + 0.24, w: barW, h: 0.16, fill: { color: ex.color }, line: { color: ex.color }, rectRadius: 0.04 });
    s.addText(`${ex.sim}`, {
      x: 5.70 + barW + 0.05, y: y + 0.22, w: 0.50, h: 0.20,
      fontSize: 9, bold: true, color: ex.color, fontFace: F.mono, margin: 0,
    });
  });

  // Key insight
  addCard(s, 0.4, 5.60, 9.2, 0.28, "0A0A20", C.purple);
  s.addText("💡 'IA' y 'artificial intelligence' tienen similitud 0.89 — el modelo entiende significado entre idiomas", {
    x: 0.5, y: 5.62, w: 9.0, h: 0.24, fontSize: 10.5, color: C.purple, fontFace: F.body, align: "center", valign: "middle", margin: 0,
  });

  s.addNotes("Similitud coseno:\n\nLa razón de usar coseno y no distancia euclidiana: el coseno es invariante a la magnitud del vector. Dos vectores pueden tener longitudes muy distintas pero señalar en la misma dirección (mismo significado).\n\nCaso interesante: 'banco' (banco financiero) y 'banco' (asiento) pueden tener embeddings diferentes según el contexto en el que aparecen los modelos modernos usan embeddings contextuales, no estáticos.\n\nDemo: usar el explorador de embeddings de la app React para mostrar estos valores en vivo.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 12 — VENTANA DE CONTEXTO
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 2 · CONTEXTO", C.purple);

  addSectionTitle(s, "La Ventana de Contexto", "El 'límite de atención' del modelo");

  // Definición
  addCard(s, 0.4, 1.75, 9.2, 0.68, "0A0A1E", C.purple);
  s.addText("La ventana de contexto es el máximo de tokens que el modelo puede procesar en una sola llamada.\nIncluye: system prompt + historial de conversación + pregunta actual + respuesta generada.", {
    x: 0.6, y: 1.83, w: 8.8, h: 0.52,
    fontSize: 12, color: C.textPri, fontFace: F.body, align: "center",
  });

  // Tabla de modelos
  const mods = [
    { name: "GPT-3.5 Turbo", ctx: "4K",   pages: 8,    cost: "$",   color: C.textSec },
    { name: "GPT-4",          ctx: "8K",   pages: 16,   cost: "$$",  color: C.yellow  },
    { name: "GPT-4o",         ctx: "128K", pages: 192,  cost: "$$$", color: C.cyan    },
    { name: "Claude 3.5",     ctx: "200K", pages: 300,  cost: "$$$", color: C.purple  },
    { name: "Llama 3.2 (local)", ctx: "128K", pages: 192, cost: "FREE", color: C.green },
    { name: "Mistral 7B",     ctx: "32K",  pages: 49,   cost: "$",   color: C.yellow  },
  ];

  s.addText("Modelo", { x: 0.4, y: 2.55, w: 2.5, h: 0.28, fontSize: 10, bold: true, color: C.textSec, fontFace: F.body });
  s.addText("Contexto", { x: 2.95, y: 2.55, w: 1.3, h: 0.28, fontSize: 10, bold: true, color: C.textSec, fontFace: F.body, align: "center" });
  s.addText("~ Páginas A4", { x: 4.30, y: 2.55, w: 1.6, h: 0.28, fontSize: 10, bold: true, color: C.textSec, fontFace: F.body, align: "center" });
  s.addText("Barra visual (relativa)", { x: 5.95, y: 2.55, w: 3.55, h: 0.28, fontSize: 10, bold: true, color: C.textSec, fontFace: F.body });

  mods.forEach((m, i) => {
    const y = 2.85 + i * 0.44;
    if (i % 2 === 0) s.addShape("RECTANGLE", { x: 0.4, y, w: 9.2, h: 0.44, fill: { color: C.bgCard }, line: { color: C.bgCard } });
    s.addText(m.name, { x: 0.5, y: y + 0.10, w: 2.4, h: 0.25, fontSize: 11, color: m.color, fontFace: F.body });
    s.addText(m.ctx, { x: 2.95, y: y + 0.10, w: 1.3, h: 0.25, fontSize: 11, bold: true, color: m.color, fontFace: F.mono, align: "center" });
    s.addText(String(m.pages), { x: 4.30, y: y + 0.10, w: 1.6, h: 0.25, fontSize: 11, color: C.textSec, fontFace: F.body, align: "center" });
    const barW = Math.min((m.pages / 300) * 3.4, 3.4);
    s.addShape("ROUNDED_RECTANGLE", { x: 5.95, y: y + 0.13, w: 3.4, h: 0.18, fill: { color: C.bgLight }, line: { color: C.bgLight }, rectRadius: 0.04 });
    s.addShape("ROUNDED_RECTANGLE", { x: 5.95, y: y + 0.13, w: barW, h: 0.18, fill: { color: m.color }, line: { color: m.color }, rectRadius: 0.04 });
    s.addText(m.cost, { x: 9.35, y: y + 0.10, w: 0.50, h: 0.25, fontSize: 10, color: m.color, fontFace: F.body, align: "right" });
  });

  // Insight clave
  addCard(s, 0.4, 5.60, 9.2, 0.28, "0A1228", C.cyan);
  s.addText("⚠️  Cuando el contexto se desborda, el modelo 'olvida' la información más antigua — efecto 'lost in the middle'", {
    x: 0.5, y: 5.62, w: 9.0, h: 0.24, fontSize: 10.5, color: C.yellow, fontFace: F.body, align: "center", valign: "middle", margin: 0,
  });

  s.addNotes("Ventana de contexto:\n\nPregunta para la clase: 'Si quieren procesar un libro de 400 páginas, ¿qué modelo necesitan?'\n- 400 páginas × 500 palabras × 1.4 tokens/palabra ≈ 280,000 tokens\n- Solo Claude 3.5 (200K) casi alcanza, necesitarían estrategia RAG\n\nEfecto 'lost in the middle': investigación de Liu et al. 2023 muestra que los LLMs recuerdan mejor el inicio y el final del contexto. La información en el MEDIO tiene peor rendimiento. Esto afecta el diseño de prompts en producción.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 13 — SEPARADOR TEMA 3
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s, C.bgTheme3);

  s.addText("TEMA 03", {
    x: 0.5, y: 1.1, w: 9.0, h: 0.45,
    fontSize: 13, bold: true, color: C.green, fontFace: F.body, align: "center",
    charSpacing: 8,
  });
  s.addText("Capacidades y\nLimitaciones de los LLM", {
    x: 0.5, y: 1.55, w: 9.0, h: 1.8,
    fontSize: 48, bold: true, color: C.textPri, fontFace: F.title, align: "center",
  });
  s.addText("¿Qué pueden hacer? · ¿Dónde fallan? · ¿Cómo elegir el modelo correcto?", {
    x: 0.5, y: 3.55, w: 9.0, h: 0.40,
    fontSize: 14, color: C.textSec, fontFace: F.body, align: "center",
  });
  s.addShape("RECTANGLE", { x: 3.5, y: 4.10, w: 3.0, h: 0.03, fill: { color: C.green }, line: { color: C.green } });

  s.addNotes("TEMA 3 — Capacidades y limitaciones. Este tema es crítico para las decisiones empresariales: saber exactamente QUÉ pueden y NO pueden hacer los LLMs evita proyectos fallidos.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 14 — CAPACIDADES
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 3 · CAPACIDADES", C.green);

  addSectionTitle(s, "¿Qué hacen bien los LLM?", "Capacidades emergentes del preentrenamiento masivo");

  const caps = [
    { icon: "✍️", title: "Generación de Texto", desc: "Redactar, resumir, parafrasear, traducir, crear contenido en múltiples estilos y formatos", color: C.green  },
    { icon: "💬", title: "Conversación Natural", desc: "Mantener diálogos coherentes, recordar el contexto de la conversación, responder con empatía", color: C.cyan   },
    { icon: "💻", title: "Generación de Código", desc: "Escribir, debuggear, explicar y refactorizar código en decenas de lenguajes de programación", color: C.purple },
    { icon: "🧩", title: "Razonamiento", desc: "Resolver problemas step-by-step, análisis lógico, matemáticas básicas a intermedias", color: C.yellow },
    { icon: "📊", title: "Extracción de Info", desc: "NER, clasificación, estructurar datos no estructurados, completar formularios automáticamente", color: C.coral  },
    { icon: "🌍", title: "Multilingüe", desc: "Funcionar en 100+ idiomas simultáneamente sin configuración adicional", color: C.green  },
  ];

  caps.forEach((c, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.4 + col * 3.15;
    const y = 1.75 + row * 1.90;
    addCard(s, x, y, 3.05, 1.80, C.bgCard, c.color);
    s.addText(c.icon, { x: x + 0.1, y: y + 0.12, w: 0.55, h: 0.55, fontSize: 26, align: "center" });
    s.addText(c.title, {
      x: x + 0.70, y: y + 0.12, w: 2.25, h: 0.35,
      fontSize: 12, bold: true, color: c.color, fontFace: F.body, align: "left", margin: 0,
    });
    s.addText(c.desc, {
      x: x + 0.12, y: y + 0.55, w: 2.80, h: 1.15,
      fontSize: 10.5, color: C.textSec, fontFace: F.body,
    });
  });

  s.addNotes("Capacidades:\n\nPuntos importantes:\n- Estas capacidades EMERGEN del entrenamiento, no fueron programadas explícitamente\n- El modelo de 'siguiente token' produce capacidades que sorprendieron a los propios creadores\n- Few-shot learning: con 3-5 ejemplos en el prompt, el modelo aprende la tarea\n- Zero-shot: puede hacer tareas que nunca vio explícitamente en entrenamiento\n\nEjemplo práctico para la clase: pedir al modelo que resuma un texto en 3 puntos, luego que lo clasifique, luego que lo traduzca — todo en el mismo chat, sin reentrenamiento.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 15 — LIMITACIONES
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 3 · LIMITACIONES", C.coral);

  addSectionTitle(s, "Limitaciones Críticas", "Lo que los LLMs NO pueden hacer — y por qué importa en producción");

  const limits = [
    {
      icon: "🌀", title: "Alucinaciones",
      desc: "Genera información plausible pero incorrecta. Puede inventar citas, datos, URLs, nombres o eventos.",
      impact: "Crítico en salud, legal, finanzas",
      color: C.coral,
    },
    {
      icon: "📅", title: "Knowledge Cutoff",
      desc: "El conocimiento está congelado en la fecha de entrenamiento. No sabe nada posterior a ese punto.",
      impact: "Requiere RAG para info reciente",
      color: C.yellow,
    },
    {
      icon: "🔢", title: "Aritmética Compleja",
      desc: "Errores en cálculos matemáticos complejos. Suma básica OK; álgebra lineal o cálculo = propenso a errores.",
      impact: "Delegar a herramientas externas",
      color: C.coral,
    },
    {
      icon: "🔒", title: "Razonamiento Lógico Estricto",
      desc: "Falla en problemas de lógica formal, silogismos complejos, y razonamiento espacial preciso.",
      impact: "Usar LLMs como orquestador, no executor",
      color: C.yellow,
    },
    {
      icon: "🎯", title: "Consistencia",
      desc: "Puede dar respuestas distintas a la misma pregunta. Temperature > 0 implica variabilidad inherente.",
      impact: "Validar outputs en sistemas críticos",
      color: C.coral,
    },
    {
      icon: "🔍", title: "Memoria Persistente",
      desc: "Sin arquitectura adicional, olvida todo al terminar la conversación (cada llamada es independiente).",
      impact: "Requiere sistema de memoria externo",
      color: C.yellow,
    },
  ];

  limits.forEach((l, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.4 + col * 3.15;
    const y = 1.75 + row * 1.85;
    addCard(s, x, y, 3.05, 1.75, C.bgCard, l.color);
    s.addText(l.icon, { x: x + 0.1, y: y + 0.10, w: 0.50, h: 0.50, fontSize: 24, align: "center" });
    s.addText(l.title, { x: x + 0.65, y: y + 0.10, w: 2.30, h: 0.30, fontSize: 12, bold: true, color: l.color, fontFace: F.body, align: "left", margin: 0 });
    s.addText(l.desc, { x: x + 0.12, y: y + 0.48, w: 2.82, h: 0.80, fontSize: 10, color: C.textSec, fontFace: F.body });
    addCard(s, x + 0.12, y + 1.35, 2.82, 0.28, "0A0E1A", l.color);
    s.addText("⚠️ " + l.impact, { x: x + 0.12, y: y + 1.35, w: 2.82, h: 0.28, fontSize: 9.5, color: l.color, fontFace: F.body, align: "center", valign: "middle", margin: 0 });
  });

  s.addNotes("Limitaciones — CRÍTICO para proyectos empresariales:\n\n1. ALUCINACIONES: el modelo no 'sabe' que está inventando. Produce texto que PARECE correcto. La solución no es 'pedir que no invente' — requiere validación y RAG.\n\n2. KNOWLEDGE CUTOFF: GPT-4 tiene conocimiento hasta inicio 2024 (aproximado). Para info reciente usar RAG con fuentes actualizadas.\n\n3. MATEMÁTICAS: el modelo predice tokens, no calcula. 2+2=4 funciona por patrones en datos de entrenamiento, no por comprensión matemática. Para cálculos serios: conectar calculadora/código Python.\n\nPregunta para reflexión: '¿Usarían un LLM para determinar la dosis de un medicamento o para redactar el informe médico?' — redactar sí, dosis no (sin validación adicional).");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 16 — ALUCINACIONES EN DETALLE
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 3 · LIMITACIONES", C.coral);

  addSectionTitle(s, "El Problema de las Alucinaciones", "La limitación más importante en producción");

  // Definición
  addCard(s, 0.4, 1.75, 9.2, 0.55, "1A0808", C.coral);
  s.addText("\"Alucinación: el LLM genera información que suena plausible y confiada, pero es factualmente incorrecta o inventada.\"", {
    x: 0.6, y: 1.83, w: 8.8, h: 0.40,
    fontSize: 12.5, color: C.textPri, fontFace: F.body, italic: true, align: "center",
  });

  // Tipos y causas
  addCard(s, 0.4, 2.42, 4.5, 3.05, C.bgCard, C.bgLight);
  s.addText("Tipos de Alucinaciones", {
    x: 0.55, y: 2.50, w: 4.2, h: 0.30, fontSize: 12, bold: true, color: C.coral, fontFace: F.body, margin: 0,
  });
  const types = [
    ["📰", "Hechos incorrectos", "Fechas, nombres, estadísticas inventadas"],
    ["📚", "Citas falsas", "Atribuye frases a personas que nunca las dijeron"],
    ["🔗", "URLs fantasmas", "Genera links que no existen pero parecen reales"],
    ["📖", "Papers inexistentes", "Crea referencias bibliográficas plausibles pero falsas"],
    ["📊", "Datos de compañías", "Inventa métricas, empleados, ingresos ficticios"],
  ];
  types.forEach((t, i) => {
    s.addText(t[0], { x: 0.55, y: 2.90 + i * 0.50, w: 0.35, h: 0.38, fontSize: 18, align: "center" });
    s.addText(t[1], { x: 0.95, y: 2.90 + i * 0.50, w: 2.5, h: 0.22, fontSize: 11, bold: true, color: C.textPri, fontFace: F.body, margin: 0 });
    s.addText(t[2], { x: 0.95, y: 3.10 + i * 0.50, w: 3.8, h: 0.22, fontSize: 10, color: C.textSec, fontFace: F.body, margin: 0 });
  });

  // Estrategias de mitigación
  addCard(s, 5.1, 2.42, 4.5, 3.05, C.bgCard, C.bgLight);
  s.addText("Cómo Mitigarlas", {
    x: 5.25, y: 2.50, w: 4.2, h: 0.30, fontSize: 12, bold: true, color: C.green, fontFace: F.body, margin: 0,
  });
  const mitigs = [
    { icon: "🔍", title: "RAG", desc: "Proveer fuentes de verdad en el contexto" },
    { icon: "🌡️", title: "Temperature baja", desc: "temperature: 0 para tareas de hechos" },
    { icon: "✅", title: "Validación externa", desc: "Verificar datos críticos con herramientas" },
    { icon: "📋", title: "Prompts específicos", desc: "'Si no sabes, responde No lo sé'" },
    { icon: "🔄", title: "Self-consistency", desc: "Pedir múltiples respuestas y votar" },
  ];
  mitigs.forEach((m, i) => {
    const y = 2.90 + i * 0.50;
    addIconCircle(s, m.icon, 5.25, y + 0.04, 0.34, "0A2010");
    s.addText(m.title, { x: 5.65, y: y + 0.02, w: 3.8, h: 0.22, fontSize: 11, bold: true, color: C.green, fontFace: F.body, margin: 0 });
    s.addText(m.desc, { x: 5.65, y: y + 0.23, w: 3.8, h: 0.22, fontSize: 10, color: C.textSec, fontFace: F.body, margin: 0 });
  });

  s.addNotes("Alucinaciones:\n\n¿POR QUÉ alucina el modelo? No porque 'quiera mentir', sino porque:\n1. El objetivo de entrenamiento es generar texto plausible, no texto verdadero\n2. El modelo no tiene acceso a una 'base de verdad' interna\n3. Prefiere dar una respuesta antes que admitir incertidumbre\n\nEjercicio en clase: Pedir al modelo algo que no puede saber con certeza, ej: 'Dame las ventas exactas de [empresa local pequeña] en 2023'. Ver si inventa datos.\n\nDato alarmante: Abogados han sido multados por citar casos jurídicos inventados por ChatGPT en documentos legales reales.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 17 — COMPARATIVA DE MODELOS
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);
  addThemeBadge(s, "TEMA 3 · MODELOS", C.green);

  addSectionTitle(s, "Comparativa de Modelos LLM", "¿Cuál elegir para tu proyecto?");

  // Tabla comparativa
  const headers = ["Modelo", "Empresa", "Parámetros", "Contexto", "Fortalezas", "Precio Input"];
  const rows = [
    ["GPT-4o",          "OpenAI",    "~1.8T*",  "128K",  "Razonamiento, visión, código",  "$2.50/M"],
    ["GPT-4o-mini",     "OpenAI",    "~8B*",    "128K",  "Costo/calidad, generalista",    "$0.15/M"],
    ["Claude 3.5 Sonnet","Anthropic","?",        "200K",  "Escritura, análisis, seguridad","$3.00/M"],
    ["Gemini 1.5 Pro",  "Google",    "?",        "1M",    "Contexto masivo, multimodal",   "$1.25/M"],
    ["Llama 3.1 70B",   "Meta",      "70B",     "128K",  "Open-source, privacidad",       "GRATIS**"],
    ["Llama 3.2 3B",    "Meta",      "3B",      "128K",  "LLM local rápido, educación",   "GRATIS**"],
    ["Mistral 7B",      "Mistral AI","7B",      "32K",   "Eficiente, buena calidad",       "GRATIS**"],
  ];

  const colW = [1.80, 1.20, 1.10, 0.90, 2.50, 1.10];
  const colX = [0.4, 2.22, 3.44, 4.56, 5.48, 8.00];

  // Header
  headers.forEach((h, i) => {
    addCard(s, colX[i], 1.75, colW[i], 0.35, C.bgMid, C.bgLight);
    s.addText(h, { x: colX[i] + 0.05, y: 1.75, w: colW[i] - 0.05, h: 0.35, fontSize: 10, bold: true, color: C.textSec, fontFace: F.body, valign: "middle" });
  });

  const rowColors = ["F5A623", "58A6FF", "A78BFA", "34D399", "22C55E", "4ADE80", "86EFAC"];
  rows.forEach((row, ri) => {
    const y = 2.15 + ri * 0.43;
    if (ri % 2 === 0) s.addShape("RECTANGLE", { x: 0.4, y, w: 9.2, h: 0.43, fill: { color: C.bgCard }, line: { color: C.bgCard } });
    row.forEach((cell, ci) => {
      const color = ci === 0 ? rowColors[ri] : ci === 5 ? (cell === "GRATIS**" ? C.green : C.yellow) : C.textSec;
      const bold = ci === 0;
      s.addText(cell, { x: colX[ci] + 0.05, y: y + 0.08, w: colW[ci] - 0.05, h: 0.28, fontSize: 10, color, bold, fontFace: ci < 2 ? F.body : F.body });
    });
  });

  // Notas al pie
  s.addText("* Estimado, no confirmado por la empresa  |  ** Gratis con Ollama local (requiere hardware propio)", {
    x: 0.4, y: 5.22, w: 9.2, h: 0.22, fontSize: 9, color: C.textDim, fontFace: F.body,
  });

  addCard(s, 0.4, 5.50, 9.2, 0.30, "0A1228", C.cyan);
  s.addText("🎯 Para este curso usamos Llama 3.2 vía Ollama: gratuito, privado, sin límites y funciona sin internet", {
    x: 0.5, y: 5.53, w: 9.0, h: 0.24, fontSize: 10.5, color: C.cyan, fontFace: F.body, align: "center", valign: "middle", margin: 0,
  });

  s.addNotes("Comparativa de modelos:\n\n- Los precios cambian constantemente. Verificar en la web del proveedor antes de cotizar a un cliente.\n- Para proyectos empresariales: la elección no es solo precio/calidad. También considerar: privacidad, latencia, disponibilidad geográfica, SLA, cumplimiento (GDPR).\n- Modelos open-source (Llama, Mistral): se pueden ejecutar en infraestructura propia → máxima privacidad\n- GPT-4o vs Claude 3.5: en benchmarks son muy comparables. Para escritura, muchos prefieren Claude. Para código, muchos prefieren GPT-4o.\n- Gemini 1.5 Pro con contexto de 1M tokens es único — puede procesar horas de video + código completo de una app en una sola llamada.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 18 — DEMO EN VIVO
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s, "080D14");

  // Fondo técnico
  s.addShape("RECTANGLE", { x: 0, y: 0, w: 0.04, h: "100%", fill: { color: C.green }, line: { color: C.green } });

  s.addText("🛠️  DEMO EN VIVO", {
    x: 0.5, y: 0.6, w: 9.0, h: 0.40,
    fontSize: 14, bold: true, color: C.green, fontFace: F.body, align: "center", charSpacing: 5,
  });
  s.addText("Ollama + FastAPI + React", {
    x: 0.5, y: 1.0, w: 9.0, h: 0.70,
    fontSize: 42, bold: true, color: C.textPri, fontFace: F.title, align: "center",
  });

  const steps = [
    { num: "1", cmd: "ollama serve", desc: "Iniciar el servidor LLM local", color: C.cyan },
    { num: "2", cmd: "ollama pull llama3.2", desc: "Descargar el modelo (~2 GB)", color: C.purple },
    { num: "3", cmd: "uvicorn main:app --reload", desc: "Iniciar API FastAPI (backend)", color: C.green },
    { num: "4", cmd: "npm run dev", desc: "Iniciar app React (frontend)", color: C.yellow },
  ];

  steps.forEach((st, i) => {
    const y = 1.90 + i * 0.88;
    addCard(s, 0.4, y, 9.2, 0.78, C.bgCard, st.color);
    // Número
    s.addShape("OVAL", { x: 0.5, y: y + 0.14, w: 0.50, h: 0.50, fill: { color: st.color }, line: { color: st.color } });
    s.addText(st.num, { x: 0.5, y: y + 0.14, w: 0.50, h: 0.50, fontSize: 16, bold: true, color: C.bgDark, align: "center", valign: "middle", margin: 0 });
    // Comando
    addCard(s, 1.10, y + 0.12, 5.5, 0.38, "030810", st.color);
    s.addText("$ " + st.cmd, { x: 1.15, y: y + 0.12, w: 5.4, h: 0.38, fontSize: 14, color: st.color, fontFace: F.mono, valign: "middle", margin: 0 });
    // Descripción
    s.addText(st.desc, { x: 6.70, y: y + 0.20, w: 2.7, h: 0.30, fontSize: 11, color: C.textSec, fontFace: F.body });
  });

  addCard(s, 0.4, 5.55, 9.2, 0.28, "071A07", C.green);
  s.addText("🌐 Frontend: localhost:5173  |  🔧 API: localhost:8000/docs  |  🦙 Ollama: localhost:11434", {
    x: 0.5, y: 5.57, w: 9.0, h: 0.24, fontSize: 10.5, color: C.green, fontFace: F.mono, align: "center", valign: "middle", margin: 0,
  });

  s.addNotes("Demo en vivo — pasos para el instructor:\n1. Mostrar que Ollama está corriendo: ollama ps\n2. Demostrar la API de Ollama directamente con curl\n3. Mostrar el Swagger UI de FastAPI (localhost:8000/docs)\n4. Abrir la app React y hacer una pregunta sobre transformers\n5. Mostrar el tokenizador en la app\n6. Mostrar la comparación de similitud entre 'IA' y 'artificial intelligence'\n\nProblemas comunes y soluciones:\n- 'Connection refused': asegurarse de que ollama serve está corriendo\n- 'Model not found': ejecutar ollama pull llama3.2\n- CORS errors: revisar el backend (CORS está configurado en main.py)");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 19 — RESUMEN Y PUNTOS CLAVE
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s);

  s.addText("🎯 Puntos Clave de la Sesión 1", {
    x: 0.4, y: 0.30, w: 9.2, h: 0.55,
    fontSize: 30, bold: true, color: C.textPri, fontFace: F.title,
  });

  const points = [
    { num: "01", topic: "Transformer", key: "Predecir el siguiente token con self-attention es la base de todos los LLMs modernos", color: C.cyan    },
    { num: "02", topic: "Tokens",      key: "Los LLMs no ven palabras sino tokens. El español usa ~30% más tokens que el inglés = mayor costo", color: C.cyan    },
    { num: "03", topic: "Attention",   key: "El mecanismo Q·K·V permite que cada token 'vea' a todos los demás simultáneamente, capturando contexto", color: C.cyan    },
    { num: "04", topic: "Embeddings",  key: "El texto se convierte en vectores numéricos. La similitud coseno mide el significado, no las letras", color: C.purple  },
    { num: "05", topic: "Contexto",    key: "La ventana de contexto es el límite de 'memoria' del modelo en una llamada. Varía de 4K a 1M tokens", color: C.purple  },
    { num: "06", topic: "Limitaciones","key": "Alucinaciones, knowledge cutoff y aritmética compleja son las limitaciones más críticas en producción", color: C.coral   },
  ];

  points.forEach((p, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.4 + col * 4.7;
    const y = 1.00 + row * 1.48;
    addCard(s, x, y, 4.55, 1.35, C.bgCard, p.color);
    s.addShape("ROUNDED_RECTANGLE", { x, y, w: 0.60, h: 0.40, fill: { color: p.color }, line: { color: p.color }, rectRadius: 0.05 });
    s.addText(p.num, { x, y, w: 0.60, h: 0.40, fontSize: 13, bold: true, color: C.bgDark, align: "center", valign: "middle", margin: 0 });
    s.addText(p.topic, { x: x + 0.68, y: y + 0.05, w: 3.75, h: 0.28, fontSize: 12, bold: true, color: p.color, fontFace: F.body, margin: 0 });
    s.addText(p.key, { x: x + 0.10, y: y + 0.45, w: 4.35, h: 0.80, fontSize: 10.5, color: C.textSec, fontFace: F.body });
  });

  s.addNotes("Slide de resumen. Pedir a los alumnos que apaguen el ordenador y reciten de memoria estos 6 puntos. El objetivo de la sesión es que estos conceptos queden claros antes de pasar a las sesiones de consumo de APIs y RAG.");
}

// ─────────────────────────────────────────────────────────────────────────
// SLIDE 20 — RECURSOS Y PRÓXIMA SESIÓN
// ─────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  setDarkBg(s, "080D14");

  s.addShape("RECTANGLE", { x: 0, y: 0, w: 0.04, h: "100%", fill: { color: C.cyan }, line: { color: C.cyan } });

  s.addText("📚 Recursos y Próximos Pasos", {
    x: 0.5, y: 0.30, w: 9.2, h: 0.50,
    fontSize: 28, bold: true, color: C.textPri, fontFace: F.title,
  });

  // Col izquierda: papers y lecturas
  addCard(s, 0.4, 0.95, 4.5, 3.10, C.bgCard, C.bgLight);
  s.addText("📄 Lecturas Obligatorias", { x: 0.55, y: 1.02, w: 4.2, h: 0.30, fontSize: 12, bold: true, color: C.cyan, fontFace: F.body, margin: 0 });
  const papers = [
    ["Attention Is All You Need", "Vaswani et al. (2017) — El paper fundacional", C.cyan],
    ["GPT-3 Paper", "Brown et al. (2020) — Few-shot learners", C.cyan],
    ["Chain-of-Thought Prompting", "Wei et al. (2022) — Razonamiento paso a paso", C.purple],
    ["RAG Paper", "Lewis et al. (2020) — Retrieval-Augmented Generation", C.green],
  ];
  papers.forEach((p, i) => {
    const y = 1.40 + i * 0.65;
    s.addShape("OVAL", { x: 0.55, y: y + 0.10, w: 0.12, h: 0.12, fill: { color: p[2] }, line: { color: p[2] } });
    s.addText(p[0], { x: 0.73, y, w: 4.05, h: 0.27, fontSize: 11, bold: true, color: p[2], fontFace: F.body, margin: 0 });
    s.addText(p[1], { x: 0.73, y: y + 0.28, w: 4.05, h: 0.22, fontSize: 10, color: C.textSec, fontFace: F.body, margin: 0 });
  });

  // Col derecha: herramientas y siguiente sesión
  addCard(s, 5.1, 0.95, 4.5, 1.45, C.bgCard, C.bgLight);
  s.addText("🔧 Herramientas para Explorar", { x: 5.25, y: 1.02, w: 4.2, h: 0.30, fontSize: 12, bold: true, color: C.purple, fontFace: F.body, margin: 0 });
  const tools = [["🦙 ollama.com", "LLMs locales gratuitos"], ["🤗 huggingface.co", "Modelos y datasets"], ["📊 Tokenizer Playground (OpenAI)", "Visualizar tokens"], ["🔍 Embedding Projector", "Visualizar vectores en 3D"]];
  tools.forEach((t, i) => {
    s.addText(t[0], { x: 5.25, y: 1.38 + i * 0.36, w: 2.5, h: 0.22, fontSize: 11, color: C.textPri, fontFace: F.body, margin: 0 });
    s.addText(t[1], { x: 5.25, y: 1.58 + i * 0.36, w: 4.2, h: 0.18, fontSize: 9.5, color: C.textSec, fontFace: F.body, margin: 0 });
  });

  // Próxima sesión
  addCard(s, 5.1, 2.52, 4.5, 1.55, "0A1428", C.cyan);
  s.addText("🚀 Sesión 2 — Próxima Clase", { x: 5.25, y: 2.60, w: 4.2, h: 0.30, fontSize: 12, bold: true, color: C.cyan, fontFace: F.body, margin: 0 });
  const next = ["✓ Consumir APIs: OpenAI, Anthropic, Cohere", "✓ Autenticación y manejo de API Keys", "✓ Parámetros avanzados de generación", "✓ Comparativa de costos entre proveedores"];
  next.forEach((n, i) => {
    s.addText(n, { x: 5.25, y: 2.98 + i * 0.27, w: 4.2, h: 0.25, fontSize: 10.5, color: C.textSec, fontFace: F.body });
  });

  // Ejercicios pendientes
  addCard(s, 0.4, 4.18, 9.2, 1.35, C.bgCard, C.yellow);
  s.addText("🏋️ Tarea para la próxima sesión:", { x: 0.6, y: 4.25, w: 9.0, h: 0.28, fontSize: 12, bold: true, color: C.yellow, fontFace: F.body, margin: 0 });
  const hw = [
    "1. Instalar Ollama y descargar llama3.2 y nomic-embed-text",
    "2. Ejecutar los 4 ejemplos Python (examples/01 al 04) y capturar los resultados",
    "3. Completar el Ejercicio 4 (Diseño de Arquitectura) del doc EXERCISES.md",
    "4. Leer el abstract de 'Attention Is All You Need' (arxiv.org/abs/1706.03762)",
  ];
  hw.forEach((h, i) => {
    s.addText(h, { x: 0.6, y: 4.58 + i * 0.25, w: 9.0, h: 0.22, fontSize: 10.5, color: C.textSec, fontFace: F.body });
  });

  // URL del repo
  addCard(s, 0.4, 5.60, 9.2, 0.28, "071A07", C.green);
  s.addText("📦 Repositorio: github.com/[usuario]/llm-fundamentals-session1  |  📧 Dudas al instructor", {
    x: 0.5, y: 5.62, w: 9.0, h: 0.24, fontSize: 10.5, color: C.green, fontFace: F.body, align: "center", valign: "middle", margin: 0,
  });

  s.addNotes("Slide final. Resumir los recursos. La tarea de instalar Ollama es CRÍTICA — la sesión 2 empieza directamente con llamadas a APIs y los alumnos deben tener el entorno listo.\n\nMencionarles que el paper 'Attention Is All You Need' tiene solo 15 páginas y es muy legible incluso sin background matemático profundo — el abstract y la introducción son suficientes para el nivel del curso.");
}

// ─────────────────────────────────────────────────────────────────────────
// GUARDAR ARCHIVO
// ─────────────────────────────────────────────────────────────────────────

pres.writeFile({ fileName: "Sesion1_Fundamentos_LLM.pptx" })
  .then(() => {
    console.log("✅ Presentación creada: Sesion1_Fundamentos_LLM.pptx");
    console.log(`   Slides: 20`);
  })
  .catch(err => {
    console.error("❌ Error:", err);
    process.exit(1);
  });
