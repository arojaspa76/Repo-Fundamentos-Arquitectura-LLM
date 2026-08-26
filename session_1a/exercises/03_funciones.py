"""
Ejemplo 03 — Funciones en Python
==================================
def, parámetros, valores por defecto, *args, **kwargs, lambda.
Aplicado a patrones reales de LLM.

Ejecutar:
    python 03_funciones.py
"""

# ── 1. Función básica ─────────────────────────────────────────────────────────
print("=" * 50)
print("1. FUNCIÓN BÁSICA")
print("=" * 50)

def calcular_costo(tokens_input: int, tokens_output: int, precio_por_millon: float = 0.15) -> float:
    """
    Calcula el costo de una llamada a la API de LLM.

    Args:
        tokens_input:      Tokens enviados al modelo
        tokens_output:     Tokens recibidos del modelo
        precio_por_millon: Precio en USD por millón de tokens (default: GPT-4o-mini)

    Returns:
        Costo en USD
    """
    total_tokens = tokens_input + tokens_output
    return (total_tokens / 1_000_000) * precio_por_millon


# Llamadas a la función
costo1 = calcular_costo(500, 200)                          # usa precio default
costo2 = calcular_costo(500, 200, precio_por_millon=3.00)  # Claude Sonnet
costo3 = calcular_costo(tokens_output=800, tokens_input=1200)  # kwargs

print(f"GPT-4o-mini:   ${costo1:.6f}")
print(f"Claude Sonnet: ${costo2:.6f}")
print(f"Con kwargs:    ${costo3:.6f}")


# ── 2. Funciones con múltiples valores de retorno ────────────────────────────
print("\n" + "=" * 50)
print("2. MÚLTIPLES VALORES DE RETORNO")
print("=" * 50)

def analizar_respuesta(texto: str) -> tuple[int, int, list[str]]:
    """Analiza una respuesta de LLM y retorna estadísticas."""
    palabras = texto.split()
    # Palabras clave de IA (simplificado)
    keywords = ["transformer", "embedding", "token", "atención", "contexto"]
    encontradas = [k for k in keywords if k.lower() in texto.lower()]

    return len(palabras), len(texto), encontradas


respuesta_llm = "El transformer usa el mecanismo de atención para procesar cada token en contexto"
palabras, chars, kw = analizar_respuesta(respuesta_llm)
print(f"Palabras:       {palabras}")
print(f"Caracteres:     {chars}")
print(f"Keywords IA:    {kw}")


# ── 3. *args y **kwargs ───────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("3. *args Y **kwargs")
print("=" * 50)

def construir_mensaje(*contenidos: str, rol: str = "user", separador: str = "\n") -> dict:
    """
    Construye un mensaje para la API de LLM.
    *args → número variable de contenidos
    **kwargs → parámetros con nombre opcionales
    """
    texto_completo = separador.join(contenidos)
    return {"role": rol, "content": texto_completo}


msg1 = construir_mensaje("¿Qué es un transformer?")
msg2 = construir_mensaje("Contexto:", "Eres un experto en IA.", rol="system", separador="\n\n")
msg3 = construir_mensaje("Intro:", "Detalle:", "Conclusión:", rol="user")

print(f"Mensaje simple:   {msg1}")
print(f"System message:   {msg2}")
print(f"Multi-contenido:  {msg3}")


# ── 4. Funciones de orden superior ───────────────────────────────────────────
print("\n" + "=" * 50)
print("4. FUNCIONES DE ORDEN SUPERIOR")
print("=" * 50)

modelos_info = [
    {"nombre": "gpt-4o-mini", "precio": 0.15, "contexto": 128_000},
    {"nombre": "claude-3-haiku", "precio": 0.25, "contexto": 200_000},
    {"nombre": "llama3.2", "precio": 0.0, "contexto": 128_000},
    {"nombre": "gpt-4o", "precio": 2.50, "contexto": 128_000},
]

# map() — transformar cada elemento
nombres = list(map(lambda m: m["nombre"].upper(), modelos_info))
print(f"map() nombres:   {nombres}")

# filter() — filtrar elementos que cumplen condición
baratos = list(filter(lambda m: m["precio"] < 1.0, modelos_info))
print(f"filter() baratos: {[m['nombre'] for m in baratos]}")

# sorted() con key
por_precio = sorted(modelos_info, key=lambda m: m["precio"])
print(f"sorted() precio:  {[f\"{m['nombre']}(${m['precio']})\" for m in por_precio]}")


# ── 5. Funciones como argumentos ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("5. FUNCIONES COMO ARGUMENTOS")
print("=" * 50)

def procesar_respuesta(texto: str, procesador=None) -> str:
    """Aplica un procesador opcional al texto de la respuesta."""
    if procesador is None:
        return texto
    return procesador(texto)


def limpiar_markdown(texto: str) -> str:
    """Elimina formato markdown básico."""
    return texto.replace("**", "").replace("*", "").replace("`", "")

def resumir(texto: str, max_chars: int = 50) -> str:
    """Trunca texto largo."""
    return texto[:max_chars] + "..." if len(texto) > max_chars else texto


respuesta = "**Importante:** El `transformer` usa *atención multi-cabeza* para procesar texto."
print(f"Original:          {respuesta}")
print(f"Sin markdown:      {procesar_respuesta(respuesta, limpiar_markdown)}")
print(f"Resumido:          {procesar_respuesta(respuesta, resumir)}")
print(f"Sin procesar:      {procesar_respuesta(respuesta)}")


# ── 6. Funciones anidadas y closures ─────────────────────────────────────────
print("\n" + "=" * 50)
print("6. CLOSURES — FACTORY FUNCTIONS")
print("=" * 50)

def crear_calculadora_costos(precio_por_millon: float):
    """
    Retorna una función configurada con un precio específico.
    Patrón útil para inicializar clientes de API.
    """
    def calcular(tokens: int) -> float:
        return (tokens / 1_000_000) * precio_por_millon

    calcular.__doc__ = f"Calcula costo a ${precio_por_millon}/M tokens"
    return calcular


calcular_openai = crear_calculadora_costos(0.15)   # GPT-4o-mini
calcular_claude = crear_calculadora_costos(3.00)   # Claude Sonnet

print(f"10K tokens OpenAI: ${calcular_openai(10_000):.6f}")
print(f"10K tokens Claude: ${calcular_claude(10_000):.6f}")

print("\n[OK] Ejemplo 03 completado\n")
