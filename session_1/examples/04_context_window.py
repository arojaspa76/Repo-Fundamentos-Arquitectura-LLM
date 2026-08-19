"""
Ejemplo 04 — Ventana de Contexto y sus Límites
===============================================
Demuestra experimentalmente cómo la ventana de contexto
afecta la capacidad del modelo de "recordar" información.

Ejecutar:
    python 04_context_window.py
"""

import requests
import time
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

OLLAMA_URL = "http://localhost:11434"
MODEL      = "llama3.2"


def chat(prompt: str, system: str = "", max_tokens: int = 200) -> dict:
    """Llamada simple a Ollama con medición de tiempo."""
    start = time.time()
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "system": system,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": 0.1}
        },
        timeout=120
    )
    data = response.json()
    elapsed = (time.time() - start) * 1000

    return {
        "response": data.get("response", ""),
        "prompt_tokens": data.get("prompt_eval_count", 0),
        "completion_tokens": data.get("eval_count", 0),
        "duration_ms": elapsed,
    }


def context_limit_experiment():
    """
    Demuestra cómo el modelo "olvida" información cuando el contexto
    crece más allá de su ventana de atención efectiva.

    Experimento: Le decimos al modelo un número secreto al inicio,
    luego agregamos texto irrelevante de relleno, y al final
    preguntamos si recuerda el número.
    """
    console.print(Panel(
        "[bold blue]Experimento: ¿Cuánto recuerda el modelo?[/bold blue]\n"
        "[dim]Le daremos información al inicio y preguntaremos al final[/dim]",
        title="Ejemplo 04A"
    ))

    secret = "42"
    filler = ("Este es texto de relleno para demostrar el efecto de la ventana de contexto. " * 50)

    # Construir prompts de diferente longitud
    scenarios = [
        ("Contexto corto", f"El número secreto es {secret}. {filler[:200]}. ¿Cuál era el número secreto?"),
        ("Contexto medio",  f"El número secreto es {secret}. {filler[:2000]}. ¿Cuál era el número secreto?"),
        ("Contexto largo",  f"El número secreto es {secret}. {filler[:5000]}. ¿Cuál era el número secreto?"),
    ]

    table = Table(show_lines=True)
    table.add_column("Escenario",   style="cyan")
    table.add_column("Tokens aprox", style="yellow", justify="right")
    table.add_column("¿Recuerda?", style="white", justify="center")
    table.add_column("Respuesta",   style="green", max_width=40)
    table.add_column("Tiempo",      style="magenta", justify="right")

    for name, prompt in scenarios:
        console.print(f"Testing: {name}...")
        result = chat(prompt, max_tokens=50)

        remembered = secret in result["response"]
        status = "✅ Sí" if remembered else "❌ No"

        table.add_row(
            name,
            str(result["prompt_tokens"]),
            status,
            result["response"][:100].strip(),
            f"{result['duration_ms']:.0f}ms"
        )

    console.print(table)
    console.print(
        "\n[dim]💡 Con contextos muy largos, la información del inicio puede perderse.\n"
        "Esto se llama 'lost in the middle' — un problema conocido en LLMs.\n"
        "Solución en producción: RAG o resúmenes progresivos.[/dim]\n"
    )


def token_cost_by_context():
    """
    Muestra cómo la longitud del contexto afecta el costo.

    INSIGHT EMPRESARIAL:
        En APIs cloud, cada token del contexto se cobra en cada llamada.
        Si tienes un system prompt largo de 1000 tokens y haces 10,000 llamadas/día,
        pagas 10,000,000 tokens solo por el system prompt.
    """
    console.print(Panel(
        "[bold blue]Impacto del Contexto en el Costo[/bold blue]",
        title="Ejemplo 04B"
    ))

    PRICE_PER_MILLION = 0.15  # GPT-4o-mini input price

    scenarios = [
        ("Solo pregunta corta",         50,    "Chatbot simple"),
        ("System prompt básico",        300,   "Asistente con rol"),
        ("System prompt + historial",  2000,   "Chat con memoria"),
        ("Documento pequeño + prompt", 5000,   "Análisis de doc 1 pág"),
        ("Documento mediano + prompt", 20000,  "Análisis de doc 40 págs"),
        ("Documento grande + prompt",  80000,  "Análisis de libro"),
    ]

    table = Table(show_lines=True)
    table.add_column("Escenario",     style="cyan",    max_width=35)
    table.add_column("Tokens",        style="yellow",  justify="right")
    table.add_column("Costo/llamada", style="green",   justify="right")
    table.add_column("Costo 1K calls",style="magenta", justify="right")
    table.add_column("Costo 100K/día",style="red",     justify="right")
    table.add_column("Uso típico",    style="white")

    for name, tokens, use in scenarios:
        cost_per_call = (tokens / 1_000_000) * PRICE_PER_MILLION
        cost_1k       = cost_per_call * 1_000
        cost_100k     = cost_per_call * 100_000

        table.add_row(
            name,
            f"{tokens:,}",
            f"${cost_per_call:.6f}",
            f"${cost_1k:.3f}",
            f"${cost_100k:.2f}",
            use
        )

    console.print(table)
    console.print(
        f"\n[dim]Precio de referencia: ${PRICE_PER_MILLION}/M tokens (GPT-4o-mini input).\n"
        "Siempre verifica precios actuales en la web del proveedor.[/dim]\n"
    )


def context_strategies():
    """
    Presenta las estrategias para manejar contextos grandes.
    """
    console.print(Panel(
        "[bold blue]Estrategias para Contextos Largos[/bold blue]",
        title="Ejemplo 04C"
    ))

    strategies = [
        (
            "1️⃣  Chunking",
            "Dividir el documento en trozos y procesarlos por partes",
            "Resumen de libros, análisis de informes extensos",
            "Simple de implementar",
            "Puede perder relaciones entre chunks"
        ),
        (
            "2️⃣  RAG (Retrieval-Augmented Generation)",
            "Buscar solo los fragmentos relevantes para cada pregunta",
            "Chatbots sobre documentación empresarial",
            "Muy escalable, preciso",
            "Requiere base de datos vectorial"
        ),
        (
            "3️⃣  Resumen Progresivo",
            "Resumir el contexto anterior antes de agregar nuevo",
            "Conversaciones largas de soporte",
            "Mantiene coherencia",
            "Puede perder detalles importantes"
        ),
        (
            "4️⃣  Modelo con Gran Contexto",
            "Usar modelos con contextos de 128K-200K tokens",
            "Análisis de código completo, documentos legales",
            "Sin pérdida de información",
            "Mayor costo por llamada"
        ),
        (
            "5️⃣  Memoria Persistente",
            "Almacenar hechos clave fuera del contexto (DB)",
            "Asistentes personales, CRM con IA",
            "Memoria ilimitada en teoría",
            "Requiere arquitectura adicional"
        ),
    ]

    for strat, desc, use_case, pro, con in strategies:
        console.print(f"\n[bold cyan]{strat}[/bold cyan]")
        console.print(f"   📋 {desc}")
        console.print(f"   🏢 Caso de uso: [yellow]{use_case}[/yellow]")
        console.print(f"   ✅ Ventaja: [green]{pro}[/green]")
        console.print(f"   ⚠️  Limitación: [red]{con}[/red]")

    console.print(
        "\n[dim]💡 En la mayoría de proyectos empresariales se combina RAG + Chunking.\n"
        "Lo veremos en profundidad en sesiones posteriores del curso.[/dim]\n"
    )


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    console.print("\n[bold]🤖 FUNDAMENTOS DE ARQUITECTURA LLM — Ejemplo 04[/bold]")
    console.print("[dim]Ventana de Contexto y sus Límites[/dim]\n")

    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ Ollama no disponible. Ejecuta: ollama serve[/red]")
        exit(1)

    context_limit_experiment()
    token_cost_by_context()
    context_strategies()

    console.print("[green]✅ Ejemplo 04 completado.[/green]")
    console.print("[dim]🎉 ¡Has completado todos los ejemplos de la Sesión 1![/dim]\n")
