"""
Ejemplo 05 — JSON y Archivos
=============================
JSON es el formato universal de las APIs de LLM.
Aprenderás a leer, escribir y parsear respuestas JSON reales.

Ejecutar:
    python 05_json_archivos.py
"""

import json
import os
from pathlib import Path

# ── 1. JSON Básico ───────────────────────────────────────────────────────────
print("=" * 50)
print("1. JSON — EL FORMATO DE LAS APIs LLM")
print("=" * 50)

# Una respuesta típica de la API de Ollama (como string)
respuesta_json_str = '''
{
    "model": "llama3.2",
    "created_at": "2024-01-15T10:30:00Z",
    "message": {
        "role": "assistant",
        "content": "Un transformer es una arquitectura de red neuronal..."
    },
    "done": true,
    "total_duration": 1234567890,
    "prompt_eval_count": 45,
    "eval_count": 120
}
'''

# json.loads() → string JSON a diccionario Python
respuesta = json.loads(respuesta_json_str)

print(f"Modelo:       {respuesta['model']}")
print(f"Contenido:    {respuesta['message']['content'][:50]}...")
print(f"Completado:   {respuesta['done']}")
print(f"Tokens input: {respuesta['prompt_eval_count']}")
print(f"Tokens output:{respuesta['eval_count']}")

# Calcular costo desde la respuesta
tokens_totales = respuesta['prompt_eval_count'] + respuesta['eval_count']
costo = tokens_totales / 1_000_000 * 0.15
print(f"\nCosto esta llamada: ${costo:.6f} USD ({tokens_totales} tokens)")


# ── 2. json.dumps() — Crear JSON ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. CREAR JSON PARA ENVIAR A LA API")
print("=" * 50)

# Construir el body de una request a Ollama
request_body = {
    "model": "llama3.2",
    "messages": [
        {"role": "system", "content": "Eres un experto en IA. Responde en espanol."},
        {"role": "user", "content": "Explica que es un embedding en 2 oraciones."}
    ],
    "stream": False,
    "options": {
        "temperature": 0.7,
        "top_p": 0.9,
        "num_predict": 256
    }
}

# json.dumps() → diccionario Python a string JSON
json_str = json.dumps(request_body, ensure_ascii=False, indent=2)
print("Body de la request:")
print(json_str[:300] + "...\n")

# Uso práctico: tamaño del payload
print(f"Tamanio del payload: {len(json_str.encode('utf-8'))} bytes")


# ── 3. Leer y Escribir Archivos ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("3. LEER Y ESCRIBIR ARCHIVOS")
print("=" * 50)

# Crear directorio de trabajo si no existe
trabajo_dir = Path("./tmp_ejemplo05")
trabajo_dir.mkdir(exist_ok=True)

# ── 3a. Escribir archivo de texto ─────────────────────────────────────────────
prompt_path = trabajo_dir / "system_prompt.txt"
system_prompt = """Eres un asistente experto en arquitectura de software e inteligencia artificial.
Responde de forma concisa, con ejemplos practicos y en espanol.
Cuando menciones codigo, usa bloques de codigo apropiados.
Evita respuestas muy largas — maximo 3 parrafos."""

with open(prompt_path, "w", encoding="utf-8") as f:
    f.write(system_prompt)

print(f"Prompt guardado en: {prompt_path}")

# ── 3b. Leer archivo de texto ──────────────────────────────────────────────────
with open(prompt_path, "r", encoding="utf-8") as f:
    contenido = f.read()

print(f"Lineas en el prompt: {len(contenido.splitlines())}")
print(f"Chars en el prompt:  {len(contenido)}")

# ── 3c. Guardar historial de chat como JSON ───────────────────────────────────
historial_path = trabajo_dir / "historial_chat.json"

historial = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Que es un transformer?"},
    {"role": "assistant", "content": "Un transformer es una arquitectura..."},
    {"role": "user", "content": "Y los embeddings?"},
    {"role": "assistant", "content": "Los embeddings son representaciones..."},
]

with open(historial_path, "w", encoding="utf-8") as f:
    json.dump(historial, f, ensure_ascii=False, indent=2)

print(f"\nHistorial guardado: {historial_path}")
print(f"Mensajes:           {len(historial)}")

# ── 3d. Leer historial para continuar la conversacion ─────────────────────────
with open(historial_path, "r", encoding="utf-8") as f:
    historial_cargado = json.load(f)

print(f"Historial cargado:  {len(historial_cargado)} mensajes")
ultimo = historial_cargado[-1]
print(f"Ultimo mensaje:     [{ultimo['role']}] {ultimo['content'][:40]}...")


# ── 4. Configuracion con JSON ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("4. CONFIGURACION CON JSON — PATRON COMUN EN LLM APPS")
print("=" * 50)

# Guardar configuracion del modelo
config_path = trabajo_dir / "modelo_config.json"
config = {
    "modelos": {
        "default": "llama3.2",
        "alternativo": "mistral",
        "cloud": "gpt-4o-mini"
    },
    "parametros": {
        "temperatura": 0.7,
        "max_tokens": 1000,
        "stream": True
    },
    "endpoints": {
        "ollama": "http://localhost:11434",
        "openai": "https://api.openai.com/v1"
    },
    "limites": {
        "max_historial": 20,
        "max_chars_input": 10000
    }
}

with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# Leer y usar config
with open(config_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

modelo = cfg["modelos"]["default"]
temp   = cfg["parametros"]["temperatura"]
url    = cfg["endpoints"]["ollama"]
print(f"Modelo configurado: {modelo}")
print(f"Temperatura:        {temp}")
print(f"Endpoint:           {url}/api/chat")


# ── 5. Variables de Entorno (.env) ────────────────────────────────────────────
print("\n" + "=" * 50)
print("5. VARIABLES DE ENTORNO — SECRETOS SEGUROS")
print("=" * 50)

# Leer variables de entorno (donde guardamos API keys)
# En produccion: usar python-dotenv y archivo .env
api_key = os.getenv("OPENAI_API_KEY", "no-configurada")
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
modelo_env = os.getenv("DEFAULT_MODEL", "llama3.2")

print(f"OPENAI_API_KEY:  {'*' * 8 if api_key != 'no-configurada' else 'no-configurada'}")
print(f"OLLAMA_URL:      {ollama_url}")
print(f"DEFAULT_MODEL:   {modelo_env}")

# Por que usar variables de entorno?
print("\nRegla de oro:")
print("  NUNCA escribas API keys directamente en el codigo")
print("  Usa .env + python-dotenv → os.getenv('MI_KEY')")
print("  Agrega .env al .gitignore")


# ── 6. Parsear Respuesta Real de Ollama ──────────────────────────────────────
print("\n" + "=" * 50)
print("6. PARSEAR RESPUESTA DE OLLAMA — PATRON REAL")
print("=" * 50)

def extraer_respuesta_ollama(json_response: dict) -> dict:
    """
    Extrae informacion util de la respuesta de Ollama.
    Esta funcion la usaras en todos tus proyectos LLM.
    """
    return {
        "texto": json_response.get("message", {}).get("content", ""),
        "modelo": json_response.get("model", "desconocido"),
        "tokens_input": json_response.get("prompt_eval_count", 0),
        "tokens_output": json_response.get("eval_count", 0),
        "completado": json_response.get("done", False),
        "duracion_ms": json_response.get("total_duration", 0) // 1_000_000,
    }


# Simular respuesta de Ollama
respuesta_ollama = {
    "model": "llama3.2",
    "message": {"role": "assistant", "content": "Los embeddings son vectores numericos que representan texto."},
    "done": True,
    "total_duration": 856000000,
    "prompt_eval_count": 32,
    "eval_count": 89
}

info = extraer_respuesta_ollama(respuesta_ollama)
print(f"Respuesta:  {info['texto']}")
print(f"Tokens:     {info['tokens_input']} in + {info['tokens_output']} out")
print(f"Duracion:   {info['duracion_ms']}ms")
costo_local = 0.0  # Ollama es gratis
print(f"Costo:      ${costo_local:.2f} (modelo local gratuito)")

# Limpiar archivos temporales
import shutil
shutil.rmtree(trabajo_dir)

print("\n[OK] Ejemplo 05 completado\n")
