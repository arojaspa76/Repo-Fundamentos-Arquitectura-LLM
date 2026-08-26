"""
Ejemplo 04 — Listas, Diccionarios, Tuplas y Sets
==================================================
Las estructuras de datos más usadas en Python para LLM.
El historial de conversación de un chatbot es una lista de dicts.

Ejecutar:
    python 04_listas_diccionarios.py
"""

# ── 1. Listas ────────────────────────────────────────────────────────────────
print("=" * 50)
print("1. LISTAS")
print("=" * 50)

# El historial de chat es una lista de mensajes
historial = []

# Agregar mensajes (así funciona un chatbot real)
historial.append({"role": "system", "content": "Eres un experto en IA."})
historial.append({"role": "user", "content": "¿Qué es un transformer?"})
historial.append({"role": "assistant", "content": "Un transformer es una arquitectura..."})
historial.append({"role": "user", "content": "¿Y los embeddings?"})

print(f"Mensajes en historial: {len(historial)}")
print(f"Primer mensaje:  {historial[0]}")
print(f"Último mensaje:  {historial[-1]}")          # índice negativo
print(f"Slice [1:3]:     {historial[1:3]}")         # slicing

# Operaciones de lista
tokens_por_mensaje = [50, 100, 200, 80]
print(f"\nTokens por mensaje: {tokens_por_mensaje}")
print(f"  Total:   {sum(tokens_por_mensaje)}")
print(f"  Máximo:  {max(tokens_por_mensaje)}")
print(f"  Mínimo:  {min(tokens_por_mensaje)}")
print(f"  Promedio: {sum(tokens_por_mensaje)/len(tokens_por_mensaje):.1f}")

# Modificar lista
historial.insert(1, {"role": "system", "content": "Responde en español."})  # insertar posición
historial.pop()             # eliminar último
historial.pop(0)            # eliminar primero

modelos = ["gpt-4o", "llama3.2", "mistral", "gpt-4o"]
modelos.sort()
print(f"\nModelos ordenados: {modelos}")
print(f"Únicos (set):      {sorted(set(modelos))}")  # eliminar duplicados con set


# ── 2. Diccionarios ───────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. DICCIONARIOS — LA ESTRUCTURA CENTRAL DE LLM APIs")
print("=" * 50)

# Una llamada a la API de LLM tiene esta estructura
api_request = {
    "model": "llama3.2",
    "messages": [
        {"role": "user", "content": "¿Cuántos tokens tiene esta frase?"}
    ],
    "temperature": 0.7,
    "max_tokens": 500,
    "stream": False
}

# Acceder a valores
print(f"Modelo:       {api_request['model']}")
print(f"Temperatura:  {api_request['temperature']}")
print(f"Mensajes:     {len(api_request['messages'])}")

# .get() — acceso seguro (no lanza error si la clave no existe)
top_p = api_request.get("top_p", 1.0)      # default 1.0
print(f"Top-p:        {top_p} (default)")

# Modificar
api_request["temperature"] = 0.0           # respuestas deterministas
api_request["max_tokens"] = 1000
api_request["stream"] = True

# Verificar si clave existe
print(f"\n¿Tiene 'stream'?      {'stream' in api_request}")
print(f"¿Tiene 'top_k'?       {'top_k' in api_request}")

# Iterar
print("\nParámetros de la request:")
for clave, valor in api_request.items():
    if clave != "messages":                # saltar el campo largo
        print(f"  {clave}: {valor}")

# Diccionario de diccionarios — comparativa de modelos
modelos_info = {
    "gpt-4o-mini": {"proveedor": "OpenAI",    "precio": 0.15, "contexto": 128_000, "local": False},
    "llama3.2":    {"proveedor": "Meta",      "precio": 0.0,  "contexto": 128_000, "local": True},
    "mistral":     {"proveedor": "Mistral",   "precio": 0.0,  "contexto": 32_768,  "local": True},
    "claude-3-5":  {"proveedor": "Anthropic", "precio": 3.00, "contexto": 200_000, "local": False},
}

print("\nComparativa de modelos:")
print(f"{'Modelo':<15} {'Proveedor':<12} {'Precio':<10} {'Contexto':<12} {'Local'}")
print("-" * 60)
for nombre, info in modelos_info.items():
    precio_str = f"${info['precio']:.2f}/M" if info["precio"] > 0 else "Gratis"
    contexto_str = f"{info['contexto']:,}"
    local_str = "SI" if info["local"] else "NO"
    print(f"{nombre:<15} {info['proveedor']:<12} {precio_str:<10} {contexto_str:<12} {local_str}")


# ── 3. Tuplas ────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("3. TUPLAS — INMUTABLES")
print("=" * 50)

# Tuplas: como listas pero no se pueden modificar (más rápidas)
dimensiones_embedding = (768,)          # nomic-embed-text
dimensiones_gpt = (3072,)              # text-embedding-3-large

# Tupla de configuración (no debe cambiar)
endpoint_ollama = ("localhost", 11434, "http")
host, puerto, protocolo = endpoint_ollama    # "unpacking"
url = f"{protocolo}://{host}:{puerto}"
print(f"URL Ollama: {url}")

# Named tuples — más expresivos
from collections import namedtuple
ModelConfig = namedtuple("ModelConfig", ["nombre", "temperatura", "max_tokens"])
config = ModelConfig("llama3.2", 0.7, 1000)
print(f"Config: modelo={config.nombre}, temp={config.temperatura}")


# ── 4. Sets ──────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("4. SETS — OPERACIONES DE CONJUNTO")
print("=" * 50)

# Capacidades de dos modelos
caps_gpt = {"texto", "código", "visión", "audio", "funciones"}
caps_llama = {"texto", "código", "visión"}

print(f"GPT capacidades:   {sorted(caps_gpt)}")
print(f"Llama capacidades: {sorted(caps_llama)}")
print(f"Ambos tienen:      {sorted(caps_gpt & caps_llama)}")   # intersección
print(f"Solo GPT tiene:    {sorted(caps_gpt - caps_llama)}")   # diferencia
print(f"Al menos uno:      {sorted(caps_gpt | caps_llama)}")   # unión

print("\n[OK] Ejemplo 04 completado\n")
