"""
ollama_service.py — Servicio de integración con Ollama
=======================================================
Contiene toda la lógica de negocio para interactuar con
el servidor Ollama local. Abstrae los detalles de la API
de Ollama detrás de métodos limpios y bien documentados.

Nota educativa:
    Ollama expone una API REST en http://localhost:11434
    que es compatible (en parte) con la API de OpenAI.
    Esto facilita migrar entre proveedores.
"""

import httpx
import time
import numpy as np
from typing import Optional, List, Dict, Any
from rich import print as rprint


# URL base de Ollama (puede sobreescribirse vía variable de entorno)
OLLAMA_BASE_URL = "http://localhost:11434"

# Timeout generoso porque los modelos locales pueden ser lentos
HTTP_TIMEOUT = 120.0


# ── Información de modelos conocidos ─────────────────────────────────────────
# Contexto en tokens para los modelos más comunes
MODEL_CONTEXT_INFO = {
    "llama3.2":        {"context": 128_000, "family": "Llama 3.2"},
    "llama3.1":        {"context": 128_000, "family": "Llama 3.1"},
    "llama3":          {"context": 8_192,   "family": "Llama 3"},
    "llama2":          {"context": 4_096,   "family": "Llama 2"},
    "mistral":         {"context": 32_768,  "family": "Mistral"},
    "phi3":            {"context": 128_000, "family": "Phi-3"},
    "gemma2":          {"context": 8_192,   "family": "Gemma 2"},
    "nomic-embed-text":{"context": 8_192,   "family": "Nomic"},
    "default":         {"context": 4_096,   "family": "Unknown"},
}


async def get_available_models() -> List[Dict[str, Any]]:
    """
    Consulta Ollama para obtener la lista de modelos instalados.

    Returns:
        Lista de diccionarios con información de cada modelo.

    Raises:
        httpx.ConnectError: Si Ollama no está corriendo.
    """
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        data = response.json()

        models = []
        for m in data.get("models", []):
            name = m.get("name", "").split(":")[0]  # quitar el tag :latest
            size_bytes = m.get("size", 0)
            size_gb = size_bytes / (1024 ** 3)

            ctx_info = MODEL_CONTEXT_INFO.get(name, MODEL_CONTEXT_INFO["default"])

            models.append({
                "name": m.get("name", ""),
                "size": f"{size_gb:.1f} GB" if size_gb > 0 else "Desconocido",
                "context_length": ctx_info["context"],
                "family": ctx_info["family"],
            })

        return models


async def chat(
    model: str,
    message: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 512,
) -> Dict[str, Any]:
    """
    Envía un mensaje al LLM y devuelve la respuesta completa.

    Conceptos demostrados:
        - Estructura de un prompt (system + user)
        - Parámetros de generación (temperature, num_predict)
        - Tiempo de inferencia local vs API cloud

    Args:
        model: Nombre del modelo Ollama (ej: "llama3.2")
        message: Mensaje del usuario
        system_prompt: Instrucción de sistema (contexto del rol del LLM)
        temperature: 0.0=determinístico, 1.0=balanceado, 2.0=muy creativo
        max_tokens: Límite de tokens en la respuesta

    Returns:
        Diccionario con 'response', 'tokens', 'duration_ms', etc.
    """
    start_time = time.time()

    payload = {
        "model": model,
        "prompt": message,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
    }

    # Agregar system prompt si se proporcionó
    if system_prompt:
        payload["system"] = system_prompt

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload
        )
        response.raise_for_status()
        data = response.json()

    duration_ms = (time.time() - start_time) * 1000

    return {
        "model": model,
        "message": data.get("response", ""),
        "prompt_tokens": data.get("prompt_eval_count", 0),
        "completion_tokens": data.get("eval_count", 0),
        "tokens_used": (
            data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
        ),
        "duration_ms": round(duration_ms, 2),
    }


async def generate_embedding(
    text: str,
    model: str = "nomic-embed-text"
) -> List[float]:
    """
    Genera un vector embedding para el texto dado.

    Nota educativa:
        Los embeddings son representaciones numéricas del SIGNIFICADO
        semántico de un texto. Un modelo como nomic-embed-text convierte
        "perro" en un vector de 768 dimensiones. El vector de "gato"
        estará geométricamente cerca porque ambas palabras son animales.

        Esto es la base de la búsqueda semántica y RAG (Retrieval-Augmented
        Generation).

    Args:
        text: Texto a convertir en embedding
        model: Modelo de embeddings (debe soportar /api/embeddings)

    Returns:
        Vector numpy array de flotantes
    """
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/embeddings",
            json={"model": model, "prompt": text}
        )
        response.raise_for_status()
        data = response.json()

    return data.get("embedding", [])


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calcula la similitud coseno entre dos vectores.

    La similitud coseno mide el ángulo entre vectores:
        1.0 = idénticos (mismo ángulo, 0°)
        0.0 = ortogonales (sin relación, 90°)
       -1.0 = opuestos (180°) — raro en embeddings de texto

    La usamos porque es invariante a la magnitud del vector:
    solo importa la DIRECCIÓN, no la longitud.

    Args:
        vec1: Primer vector de embeddings
        vec2: Segundo vector de embeddings

    Returns:
        Similitud coseno entre -1.0 y 1.0
    """
    v1 = np.array(vec1)
    v2 = np.array(vec2)

    # Normalizar para evitar división por cero
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(v1, v2) / (norm1 * norm2))


def interpret_similarity(score: float) -> str:
    """Convierte un score de similitud en lenguaje natural."""
    if score >= 0.95:
        return "🟢 Casi idénticos — el modelo considera estos textos prácticamente iguales en significado"
    elif score >= 0.85:
        return "🟢 Muy similares — tema o concepto muy relacionado"
    elif score >= 0.70:
        return "🟡 Moderadamente similares — comparten contexto o dominio"
    elif score >= 0.50:
        return "🟠 Relacionados vagamente — alguna conexión semántica"
    else:
        return "🔴 Poco relacionados — conceptos o temas diferentes"


def get_context_info(model: str) -> Dict[str, Any]:
    """
    Devuelve información sobre la ventana de contexto de un modelo.

    Nota educativa:
        La VENTANA DE CONTEXTO es el límite máximo de tokens que el modelo
        puede "ver" y procesar en una sola llamada. Incluye:
          - El system prompt
          - El historial de conversación
          - La pregunta actual
          - La respuesta que está generando

        Un modelo con 128K tokens puede procesar ~96,000 palabras (~190 páginas).
        Cuando el contexto se desborda, el modelo "olvida" la parte más antigua.

    Args:
        model: Nombre del modelo

    Returns:
        Diccionario con información del contexto
    """
    # Normalizar nombre (quitar tag :latest si existe)
    model_base = model.split(":")[0]
    info = MODEL_CONTEXT_INFO.get(model_base, MODEL_CONTEXT_INFO["default"])
    context_length = info["context"]

    # Aproximaciones: 1 token ≈ 0.75 palabras en inglés, ~0.6 en español
    words_approx = int(context_length * 0.65)
    pages_approx = round(words_approx / 500, 1)

    # Casos de uso según tamaño de contexto
    if context_length >= 100_000:
        use_cases = [
            "Análisis de documentos legales completos",
            "Procesamiento de libros o manuales técnicos",
            "Conversaciones muy largas sin pérdida de contexto",
            "Análisis de bases de código extensas",
        ]
    elif context_length >= 32_000:
        use_cases = [
            "Análisis de reportes largos (50-100 páginas)",
            "Revisión de contratos extensos",
            "Conversaciones largas con historial",
            "Análisis de múltiples documentos medianos",
        ]
    elif context_length >= 8_000:
        use_cases = [
            "Análisis de documentos cortos (10-20 páginas)",
            "Conversaciones de mediana longitud",
            "Summarización de artículos",
        ]
    else:
        use_cases = [
            "Preguntas y respuestas cortas",
            "Generación de texto breve",
            "Clasificación de textos cortos",
        ]

    return {
        "model": model,
        "context_length": context_length,
        "estimated_words": words_approx,
        "estimated_pages": pages_approx,
        "use_cases": use_cases,
    }


async def check_ollama_health() -> Dict[str, Any]:
    """Verifica si Ollama está corriendo y devuelve estado."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return {
                    "available": True,
                    "url": OLLAMA_BASE_URL,
                    "model_count": len(models),
                }
    except Exception:
        pass

    return {
        "available": False,
        "url": OLLAMA_BASE_URL,
        "model_count": 0,
    }
