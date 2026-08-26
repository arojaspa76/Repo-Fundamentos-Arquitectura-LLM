"""
Ejemplo 05 — Interfaz OpenAI-Compatible
==========================================
Ollama expone /v1/ que es 100% compatible con el SDK de OpenAI.
Mismo codigo → local (Ollama) o cloud (OpenAI/Groq/Together).

Ejecutar:
    python 05_openai_compatible.py
    pip install openai  (si no esta instalada)
"""

import os
from openai import OpenAI

OLLAMA_BASE = "http://localhost:11434/v1"
OLLAMA_KEY   = "ollama"   # cualquier string — Ollama no valida la key

# ── 1. Por que importa la compatibilidad OpenAI ───────────────────────────────
print("=" * 50)
print("1. COMPATIBILIDAD OPENAI — UN SDK, MUCHOS MODELOS")
print("=" * 50)

print("""
El SDK de OpenAI es el estandar de facto para LLMs.
Muchos proveedores implementan la misma interfaz:

  Proveedor    | base_url                          | modelo
  -------------|-----------------------------------|------------------
  OpenAI       | https://api.openai.com/v1         | gpt-4o-mini
  Ollama local | http://localhost:11434/v1          | llama3.2
  Groq (cloud) | https://api.groq.com/openai/v1    | llama-3.1-70b
  Together AI  | https://api.together.xyz/v1        | mistral-7b
  Anthropic    | Distinto SDK (anthropic)           | claude-3-haiku

Cambiando base_url y model, el MISMO codigo funciona en todos.
""")

# ── 2. Cliente Ollama con SDK OpenAI ─────────────────────────────────────────
print("=" * 50)
print("2. CLIENTE OLLAMA CON SDK OPENAI")
print("=" * 50)

# Detectar si Ollama esta corriendo
import requests
try:
    requests.get("http://localhost:11434/api/tags", timeout=2)
    MODO_SIMULADO = False
    print("Ollama detectado — usando modo REAL")
except Exception:
    MODO_SIMULADO = True
    print("[MODO SIMULADO — Ollama no disponible]")

client = OpenAI(
    base_url=OLLAMA_BASE,
    api_key=OLLAMA_KEY,
)

def chat(
    mensajes: list[dict],
    modelo: str = "llama3.2",
    temperatura: float = 0.7,
    max_tokens: int = 500,
) -> str:
    """Chat usando el SDK de OpenAI apuntando a Ollama."""
    if MODO_SIMULADO:
        ultima_pregunta = mensajes[-1]["content"]
        return f"[SIMULADO] Respuesta para: '{ultima_pregunta[:40]}...'"

    completion = client.chat.completions.create(
        model=modelo,
        messages=mensajes,
        temperature=temperatura,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content


# Ejemplo 1: Chat simple
respuesta = chat([
    {"role": "system", "content": "Responde en espanol, muy brevemente (1 frase)."},
    {"role": "user", "content": "Que es RAG en LLMs?"}
])
print(f"\nPregunta: 'Que es RAG en LLMs?'")
print(f"Respuesta: {respuesta}")


# ── 3. Extracto de informacion estructurada ───────────────────────────────────
print("\n" + "=" * 50)
print("3. EXTRACCION ESTRUCTURADA — PATRON MUY UTIL")
print("=" * 50)

import json

def extraer_json(texto_libre: str, esquema: str) -> dict | None:
    """
    Usa el LLM para extraer informacion estructurada de texto libre.
    Retorna un dict con el JSON extraido.
    """
    prompt_sistema = f"""Extrae la informacion solicitada del texto y responde SOLO con JSON valido.
No agregues explicaciones ni markdown. Solo el JSON.
Esquema esperado: {esquema}"""

    mensajes = [
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": texto_libre}
    ]

    respuesta = chat(mensajes, temperatura=0.0)

    # Limpiar posibles backticks de markdown
    respuesta_limpia = respuesta.strip().strip("```json").strip("```").strip()

    try:
        return json.loads(respuesta_limpia)
    except json.JSONDecodeError:
        return None


texto_ejemplo = """
El modelo GPT-4o-mini de OpenAI cuesta 0.15 dolares por millon de tokens de entrada
y 0.60 por millon de tokens de salida. Tiene una ventana de contexto de 128,000 tokens.
Es mas rapido que GPT-4o pero menos potente.
"""

esquema = '{"nombre": str, "proveedor": str, "precio_input_por_millon": float, "contexto_tokens": int}'

print(f"Texto: {texto_ejemplo.strip()[:100]}...")
resultado = extraer_json(texto_ejemplo, esquema)
if resultado:
    print(f"\nJSON extraido:")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
else:
    print("\n[SIMULADO] JSON extraido:")
    print(json.dumps({
        "nombre": "GPT-4o-mini",
        "proveedor": "OpenAI",
        "precio_input_por_millon": 0.15,
        "contexto_tokens": 128000
    }, indent=2))


# ── 4. Cambiar de local a cloud — 1 linea ────────────────────────────────────
print("\n" + "=" * 50)
print("4. LOCAL VS CLOUD — CAMBIAR EN 1 LINEA")
print("=" * 50)

print("""
# LOCAL (Ollama — gratis, privado):
client_local = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
respuesta = client_local.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hola"}]
)

# CLOUD (OpenAI — de pago, mas potente):
client_cloud = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    # base_url omitido → usa api.openai.com por defecto
)
respuesta = client_cloud.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hola"}]
)

# El texto de respuesta se accede EXACTAMENTE igual en ambos casos:
texto = respuesta.choices[0].message.content

# Para cambiar de local a cloud: solo cambias client y model.
# El resto del codigo no cambia.
""")

# ── 5. Listar modelos via SDK ─────────────────────────────────────────────────
print("=" * 50)
print("5. LISTAR MODELOS VIA SDK")
print("=" * 50)

if not MODO_SIMULADO:
    try:
        modelos = client.models.list()
        print(f"Modelos disponibles ({len(modelos.data)}):")
        for m in modelos.data[:5]:
            print(f"  - {m.id}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("[SIMULADO] Modelos: llama3.2, mistral, nomic-embed-text")

print("\n[OK] Ejemplo 05 completado\n")
