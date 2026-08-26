"""
schemas.py — Modelos Pydantic para validación de datos
=======================================================
Define la estructura de requests y responses de la API.
Los estudiantes pueden ver aquí cómo se tipifica la comunicación
con un LLM a través de una API REST.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# ── Enums ──────────────────────────────────────────────────────────────────


class SupportedModel(str, Enum):
    """Modelos Ollama más comunes para el curso."""
    LLAMA32 = "llama3.2"
    LLAMA31 = "llama3.1"
    MISTRAL = "mistral"
    PHI3 = "phi3"
    GEMMA2 = "gemma2"


# ── Requests ───────────────────────────────────────────────────────────────


class ChatRequest(BaseModel):
    """
    Request para el endpoint de chat.

    Ejemplo de uso:
        POST /chat
        {
            "model": "llama3.2",
            "message": "¿Qué es un transformer?",
            "system_prompt": "Responde en español de forma concisa.",
            "temperature": 0.7,
            "max_tokens": 512
        }
    """
    model: str = Field(
        default="llama3.2",
        description="Nombre del modelo Ollama a usar",
        example="llama3.2"
    )
    message: str = Field(
        ...,
        description="Mensaje del usuario",
        example="¿Qué es un transformer en IA?",
        min_length=1,
        max_length=4000
    )
    system_prompt: Optional[str] = Field(
        default="Eres un asistente experto en LLMs y arquitecturas de IA. Responde siempre en español de forma clara y educativa.",
        description="Instrucción de sistema para el modelo"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Control de creatividad: 0=determinístico, 2=muy creativo"
    )
    max_tokens: int = Field(
        default=512,
        ge=1,
        le=4096,
        description="Número máximo de tokens a generar"
    )
    stream: bool = Field(
        default=False,
        description="Si True, devuelve la respuesta en streaming"
    )


class TokenizeRequest(BaseModel):
    """
    Request para estimar tokens en un texto.

    Nota educativa: Los LLMs procesan texto como secuencias de tokens,
    no como palabras. Un token ~= 0.75 palabras en inglés,
    ~= 0.5-0.6 palabras en español.
    """
    text: str = Field(
        ...,
        description="Texto a tokenizar",
        example="Los modelos de lenguaje son fascinantes"
    )
    model: str = Field(
        default="llama3.2",
        description="Modelo de referencia para el conteo"
    )


class EmbedRequest(BaseModel):
    """
    Request para generar embeddings (representaciones vectoriales).

    Nota educativa: Los embeddings convierten texto en vectores numéricos
    en un espacio de alta dimensión. Textos similares tienen vectores
    cercanos (alta similitud coseno).
    """
    text: str = Field(
        ...,
        description="Texto a convertir en embedding",
        example="inteligencia artificial",
        min_length=1
    )
    model: str = Field(
        default="nomic-embed-text",
        description="Modelo de embeddings (recomendado: nomic-embed-text)"
    )


class SimilarityRequest(BaseModel):
    """Request para calcular similitud entre dos textos."""
    text1: str = Field(..., description="Primer texto")
    text2: str = Field(..., description="Segundo texto")
    model: str = Field(default="nomic-embed-text")


# ── Responses ──────────────────────────────────────────────────────────────


class ChatResponse(BaseModel):
    """Respuesta del endpoint de chat."""
    model: str = Field(description="Modelo que generó la respuesta")
    message: str = Field(description="Respuesta del LLM")
    tokens_used: Optional[int] = Field(None, description="Tokens aproximados usados")
    prompt_tokens: Optional[int] = Field(None, description="Tokens del prompt")
    completion_tokens: Optional[int] = Field(None, description="Tokens generados")
    duration_ms: Optional[float] = Field(None, description="Tiempo de generación en ms")


class TokenizeResponse(BaseModel):
    """
    Respuesta del endpoint de tokenización.

    Nota: Esta es una estimación basada en tiktoken (cl100k_base).
    Los modelos Ollama usan su propio tokenizador, los valores pueden
    diferir ligeramente.
    """
    text: str = Field(description="Texto original")
    token_count: int = Field(description="Número de tokens estimados")
    char_count: int = Field(description="Número de caracteres")
    word_count: int = Field(description="Número de palabras")
    tokens_per_word: float = Field(description="Ratio tokens/palabras")
    tokens_preview: List[str] = Field(
        description="Primeros 20 tokens para visualización"
    )
    educational_note: str = Field(description="Nota educativa contextual")


class EmbedResponse(BaseModel):
    """Respuesta con el vector embedding generado."""
    text: str = Field(description="Texto original")
    model: str = Field(description="Modelo usado")
    embedding: List[float] = Field(description="Vector de embeddings")
    dimensions: int = Field(description="Dimensiones del vector")
    preview: List[float] = Field(description="Primeros 5 valores del vector")


class SimilarityResponse(BaseModel):
    """Similitud coseno entre dos textos."""
    text1: str
    text2: str
    similarity: float = Field(description="Similitud coseno [0, 1]")
    interpretation: str = Field(description="Interpretación del resultado")


class ModelInfo(BaseModel):
    """Información de un modelo Ollama disponible."""
    name: str
    size: Optional[str] = None
    context_length: Optional[int] = None
    family: Optional[str] = None


class ModelsResponse(BaseModel):
    """Lista de modelos disponibles en Ollama."""
    models: List[ModelInfo]
    total: int


class ContextInfo(BaseModel):
    """Información sobre la ventana de contexto de un modelo."""
    model: str
    context_length: int = Field(description="Tokens máximos de contexto")
    estimated_words: int = Field(description="Palabras aproximadas que caben")
    estimated_pages: float = Field(description="Páginas A4 aproximadas (~500 palabras/página)")
    use_cases: List[str] = Field(description="Casos de uso apropiados según el tamaño del contexto")


class HealthResponse(BaseModel):
    """Estado de salud del servidor."""
    status: str
    ollama_available: bool
    ollama_url: str
    available_models: int
