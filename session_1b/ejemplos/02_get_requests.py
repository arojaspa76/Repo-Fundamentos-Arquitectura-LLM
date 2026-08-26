"""
Ejemplo 02 — HTTP GET con requests
=====================================
Consumir APIs publicas y de Ollama con GET.
Aprenderas a enviar parametros, manejar errores y parsear JSON.

Ejecutar:
    python 02_get_requests.py
"""

import requests

# ── 1. GET Simple ─────────────────────────────────────────────────────────────
print("=" * 50)
print("1. GET SIMPLE — PRIMERA LLAMADA HTTP")
print("=" * 50)

# La funcion mas simple posible
try:
    r = requests.get("https://httpbin.org/json", timeout=10)
    print(f"Status:  {r.status_code}")
    print(f"Tipo:    {r.headers.get('Content-Type')}")
    data = r.json()
    print(f"Datos:   {list(data.keys())}")
except Exception as e:
    print(f"[Sin internet]: {e}")
    print("[SIMULADO] Status: 200, Datos: {'slideshow': {...}}")

# ── 2. GET con parametros de query ────────────────────────────────────────────
print("\n" + "=" * 50)
print("2. GET CON PARAMETROS")
print("=" * 50)

print("Los parametros se agregan a la URL: ?clave=valor&clave2=valor2")
print("requests los convierte automaticamente con el parametro 'params'\n")

try:
    r = requests.get(
        "https://httpbin.org/get",
        params={
            "modelo": "llama3.2",
            "temperatura": "0.7",
            "formato": "json",
        },
        timeout=10,
    )
    data = r.json()
    print(f"URL final:  {data.get('url', 'N/A')}")
    print(f"Params rec: {data.get('args', {})}")
except Exception as e:
    print(f"[SIMULADO] URL final: https://httpbin.org/get?modelo=llama3.2&temperatura=0.7")

# ── 3. GET a Ollama — Listar Modelos ─────────────────────────────────────────
print("\n" + "=" * 50)
print("3. GET A OLLAMA — LISTAR MODELOS")
print("=" * 50)

OLLAMA_URL = "http://localhost:11434"

try:
    r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
    if r.status_code == 200:
        data = r.json()
        modelos = data.get("models", [])
        print(f"Modelos instalados ({len(modelos)}):")
        for m in modelos:
            size_gb = m.get("size", 0) / 1e9
            print(f"  - {m['name']:<25} {size_gb:.1f} GB")
    else:
        print(f"Error {r.status_code}: {r.text[:100]}")
except requests.exceptions.ConnectionError:
    print("Ollama no esta corriendo (normal si no lo iniciaste aun).")
    print("[SIMULADO] Modelos: llama3.2 (2.0 GB), mistral (4.1 GB)")


# ── 4. Manejar Errores Correctamente ─────────────────────────────────────────
print("\n" + "=" * 50)
print("4. MANEJO DE ERRORES")
print("=" * 50)

def get_seguro(url: str, params: dict = None, timeout: int = 10) -> dict | None:
    """
    Hace GET con manejo robusto de errores.
    Patron que debes usar en produccion.
    """
    try:
        r = requests.get(url, params=params, timeout=timeout)

        # Lanza exception si status >= 400
        r.raise_for_status()

        return r.json()

    except requests.exceptions.ConnectionError:
        print(f"  ERROR: No se puede conectar a {url}")
        print("  Verifica: URL correcta, servidor corriendo, red disponible")
        return None

    except requests.exceptions.Timeout:
        print(f"  ERROR: Timeout ({timeout}s) — el servidor no responde")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"  ERROR HTTP {e.response.status_code}: {e.response.text[:100]}")
        return None

    except ValueError:
        print("  ERROR: La respuesta no es JSON valido")
        return None


# Prueba con URL valida
print("Test 1: URL valida")
data = get_seguro("https://httpbin.org/status/200", timeout=10)
print(f"  Resultado: {'OK' if data is not None else 'Fallo'}")

# Prueba con error 404
print("\nTest 2: URL inexistente")
data = get_seguro("https://httpbin.org/status/404", timeout=10)
print(f"  Resultado: {'OK' if data is not None else 'Fallo (esperado)'}")

# Prueba con URL que no existe
print("\nTest 3: Servidor que no existe")
data = get_seguro("http://servidor-que-no-existe.local/api", timeout=3)
print(f"  Resultado: {'OK' if data is not None else 'Fallo (esperado)'}")


# ── 5. Respuesta completa — Headers, Status, Body ────────────────────────────
print("\n" + "=" * 50)
print("5. INSPECCIONAR LA RESPUESTA COMPLETA")
print("=" * 50)

try:
    r = requests.get("https://httpbin.org/headers", timeout=10)
    print(f"Status code:     {r.status_code}")
    print(f"Status texto:    {r.reason}")
    print(f"Content-Type:    {r.headers.get('Content-Type')}")
    print(f"Content-Length:  {r.headers.get('Content-Length', 'N/A')} bytes")
    print(f"Tiempo respuesta:{r.elapsed.total_seconds():.3f}s")
    print(f"Encoding:        {r.encoding}")
    print(f"URL final:       {r.url}")

    # Tres formas de leer el body:
    body_json = r.json()             # como dict (si es JSON)
    body_text = r.text               # como string
    body_bytes = r.content           # como bytes (para archivos/imagenes)
    print(f"\nBody como JSON:  {type(body_json).__name__}")
    print(f"Body como text:  {len(body_text)} chars")
    print(f"Body como bytes: {len(body_bytes)} bytes")
except Exception:
    print("[Sin internet — saltando este bloque]")

print("\n[OK] Ejemplo 02 completado\n")
