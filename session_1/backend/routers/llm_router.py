"""
llm_router.py — Endpoints de la API LLM
========================================
Define todos los endpoints relacionados con operaciones LLM:
chat, tokenización, embeddings y metadatos de modelos.

Cada endpoint incluye documentación educativa para que los
estudiantes entiendan qué está pasando internamente.
"""

import tiktoken
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import json

from models.schemas import (
    ChatRequest, ChatResponse,
    TokenizeRequest, TokenizeResponse,
    EmbedRequest, EmbedResponse,
    SimilarityRequest, SimilarityResponse,
    ModelsResponse, ModelInfo,
    ContextInfo,
)
from services.ollama_service import (
    chat as ollama_chat,
    generate_embedding,
    cosine_similarity,
    interpret_similarity,
    get_available_models,
    get_context_info,
    OLLAMA_BASE_URL,
)

router = APIRouter(prefix="/api", tags=["LLM Operations"])


# ── CHAT ───────────────────────────────────────────────────────────────────


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat con el LLM",
    description="""
    Envía un mensaje al LLM local (Ollama) y recibe una respuesta.

    ## Conceptos demostrados:
    - **System prompt**: Instrucción de contexto/rol para el modelo
    - **Temperature**: Controla la aleatoriedad (0=predecible, 2=caótico)
    - **Max tokens**: Límite de la respuesta
    - **Latencia local**: Los modelos locales son más lentos que APIs cloud

    ## Ejemplo de uso:
    ```python
    import requests
    response = requests.post("http://localhost:8000/api/chat", json={
        "model": "llama3.2",
        "message": "¿Qué es la atención en los transformers?",
        "temperature": 0.7
    })
    print(response.json()["message"])
    ```
    """,
)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal de chat. Conecta el frontend con Ollama.

    El flujo es:
        Usuario → FastAPI → Ollama (LLM local) → FastAPI → Usuario

    Internamente, el LLM:
    1. Tokeniza el prompt
    2. Genera embeddings de los tokens
    3. Aplica mecanismo de atención
    4. Predice el siguiente token (repetidamente)
    5. Detokeniza la respuesta
    """
    try:
        result = await ollama_chat(
            model=request.model,
            message=request.message,
            system_prompt=request.system_prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return ChatResponse(**result)

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Ollama no está disponible",
                "solution": "Ejecuta 'ollama serve' en una terminal",
                "url": OLLAMA_BASE_URL,
            }
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": f"Modelo '{request.model}' no encontrado",
                    "solution": f"Ejecuta: ollama pull {request.model}",
                }
            )
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── TOKENIZACIÓN ───────────────────────────────────────────────────────────


@router.post(
    "/tokenize",
    response_model=TokenizeResponse,
    summary="Explorar tokenización de texto",
    description="""
    Muestra cómo un LLM convierte texto en tokens.

    ## Conceptos demostrados:
    - Los tokens NO son palabras completas (pueden ser sílabas o subpalabras)
    - El español usa más tokens que el inglés para el mismo contenido
    - El costo de las APIs cloud se cobra por tokens, no por palabras

    **Nota**: Usa tiktoken (tokenizador de OpenAI) como aproximación.
    Los modelos Llama/Mistral tienen tokenizadores propios pero similares.
    """,
)
async def tokenize_endpoint(request: TokenizeRequest):
    """
    Tokeniza texto y devuelve estadísticas educativas.

    Por qué es importante entender la tokenización:
    - Los costos de APIs se calculan por tokens (input + output)
    - El límite de contexto se mide en tokens, no en palabras
    - Algunos idiomas son más "eficientes" que otros en tokens
    """
    try:
        # Usar el tokenizador cl100k_base (GPT-4, text-embedding-3)
        # Es una buena aproximación para modelos modernos
        encoding = tiktoken.get_encoding("cl100k_base")
        token_ids = encoding.encode(request.text)

        # Decodificar para mostrar los tokens visualmente
        tokens_preview = []
        for token_id in token_ids[:20]:  # solo los primeros 20
            token_bytes = encoding.decode_single_token_bytes(token_id)
            try:
                token_str = token_bytes.decode("utf-8")
            except UnicodeDecodeError:
                token_str = f"[0x{token_bytes.hex()}]"
            tokens_preview.append(repr(token_str))

        word_count = len(request.text.split())
        token_count = len(token_ids)
        tokens_per_word = round(token_count / max(word_count, 1), 2)

        # Nota educativa adaptada al resultado
        if tokens_per_word < 1.2:
            note = "✅ Texto muy eficiente en tokens (mayormente en inglés o texto técnico corto)"
        elif tokens_per_word < 1.8:
            note = "🔵 Eficiencia normal. El español suele usar ~1.3-1.5 tokens por palabra"
        else:
            note = "⚠️ Alto número de tokens por palabra. Puede deberse a caracteres especiales, idiomas no latinos, o emojis"

        return TokenizeResponse(
            text=request.text,
            token_count=token_count,
            char_count=len(request.text),
            word_count=word_count,
            tokens_per_word=tokens_per_word,
            tokens_preview=tokens_preview,
            educational_note=note,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tokenizando: {str(e)}")


# ── EMBEDDINGS ─────────────────────────────────────────────────────────────


@router.post(
    "/embed",
    response_model=EmbedResponse,
    summary="Generar embedding vectorial",
    description="""
    Convierte texto en un vector numérico de alta dimensión (embedding).

    ## Conceptos demostrados:
    - El texto se convierte en coordenadas en un espacio vectorial
    - Palabras/frases similares tienen vectores cercanos
    - Los embeddings son la base de búsqueda semántica y RAG

    **Requiere**: `ollama pull nomic-embed-text`
    """,
)
async def embed_endpoint(request: EmbedRequest):
    """
    Genera un embedding para el texto proporcionado.

    Casos de uso empresariales:
    - Búsqueda semántica en documentos internos
    - Recomendación de contenido similar
    - Clustering de texto (agrupar documentos por tema)
    - Base de RAG (Retrieval-Augmented Generation)
    """
    try:
        embedding = await generate_embedding(request.text, request.model)

        return EmbedResponse(
            text=request.text,
            model=request.model,
            embedding=embedding,
            dimensions=len(embedding),
            preview=embedding[:5],
        )

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama no está disponible. Ejecuta: ollama serve"
        )
    except Exception as e:
        if "model" in str(e).lower() or "404" in str(e):
            raise HTTPException(
                status_code=404,
                detail=f"Modelo '{request.model}' no encontrado. Ejecuta: ollama pull {request.model}"
            )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/similarity",
    response_model=SimilarityResponse,
    summary="Comparar similitud semántica entre dos textos",
    description="""
    Calcula qué tan similares son dos textos usando embeddings.

    ## Conceptos demostrados:
    - Los embeddings capturan SIGNIFICADO, no solo palabras
    - "automóvil" y "carro" tendrán alta similitud aunque no compartan letras
    - Base matemática: distancia coseno entre vectores

    **Requiere**: `ollama pull nomic-embed-text`
    """,
)
async def similarity_endpoint(request: SimilarityRequest):
    """
    Calcula similitud semántica entre dos textos.

    Ejemplo de insight: los modelos entienden sinónimos y contexto
    porque los embeddings capturan el SIGNIFICADO, no las letras.
    """
    try:
        emb1 = await generate_embedding(request.text1, request.model)
        emb2 = await generate_embedding(request.text2, request.model)

        score = cosine_similarity(emb1, emb2)
        interpretation = interpret_similarity(score)

        return SimilarityResponse(
            text1=request.text1,
            text2=request.text2,
            similarity=round(score, 4),
            interpretation=interpretation,
        )

    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Ollama no está disponible")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── MODELOS ────────────────────────────────────────────────────────────────


@router.get(
    "/models",
    response_model=ModelsResponse,
    summary="Listar modelos disponibles en Ollama",
)
async def list_models():
    """Lista todos los modelos Ollama instalados localmente."""
    try:
        models_data = await get_available_models()
        models = [ModelInfo(**m) for m in models_data]
        return ModelsResponse(models=models, total=len(models))

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama no está disponible. ¿Está corriendo 'ollama serve'?"
        )


@router.get(
    "/context-info/{model}",
    response_model=ContextInfo,
    summary="Información de ventana de contexto",
    description="""
    Devuelve información educativa sobre la ventana de contexto del modelo.

    La ventana de contexto es cuánta información puede "recordar" el LLM
    en una sola conversación. Es uno de los parámetros más importantes
    al elegir un modelo para una tarea empresarial.
    """,
)
async def context_info_endpoint(model: str):
    """
    Devuelve información sobre la ventana de contexto de un modelo.

    Esto es fundamental para decisiones de arquitectura:
    - ¿El documento que quiero procesar cabe en el contexto?
    - ¿Necesito chunking (dividir en partes) o RAG?
    - ¿Qué modelo debo elegir para mi caso de uso?
    """
    info = get_context_info(model)
    return ContextInfo(**info)
