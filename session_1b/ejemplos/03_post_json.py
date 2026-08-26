"""
Ejemplo 03 — HTTP POST con JSON
==================================
POST es el verbo que usas para enviar datos al LLM.
Cada llamada a chat/generate es un POST con JSON.

Ejecutar:
    python 03_post_json.py
"""

import json
import requests

# ── 1. POST Basico ────────────────────────────────────────────────────────────
print("=" * 50)
print("1. HTTP POST — ENVIAR DATOS AL SERVIDOR")
print("=" * 50)

print("""
GET  = solo pregunta (sin body)
POST = pregunta + datos (con body JSON)

Flujo de un POST a Ollama:
  1. Construyes el dict Python con el payload
  2. requests lo serializa a JSON automaticamente
  3. Agrega header Content-Type: application/json
  4. Envia el body en la request
  5. El servidor procesa y devuelve JSON
""")

# POST a httpbin (espeja lo que envias)
payload = {
    "model": "llama3.2",
    "messages": [{"role": "user", "content": "Que es un token?"}],
    "temperature": 0.7
}

try:
    r = requests.post(
        "https://httpbin.org/post",
        json=payload,           # requests hace json.dumps() + Content-Type header automaticamente
        timeout=10,
    )
    data = r.json()
    cuerpo_enviado = data.get("json", {})   # httpbin nos devuelve lo que enviamos
    print(f"Status:  {r.status_code}")
    print(f"Body enviado — model: {cuerpo_enviado.get('model')}")
    print(f"Body enviado — temp:  {cuerpo_enviado.get('temperature')}")
    print(f"Mensajes enviados:    {len(cuerpo_enviado.get('messages', []))}")
except Exception:
    print("[SIMULADO] POST a httpbin exitoso")
    print("Body enviado — model: llama3.2, temperature: 0.7")


# ── 2. POST vs json= vs data= ────────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. DIFERENCIA: json= vs data=")
print("=" * 50)

print("""
requests.post(url, json=payload)
  → Serializa automaticamente el dict a JSON
  → Agrega Content-Type: application/json
  → SIEMPRE usa esto para APIs LLM

requests.post(url, data=payload)
  → Envia como form-urlencoded (NO JSON)
  → Para formularios HTML, NO para LLMs
  → Nunca usar con Ollama/OpenAI

requests.post(url, data=json.dumps(payload))
  → Manual — NO recomendado
  → Olvidas el header Content-Type
""")

# ── 3. Autenticacion con Bearer Token ─────────────────────────────────────────
print("=" * 50)
print("3. AUTENTICACION — BEARER TOKEN")
print("=" * 50)

print("""
Las APIs cloud (OpenAI, Anthropic, etc.) requieren autenticacion.
Se usa un header especial: Authorization: Bearer <tu-api-key>

  headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"  # requests agrega esto con json=
  }

  r = requests.post(url, json=payload, headers=headers)
""")

# Simular request con auth (httpbin permite probar headers)
API_KEY_FAKE = "sk-abc123def456"
headers = {"Authorization": f"Bearer {API_KEY_FAKE}"}

try:
    r = requests.post(
        "https://httpbin.org/post",
        json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "Hola"}]},
        headers=headers,
        timeout=10,
    )
    data = r.json()
    auth_recibida = data.get("headers", {}).get("Authorization", "N/A")
    print(f"Header Authorization enviado: {auth_recibida[:30]}...")
except Exception:
    print(f"[SIMULADO] Authorization: Bearer {API_KEY_FAKE[:10]}... enviado correctamente")


# ── 4. POST a Ollama — Request Real ──────────────────────────────────────────
print("\n" + "=" * 50)
print("4. POST A OLLAMA — REQUEST COMPLETA")
print("=" * 50)

OLLAMA_URL = "http://localhost:11434"

def chat_ollama(
    mensajes: list[dict],
    modelo: str = "llama3.2",
    temperatura: float = 0.7,
) -> dict | None:
    """
    Envia una conversacion a Ollama via HTTP POST.
    Retorna el dict completo de la respuesta.
    """
    payload = {
        "model": modelo,
        "messages": mensajes,
        "stream": False,
        "options": {
            "temperature": temperatura,
            "num_predict": 256,
        }
    }

    print(f"  POST {OLLAMA_URL}/api/chat")
    print(f"  Payload: model={modelo}, {len(mensajes)} mensaje(s)")

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        return r.json()

    except requests.exceptions.ConnectionError:
        print("  ERROR: Ollama no disponible")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP Error {e.response.status_code}: {e.response.text[:100]}")
        return None


# Construir conversacion
conversacion = [
    {"role": "system", "content": "Responde en espanol, de forma muy breve (1-2 frases)."},
    {"role": "user", "content": "Que es un embedding en IA?"}
]

respuesta_raw = chat_ollama(conversacion)

if respuesta_raw:
    texto = respuesta_raw["message"]["content"]
    tokens_in = respuesta_raw.get("prompt_eval_count", 0)
    tokens_out = respuesta_raw.get("eval_count", 0)
    duracion_ms = respuesta_raw.get("total_duration", 0) // 1_000_000

    print(f"\n  Respuesta: {texto[:150]}...")
    print(f"  Tokens: {tokens_in} in + {tokens_out} out = {tokens_in + tokens_out} total")
    print(f"  Tiempo: {duracion_ms}ms")
else:
    print("  [SIMULADO]")
    print("  Respuesta: Un embedding es una representacion numerica de texto")
    print("  en forma de vector. Permite comparar semanticamente palabras o frases.")
    print("  Tokens: 35 in + 28 out = 63 total | Tiempo: ~820ms")


# ── 5. POST para Generar Embeddings ──────────────────────────────────────────
print("\n" + "=" * 50)
print("5. POST — GENERAR EMBEDDINGS")
print("=" * 50)

print("Embeddings = vectores numericos que representan texto.")
print("Endpoint: POST /api/embeddings\n")

def generar_embedding(texto: str, modelo: str = "nomic-embed-text") -> list[float] | None:
    """Genera el embedding vectorial de un texto."""
    payload = {"model": modelo, "prompt": texto}
    try:
        r = requests.post(f"{OLLAMA_URL}/api/embeddings", json=payload, timeout=15)
        r.raise_for_status()
        return r.json()["embedding"]
    except Exception:
        return None


textos = [
    "Transformer architecture uses attention mechanism",
    "El gato se sento en la alfombra",
]

for t in textos:
    emb = generar_embedding(t)
    if emb:
        print(f"  Texto:     '{t[:40]}...' " if len(t) > 40 else f"  Texto:     '{t}'")
        print(f"  Embedding: [{emb[0]:.4f}, {emb[1]:.4f}, ... ] dim={len(emb)}")
    else:
        print(f"  Texto:     '{t[:40]}'")
        print(f"  Embedding: [SIMULADO] dim=768 (nomic-embed-text)")


# ── 6. Comparar dos textos por similitud coseno ───────────────────────────────
print("\n" + "=" * 50)
print("6. SIMILITUD COSENO — COMPARAR TEXTOS")
print("=" * 50)

import math

def similitud_coseno(v1: list[float], v2: list[float]) -> float:
    """Similitud coseno entre dos vectores (0=diferente, 1=identico)."""
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a ** 2 for a in v1))
    mag2 = math.sqrt(sum(b ** 2 for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


preguntas = [
    ("Como funciona un transformer?", "Explica la arquitectura transformer"),
    ("Como funciona un transformer?", "Cual es la capital de Francia?"),
]

for t1, t2 in preguntas:
    e1 = generar_embedding(t1)
    e2 = generar_embedding(t2)
    if e1 and e2:
        sim = similitud_coseno(e1, e2)
        print(f"  '{t1[:35]}'")
        print(f"  '{t2[:35]}'")
        print(f"  Similitud: {sim:.4f} ({'Alta' if sim > 0.8 else 'Baja'})\n")
    else:
        print(f"  '{t1[:35]}' vs '{t2[:35]}'")
        sim_sim = 0.94 if "transformer" in t2.lower() else 0.31
        print(f"  Similitud: {sim_sim:.2f} [SIMULADO] ({'Alta' if sim_sim > 0.8 else 'Baja'})\n")

print("[OK] Ejemplo 03 completado\n")
