"""
main.py — Punto de entrada del Backend FastAPI
===============================================
Servidor API para el curso "Fundamentos de Arquitectura LLM"
Sesión 1: Arquitectura y Componentes Esenciales de los LLM

Ejecutar con:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Documentación interactiva disponible en:
    http://localhost:8000/docs  (Swagger UI)
    http://localhost:8000/redoc (ReDoc)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from routers.llm_router import router as llm_router
from services.ollama_service import check_ollama_health
from models.schemas import HealthResponse


# ── Lifespan (startup / shutdown) ──────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ejecuta tareas al iniciar y apagar el servidor."""
    # STARTUP
    print("\n" + "="*60)
    print("🚀 Fundamentos de Arquitectura LLM — Backend Iniciado")
    print("="*60)

    health = await check_ollama_health()
    if health["available"]:
        print(f"✅ Ollama conectado en {health['url']}")
        print(f"   Modelos disponibles: {health['model_count']}")
    else:
        print(f"⚠️  Ollama NO disponible en {health['url']}")
        print("   Para iniciar Ollama: ejecuta 'ollama serve' en otra terminal")

    print("\n📚 Documentación API:")
    print("   Swagger UI: http://localhost:8000/docs")
    print("   ReDoc:      http://localhost:8000/redoc")
    print("="*60 + "\n")

    yield  # La aplicación corre aquí

    # SHUTDOWN
    print("\n🛑 Servidor detenido correctamente")


# ── Aplicación FastAPI ──────────────────────────────────────────────────────

app = FastAPI(
    title="🤖 LLM Fundamentals API",
    description="""
## API Educativa — Fundamentos de Arquitectura LLM

Esta API fue construida para el **Curso de Fundamentos de Arquitectura LLM**,
Sesión 1: Arquitectura y Componentes Esenciales de los LLM.

### ¿Qué puedo hacer con esta API?

| Endpoint | Descripción | Concepto LLM |
|----------|-------------|--------------|
| `POST /api/chat` | Chatear con un LLM local | Inferencia, prompts |
| `POST /api/tokenize` | Explorar tokenización | Tokens, vocabulario |
| `POST /api/embed` | Generar embeddings | Espacio vectorial |
| `POST /api/similarity` | Comparar textos semánticamente | Similitud coseno |
| `GET /api/models` | Ver modelos disponibles | Gestión de modelos |
| `GET /api/context-info/{model}` | Ventana de contexto | Límites del modelo |

### Requisito previo
Tener **Ollama** corriendo localmente:
```bash
ollama serve
ollama pull llama3.2
ollama pull nomic-embed-text
```
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS — permite que el frontend React se conecte ────────────────────────

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Registrar routers ───────────────────────────────────────────────────────

app.include_router(llm_router)


# ── Endpoints base ─────────────────────────────────────────────────────────

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Sistema"],
    summary="Estado del servidor",
)
async def health_check():
    """
    Verifica que el servidor esté activo y que Ollama esté disponible.
    Útil para monitoreo y para confirmar la configuración inicial.
    """
    ollama_info = await check_ollama_health()
    return HealthResponse(
        status="ok",
        ollama_available=ollama_info["available"],
        ollama_url=ollama_info["url"],
        available_models=ollama_info["model_count"],
    )


@app.get("/", tags=["Sistema"], summary="Información del servidor")
async def root():
    """Información básica de la API."""
    return {
        "name": "LLM Fundamentals API",
        "version": "1.0.0",
        "description": "API educativa para el curso Fundamentos de Arquitectura LLM",
        "session": "Sesión 1 — Arquitectura y Componentes Esenciales",
        "docs": "/docs",
        "health": "/health",
    }


# ── Punto de entrada directo ────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", 8000))
    reload = os.getenv("BACKEND_RELOAD", "true").lower() == "true"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
