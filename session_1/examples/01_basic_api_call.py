"""
Ejemplo 01 — Primera llamada a la API de Ollama
================================================
Este script demuestra la forma más simple de interactuar
con un LLM local usando la API REST de Ollama.

Ejecutar:
    python 01_basic_api_call.py

Requisito previo:
    ollama serve                 # en otra terminal
    ollama pull llama3.2         # una sola vez
"""

import requests
import json
import time

OLLAMA_URL = "http://localhost:11434"
MODEL      = "llama3.2"


# ── Parte 1: Llamada más simple posible ───────────────────────────────────

def hello_llm():
    """
    La llamada más básica a un LLM.
    Solo necesitas: endpoint URL, nombre del modelo y el prompt.
    """
    print("=" * 60)
    print("EJEMPLO 1A: Llamada básica")
    print("=" * 60)

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": "¿Qué es un Large Language Model? Responde en exactamente 2 oraciones.",
            "stream": False,                # stream=False = esperar respuesta completa
        }
    )

    data = response.json()
    print(f"Respuesta: {data['response']}")
    print(f"Tokens usados: {data.get('prompt_eval_count', '?')} prompt + {data.get('eval_count', '?')} respuesta")


# ── Parte 2: Con system prompt ─────────────────────────────────────────────

def chat_with_system_prompt():
    """
    El system prompt define el ROL y COMPORTAMIENTO del LLM.
    Es la instrucción de contexto que se envía antes del mensaje del usuario.

    Concepto clave: Los LLMs no tienen "personalidad" propia,
    el system prompt define cómo se van a comportar.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 1B: Con System Prompt")
    print("=" * 60)

    system_prompt = """Eres un profesor universitario experto en Inteligencia Artificial.
    Explicas conceptos complejos usando analogías del mundo real.
    Siempre das un ejemplo práctico al final de tu explicación.
    Responde siempre en español."""

    user_message = "¿Qué son los tokens en el contexto de los LLM?"

    print(f"System: {system_prompt[:80]}...")
    print(f"Usuario: {user_message}")
    print("\nRespuesta del LLM:")
    print("-" * 40)

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "system": system_prompt,    # <- aquí va el system prompt
            "prompt": user_message,
            "stream": False,
        }
    )

    print(response.json()["response"])


# ── Parte 3: Parámetros de generación ─────────────────────────────────────

def explore_temperature():
    """
    La TEMPERATURA controla la aleatoriedad de las respuestas.

    temperature = 0.0 → Siempre elige el token más probable (predecible)
    temperature = 1.0 → Mezcla probabilística (balance)
    temperature = 2.0 → Alta aleatoriedad (creativo pero puede ser incoherente)

    En producción empresarial, values entre 0.0-0.3 para tareas precisas
    (clasificación, extracción) y 0.7-1.0 para generación creativa.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 1C: Explorar Temperature")
    print("=" * 60)

    prompt = "Completa esta oración: 'Un transformer es como...'"

    for temp in [0.0, 0.7, 1.5]:
        print(f"\n🌡️  Temperature = {temp}:")
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temp,
                    "num_predict": 50,   # limitar a 50 tokens para comparar
                }
            }
        )
        print(f"   {response.json()['response'].strip()}")


# ── Parte 4: Streaming ─────────────────────────────────────────────────────

def streaming_response():
    """
    Con stream=True, los tokens llegan de a uno mientras se generan.
    Esto da la sensación de que el modelo "está pensando" en tiempo real.

    En producción: usar streaming mejora la experiencia del usuario
    al no esperar toda la respuesta para ver algo.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 1D: Respuesta en Streaming")
    print("=" * 60)
    print("Los tokens van apareciendo de a uno:\n")

    start = time.time()

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": "Enumera 5 casos de uso empresarial de los LLM, uno por línea.",
            "stream": True,             # <- stream=True
        },
        stream=True                     # requests también debe streamear
    )

    full_response = ""
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            token = chunk.get("response", "")
            print(token, end="", flush=True)
            full_response += token
            if chunk.get("done", False):
                break

    elapsed = time.time() - start
    tokens = len(full_response.split())  # aproximación
    print(f"\n\n⏱️  Generado en {elapsed:.1f}s (~{tokens} palabras)")


# ── Parte 5: Listar modelos disponibles ────────────────────────────────────

def list_available_models():
    """
    Consulta qué modelos tienes instalados en Ollama.
    Útil para verificar la configuración antes de usar el sistema.
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 1E: Modelos disponibles en Ollama")
    print("=" * 60)

    response = requests.get(f"{OLLAMA_URL}/api/tags")
    models = response.json().get("models", [])

    if not models:
        print("⚠️  No hay modelos instalados. Ejecuta: ollama pull llama3.2")
        return

    print(f"{'Modelo':<30} {'Tamaño':<12} {'Modificado'}")
    print("-" * 60)
    for m in models:
        size_gb = m.get("size", 0) / (1024 ** 3)
        name    = m.get("name", "")
        modified = m.get("modified_at", "")[:10]
        print(f"{name:<30} {size_gb:.1f} GB      {modified}")


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🤖 FUNDAMENTOS DE ARQUITECTURA LLM — Ejemplo 01")
    print("Primera llamada a la API de Ollama\n")

    # Verificar que Ollama esté corriendo
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
    except requests.exceptions.ConnectionError:
        print("❌ Ollama no está corriendo.")
        print("   Solución: abre una terminal y ejecuta: ollama serve")
        exit(1)

    list_available_models()
    hello_llm()
    chat_with_system_prompt()
    explore_temperature()
    streaming_response()

    print("\n✅ Todos los ejemplos completados.")
    print("💡 Siguiente paso: ejecuta python 02_tokenization.py")
