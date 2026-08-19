# 🏋️ Guía de Ejercicios Prácticos — Sesión 1

## Arquitectura y Componentes Esenciales de los LLM

> **Dificultad:** ⭐ Básico | ⭐⭐ Intermedio | ⭐⭐⭐ Desafío  
> **Tiempo estimado:** 90 minutos total

---

## Ejercicio 1 ⭐ — El Tokenizador (20 min)

**Objetivo:** Comprender cómo los LLMs dividen el texto en tokens y su impacto en costos.

### Instrucciones

1. Abre la aplicación web (frontend React, pestaña "Tokenizador")
2. O ejecuta directamente: `python examples/02_tokenization.py`

### Tareas

**1.1 — Comparación de idiomas**

Tokeniza estas frases (misma idea, distintos idiomas) y completa la tabla:

| Idioma | Texto | Tokens | Tokens/Palabra |
|--------|-------|--------|----------------|
| Inglés | "The attention mechanism is the key innovation of transformers" | __ | __ |
| Español | "El mecanismo de atención es la innovación clave de los transformers" | __ | __ |
| Portugués | "O mecanismo de atenção é a principal inovação dos transformers" | __ | __ |
| Francés | "Le mécanisme d'attention est l'innovation clé des transformers" | __ | __ |

**Reflexión:** ¿Cuál idioma es más eficiente? ¿Por qué crees que ocurre esto?

**1.2 — Impacto en costos**

Con los datos del ejercicio anterior, calcula cuánto costaría traducir 100,000 documentos de 1 página (~500 palabras) del español al inglés usando GPT-4o-mini:

- Precio: $0.15 USD por millón de tokens (input)  
- Precio: $0.60 USD por millón de tokens (output)
- Tokens de input = ___ tokens/doc × 100,000 docs = ___
- Tokens de output ≈ mismo que input (traducción 1:1)
- **Costo total estimado = $_____**

**1.3 — Tokens sorprendentes**

Tokeniza cada uno de estos y observa el resultado:

```
100,000,000
www.ejemplo-empresa.com/ruta/muy/larga
¡¡¡Urgente!!! ⚠️ Error crítico en producción 🔴
# -*- coding: utf-8 -*-
```

¿Qué patrón observas con los números, URLs y caracteres especiales?

---

## Ejercicio 2 ⭐⭐ — Explorando Embeddings (25 min)

**Objetivo:** Ver experimentalmente que los embeddings capturan significado semántico.

### Instrucciones

1. Abre la pestaña "Embeddings" en la app web
2. O ejecuta: `python examples/03_embeddings.py`  
3. Asegúrate de tener instalado: `ollama pull nomic-embed-text`

### Tareas

**2.1 — Predicción vs. Realidad**

Antes de ejecutar: predice si la similitud será ALTA (>0.80), MEDIA (0.50-0.80) o BAJA (<0.50):

| Par de textos | Tu predicción | Resultado real |
|--------------|---------------|----------------|
| "data science" / "ciencia de datos" | ___ | ___ |
| "red neuronal" / "neural network" | ___ | ___ |
| "ceo" / "chief executive officer" | ___ | ___ |
| "manzana" / "apple (la fruta)" | ___ | ___ |
| "python (lenguaje)" / "python (serpiente)" | ___ | ___ |
| "arquitectura de software" / "edificio" | ___ | ___ |

**Reflexión:** ¿En qué casos te equivocaste? ¿Por qué crees que ocurrió?

**2.2 — Búsqueda semántica**

Crea tu propia "mini base de conocimiento" con 5 frases sobre un tema de tu trabajo o área de interés. Luego haz 3 consultas y verifica si el resultado más similar es el que esperabas.

**2.3 — El experimento rey-reina**

Ejecuta el ejemplo de aritmética de embeddings. ¿Qué resultado obtienes para:
- `doctor - hombre + mujer = ?`
- `París - Francia + Colombia = ?` (pista: podría darte "Bogotá")

---

## Ejercicio 3 ⭐⭐ — Chat y Temperature (20 min)

**Objetivo:** Entender el impacto del system prompt y la temperatura en las respuestas.

### Instrucciones

Usa la pestaña "Chat con LLM" de la app web.

### Tareas

**3.1 — El poder del system prompt**

Haz la MISMA pregunta con diferentes system prompts y documenta las diferencias:

**Pregunta:** "¿Deberías usar un LLM para tomar decisiones financieras importantes?"

| System Prompt | Tono de respuesta | ¿Menciona riesgos? | Longitud aprox. |
|--------------|-------------------|--------------------|-----------------|
| "Asistente LLM Expert" (default) | ___ | ___ | ___ |
| "Respuestas Concisas" | ___ | ___ | ___ |
| "Profesor Universitario" | ___ | ___ | ___ |
| "Consultor Empresarial" | ___ | ___ | ___ |

**Reflexión:** ¿Qué tan diferente fue la misma información presentada de distintas formas?

**3.2 — Experimentar con Temperature**

Haz la MISMA pregunta 3 veces cambiando solo la temperatura:

**Pregunta:** "Dame un nombre creativo para una startup de IA"

| Temperature | Respuesta | ¿Fue la misma? | ¿Fue coherente? |
|-------------|-----------|----------------|-----------------|
| 0.0 (x3) | ___ | ___ | ___ |
| 0.7 (x3) | ___ | ___ | ___ |
| 1.5 (x3) | ___ | ___ | ___ |

**Reflexión:** ¿Para qué tipos de tareas empresariales usarías temperatura baja vs alta?

**3.3 — Detectar alucinaciones**

Pregúntale al modelo cosas que NO puede saber con certeza:

- "¿Cuántos empleados tiene la empresa [poner una empresa local pequeña]?"
- "¿Cuál fue el precio de cierre de Apple el 15 de agosto de 2024?"
- "¿Qué dijo el CEO de [empresa] en su última conferencia?"

¿Cómo responde el modelo? ¿Admite incertidumbre o inventa datos?

---

## Ejercicio 4 ⭐⭐⭐ — Desafío: Diseño de Arquitectura (25 min)

**Objetivo:** Aplicar los conceptos a un caso de uso empresarial real.

### Escenario

Una empresa de seguros quiere implementar un chatbot que responda preguntas sobre sus pólizas. Tienen:
- 500 documentos de pólizas (cada uno ~20 páginas = ~10,000 tokens)
- Proyección de 10,000 consultas/día
- Presupuesto: $200 USD/mes en APIs

### Preguntas de diseño

**4.1 — ¿Cabe todo en el contexto?**

Si quisieras incluir todos los documentos en el contexto de cada llamada:
- Total tokens = 500 × 10,000 = _____ tokens
- ¿Qué modelo necesitarías? (ver tabla de contextos)
- Costo estimado por llamada con GPT-4o = $_____
- Costo mensual con 10,000 llamadas/día = $_____
- ¿Es viable con el presupuesto de $200/mes? ___

**4.2 — Estrategia alternativa: RAG**

Con una estrategia RAG (solo incluir los 3 fragmentos más relevantes por consulta):
- Tokens por consulta ≈ 3 fragmentos × 500 tokens + 200 prompt = ___ tokens
- Costo por llamada con GPT-4o-mini = $_____  
- Costo mensual = $_____
- ¿Es viable ahora? ___

**4.3 — Recomendación final**

Escribe en 3-4 oraciones qué arquitectura recomendarías y por qué, considerando:
- Costo
- Precisión de las respuestas
- Privacidad (las pólizas son confidenciales)
- Escalabilidad

---

## 📊 Evaluación

| Ejercicio | Puntos | Criterio |
|-----------|--------|---------|
| 1.1 Tabla completada | 10 | Datos correctos |
| 1.2 Cálculo de costo | 10 | Metodología correcta |
| 2.1 Predicciones | 15 | Reflexión sobre errores |
| 3.1 System prompts | 15 | Análisis comparativo |
| 3.3 Alucinaciones | 15 | Casos identificados |
| 4 Arquitectura | 35 | Profundidad del análisis |

**Total: 100 puntos**

---

## 🔍 Soluciones y Discusión

Las respuestas de los ejercicios 4.1 y 4.2 se discutirán en clase.
Para los ejercicios de predicción (2.1, 3.1): no hay una respuesta única correcta;
lo valioso es la reflexión sobre el comportamiento observado.

---

*Sesión 1 — Fundamentos de Arquitectura LLM · BSG Institute*
