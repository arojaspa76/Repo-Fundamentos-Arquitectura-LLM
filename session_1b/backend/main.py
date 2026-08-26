"""
Backend — Gateway LLM con FastAPI
====================================
Un backend real que expone tu Ollama local como una API REST.
El frontend React se conecta a este endpoint.

Ejecutar:
    cd session_1b/backend
    uvicorn main:app --reload --port 8000

Documentacion interactiva:
    http://localhost:8000/docs
"""

import time
import json
import httpx
from typing import Optional, AsyncIterator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# ─────────────────────────────────────────────────────────────────────────────
# Configuracion
# ─────────────────────────────────────────────────────────────────────────────
OLLAMA_URL    = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"

# ─────────────────────────────────────────────────────────────────────────────
# App FastAPI
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="BSG LLM Gateway",
    description="Gateway entre frontend React y Ollama local",
    version="1.0.0",
)

# CORS — permite que el frontend React (puerto 5173) llame al backend (8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# Modelos Pydantic (validacion de datos)
# ─────────────────────────────────────────────────────────────────────────────
class Mensaje(BaseModel):
    role: str = Field(..., description="'user', 'assistant', o 'system'")
    content: str = Field(..., description="Contenido del mensaje")


class ChatRequest(BaseModel):
    messages: list[Mensaje] = Field(..., description="Historial de conversacion")
    model: str = Field(DEFAULT_MODEL, description="Modelo Ollama a usar")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="0=deterministico, 1=creativo")
    max_tokens: int = Field(1000, ge=1, le=4096)
    stream: bool = Field(False, description="True para streaming token a token")


class ChatResponse(BaseModel):
    respuesta: str
    modelo: str
    tokens_input: int
    tokens_output: int
    tokens_total: int
    duracion_ms: int
    costo_estimado_usd: float


class ModelInfo(BaseModel):
    nombre: str
    tamanio_gb: float
    familia: str


# ─────────────────────────────────────────────────────────────────────────────
# Helper — cliente Ollama
# ─────────────────────────────────────────────────────────────────────────────
async def llamar_ollama(payload: dict) -> dict:
    """Llama a Ollama de forma asincrona."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
        r.raise_for_status()
        return r.json()


async def stream_ollama(payload: dict) -> AsyncIterator[str]:
    """Genera chunks de streaming desde Ollama."""
    payload["stream"] = True
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as r:
            async for linea in r.aiter_lines():
                if linea:
                    yield linea


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    """Health check del gateway."""
    return {"status": "ok", "servicio": "BSG LLM Gateway", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health():
    """Verifica que Ollama este disponible."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(f"{OLLAMA_URL}/api/tags")
            if r.status_code == 200:
                modelos = r.json().get("models", [])
                return {
                    "status": "ok",
                    "ollama": "disponible",
                    "modelos_instalados": len(modelos),
                }
    except Exception as e:
        pass
    return {"status": "degraded", "ollama": "no disponible", "error": str(e)}


@app.get("/modelos", response_model=list[ModelInfo], tags=["Modelos"])
async def listar_modelos():
    """Lista todos los modelos instalados en Ollama."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{OLLAMA_URL}/api/tags")
            r.raise_for_status()
            modelos = r.json().get("models", [])
            return [
                ModelInfo(
                    nombre=m["name"],
                    tamanio_gb=m.get("size", 0) / 1e9,
                    familia=m.get("details", {}).get("family", "desconocida"),
                )
                for m in modelos
            ]
    except httpx.ConnectError:
        raise HTTPException(503, "Ollama no disponible. Ejecuta: ollama serve")
    except Exception as e:
        raise HTTPException(500, f"Error al listar modelos: {e}")


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(req: ChatRequest):
    """
    Endpoint principal de chat.
    Recibe historial de mensajes y retorna la respuesta del LLM.
    """
    if req.stream:
        raise HTTPException(400, "Para streaming usa POST /chat/stream")

    payload = {
        "model": req.model,
        "messages": [m.model_dump() for m in req.messages],
        "stream": False,
        "options": {
            "temperature": req.temperature,
            "num_predict": req.max_tokens,
        },
    }

    try:
        t0 = time.time()
        data = await llamar_ollama(payload)
        duracion_ms = int((time.time() - t0) * 1000)

        tokens_in  = data.get("prompt_eval_count", 0)
        tokens_out = data.get("eval_count", 0)

        # Costo estimado (0 si es local, precio real si fuera cloud)
        costo = 0.0  # Ollama es gratis

        return ChatResponse(
            respuesta=data["message"]["content"],
            modelo=data.get("model", req.model),
            tokens_input=tokens_in,
            tokens_output=tokens_out,
            tokens_total=tokens_in + tokens_out,
            duracion_ms=duracion_ms,
            costo_estimado_usd=costo,
        )

    except httpx.ConnectError:
        raise HTTPException(503, "Ollama no disponible. Ejecuta: ollama serve")
    except httpx.HTTPStatusError as e:
        raise HTTPException(e.response.status_code, f"Error de Ollama: {e.response.text}")
    except Exception as e:
        raise HTTPException(500, f"Error interno: {e}")


@app.post("/chat/stream", tags=["Chat"])
async def chat_stream(req: ChatRequest):
    """
    Endpoint de chat con streaming.
    Retorna Server-Sent Events (SSE) con tokens uno a uno.
    """
    payload = {
        "model": req.model,
        "messages": [m.model_dump() for m in req.messages],
        "options": {"temperature": req.temperature, "num_predict": req.max_tokens},
    }

    async def generar():
        try:
            async for linea in stream_ollama(payload):
                chunk = json.loads(linea)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    # Server-Sent Events format
                    yield f"data: {json.dumps({'token': token})}\n\n"
                if chunk.get("done"):
                    yield f"data: {json.dumps({'done': True})}\n\n"
                    break
        except httpx.ConnectError:
            yield f"data: {json.dumps({'error': 'Ollama no disponible'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generar(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/embeddings", tags=["Embeddings"])
async def generar_embeddings(
    texto: str,
    modelo: str = "nomic-embed-text",
):
    """Genera el embedding vectorial de un texto."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": modelo, "prompt": texto},
            )
            r.raise_for_status()
            data = r.json()
            embedding = data["embedding"]
            return {
                "texto": texto[:100],
                "modelo": modelo,
                "dimensiones": len(embedding),
                "embedding": embedding[:5],   # solo primeros 5 para la demo
                "embedding_completo": embedding,
            }
    except httpx.ConnectError:
        raise HTTPException(503, "Ollama no disponible")
    except Exception as e:
        raise HTTPException(500, f"Error: {e}")
