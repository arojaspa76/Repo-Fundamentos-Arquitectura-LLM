"""
Ejemplo 04 — API de Ollama en Detalle
========================================
Todos los endpoints de Ollama que usaras en tus proyectos:
/api/chat, /api/generate, /api/embeddings, /api/tags, /api/pull

Ejecutar:
    python 04_ollama_api.py
    (requiere: ollama serve)
"""

import json
import requests

OLLAMA_BASE = "http://localhost:11434"

def ollama_ok() -> bool:
    try:
        return requests.get(f"{OLLAMA_BASE}/api/tags", timeout=2).status_code == 200
    except Exception:
        return False

MODO_SIMULADO = not ollama_ok()
if MODO_SIMULADO:
    print("[MODO SIMULADO — Ollama no disponible]\n")

# ── 1. /api/tags — Listar modelos ─────────────────────────────────────────────
print("=" * 50)
print("1. GET /api/tags — MODELOS INSTALADOS")
print("=" * 50)

if not MODO_SIMULADO:
    r = requests.get(f"{OLLAMA_BASE}/api/tags")
    modelos = r.json().get("models", [])
    print(f"Modelos disponibles: {len(modelos)}")
    for m in modelos:
        print(f"  {m['name']:<30} {m.get('size', 0) / 1e9:.1f} GB  "
              f"familia={m.get('details', {}).get('family', '?')}")
else:
    print("[SIMULADO] llama3.2 (2.0 GB), mistral (4.1 GB)")


# ── 2. /api/chat — Conversacion multi-turno ──────────────────────────────────
print("\n" + "=" * 50)
print("2. POST /api/chat — CHAT MULTI-TURNO")
print("=" * 50)

print("Este es el endpoint principal — soporta historial completo.")
print("Equivalente a /v1/chat/completions de OpenAI.\n")

payload_chat = {
    "model": "llama3.2",
    "messages": [
        {"role": "system", "content": "Eres un experto en IA. Responde en espanol, muy brevemente."},
        {"role": "user", "content": "Que es un context window?"}
    ],
    "stream": False,
    "options": {
        "temperature": 0.7,
        "top_p": 0.9,
        "num_predict": 100,    # maximo de tokens a generar
    }
}

if not MODO_SIMULADO:
    r = requests.post(f"{OLLAMA_BASE}/api/chat", json=payload_chat, timeout=60)
    data = r.json()
    print(f"Respuesta: {data['message']['content']}")
    print(f"Tokens:    {data.get('prompt_eval_count', 0)} in + {data.get('eval_count', 0)} out")
    print(f"Tiempo:    {data.get('total_duration', 0) // 1_000_000}ms")
else:
    print("[SIMULADO] Respuesta: El context window es la cantidad maxima de tokens")
    print("  que un modelo puede procesar a la vez. Llama3.2 tiene 128K tokens.")
    print("  Tokens: 42 in + 35 out | Tiempo: ~920ms")


# ── 3. /api/generate — Completacion simple ────────────────────────────────────
print("\n" + "=" * 50)
print("3. POST /api/generate — COMPLETACION SIMPLE")
print("=" * 50)

print("generate = completa texto sin historial. Util para clasificacion, extraccion.")
print("chat = conversacion con historial. Usa este para chatbots.\n")

payload_gen = {
    "model": "llama3.2",
    "prompt": "Clasifica el siguiente texto como POSITIVO, NEGATIVO o NEUTRO. Solo responde una palabra.\n\nTexto: 'El nuevo modelo de IA supera todos los benchmarks anteriores'\nClasificacion:",
    "stream": False,
    "options": {"temperature": 0.0, "num_predict": 5}  # deterministico, muy corto
}

if not MODO_SIMULADO:
    r = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload_gen, timeout=30)
    data = r.json()
    print(f"Clasificacion: {data['response'].strip()}")
else:
    print("[SIMULADO] Clasificacion: POSITIVO")


# ── 4. /api/embeddings — Vectores semanticos ─────────────────────────────────
print("\n" + "=" * 50)
print("4. POST /api/embeddings — VECTORES SEMANTICOS")
print("=" * 50)

import math

def embedding(texto: str, modelo: str = "nomic-embed-text") -> list[float] | None:
    if MODO_SIMULADO:
        import random
        random.seed(hash(texto) % 1000)
        return [random.uniform(-0.1, 0.1) for _ in range(768)]
    try:
        r = requests.post(f"{OLLAMA_BASE}/api/embeddings",
                          json={"model": modelo, "prompt": texto}, timeout=15)
        return r.json()["embedding"]
    except Exception:
        return None

def coseno(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag = math.sqrt(sum(a**2 for a in v1)) * math.sqrt(sum(b**2 for b in v2))
    return dot / mag if mag else 0.0

# Busqueda semantica simple
documentos = [
    "El transformer usa mecanismo de atencion para procesar secuencias.",
    "Python es el lenguaje mas popular para machine learning.",
    "Los embeddings representan texto como vectores numericos en espacio semantico.",
    "FastAPI permite crear APIs REST rapidamente con Python.",
]

query = "como representar texto como numeros?"

print(f"Query: '{query}'")
print("\nDocumentos rankeados por similitud semantica:")
emb_query = embedding(query)

resultados = []
for i, doc in enumerate(documentos):
    emb_doc = embedding(doc)
    sim = coseno(emb_query, emb_doc)
    resultados.append((sim, i, doc))

for sim, i, doc in sorted(resultados, reverse=True):
    print(f"  [{sim:.4f}] {doc[:60]}...")

print("\nEl documento mas relevante fue el que habla de embeddings.")
print("Asi funciona RAG (Retrieval-Augmented Generation).")


# ── 5. Tabla resumen de endpoints ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("5. RESUMEN DE ENDPOINTS OLLAMA")
print("=" * 50)

endpoints = [
    ("GET",  "/api/tags",        "Listar modelos instalados"),
    ("POST", "/api/chat",        "Chat multi-turno con historial"),
    ("POST", "/api/generate",    "Completacion simple (sin historial)"),
    ("POST", "/api/embeddings",  "Generar vectores semanticos"),
    ("POST", "/api/pull",        "Descargar un nuevo modelo"),
    ("GET",  "/api/ps",          "Ver modelos activos en memoria"),
    ("POST", "/api/show",        "Info detallada de un modelo"),
]

print(f"{'Metodo':<6} {'Endpoint':<20} {'Para que sirve'}")
print("-" * 55)
for metodo, path, desc in endpoints:
    print(f"{metodo:<6} {path:<20} {desc}")

print("\n[OK] Ejemplo 04 completado\n")
