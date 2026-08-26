# Setup — Sesión 1b: APIs REST y LLMs

## Requisitos

- Python 3.10+
- Node.js 18+ (para el frontend React)
- Ollama corriendo localmente

---

## Instalación paso a paso

### 1. Dependencias Python

```bash
pip install -r requirements.txt
```

### 2. Ollama

```bash
# Instalar Ollama
# macOS/Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: descargar desde https://ollama.ai/download

# Iniciar servidor
ollama serve

# Descargar modelos (otra terminal)
ollama pull llama3.2          # chat (2 GB)
ollama pull nomic-embed-text  # embeddings (274 MB)
```

### 3. Backend FastAPI

```bash
cd session_1b/backend
uvicorn main:app --reload --port 8000
```

Verificar: http://localhost:8000/docs

### 4. Frontend React

```bash
cd session_1b/frontend
npm install
npm run dev
```

Abrir: http://localhost:5173

---

## Endpoints del backend

| Método | Endpoint         | Descripción |
|--------|-----------------|-------------|
| GET    | `/`             | Health check |
| GET    | `/health`       | Estado de Ollama |
| GET    | `/modelos`      | Modelos instalados |
| POST   | `/chat`         | Chat (sin streaming) |
| POST   | `/chat/stream`  | Chat con streaming SSE |
| POST   | `/embeddings`   | Generar embeddings |

### Ejemplo curl

```bash
# Chat simple
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Que es un transformer?"}],
    "model": "llama3.2",
    "temperature": 0.7
  }'

# Listar modelos
curl http://localhost:8000/modelos
```

---

## Arquitectura del sistema

```
Usuario
  |
  | (navegador)
  v
React Frontend (port 5173)
  |
  | HTTP POST /chat
  v
FastAPI Backend (port 8000)
  |
  | HTTP POST /api/chat
  v
Ollama (port 11434)
  |
  | (modelo local)
  v
llama3.2 / mistral / etc.
```

---

## Resolución de problemas

### "CORS error" en el navegador
El backend tiene CORS habilitado. Si el error persiste:
- Verificar que el backend corre en `localhost:8000`
- En `vite.config.js` el proxy redirige `/api` al backend

### "502 Bad Gateway" o timeout
- Verificar que Ollama está corriendo: `curl http://localhost:11434/api/tags`
- El modelo puede tardar 30s+ en cargarse la primera vez

### Frontend no conecta al backend
- Backend en `localhost:8000` ✓
- Frontend en `localhost:5173` ✓
- Sin firewall bloqueando estos puertos
