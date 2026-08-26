"""
Ejemplo 06 — Clases y Programacion Orientada a Objetos
========================================================
En LLM: cada cliente de API es una clase.
El SDK de Anthropic, OpenAI y Ollama usan clases.

Ejecutar:
    python 06_oop_basico.py
"""

# ── 1. Clase Basica ───────────────────────────────────────────────────────────
print("=" * 50)
print("1. CLASE BASICA — MODELO LLM")
print("=" * 50)

class ModeloLLM:
    """Representa un modelo de lenguaje con su configuracion."""

    # Atributo de CLASE (compartido por todas las instancias)
    proveedor_default = "Ollama"

    def __init__(self, nombre: str, temperatura: float = 0.7, max_tokens: int = 1000):
        """Constructor — se ejecuta al crear una instancia."""
        # Atributos de INSTANCIA (cada objeto tiene los suyos)
        self.nombre = nombre
        self.temperatura = temperatura
        self.max_tokens = max_tokens
        self.historial = []          # historial privado de cada instancia
        self._llamadas = 0           # convencion: _ = "semi-privado"

    def construir_request(self, pregunta: str) -> dict:
        """Construye el body JSON para la API."""
        self.historial.append({"role": "user", "content": pregunta})
        self._llamadas += 1
        return {
            "model": self.nombre,
            "messages": self.historial.copy(),
            "temperature": self.temperatura,
            "max_tokens": self.max_tokens,
        }

    def agregar_respuesta(self, respuesta: str) -> None:
        """Registra la respuesta del asistente en el historial."""
        self.historial.append({"role": "assistant", "content": respuesta})

    def limpiar_historial(self) -> None:
        """Reinicia la conversacion."""
        self.historial = []
        print(f"  Historial de {self.nombre} limpiado.")

    def stats(self) -> str:
        """Retorna estadisticas del modelo."""
        return f"{self.nombre}: {self._llamadas} llamadas, {len(self.historial)} mensajes"

    def __str__(self) -> str:
        """Representacion legible (print())."""
        return f"ModeloLLM(nombre={self.nombre}, temp={self.temperatura})"

    def __repr__(self) -> str:
        """Representacion tecnica (depuracion)."""
        return f"ModeloLLM('{self.nombre}', {self.temperatura}, {self.max_tokens})"


# Crear instancias
llama = ModeloLLM("llama3.2")
mistral = ModeloLLM("mistral", temperatura=0.3, max_tokens=500)

print(f"Modelo 1: {llama}")
print(f"Modelo 2: {mistral}")

# Usar la instancia
req = llama.construir_request("Que es un transformer?")
llama.agregar_respuesta("Un transformer es una arquitectura de red neuronal...")
req2 = llama.construir_request("Y los embeddings?")

print(f"\nStats llama:   {llama.stats()}")
print(f"Stats mistral: {mistral.stats()}")
print(f"Ultimo req (model): {req2['model']}, temp: {req2['temperature']}")


# ── 2. Herencia ────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. HERENCIA — ESPECIALIZACION DE CLIENTES")
print("=" * 50)

class ModeloLocal(ModeloLLM):
    """Modelo que corre localmente con Ollama — siempre gratis."""

    def __init__(self, nombre: str, url: str = "http://localhost:11434", **kwargs):
        super().__init__(nombre, **kwargs)   # llama al __init__ del padre
        self.url = url
        self.costo_por_millon = 0.0

    def endpoint_chat(self) -> str:
        return f"{self.url}/api/chat"

    def calcular_costo(self, tokens: int) -> float:
        return 0.0   # gratis!

    def __str__(self) -> str:
        return f"ModeloLocal(nombre={self.nombre}, url={self.url})"


class ModeloCloud(ModeloLLM):
    """Modelo en la nube con costo por token."""

    def __init__(self, nombre: str, api_key: str, precio_millon: float, **kwargs):
        super().__init__(nombre, **kwargs)
        self.api_key = api_key
        self.precio_millon = precio_millon
        self._tokens_usados = 0

    def calcular_costo(self, tokens: int) -> float:
        self._tokens_usados += tokens
        return (tokens / 1_000_000) * self.precio_millon

    def costo_acumulado(self) -> float:
        return (self._tokens_usados / 1_000_000) * self.precio_millon

    def __str__(self) -> str:
        return f"ModeloCloud(nombre={self.nombre}, precio=${self.precio_millon}/M)"


# Instanciar subclases
llama_local = ModeloLocal("llama3.2")
gpt = ModeloCloud("gpt-4o-mini", api_key="sk-...", precio_millon=0.15)
claude = ModeloCloud("claude-3-haiku", api_key="sk-ant-...", precio_millon=0.25)

print(f"Local:  {llama_local}")
print(f"GPT:    {gpt}")
print(f"Claude: {claude}")

print(f"\nEndpoint local: {llama_local.endpoint_chat()}")
print(f"Costo llama (10K tokens):  ${llama_local.calcular_costo(10_000):.4f}")
print(f"Costo GPT   (10K tokens):  ${gpt.calcular_costo(10_000):.4f}")
print(f"Costo Claude(10K tokens):  ${claude.calcular_costo(10_000):.4f}")

# Los subclases heredan metodos del padre
llama_local.construir_request("Hola!")
llama_local.agregar_respuesta("Hola, como puedo ayudarte?")
print(f"\nStats (heredado): {llama_local.stats()}")


# ── 3. isinstance() y polimorfismo ────────────────────────────────────────────
print("\n" + "=" * 50)
print("3. POLIMORFISMO — USAR CUALQUIER MODELO IGUAL")
print("=" * 50)

def procesar_con_modelo(modelo: ModeloLLM, pregunta: str) -> None:
    """Funciona con cualquier ModeloLLM (local o cloud)."""
    req = modelo.construir_request(pregunta)

    # Calcular costo si el modelo lo soporta
    tokens_estimados = len(pregunta.split()) * 2
    if isinstance(modelo, ModeloCloud):
        costo = modelo.calcular_costo(tokens_estimados)
        tipo = "CLOUD"
    else:
        costo = 0.0
        tipo = "LOCAL"

    print(f"  [{tipo}] {modelo.nombre}: request lista, ~{tokens_estimados} tokens, ${costo:.6f}")


modelos_disponibles = [llama_local, gpt, claude]
pregunta = "Que es un embedding?"

print(f"Pregunta: '{pregunta}'")
for m in modelos_disponibles:
    procesar_con_modelo(m, pregunta)


# ── 4. Clase con @property ────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("4. PROPIEDADES — ATRIBUTOS CON LOGICA")
print("=" * 50)

class ConversacionLLM:
    """Gestiona una conversacion completa con un LLM."""

    def __init__(self, modelo: str, max_mensajes: int = 20):
        self._modelo = modelo
        self.max_mensajes = max_mensajes
        self._mensajes = []

    @property
    def modelo(self) -> str:
        """Getter — acceder como atributo."""
        return self._modelo

    @modelo.setter
    def modelo(self, nuevo_modelo: str) -> None:
        """Setter — validacion al asignar."""
        modelos_validos = ["llama3.2", "mistral", "gpt-4o-mini", "claude-3-haiku"]
        if nuevo_modelo not in modelos_validos:
            raise ValueError(f"Modelo '{nuevo_modelo}' no valido. Usa: {modelos_validos}")
        self._modelo = nuevo_modelo
        print(f"  Modelo cambiado a: {nuevo_modelo}")

    @property
    def tokens_estimados(self) -> int:
        """Calcula tokens aproximados del historial."""
        total_chars = sum(len(m["content"]) for m in self._mensajes)
        return total_chars // 4   # aprox 4 chars por token

    @property
    def cerca_del_limite(self) -> bool:
        """True si el historial esta al 80% de capacidad."""
        return len(self._mensajes) >= self.max_mensajes * 0.8

    def agregar(self, rol: str, contenido: str) -> None:
        if len(self._mensajes) >= self.max_mensajes:
            # Eliminar mensajes mas antiguos (excepto system)
            self._mensajes = [m for m in self._mensajes if m["role"] == "system"]
            print("  Historial truncado — demasiados mensajes")
        self._mensajes.append({"role": rol, "content": contenido})


conv = ConversacionLLM("llama3.2", max_mensajes=10)
conv.agregar("system", "Eres un experto en Python.")
conv.agregar("user", "Explica las listas en Python.")
conv.agregar("assistant", "Las listas son estructuras de datos ordenadas y mutables...")
conv.agregar("user", "Dame un ejemplo con LLMs.")

print(f"Modelo actual:    {conv.modelo}")          # getter
print(f"Tokens estimados: {conv.tokens_estimados}")
print(f"Cerca del limite: {conv.cerca_del_limite}")

# Probar setter con validacion
try:
    conv.modelo = "llama3.2"       # OK
    conv.modelo = "modelo-falso"   # ValueError
except ValueError as e:
    print(f"  Error esperado: {e}")

print("\n[OK] Ejemplo 06 completado\n")
