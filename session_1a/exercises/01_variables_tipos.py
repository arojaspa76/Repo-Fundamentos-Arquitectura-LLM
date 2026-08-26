"""
Ejemplo 01 — Variables y Tipos de Datos en Python
===================================================
Python es el lenguaje #1 para IA por su simplicidad y ecosistema.
En este ejemplo aprenderás todo lo necesario para empezar.

Ejecutar:
    python 01_variables_tipos.py
"""

# ── 1. Variables ──────────────────────────────────────────────────────────────
# En Python NO se declara el tipo — se infiere automáticamente
nombre = "Claude"          # str  (texto)
version = 3.5              # float (número decimal)
tokens = 4096              # int  (número entero)
activo = True              # bool (verdadero/falso)
sin_valor = None           # NoneType (equivale a null/nil)

print("=" * 50)
print("1. VARIABLES BÁSICAS")
print("=" * 50)
print(f"Nombre:    {nombre}  ({type(nombre).__name__})")
print(f"Versión:   {version}  ({type(version).__name__})")
print(f"Tokens:    {tokens}  ({type(tokens).__name__})")
print(f"Activo:    {activo}  ({type(activo).__name__})")
print(f"Sin valor: {sin_valor}  ({type(sin_valor).__name__})")

# ── 2. Strings (Cadenas de texto) ────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. STRINGS — MUY IMPORTANTES EN LLM")
print("=" * 50)

modelo = "llama3.2"
temperatura = 0.7

# f-strings: la forma moderna de formatear (USARÁS ESTO TODO EL TIEMPO)
prompt = f"Usando el modelo {modelo} con temperatura {temperatura}"
print(f"Prompt: {prompt}")

# Operaciones con strings
texto = "Arquitectura Transformer"
print(f"Mayúsculas:   {texto.upper()}")
print(f"Minúsculas:   {texto.lower()}")
print(f"Longitud:     {len(texto)} caracteres")
print(f"Contiene 'Trans': {'Trans' in texto}")
print(f"Reemplazar:   {texto.replace('Transformer', 'LLM')}")
print(f"Dividir:      {texto.split(' ')}")

# Multilinea con triple comilla — muy usado para prompts de LLM
system_prompt = """
Eres un asistente experto en arquitectura de software.
Responde de forma concisa y con ejemplos de código.
Siempre menciona las mejores prácticas de la industria.
"""
print(f"\nSystem prompt ({len(system_prompt.strip())} chars):")
print(system_prompt.strip())

# ── 3. Números ────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("3. NÚMEROS — CÁLCULO DE COSTOS DE LLM")
print("=" * 50)

tokens_input = 1_500       # guión bajo para legibilidad
tokens_output = 800
precio_por_millon = 0.15   # USD por millón de tokens (GPT-4o-mini input)

costo = (tokens_input + tokens_output) / 1_000_000 * precio_por_millon
print(f"Tokens usados:    {tokens_input:,} input + {tokens_output:,} output")
print(f"Precio:           ${precio_por_millon}/M tokens")
print(f"Costo esta call:  ${costo:.6f} USD")
print(f"Costo 10K calls:  ${costo * 10_000:.2f} USD")

# Operaciones comunes
print(f"\nOperaciones: 10 // 3 = {10 // 3} (división entera)")
print(f"             10 %  3 = {10 % 3} (módulo/resto)")
print(f"             2  ** 8 = {2 ** 8} (potencia)")

# ── 4. Booleanos y comparaciones ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("4. BOOLEANOS Y COMPARACIONES")
print("=" * 50)

contexto_disponible = tokens_input < 128_000   # ventana de contexto
tiene_gpu = False
modo_streaming = True

print(f"¿Cabe en contexto?  {contexto_disponible}")
print(f"¿Tiene GPU?         {tiene_gpu}")
print(f"¿Streaming activo?  {modo_streaming}")

# Operadores lógicos
puede_usar_gpu = tiene_gpu and contexto_disponible
print(f"¿Puede usar GPU?    {puede_usar_gpu}")
print(f"¿Necesita RAG?      {not contexto_disponible}")

# ── 5. Conversión de tipos ───────────────────────────────────────────────────
print("\n" + "=" * 50)
print("5. CONVERSIÓN DE TIPOS")
print("=" * 50)

temperatura_str = "0.7"          # viene de un archivo de config como string
temperatura_num = float(temperatura_str)
tokens_str = str(tokens)         # convertir a string para concatenar

print(f"String '0.7' → float: {temperatura_num}")
print(f"int 4096 → string:    '{tokens_str}'")
print(f"float 3.9 → int:      {int(3.9)}")     # trunca, no redondea
print(f"Redondear 3.56789:    {round(3.56789, 2)}")

# ── Resumen para el curso ─────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("RESUMEN: ¿QUE USARÁS EN EL CURSO?")
print("=" * 50)
print("  ★ f-strings  → construir prompts dinámicos")
print("  ★ int/float  → calcular costos de tokens")
print("  ★ bool       → flags de configuración (streaming, cache)")
print("  ★ None       → verificar si hay respuesta del modelo")
print("  ★ str()      → convertir respuestas para procesar")
print()
