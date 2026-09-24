"""
proveedores.py
================
Adaptadores mínimos para invocar distintos proveedores de LLM bajo una
interfaz común. Sigue el mismo patrón de "modo simulado" usado en las
sesiones anteriores del curso: si no hay API key configurada para un
proveedor, la función NO falla — devuelve una respuesta simulada
determinística para que todo el pipeline de evaluación/costeo/registro
se pueda probar de punta a punta sin gastar dinero ni requerir credenciales.

Proveedores soportados:
- openai      (API de OpenAI, ej. gpt-4o-mini)
- anthropic   (API de Anthropic, ej. claude-haiku)
- google      (API de Google Gemini)
- ollama      (modelo local vía Ollama, sin costo, ver ../ollama/GUIA_OLLAMA.md)

Ninguna API key se hardcodea: todas se leen de variables de entorno con
os.getenv(), siguiendo la práctica del curso desde la Sesión 1b.
"""
from __future__ import annotations

import hashlib
import os
import time
from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class RespuestaProveedor:
    proveedor: str
    modelo: str
    texto: str
    tokens_entrada: int
    tokens_salida: int
    latencia_segundos: float
    modo_simulado: bool


def _tokens_aprox(texto: str) -> int:
    """Aproximación gruesa: ~4 caracteres por token (regla de dedo usada
    por los proveedores en su propia documentación de pricing)."""
    return max(1, round(len(texto) / 4))


def _respuesta_simulada(proveedor: str, modelo: str, prompt: str, inicio: float) -> RespuestaProveedor:
    """Genera una respuesta simulada determinística (hash del prompt) para
    que las corridas sean reproducibles en modo demo/CI sin llamar a ninguna
    API real."""
    semilla = hashlib.sha256(f"{proveedor}:{modelo}:{prompt}".encode()).hexdigest()[:8]
    texto = (
        f"[MODO_SIMULADO:{proveedor}] Respuesta de ejemplo ({semilla}) para: "
        f"\"{prompt[:80]}\". Configure la API key correspondiente para obtener "
        f"una respuesta real del modelo."
    )
    return RespuestaProveedor(
        proveedor=proveedor,
        modelo=modelo,
        texto=texto,
        tokens_entrada=_tokens_aprox(prompt),
        tokens_salida=_tokens_aprox(texto),
        latencia_segundos=round(time.time() - inicio, 4),
        modo_simulado=True,
    )


def llamar_openai(prompt: str, modelo: str = "gpt-4o-mini", timeout: float = 30.0) -> RespuestaProveedor:
    inicio = time.time()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _respuesta_simulada("openai", modelo, prompt, inicio)
    try:
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": modelo,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        texto = data["choices"][0]["message"]["content"]
        uso = data.get("usage", {})
        return RespuestaProveedor(
            proveedor="openai",
            modelo=modelo,
            texto=texto,
            tokens_entrada=uso.get("prompt_tokens", _tokens_aprox(prompt)),
            tokens_salida=uso.get("completion_tokens", _tokens_aprox(texto)),
            latencia_segundos=round(time.time() - inicio, 4),
            modo_simulado=False,
        )
    except Exception:
        return _respuesta_simulada("openai", modelo, prompt, inicio)


def llamar_anthropic(prompt: str, modelo: str = "claude-haiku-4-5", timeout: float = 30.0) -> RespuestaProveedor:
    inicio = time.time()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return _respuesta_simulada("anthropic", modelo, prompt, inicio)
    try:
        resp = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": modelo,
                "max_tokens": 512,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        texto = "".join(b.get("text", "") for b in data.get("content", []))
        uso = data.get("usage", {})
        return RespuestaProveedor(
            proveedor="anthropic",
            modelo=modelo,
            texto=texto,
            tokens_entrada=uso.get("input_tokens", _tokens_aprox(prompt)),
            tokens_salida=uso.get("output_tokens", _tokens_aprox(texto)),
            latencia_segundos=round(time.time() - inicio, 4),
            modo_simulado=False,
        )
    except Exception:
        return _respuesta_simulada("anthropic", modelo, prompt, inicio)


def llamar_google(prompt: str, modelo: str = "gemini-2.5-flash", timeout: float = 30.0) -> RespuestaProveedor:
    inicio = time.time()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return _respuesta_simulada("google", modelo, prompt, inicio)
    try:
        resp = httpx.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
            params={"key": api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        texto = data["candidates"][0]["content"]["parts"][0]["text"]
        meta = data.get("usageMetadata", {})
        return RespuestaProveedor(
            proveedor="google",
            modelo=modelo,
            texto=texto,
            tokens_entrada=meta.get("promptTokenCount", _tokens_aprox(prompt)),
            tokens_salida=meta.get("candidatesTokenCount", _tokens_aprox(texto)),
            latencia_segundos=round(time.time() - inicio, 4),
            modo_simulado=False,
        )
    except Exception:
        return _respuesta_simulada("google", modelo, prompt, inicio)


def llamar_ollama(prompt: str, modelo: str = "llama3.2", timeout: float = 60.0) -> RespuestaProveedor:
    """Llama a un modelo local servido por Ollama (http://localhost:11434
    por defecto). No requiere API key: si el servidor de Ollama no está
    corriendo, cae a modo simulado igual que los demás proveedores."""
    inicio = time.time()
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    try:
        resp = httpx.post(
            f"{base_url}/api/generate",
            json={"model": modelo, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        texto = data.get("response", "")
        return RespuestaProveedor(
            proveedor="ollama",
            modelo=modelo,
            texto=texto,
            tokens_entrada=data.get("prompt_eval_count", _tokens_aprox(prompt)),
            tokens_salida=data.get("eval_count", _tokens_aprox(texto)),
            latencia_segundos=round(time.time() - inicio, 4),
            modo_simulado=False,
        )
    except Exception:
        return _respuesta_simulada("ollama", modelo, prompt, inicio)


PROVEEDORES = {
    "openai": llamar_openai,
    "anthropic": llamar_anthropic,
    "google": llamar_google,
    "ollama": llamar_ollama,
}


def invocar(proveedor: str, prompt: str, modelo: Optional[str] = None) -> RespuestaProveedor:
    if proveedor not in PROVEEDORES:
        raise ValueError(
            f"Proveedor '{proveedor}' no soportado. Use uno de: {list(PROVEEDORES)}"
        )
    fn = PROVEEDORES[proveedor]
    return fn(prompt, modelo) if modelo else fn(prompt)
