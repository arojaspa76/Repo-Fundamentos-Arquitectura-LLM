"""
Ejemplo 07 — Primera llamada a la API de Ollama
=================================================
Aqui conectamos todo lo aprendido:
variables, dicts, funciones, clases, JSON + requests HTTP.

REQUISITO: Ollama corriendo localmente
    ollama serve
    ollama pull llama3.2

Ejecutar:
    python 07_primera_api_call.py
"""

import json
import requests
from typing import Optional

OLLAMA_URL = "http://localhost:11434"

# ── 1. Health Check — Ver si Ollama esta corriendo ────────────────────────────
print("=" * 50)
print("1. VERIFICAR QUE OLLAMA ESTA CORRIENDO")
print("=" * 50)

def ollama_disponible(url: str = OLLAMA_URL) -> bool:
    """Verifica si el servidor Ollama esta activo."""
    try:
        r = requests.get(f"{url}/api/tags", timeout=3)
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

if not ollama_disponible():
    print("AVISO: Ollama no esta corriendo.")
    print("Para iniciarlo: ollama serve")
    print("Para descargar llama3.2: ollama pull llama3.2")
    print("\nEjecutando en modo SIMULADO para que puedas ver el codigo...\n")
    MODO_SIMULADO = True
else:
    MODO_SIMULADO = False
    print("Ollama detectado correctamente!")

# ── 2. Listar modelos disponibles ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. MODELOS DISPONIBLES EN OLLAMA")
print("=" * 50)

def listar_modelos(url: str = OLLAMA_URL) -> list[str]:
    """Retorna lista de modelos instalados en Ollama."""
    r = requests.get(f"{url}/api/tags")
    r.raise_for_status()
    data = r.json()
    return [m["name"] for m in data.get("models", [])]

if not MODO_SIMULADO:
    try:
        modelos = listar_modelos()
        print(f"Modelos instalados ({len(modelos)}):")
        for m in modelos:
            print(f"  - {m}")
    except Exception as e:
        print(f"Error listando modelos: {e}")
else:
    print("[SIMULADO] Modelos: llama3.2, mistral")


# ── 3. Llamada Basica — POST /api/chat ────────────────────────────────────────
print("\n" + "=" * 50)
print("3. PRIMERA LLAMADA AL LLM")
print("=" * 50)

def chat_simple(
    pregunta: str,
    modelo: str = "llama3.2",
    temperatura: float = 0.7,
    url: str = OLLAMA_URL,
) -> Optional[str]:
    """
    Envia una pregunta al LLM y retorna la respuesta como string.

    Args:
        pregunta:    El mensaje del usuario
        modelo:      Nombre del modelo Ollama
        temperatura: 0.0 (determinista) a 1.0 (creativo)
        url:         URL base de Ollama

    Returns:
        Texto de respuesta, o None si hay error
    """
    payload = {
        "model": modelo,
        "messages": [{"role": "user", "content": pregunta}],
        "stream": False,
        "options": {"temperature": temperatura}
    }

    try:
        print(f"  Enviando a {url}/api/chat...")
        r = requests.post(
            f"{url}/api/chat",
            json=payload,
            timeout=60,
        )
        r.raise_for_status()

        data = r.json()
        return data["message"]["content"]

    except requests.exceptions.ConnectionError:
        print("  ERROR: No se puede conectar a Ollama")
        return None
    except requests.exceptions.Timeout:
        print("  ERROR: Timeout — el modelo tarda demasiado")
        return None
    except Exception as e:
        print(f"  ERROR inesperado: {e}")
        return None


if not MODO_SIMULADO:
    respuesta = chat_simple("Que es un transformer? Responde en 2 oraciones.")
    if respuesta:
        print(f"Pregunta: Que es un transformer?")
        print(f"Respuesta: {respuesta}")
else:
    print("[SIMULADO] Pregunta: Que es un transformer?")
    print("[SIMULADO] Respuesta: Un transformer es una arquitectura de red")
    print("  neuronal basada en el mecanismo de atencion. Fue introducida")
    print("  en 2017 y es la base de modelos como GPT y BERT.")


# ── 4. Llamada con Historial (multi-turno) ────────────────────────────────────
print("\n" + "=" * 50)
print("4. CONVERSACION MULTI-TURNO")
print("=" * 50)

class ClienteOllama:
    """Cliente simple para Ollama con historial de conversacion."""

    def __init__(self, modelo: str = "llama3.2", url: str = OLLAMA_URL):
        self.modelo = modelo
        self.url = url
        self.historial = []
        self._tokens_usados = 0

    def set_system(self, instruccion: str) -> None:
        """Define el rol/comportamiento del asistente."""
        # Limpiar cualquier system message anterior
        self.historial = [m for m in self.historial if m["role"] != "system"]
        self.historial.insert(0, {"role": "system", "content": instruccion})

    def chat(self, mensaje: str) -> str:
        """Envia mensaje y retorna respuesta, manteniendo historial."""
        self.historial.append({"role": "user", "content": mensaje})

        payload = {
            "model": self.modelo,
            "messages": self.historial,
            "stream": False,
        }

        r = requests.post(f"{self.url}/api/chat", json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()

        respuesta_texto = data["message"]["content"]
        self.historial.append({"role": "assistant", "content": respuesta_texto})

        # Acumular tokens
        self._tokens_usados += data.get("prompt_eval_count", 0)
        self._tokens_usados += data.get("eval_count", 0)

        return respuesta_texto

    def tokens_usados(self) -> int:
        return self._tokens_usados

    def limpiar(self) -> None:
        system_msgs = [m for m in self.historial if m["role"] == "system"]
        self.historial = system_msgs


if not MODO_SIMULADO:
    cliente = ClienteOllama("llama3.2")
    cliente.set_system("Eres un profesor de IA. Responde muy brevemente (1-2 frases).")

    preguntas = [
        "Que es un token en LLM?",
        "Y cuantos tokens tiene aproximadamente una palabra en espanol?",
        "Entonces, cuantos tokens tendria una pagina de texto?",
    ]

    for i, pregunta in enumerate(preguntas, 1):
        print(f"\nUsuario [{i}]: {pregunta}")
        try:
            resp = cliente.chat(pregunta)
            print(f"Asistente:  {resp[:200]}...")
        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nTokens totales usados: {cliente.tokens_usados()}")
else:
    print("[SIMULADO] Conversacion multi-turno:")
    print("  Usuario: Que es un token?")
    print("  Asistente: Un token es la unidad minima de texto que procesa un LLM.")
    print("  Usuario: Cuantos tokens tiene una palabra?")
    print("  Asistente: En espanol, aproximadamente 1.3 tokens por palabra.")
    print("  Usuario: Y una pagina de texto?")
    print("  Asistente: Una pagina (~500 palabras) tiene unos 650 tokens aprox.")
    print("\n  [Tokens totales simulados: ~380]")


# ── 5. Manejo de Errores — Retry con Backoff ──────────────────────────────────
print("\n" + "=" * 50)
print("5. RETRY CON BACKOFF — PRODUCCION")
print("=" * 50)

import time

def chat_con_retry(
    pregunta: str,
    modelo: str = "llama3.2",
    max_intentos: int = 3,
    url: str = OLLAMA_URL,
) -> Optional[str]:
    """
    Llama al LLM con reintentos automaticos y backoff exponencial.
    Patron esencial para sistemas en produccion.
    """
    for intento in range(1, max_intentos + 1):
        try:
            print(f"  Intento {intento}/{max_intentos}...")
            payload = {
                "model": modelo,
                "messages": [{"role": "user", "content": pregunta}],
                "stream": False,
            }
            r = requests.post(f"{url}/api/chat", json=payload, timeout=30)
            r.raise_for_status()
            return r.json()["message"]["content"]

        except requests.exceptions.Timeout:
            if intento < max_intentos:
                espera = 2 ** intento   # 2s, 4s, 8s...
                print(f"  Timeout — esperando {espera}s antes de reintentar...")
                time.sleep(espera)
            else:
                print("  Todos los intentos fallaron (Timeout).")

        except requests.exceptions.ConnectionError:
            print(f"  Ollama no disponible en intento {intento}")
            if intento < max_intentos:
                time.sleep(2 ** intento)

        except Exception as e:
            print(f"  Error inesperado: {e}")
            break

    return None


if not MODO_SIMULADO:
    print("Probando chat_con_retry:")
    r = chat_con_retry("Nombre 3 modelos LLM populares.")
    if r:
        print(f"Respuesta: {r[:150]}...")
else:
    print("[SIMULADO] chat_con_retry:")
    print("  Intento 1/3...")
    print("  Respuesta: GPT-4, Llama 3, Claude 3 son tres modelos LLM muy populares.")


# ── 6. Resumen — Que aprendiste ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("RESUMEN: FLUJO COMPLETO DE UNA APP LLM")
print("=" * 50)
print("""
1. Usuario escribe pregunta
   ↓
2. Tu codigo construye el payload JSON
   { model, messages, temperature, ... }
   ↓
3. POST HTTP → Ollama/OpenAI/Anthropic
   requests.post(url, json=payload)
   ↓
4. API retorna respuesta JSON
   { message: { role, content }, tokens, ... }
   ↓
5. Parseas el JSON y extraes el texto
   data["message"]["content"]
   ↓
6. Muestras al usuario / guardas en historial
""")

print("[OK] Ejemplo 07 completado\n")
