# 🤖 Fundamentos de Arquitectura LLM — Sesión 1
## Arquitectura y Componentes Esenciales de los LLM

> **Curso:** Fundamentos de Arquitectura LLM  
> **Capítulo 1:** Conceptos Fundamentales de LLM  
> **Sesión:** 1 — Arquitectura Transformer, Embeddings y Limitaciones  
> **Stack:** Python 3.11+ · FastAPI · Ollama · React 18 · Vite  

---

## 📋 Tabla de Contenidos

- [¿Qué aprenderás?](#qué-aprenderás)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación Rápida](#instalación-rápida)
- [Instalación de Ollama (LLM Local)](#instalación-de-ollama)
- [Ejecutar el Backend FastAPI](#ejecutar-el-backend-fastapi)
- [Ejecutar el Frontend React](#ejecutar-el-frontend-react)
- [Ejemplos de Código](#ejemplos-de-código)
- [Ejercicios Prácticos](#ejercicios-prácticos)
- [Conceptos Clave](#conceptos-clave)
- [Recursos Adicionales](#recursos-adicionales)

---

## 🎯 ¿Qué aprenderás?

Al finalizar esta sesión serás capaz de:

1. **Explicar** la arquitectura Transformer y el mecanismo de atención
2. **Comprender** qué son los tokens y cómo los LLM procesan el texto
3. **Visualizar** embeddings y su representación vectorial
4. **Identificar** la ventana de contexto y sus límites prácticos
5. **Reconocer** las capacidades y limitaciones típicas de los LLM
6. **Ejecutar** un LLM localmente con Ollama y consumir su API

---

## 🏗️ Arquitectura del Proyecto

```
llm-session1/
├── README.md                    ← Este archivo
├── requirements.txt             ← Dependencias Python
├── .env.example                 ← Variables de entorno de ejemplo
├── .gitignore
│
├── backend/                     ← API FastAPI
│   ├── main.py                  ← Punto de entrada
│   ├── models/
│   │   └── schemas.py           ← Pydantic models
│   ├── routers/
│   │   └── llm_router.py        ← Endpoints LLM
│   └── services/
│       └── ollama_service.py    ← Lógica de negocio Ollama
│
├── frontend/                    ← App React + Vite
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── components/
│           ├── ChatInterface.jsx     ← Chat con LLM local
│           ├── TokenVisualizer.jsx   ← Visualiza tokens
│           └── EmbeddingExplorer.jsx ← Explora embeddings
│
├── examples/                    ← Scripts Python educativos
│   ├── 01_basic_api_call.py     ← Primera llamada a la API
│   ├── 02_tokenization.py       ← Exploración de tokens
│   ├── 03_embeddings.py         ← Trabajo con embeddings
│   └── 04_context_window.py     ← Límites de contexto
│
├── docs/
│   ├── OLLAMA_SETUP.md          ← Guía de instalación Ollama
│   ├── CONCEPTS.md              ← Glosario de conceptos
│   └── EXERCISES.md             ← Guía de ejercicios
│
└── notebooks/
    └── 01_transformer_basics.ipynb  ← Notebook interactivo
```

---

## 📦 Requisitos Previos

| Herramienta | Versión mínima | Enlace |
|------------|---------------|--------|
| Python | 3.11+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Ollama | Última | [ollama.com](https://ollama.com) |
| Git | 2.x | [git-scm.com](https://git-scm.com) |

> **RAM recomendada:** 8 GB mínimo para modelos pequeños (Llama 3.2 3B), 16 GB para modelos medianos (Llama 3.1 8B)

---

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/llm-fundamentals-session1.git
cd llm-fundamentals-session1
```

### 2. Configurar entorno Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

---

## 🦙 Instalación de Ollama

Ollama te permite ejecutar LLMs **completamente local** sin necesidad de API keys ni costos.

### Instalación por sistema operativo

**macOS:**
```bash
brew install ollama
# O descargar desde https://ollama.com/download
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Descargar el instalador desde [https://ollama.com/download/windows](https://ollama.com/download/windows)

### Descargar y ejecutar un modelo

```bash
# Iniciar el servidor Ollama (si no está ya corriendo)
ollama serve

# En otra terminal: descargar modelo Llama 3.2 (2GB - recomendado para la clase)
ollama pull llama3.2

# Probar que funciona
ollama run llama3.2 "¿Qué es un LLM? Responde en 2 oraciones."

# Otros modelos disponibles:
ollama pull mistral          # 4.1GB - muy bueno
ollama pull phi3             # 2.3GB - rápido
ollama pull nomic-embed-text # Para embeddings
```

### Verificar instalación

```bash
# Listar modelos instalados
ollama list

# Ver modelos corriendo
ollama ps

# La API de Ollama estará disponible en:
# http://localhost:11434
```

### Test rápido de la API de Ollama

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "¿Qué es un transformer en IA?",
  "stream": false
}'
```

---

## ⚙️ Ejecutar el Backend FastAPI

```bash
# Asegurarse de tener Ollama corriendo primero
ollama serve &

# Ir al directorio del backend
cd backend

# Ejecutar el servidor de desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:
- **API:** http://localhost:8000
- **Documentación interactiva (Swagger):** http://localhost:8000/docs
- **Documentación alternativa (ReDoc):** http://localhost:8000/redoc

### Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Estado del servidor |
| GET | `/models` | Listar modelos Ollama disponibles |
| POST | `/chat` | Enviar mensaje al LLM |
| POST | `/tokenize` | Tokenizar texto (conteo aproximado) |
| POST | `/embed` | Generar embeddings |
| GET | `/context-info/{model}` | Info de ventana de contexto |

---

## 🎨 Ejecutar el Frontend React

```bash
# Ir al directorio del frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

La aplicación estará disponible en: **http://localhost:5173**

---

## 💻 Ejemplos de Código

### Ejemplo básico — Primera llamada a Ollama

```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": "Explica qué es la atención en los transformers en 3 líneas",
        "stream": False
    }
)

print(response.json()["response"])
```

### Ejemplo con nuestra API FastAPI

```python
import requests

# Chat básico
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "model": "llama3.2",
        "message": "¿Qué son los embeddings?",
        "system_prompt": "Eres un experto en LLMs. Responde de forma concisa."
    }
)
print(response.json())

# Tokenizar texto
response = requests.post(
    "http://localhost:8000/tokenize",
    json={"text": "Los modelos de lenguaje son fascinantes"}
)
print(f"Tokens aproximados: {response.json()['token_count']}")
```

---

## 🏋️ Ejercicios Prácticos

Ver el archivo [`docs/EXERCISES.md`](docs/EXERCISES.md) para la guía completa.

**Ejercicio 1 — El Tokenizador:**
Usa el endpoint `/tokenize` para comparar cuántos tokens usan diferentes idiomas para el mismo concepto. ¿Por qué importa esto?

**Ejercicio 2 — Ventana de Contexto:**
Envía mensajes progresivamente más largos al modelo. ¿Cuándo empieza a "olvidar" información del inicio?

**Ejercicio 3 — Alucinaciones:**
Pregúntale al modelo sobre un evento ficticio y observa su respuesta. ¿Cómo detectar y mitigar alucinaciones?

**Ejercicio 4 — Comparar Modelos:**
Si tienes varios modelos instalados, compara sus respuestas a la misma pregunta técnica. ¿Qué diferencias notas?

---

## 📚 Conceptos Clave

| Concepto | Definición rápida |
|----------|------------------|
| **Token** | Unidad mínima de texto que procesa un LLM (~0.75 palabras en inglés) |
| **Transformer** | Arquitectura neuronal basada en mecanismos de atención (2017) |
| **Self-Attention** | Mecanismo que permite al modelo relacionar todas las palabras entre sí |
| **Embedding** | Representación vectorial densa de texto en espacio n-dimensional |
| **Ventana de Contexto** | Cantidad máxima de tokens que el modelo puede procesar a la vez |
| **Temperatura** | Parámetro que controla la creatividad/aleatoriedad de las respuestas |
| **Top-P / Top-K** | Parámetros de muestreo para controlar la diversidad de tokens |
| **Alucinación** | Cuando el modelo genera información plausible pero falsa |
| **Fine-tuning** | Ajuste fino del modelo para tareas específicas |
| **RAG** | Retrieval-Augmented Generation — enriquecer el contexto con documentos externos |

---

## 🔗 Recursos Adicionales

### Lectura obligatoria
- 📄 [Attention Is All You Need (Paper original Transformer)](https://arxiv.org/abs/1706.03762)
- 📄 [Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)

### Herramientas y Plataformas
- 🦙 [Ollama — LLMs locales](https://ollama.com)
- 🤗 [Hugging Face — Modelos y datasets](https://huggingface.co)
- 📊 [Tokenizer Playground (OpenAI)](https://platform.openai.com/tokenizer)
- 🔍 [Embedding Projector (TensorFlow)](https://projector.tensorflow.org)

### Videos Recomendados
- 🎥 "Attention in transformers, visually explained" — 3Blue1Brown
- 🎥 "But what is a GPT? Visual intro to transformers" — 3Blue1Brown

---

## 🧑‍💻 Autor y Créditos

Desarrollado para el curso **Fundamentos de Arquitectura LLM** — Sesión 1  
Plataforma: BSG Institute  

---

## 📄 Licencia

MIT License — Libre para uso educativo y comercial.
