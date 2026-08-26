"""
Ejemplo 01 — HTTP y REST desde Cero
======================================
Antes de llamar a un LLM, necesitas entender HTTP.
Todo: navegador, app movil, SDK de OpenAI — usa HTTP bajo el capot.

Ejecutar:
    python 01_http_conceptos.py
"""

import requests

print("=" * 50)
print("HTTP Y REST: LOS FUNDAMENTOS")
print("=" * 50)

print("""
CONCEPTO CLAVE: HTTP es el protocolo de comunicacion de la web.
Cuando tu codigo llama a Ollama o OpenAI, hace una llamada HTTP.

  Tu Codigo  ──── HTTP Request ────>  Servidor LLM
             <─── HTTP Response ────

Estructura de una Request:
  METODO  URL
  Headers (metadatos)
  Body    (datos JSON — solo en POST/PUT)

Estructura de una Response:
  Status Code (200=OK, 400=Error cliente, 500=Error servidor)
  Headers
  Body (JSON con la respuesta)
""")

# ── 1. HTTP GET — Obtener informacion ─────────────────────────────────────────
print("=" * 50)
print("1. HTTP GET — LEER INFORMACION")
print("=" * 50)

print("GET = 'Dame informacion de este recurso'")
print("Ejemplos reales:")
print("  GET /api/tags         → listar modelos en Ollama")
print("  GET /v1/models        → listar modelos en OpenAI")
print("  GET /api/users/42     → obtener usuario #42")

# Llamada GET real a una API publica
print("\nHaciendo GET a https://httpbin.org/get ...")
try:
    r = requests.get("https://httpbin.org/get", timeout=10)

    print(f"\nStatus Code: {r.status_code}")
    print(f"Content-Type: {r.headers.get('Content-Type', 'N/A')}")

    data = r.json()
    print(f"Tu IP publica:  {data.get('origin', 'N/A')}")
    print(f"URL solicitada: {data.get('url', 'N/A')}")
    print(f"Headers enviados: {list(data.get('headers', {}).keys())}")

except requests.exceptions.ConnectionError:
    print("[Sin internet — mostrando respuesta simulada]")
    print("Status Code: 200")
    print("{'origin': '1.2.3.4', 'url': 'https://httpbin.org/get'}")

# ── 2. Status Codes — Que significan ─────────────────────────────────────────
print("\n" + "=" * 50)
print("2. STATUS CODES — ENTENDER LAS RESPUESTAS")
print("=" * 50)

status_codes = {
    200: ("OK", "Todo bien — la respuesta tiene el contenido"),
    201: ("Created", "Recurso creado exitosamente (POST exitoso)"),
    400: ("Bad Request", "Tu request tiene errores (JSON mal formado, parametros invalidos)"),
    401: ("Unauthorized", "Falta API key o es invalida"),
    403: ("Forbidden", "No tienes permisos (plan no incluye este modelo)"),
    404: ("Not Found", "El endpoint o recurso no existe"),
    429: ("Too Many Requests", "Superaste el rate limit — espera o reduce frecuencia"),
    500: ("Internal Server Error", "Error del servidor LLM"),
    503: ("Service Unavailable", "Servidor sobrecargado o en mantenimiento"),
}

print(f"{'Codigo':<8} {'Nombre':<25} {'Significado'}")
print("-" * 70)
for code, (nombre, desc) in status_codes.items():
    print(f"{code:<8} {nombre:<25} {desc}")

# Verificar status code en tu codigo
print("\nComo verificar en tu codigo:")
print("""
  r = requests.post(url, json=payload)

  if r.status_code == 200:
      data = r.json()
      respuesta = data["message"]["content"]

  elif r.status_code == 429:
      print("Rate limit — esperando 60s...")
      time.sleep(60)

  elif r.status_code == 401:
      print("API key invalida o faltante")

  else:
      print(f"Error inesperado: {r.status_code}")
      print(r.text)
""")

# ── 3. Headers — Metadatos de la Request ─────────────────────────────────────
print("=" * 50)
print("3. HEADERS — LOS METADATOS DE LA REQUEST")
print("=" * 50)

print("Headers son pares clave-valor que acompanan la request.")
print("Los mas importantes para APIs LLM:\n")

headers_importantes = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-tu-api-key-aqui",
    "Accept": "application/json",
    "User-Agent": "mi-app/1.0",
}

for header, valor in headers_importantes.items():
    print(f"  {header}: {valor}")

print("""
Content-Type: application/json  → dices que el body es JSON
Authorization: Bearer sk-...    → tu API key para autenticarte

Ejemplo con requests:
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
  }
  r = requests.post(url, json=payload, headers=headers)

NOTA: Ollama local NO necesita Authorization (es tu propio servidor).
OpenAI, Anthropic, etc. SI requieren la key en el header.
""")

# ── 4. Los 4 Verbos HTTP que usaras ──────────────────────────────────────────
print("=" * 50)
print("4. LOS 4 VERBOS HTTP")
print("=" * 50)

verbos = [
    ("GET",    "Leer/obtener informacion",        "GET /api/tags (listar modelos)"),
    ("POST",   "Crear/enviar datos nuevos",       "POST /api/chat (enviar mensaje al LLM)"),
    ("PUT",    "Actualizar completamente",        "PUT /api/config (reemplazar configuracion)"),
    ("DELETE", "Eliminar un recurso",             "DELETE /api/session/123 (eliminar sesion)"),
]

print(f"{'Verbo':<10} {'Accion':<30} {'Ejemplo con LLM'}")
print("-" * 70)
for verbo, accion, ejemplo in verbos:
    print(f"{verbo:<10} {accion:<30} {ejemplo}")

print("""
En el curso usaremos principalmente:
  GET  → verificar que Ollama corre, listar modelos
  POST → enviar mensajes al LLM, generar embeddings
""")

# ── 5. REST = Convencion de URLs ─────────────────────────────────────────────
print("=" * 50)
print("5. REST: CONVENCIONES DE URL")
print("=" * 50)

print("""
REST no es un protocolo, es una convencion de diseno.
Las URLs representan RECURSOS (sustantivos), los verbos son las acciones.

API de Ollama (REST):
  GET  /api/tags              → lista todos los modelos
  POST /api/chat              → chat con un modelo
  POST /api/generate          → generar texto (sin historial)
  POST /api/embeddings        → generar embeddings de texto
  POST /api/pull              → descargar un nuevo modelo

API de OpenAI (REST):
  GET  /v1/models             → lista modelos disponibles
  POST /v1/chat/completions   → chat (compatible con Ollama!)
  POST /v1/embeddings         → generar embeddings

URL base + path = endpoint completo:
  http://localhost:11434  +  /api/chat  =  http://localhost:11434/api/chat
""")

print("[OK] Ejemplo 01 completado\n")
