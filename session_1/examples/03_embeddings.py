"""
Ejemplo 03 — Embeddings y Similitud Semántica
==============================================
Demuestra cómo los LLM representan el significado del texto
como vectores numéricos en un espacio de alta dimensión.

Ejecutar:
    ollama pull nomic-embed-text   # una sola vez
    python 03_embeddings.py

Requisitos:
    pip install requests numpy scipy
"""

import requests
import numpy as np
from rich import print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

console = Console()

OLLAMA_URL    = "http://localhost:11434"
EMBED_MODEL   = "nomic-embed-text"


# ── Función helper ────────────────────────────────────────────────────────

def get_embedding(text: str) -> np.ndarray:
    """Genera un embedding para el texto dado usando Ollama."""
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=30
    )
    response.raise_for_status()
    return np.array(response.json()["embedding"])


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """
    Similitud coseno entre dos vectores.

    Formula: cos(θ) = (v1 · v2) / (|v1| × |v2|)

    Rango: [-1, 1] donde:
        1.0 = idénticos (ángulo 0°)
        0.0 = ortogonales (sin relación, ángulo 90°)
       -1.0 = opuestos (ángulo 180°)
    """
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (norm1 * norm2))


# ── Ejemplo 1: Inspeccionar un embedding ─────────────────────────────────

def inspect_embedding():
    """
    Muestra cómo luce un embedding internamente.

    CONCEPTO CLAVE:
        Un embedding transforma texto en un vector de N números flotantes.
        nomic-embed-text produce vectores de 768 dimensiones.
        GPT text-embedding-3-small: 1,536 dimensiones.
        GPT text-embedding-3-large: 3,072 dimensiones.

        Cada dimensión representa una característica semántica abstracta
        (los ingenieros no pueden interpretar directamente cada dimensión).
    """
    console.print(Panel(
        "[bold blue]Anatomía de un Embedding[/bold blue]",
        title="Ejemplo 03A"
    ))

    word = "inteligencia artificial"
    console.print(f'Generando embedding para: "[yellow]{word}[/yellow]"...\n')

    emb = get_embedding(word)

    console.print(f"📐 Dimensiones del vector: [bold]{len(emb):,}[/bold]")
    console.print(f"📊 Rango de valores: [{emb.min():.4f}, {emb.max():.4f}]")
    console.print(f"📏 Norma (longitud): {np.linalg.norm(emb):.4f}")
    console.print(f"\n🔢 Primeros 10 valores:")
    console.print(f"   [{', '.join(f'{v:.6f}' for v in emb[:10])}]")
    console.print(f"\n[dim]   ... y {len(emb)-10} valores más[/dim]")

    console.print(
        "\n[dim]💡 Estos números por sí solos no significan nada legible para humanos.\n"
        "   Su utilidad está en comparar vectors entre sí (distancia/ángulo).[/dim]\n"
    )


# ── Ejemplo 2: Similitud semántica ────────────────────────────────────────

def semantic_similarity_demo():
    """
    Demuestra que los embeddings capturan SIGNIFICADO, no ortografía.

    Palabras como "automóvil" y "carro" tendrán alta similitud
    aunque no compartan ninguna letra en común.
    """
    console.print(Panel(
        "[bold blue]Similitud Semántica con Embeddings[/bold blue]",
        title="Ejemplo 03B"
    ))

    pairs = [
        # (texto1, texto2, relación esperada)
        ("automóvil",           "carro",                    "Sinónimos exactos"),
        ("perro",               "gato",                     "Misma categoría (mascotas)"),
        ("inteligencia artificial", "machine learning",     "Área relacionada"),
        ("inteligencia artificial", "artificial intelligence", "Mismo concepto, distinto idioma"),
        ("banco financiero",    "banco de parque",          "Polisemia (misma palabra, distinto significado)"),
        ("amor",                "odio",                     "Conceptos opuestos"),
        ("pizza",               "física cuántica",          "Sin relación"),
        ("rey",                 "reina",                    "Relación de género"),
        ("python",              "serpiente",                "Ambigüedad (lenguaje vs animal)"),
        ("LLM",                 "Large Language Model",     "Acrónimo y su expansión"),
    ]

    table = Table(title="Similitud coseno entre pares de textos", show_lines=True)
    table.add_column("Texto 1",      style="cyan",    max_width=30)
    table.add_column("Texto 2",      style="magenta", max_width=35)
    table.add_column("Similitud",    style="yellow",  justify="center")
    table.add_column("Barra",        style="green",   width=20)
    table.add_column("Relación",     style="white")

    with Progress() as progress:
        task = progress.add_task("Calculando embeddings...", total=len(pairs))

        for t1, t2, relation in pairs:
            emb1 = get_embedding(t1)
            emb2 = get_embedding(t2)
            sim  = cosine_similarity(emb1, emb2)

            # Barra visual
            filled = int(sim * 20)
            bar = "█" * filled + "░" * (20 - filled)

            # Color según similitud
            if   sim >= 0.85: sim_str = f"[green]{sim:.4f}[/green]"
            elif sim >= 0.70: sim_str = f"[yellow]{sim:.4f}[/yellow]"
            elif sim >= 0.50: sim_str = f"[orange3]{sim:.4f}[/orange3]"
            else:             sim_str = f"[red]{sim:.4f}[/red]"

            table.add_row(t1, t2, sim_str, bar, relation)
            progress.advance(task)

    console.print(table)
    console.print(
        "\n[dim]💡 Observa que 'inteligencia artificial' y 'artificial intelligence' "
        "tienen alta similitud a pesar de estar en idiomas diferentes.\n"
        "Los embeddings capturan el SIGNIFICADO, no las letras.[/dim]\n"
    )


# ── Ejemplo 3: Álgebra de embeddings ─────────────────────────────────────

def embedding_arithmetic():
    """
    Uno de los fenómenos más fascinantes de los embeddings:
    se puede hacer ARITMÉTICA con el significado de las palabras.

    El famoso ejemplo de Word2Vec:
        vector("rey") - vector("hombre") + vector("mujer") ≈ vector("reina")

    Esto demuestra que el espacio vectorial captura relaciones semánticas.
    """
    console.print(Panel(
        "[bold blue]Aritmética de Embeddings[/bold blue]\n"
        "[dim]rey - hombre + mujer ≈ reina[/dim]",
        title="Ejemplo 03C"
    ))

    console.print("Generando embeddings para el experimento...\n")

    words = ["rey", "reina", "hombre", "mujer", "presidente", "presidenta",
             "actor", "actriz", "doctor", "doctora"]

    embeddings = {}
    for word in words:
        embeddings[word] = get_embedding(word)
        console.print(f"   ✓ {word}")

    # Experimento: rey - hombre + mujer = ?
    console.print("\n🧮 Calculando: rey - hombre + mujer")
    result_vector = embeddings["rey"] - embeddings["hombre"] + embeddings["mujer"]

    # Comparar con todos los embeddings disponibles
    console.print("\nPalabras más cercanas al resultado:")
    similarities = {
        word: cosine_similarity(result_vector, emb)
        for word, emb in embeddings.items()
        if word not in ["rey", "hombre", "mujer"]  # excluir las usadas
    }

    for word, sim in sorted(similarities.items(), key=lambda x: -x[1]):
        bar = "█" * int(sim * 30)
        console.print(f"   {word:<15} {sim:.4f}  {bar}")

    console.print(
        "\n[dim]💡 El modelo debería poner 'reina' o 'presidenta' como más cercano.\n"
        "Este tipo de álgebra vectorial es la base de sistemas de analogía\n"
        "y de cómo los LLMs 'razonan' por similitud.[/dim]\n"
    )


# ── Ejemplo 4: Búsqueda semántica básica ─────────────────────────────────

def semantic_search_demo():
    """
    Implementación básica de búsqueda semántica.

    CASO DE USO EMPRESARIAL:
        En lugar de buscar por palabras clave exactas, la búsqueda semántica
        encuentra documentos por SIGNIFICADO. Esto es la base de RAG
        (Retrieval-Augmented Generation) para chatbots empresariales.
    """
    console.print(Panel(
        "[bold blue]Búsqueda Semántica Básica[/bold blue]\n"
        "[dim]Base de un sistema RAG empresarial[/dim]",
        title="Ejemplo 03D"
    ))

    # "Base de datos" de fragmentos de documentos
    documents = [
        "El transformer es una arquitectura de red neuronal basada en mecanismos de atención.",
        "Los embeddings representan texto como vectores numéricos en espacio de alta dimensión.",
        "La ventana de contexto limita cuánto texto puede procesar el modelo en una llamada.",
        "La temperatura controla la aleatoriedad en la generación de texto del LLM.",
        "El fine-tuning ajusta un modelo preentrenado para tareas específicas.",
        "RAG combina recuperación de documentos con generación de texto para respuestas precisas.",
        "Los tokens son las unidades mínimas que procesa un LLM, aproximadamente 0.75 palabras.",
        "La alucinación ocurre cuando el modelo genera información plausible pero falsa.",
        "Los modelos GPT son decoders-only, mientras BERT es un encoder-only.",
        "El costo de APIs cloud se calcula por millón de tokens procesados.",
    ]

    # Indexar documentos (en producción: esto se hace una vez y se almacena)
    console.print("📚 Indexando base de conocimiento...")
    doc_embeddings = []
    for doc in documents:
        doc_embeddings.append(get_embedding(doc))
    console.print(f"   ✓ {len(documents)} fragmentos indexados\n")

    # Consultas de prueba
    queries = [
        "¿Cómo funciona la arquitectura de los transformers?",
        "¿Cuánto cuesta usar OpenAI?",
        "información incorrecta del modelo",
        "¿Cómo ajustar el modelo para mi empresa?",
    ]

    for query in queries:
        console.print(f"🔍 Consulta: [yellow]{query}[/yellow]")
        query_emb = get_embedding(query)

        # Calcular similitud con todos los documentos
        scores = [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embeddings]
        best_idx = np.argmax(scores)

        console.print(f"   📄 Resultado: [green]{documents[best_idx][:80]}...[/green]")
        console.print(f"   📊 Similitud: {scores[best_idx]:.4f}\n")

    console.print(
        "[dim]💡 En un sistema RAG real, los fragmentos recuperados se inyectan\n"
        "   en el contexto del LLM para que responda con información actualizada.[/dim]\n"
    )


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    console.print("\n[bold]🤖 FUNDAMENTOS DE ARQUITECTURA LLM — Ejemplo 03[/bold]")
    console.print("[dim]Embeddings y Similitud Semántica[/dim]\n")

    # Verificar Ollama
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ Ollama no está corriendo. Ejecuta: ollama serve[/red]")
        exit(1)

    try:
        inspect_embedding()
        semantic_similarity_demo()
        embedding_arithmetic()
        semantic_search_demo()
    except Exception as e:
        if "404" in str(e) or "model" in str(e).lower():
            console.print(f"[red]❌ Modelo no encontrado.[/red]")
            console.print(f"[yellow]   Solución: ollama pull {EMBED_MODEL}[/yellow]")
        else:
            raise

    console.print("[green]✅ Ejemplo 03 completado.[/green]")
    console.print("[dim]💡 Siguiente: python 04_context_window.py[/dim]\n")
