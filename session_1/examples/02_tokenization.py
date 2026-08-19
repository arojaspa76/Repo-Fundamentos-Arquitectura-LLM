"""
Ejemplo 02 — Tokenización y su impacto
=======================================
Explora cómo los LLM convierten texto en tokens y por qué
esto importa en contexto de costos y límites de contexto.

Ejecutar:
    python 02_tokenization.py

Requisito:
    pip install tiktoken
"""

import tiktoken
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()


# ── Tokenizadores disponibles ─────────────────────────────────────────────

ENCODINGS = {
    "cl100k_base": "GPT-4, text-embedding-3, Claude (aproximado)",
    "p50k_base":   "GPT-3, Codex",
    "r50k_base":   "GPT-2, GPT-3 legacy",
}


def explore_tokens():
    """
    Muestra visualmente cómo se divide el texto en tokens.

    CONCEPTO CLAVE:
        Un token NO es siempre una palabra. Puede ser:
        - Una palabra completa: "transformer" → [transformer]
        - Parte de una palabra: "transformers" → [transform] [ers]
        - Un signo de puntuación: "," → [,]
        - Un espacio + palabra: " the" → [ the]
        - Un emoji: "🤖" → [multiple tokens]
    """
    console.print(Panel(
        "[bold blue]Exploración de Tokens[/bold blue]\n"
        "Observa cómo el mismo concepto usa diferente número de tokens en cada idioma",
        title="Ejemplo 02A"
    ))

    encoding = tiktoken.get_encoding("cl100k_base")

    textos = [
        ("Inglés",    "The transformer architecture uses self-attention mechanisms"),
        ("Español",   "La arquitectura transformer usa mecanismos de auto-atención"),
        ("Francés",   "L'architecture transformer utilise des mécanismes d'auto-attention"),
        ("Chino",     "Transformer架构使用自注意力机制"),
        ("Árabe",     "تستخدم بنية المحول آليات الانتباه الذاتي"),
        ("Código",    "def attention(Q, K, V): return softmax(Q @ K.T) @ V"),
        ("Números",   "El modelo procesó 1,234,567 tokens en $0.002 por 1K tokens"),
    ]

    table = Table(title="Comparación de tokens por idioma", show_lines=True)
    table.add_column("Idioma", style="cyan")
    table.add_column("Texto", style="white", max_width=50)
    table.add_column("Tokens", style="yellow", justify="right")
    table.add_column("Palabras", style="green", justify="right")
    table.add_column("T/P", style="magenta", justify="right")

    for idioma, texto in textos:
        tokens = encoding.encode(texto)
        palabras = len(texto.split())
        ratio = round(len(tokens) / max(palabras, 1), 2)
        table.add_row(idioma, texto[:50], str(len(tokens)), str(palabras), str(ratio))

    console.print(table)
    console.print(
        "\n[dim]💡 El inglés es el idioma más eficiente porque el vocabulario del tokenizador "
        "fue construido principalmente con texto en inglés. Otros idiomas usan más tokens "
        "para expresar los mismos conceptos → mayor costo en APIs cloud.[/dim]\n"
    )


def visualize_tokens(text: str):
    """
    Muestra los tokens individuales de un texto con colores alternados.

    Esto es exactamente lo que 've' el modelo: no palabras sino tokens.
    """
    console.print(Panel(
        f"[bold blue]Tokens visualizados: [/bold blue][white]{text}[/white]",
        title="Ejemplo 02B — Vista de tokens"
    ))

    encoding = tiktoken.get_encoding("cl100k_base")
    token_ids = encoding.encode(text)

    colors = ["blue", "green", "yellow", "magenta", "cyan", "red"]
    output_parts = []

    for i, token_id in enumerate(token_ids):
        token_bytes = encoding.decode_single_token_bytes(token_id)
        try:
            token_str = token_bytes.decode("utf-8")
        except UnicodeDecodeError:
            token_str = f"[{token_id}]"

        color = colors[i % len(colors)]
        # Mostrar el token con color y marcador visual
        output_parts.append(f"[{color}]▌{repr(token_str)}[/{color}]")

    console.print(" ".join(output_parts))
    console.print(f"\n[dim]Total: {len(token_ids)} tokens | "
                  f"Palabras: {len(text.split())} | "
                  f"Caracteres: {len(text)}[/dim]\n")


def context_window_demo():
    """
    Demuestra los límites de la ventana de contexto.

    CONCEPTO CLAVE:
        Cada modelo tiene un límite máximo de tokens que puede procesar.
        Cuando el texto supera ese límite, el modelo "olvida" el inicio.

        Esto tiene impacto directo en:
        - ¿Cuánto historial de conversación puede mantener el modelo?
        - ¿Caben los documentos que quiero procesar?
        - ¿Necesito estrategias de chunking o RAG?
    """
    console.print(Panel(
        "[bold blue]Ventanas de contexto de modelos populares[/bold blue]",
        title="Ejemplo 02C"
    ))

    table = Table(show_lines=True)
    table.add_column("Modelo",          style="cyan")
    table.add_column("Contexto (tokens)", style="yellow", justify="right")
    table.add_column("≈ Palabras",       style="green", justify="right")
    table.add_column("≈ Páginas A4",     style="magenta", justify="right")
    table.add_column("Caso de uso",      style="white")

    models = [
        ("GPT-3.5 Turbo",     4_096,    3_072,   6,   "Chats cortos, preguntas simples"),
        ("GPT-4 (legacy)",    8_192,    6_144,  12,   "Análisis de documentos cortos"),
        ("GPT-4o",          128_000,   96_000, 192,   "Documentos legales, libros"),
        ("Claude 3.5 Sonnet",200_000,  150_000, 300,  "Análisis masivo de código/docs"),
        ("Llama 3.2 (local)",128_000,   96_000, 192,  "LLM local potente"),
        ("Mistral 7B",        32_768,   24_576,  49,   "Balance costo/capacidad"),
        ("Phi-3 Mini",       128_000,   96_000, 192,  "LLM pequeño, contexto grande"),
    ]

    for model, ctx, words, pages, use in models:
        table.add_row(model, f"{ctx:,}", f"{words:,}", str(pages), use)

    console.print(table)

    # Calcular cuánto texto de ejemplo cabe
    encoding = tiktoken.get_encoding("cl100k_base")
    sample_text = "La inteligencia artificial es una tecnología transformadora. " * 100
    sample_tokens = len(encoding.encode(sample_text))

    console.print(
        f"\n[dim]Ejemplo: un texto de 100 frases repetidas = "
        f"{sample_tokens} tokens ≈ {sample_tokens/4096:.1f}x el contexto de GPT-3.5[/dim]\n"
    )


def cost_calculator():
    """
    Calcula el costo de diferentes operaciones en APIs cloud.

    Esto es fundamental para arquitecturas empresariales:
    el costo escala linealmente con los tokens procesados.
    """
    console.print(Panel(
        "[bold blue]Calculadora de Costos[/bold blue]",
        title="Ejemplo 02D"
    ))

    # Precios aproximados (USD por millón de tokens) - validar en sitios oficiales
    providers = {
        "OpenAI GPT-4o-mini":    {"input": 0.15,  "output": 0.60},
        "OpenAI GPT-4o":         {"input": 2.50,  "output": 10.00},
        "Anthropic Claude Haiku":{"input": 0.25,  "output": 1.25},
        "Google Gemini Flash":   {"input": 0.075, "output": 0.30},
        "Ollama (local)":        {"input": 0.0,   "output": 0.0},
    }

    # Escenario: procesar 1,000 documentos de 1 página cada uno
    input_tokens  = 1_000 * 500   # 1000 docs × 500 tokens/doc
    output_tokens = 1_000 * 100   # 1000 respuestas × 100 tokens/respuesta

    console.print(f"\n📋 Escenario: Procesar [yellow]1,000 documentos[/yellow] de 1 página")
    console.print(f"   Input:  {input_tokens:,} tokens | Output: {output_tokens:,} tokens\n")

    table = Table(show_lines=True)
    table.add_column("Proveedor",    style="cyan")
    table.add_column("Costo Input",  style="yellow", justify="right")
    table.add_column("Costo Output", style="green", justify="right")
    table.add_column("Total",        style="magenta", justify="right")

    for name, prices in providers.items():
        cost_in  = (input_tokens  / 1_000_000) * prices["input"]
        cost_out = (output_tokens / 1_000_000) * prices["output"]
        total    = cost_in + cost_out

        cost_in_str  = f"${cost_in:.4f}"  if cost_in  > 0 else "GRATIS"
        cost_out_str = f"${cost_out:.4f}" if cost_out > 0 else "GRATIS"
        total_str    = f"${total:.4f}"    if total    > 0 else "GRATIS 🎉"

        table.add_row(name, cost_in_str, cost_out_str, total_str)

    console.print(table)
    console.print(
        "\n[dim]💡 El costo local con Ollama es $0, pero requiere tu propio hardware.\n"
        "Para decisiones empresariales: evalúa costo vs privacidad vs latencia.[/dim]\n"
    )


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    console.print("\n[bold]🤖 FUNDAMENTOS DE ARQUITECTURA LLM — Ejemplo 02[/bold]")
    console.print("[dim]Tokenización y su impacto en costos y límites[/dim]\n")

    explore_tokens()
    visualize_tokens("Los transformers usan mecanismos de auto-atención")
    visualize_tokens("Transformers use self-attention mechanisms")
    context_window_demo()
    cost_calculator()

    console.print("[green]✅ Ejemplo 02 completado.[/green]")
    console.print("[dim]💡 Siguiente: python 03_embeddings.py[/dim]\n")
