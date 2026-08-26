"""
Ejemplo 06 — Streaming de Respuestas LLM
==========================================
En lugar de esperar toda la respuesta, recibes tokens uno a uno.
Asi funciona ChatGPT cuando "escribe" progresivamente.

Ejecutar:
    python 06_streaming.py
"""

import sys
import time
import json
import requests
from openai import OpenAI

OLLAMA_URL  = "http://localhost:11434"
OLLAMA_BASE = f"{OLLAMA_URL}/v1"

def ollama_ok():
    try:
        return requests.get(f"{OLLAMA_URL}/api/tags", timeout=2).status_code == 200
    except Exception:
        return False

MODO_SIMULADO = not ollama_ok()
if MODO_SIMULADO:
    print("[MODO SIMULADO]\n")

# ── 1. Por que usar streaming ─────────────────────────────────────────────────
print("=" * 50)
print("1. POR QUE STREAMING?")
print("=" * 50)

print("""
Sin streaming:
  Tu codigo espera  ─────── 5-30 segundos ──────> Respuesta completa
  El usuario ve: [cargando...] y luego todo el texto de golpe

Con streaming:
  Primer token ~200ms  → "Un"
  Segundo token ~50ms  → "Un transformer"
  ...
  → El usuario lee mientras el modelo genera

Ventajas del streaming:
  - Experiencia de usuario mucho mejor
  - Puedes interrumpir generaciones largas
  - Detectar errores antes (primer token con error)
  - Implementacion natural con HTTP chunked transfer
""")

# ── 2. Streaming con requests (nivel bajo) ────────────────────────────────────
print("=" * 50)
print("2. STREAMING CON REQUESTS — NIVEL BAJO")
print("=" * 50)

def stream_ollama_raw(pregunta: str, modelo: str = "llama3.2") -> str:
    """
    Streaming usando requests directamente.
    Cada chunk es una linea JSON.
    """
    payload = {
        "model": modelo,
        "messages": [{"role": "user", "content": pregunta}],
        "stream": True,   # CLAVE: True activa el streaming
    }

    texto_completo = ""

    if MODO_SIMULADO:
        # Simular streaming con delays
        respuesta_sim = "El streaming en LLMs funciona enviando tokens de forma incremental. Cada token es una pequeña pieza de texto que el modelo genera secuencialmente."
        palabras = respuesta_sim.split()
        for i, palabra in enumerate(palabras):
            fragmento = palabra + (" " if i < len(palabras) - 1 else "")
            print(fragmento, end="", flush=True)
            time.sleep(0.05)
        print()
        return respuesta_sim

    with requests.post(
        f"{OLLAMA_URL}/api/chat",
        json=payload,
        stream=True,          # requests.stream=True → no descarga todo de golpe
        timeout=60,
    ) as r:
        r.raise_for_status()
        for linea in r.iter_lines():    # cada linea es un chunk JSON
            if linea:
                chunk = json.loads(linea)
                token = chunk.get("message", {}).get("content", "")
                texto_completo += token
                print(token, end="", flush=True)   # imprimir sin newline
                if chunk.get("done"):
                    break

    print()   # newline al final
    return texto_completo


print("Generando respuesta token por token:")
print("-" * 40)
texto = stream_ollama_raw("Explica en 2 frases que es el mecanismo de atencion.")
print("-" * 40)
print(f"Total chars: {len(texto)}")


# ── 3. Streaming con SDK OpenAI ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("3. STREAMING CON SDK OPENAI — NIVEL ALTO")
print("=" * 50)

client = OpenAI(base_url=OLLAMA_BASE, api_key="ollama")

def stream_sdk(pregunta: str, modelo: str = "llama3.2") -> str:
    """
    Streaming usando el SDK de OpenAI.
    Mas limpio y pythonic que usar requests directamente.
    """
    if MODO_SIMULADO:
        respuesta_sim = "El context window define cuanta informacion puede procesar un LLM simultaneamente. Un contexto mayor permite conversaciones mas largas y documentos mas extensos."
        palabras = respuesta_sim.split()
        for i, p in enumerate(palabras):
            print(p + (" " if i < len(palabras) - 1 else ""), end="", flush=True)
            time.sleep(0.04)
        print()
        return respuesta_sim

    texto = ""
    # stream=True devuelve un iterador de chunks
    with client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": pregunta}],
        stream=True,
    ) as stream:
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            texto += delta
            print(delta, end="", flush=True)
    print()
    return texto


print("SDK OpenAI apuntando a Ollama:")
print("-" * 40)
stream_sdk("En 2 frases, por que el context window importa en LLMs?")
print("-" * 40)


# ── 4. Streaming en una aplicacion real ──────────────────────────────────────
print("\n" + "=" * 50)
print("4. STREAMING EN APLICACION REAL — CALLBACK PATTERN")
print("=" * 50)

def chat_con_streaming(
    mensajes: list[dict],
    modelo: str = "llama3.2",
    on_token=None,       # callback: funcion que recibe cada token
    on_complete=None,    # callback: funcion que recibe el texto completo
) -> str:
    """
    Version production-ready con callbacks.
    Permite integrar streaming en cualquier UI (terminal, web, app).
    """
    texto = ""

    if MODO_SIMULADO:
        sim = "Finalizando con streaming: este patron permite actualizar la UI incrementalmente sin bloquear el hilo principal de la aplicacion."
        for token in sim.split():
            token_con_espacio = token + " "
            texto += token_con_espacio
            if on_token:
                on_token(token_con_espacio)
            time.sleep(0.03)
        if on_complete:
            on_complete(texto)
        return texto

    with client.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=True,
    ) as stream:
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            if delta:
                texto += delta
                if on_token:
                    on_token(delta)
    if on_complete:
        on_complete(texto)
    return texto


# Ejemplo con callbacks — simulando actualizacion de UI
tokens_recibidos = 0

def mi_on_token(token: str):
    global tokens_recibidos
    tokens_recibidos += 1
    print(token, end="", flush=True)

def mi_on_complete(texto_completo: str):
    print(f"\n[Completado: {len(texto_completo)} chars, ~{tokens_recibidos} tokens]")


print("Usando callbacks:")
print("-" * 40)
chat_con_streaming(
    [{"role": "user", "content": "Define brevemente: temperatura en un LLM."}],
    on_token=mi_on_token,
    on_complete=mi_on_complete,
)


# ── 5. Cuando NO usar streaming ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("5. CUANDO USAR Y NO USAR STREAMING")
print("=" * 50)

print("""
USA STREAMING cuando:
  - Construyes un chat UI (terminal, web, app)
  - La respuesta es larga (>50 tokens)
  - La UX importa y el usuario espera la respuesta
  - Quieres poder interrumpir generaciones largas

NO USES STREAMING cuando:
  - Procesas batch (100 documentos en background)
  - Necesitas parsear la respuesta completa como JSON
  - Usas function calling / tool use (la respuesta es JSON)
  - Es un sistema automatizado sin usuario interactuando
""")

print("[OK] Ejemplo 06 completado\n")
