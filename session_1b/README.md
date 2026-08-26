# Sesión 1b — APIs REST y LLMs en la Práctica
**BSG Institute · 3 horas · Nivel: Sin experiencia con APIs/REST**

---

## ¿Para quién es esta sesión?

Para profesionales que:
- Entienden conceptos de software pero nunca han consumido una API REST
- Quieren conectar aplicaciones a modelos de lenguaje (Ollama, OpenAI, Anthropic)
- Necesitan entender el protocolo HTTP antes de usar los SDKs de LLM

---

## Agenda (3 horas)

### Bloque 1 — HTTP y REST desde Cero (60 min)
- `01_http_conceptos.py` — Qué es HTTP, verbos, status codes, headers
- `02_get_requests.py` — Consumir APIs públicas con requests
- `03_post_json.py` — Enviar datos JSON, autenticación básica

### Break (10 min)

### Bloque 2 — APIs de LLM en Detalle (60 min)
- `04_ollama_api.py` — API de Ollama: chat, generate, embeddings
- `05_openai_compatible.py` — Interfaz OpenAI-compatible (Ollama + SDK)
- `06_streaming.py` — Streaming de respuestas token a token

### Bloque 3 — Tu Propio Backend LLM (50 min)
- `backend/main.py` — Gateway LLM con FastAPI
- `frontend/` — Interfaz React simple para chatear
- Demo en vivo: React → FastAPI → Ollama

---

## Conceptos clave

| Concepto | Para qué sirve |
|----------|----------------|
| HTTP POST | Enviar prompts al LLM |
| JSON | Formato de request y response |
| Status codes | Detectar errores (429, 500, 200) |
| Headers | Autenticación, content-type |
| Streaming | Mostrar texto token por token |
| FastAPI | Crear tu propio endpoint LLM |
| CORS | Conectar frontend React con backend |

---

## Requisitos

Ver `docs/SETUP.md` para instrucciones detalladas.

- Python 3.10+
- Ollama corriendo: `ollama serve` + `ollama pull llama3.2`
- Node.js 18+ (para el frontend React)
