"""
Ejemplo 02 — Estructuras de Control
=====================================
if/else, for, while, comprensiones de lista.
Todo aplicado a contextos de IA/LLM.

Ejecutar:
    python 02_estructuras_control.py
"""

# ── 1. if / elif / else ───────────────────────────────────────────────────────
print("=" * 50)
print("1. IF / ELIF / ELSE")
print("=" * 50)

tokens_usados = 95_000
limite_contexto = 128_000

# Lógica real de un sistema LLM
if tokens_usados > limite_contexto:
    print("ERROR: Contexto excedido — aplicar chunking o RAG")
elif tokens_usados > limite_contexto * 0.9:
    print("AVISO: Cerca del límite — considerar resumir el historial")
elif tokens_usados > limite_contexto * 0.7:
    print("OK: Usando bastante contexto — monitorear")
else:
    print("OK: Contexto con espacio suficiente")

# Operador ternario (if en una línea)
modelo = "llama3.2"
tipo = "local" if "llama" in modelo else "cloud"
print(f"Modelo {modelo} → tipo: {tipo}")

# ── 2. Bucle for ──────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. BUCLE FOR")
print("=" * 50)

# Iterar sobre una lista
modelos = ["llama3.2", "mistral", "gpt-4o", "claude-3-5-sonnet"]

print("Modelos disponibles:")
for i, modelo in enumerate(modelos, start=1):    # enumerate da índice + valor
    tipo = "local" if modelo.startswith("llama") or modelo == "mistral" else "cloud"
    print(f"  {i}. {modelo:25s} [{tipo}]")

# range() — para repetir N veces
print("\nSimulando 3 requests al LLM:")
for intento in range(1, 4):                      # range(1, 4) = 1, 2, 3
    print(f"  Intento {intento}: POST /api/generate")

# Iterar sobre diccionario
print("\nPrecios por modelo ($/M tokens input):")
precios = {"gpt-4o": 2.50, "gpt-4o-mini": 0.15, "claude-3-5-sonnet": 3.00, "llama3.2": 0.0}
for nombre, precio in precios.items():
    barra = "=" * int(precio * 10) if precio > 0 else "-"
    print(f"  {nombre:20s} ${precio:.2f}  {barra}")

# ── 3. Bucle while ────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("3. BUCLE WHILE — RETRY CON BACKOFF")
print("=" * 50)

import time

MAX_INTENTOS = 3
intentos = 0
exito = False

while intentos < MAX_INTENTOS and not exito:
    intentos += 1
    print(f"  Llamada al LLM — intento {intentos}/{MAX_INTENTOS}...")

    # Simulamos que el 3er intento funciona
    if intentos == 3:
        exito = True
        print("  Respuesta recibida OK")
    else:
        espera = 2 ** intentos           # backoff exponencial: 2, 4, 8 seg
        print(f"  Timeout — esperando {espera}s...")
        time.sleep(0.1)                  # en el ejemplo esperamos menos

if not exito:
    print("  ERROR: Todos los intentos fallaron")

# ── 4. Comprensiones de lista ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("4. COMPRENSIONES DE LISTA (Pythonic)")
print("=" * 50)

# Forma clásica (Java/C#):
modelos_locales_clasico = []
for m in modelos:
    if m in ["llama3.2", "mistral"]:
        modelos_locales_clasico.append(m)

# Forma Python (comprensión):
modelos_locales = [m for m in modelos if m in ["llama3.2", "mistral"]]
print(f"Modelos locales:       {modelos_locales}")

# Con transformación
costos = [tokens * 0.15 / 1_000_000 for tokens in [500, 1000, 5000, 10000]]
costos_fmt = [f"${c:.6f}" for c in costos]
print(f"Costos (500→10K tok):  {costos_fmt}")

# Comprensión de diccionario
precios_eur = {modelo: precio * 0.92 for modelo, precio in precios.items()}
print(f"Precios en EUR:        {precios_eur}")

# ── 5. break y continue ───────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("5. BREAK Y CONTINUE")
print("=" * 50)

# Buscar primer modelo dentro del presupuesto
presupuesto = 1.00    # USD por millón de tokens

print(f"Buscando modelo con precio <= ${presupuesto}/M:")
for nombre, precio in precios.items():
    if precio == 0:
        continue                          # saltar modelos gratuitos
    if precio <= presupuesto:
        print(f"  Encontrado: {nombre} (${precio:.2f}/M)")
        break                             # dejar de buscar
else:
    print("  Ningún modelo dentro del presupuesto")

print("\n[OK] Ejemplo 02 completado\n")
