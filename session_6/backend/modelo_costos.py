"""
modelo_costos.py
=================
Modelo de costos por tokens/latencia — Sesión 6.

La Sesión 5 calculó el costo de UNA llamada (tokens × tarifa) y una
proyección lineal simple a escala. Esta sesión formaliza el modelo
agregando la dimensión que la Sesión 5 dejó fuera deliberadamente:
la LATENCIA no es un dato accesorio, es un costo en sí mismo — un
PoC que responde en 800ms en promedio pero tarda 6 segundos en el
5% peor de los casos no es "rápido", es impredecible, y esa
impredecibilidad tiene consecuencia de negocio (usuarios que
abandonan, timeouts en cadena, SLAs incumplidos).

Percentiles, no promedios
--------------------------
La práctica de reportar latencia en percentiles (P50/P95/P99) en vez
de solo el promedio es estándar en sistemas distribuidos de
producción — no es una elección arbitraria de este curso. Dean, J. &
Barroso, L. A. (2013), "The Tail at Scale", Communications of the ACM,
56(2), 74-80, documentan por qué: en un sistema con múltiples
componentes (por ejemplo, una llamada a un LLM seguida de post-
procesamiento y guardado en base de datos), la latencia total de la
petición está dominada por el componente más lento de la cadena — el
promedio esconde exactamente el comportamiento que rompe la
experiencia del usuario en el peor caso. Por eso este módulo calcula
SIEMPRE P50, P95 y P99, nunca solo un promedio.

Costo efectivo (cost of unpredictability)
-------------------------------------------
Más allá del costo monetario por token, este módulo introduce un
"costo efectivo" simple: si el equipo define un umbral de SLA (por
ejemplo, "toda respuesta debe llegar en menos de 3 segundos"), se
puede calcular qué fracción de las llamadas lo incumple — esa fracción
es una señal de riesgo operativo tan real como el costo en dólares,
y se reporta junto a él para que la decisión de qué proveedor usar no
se tome mirando solo el precio por token.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

TARIFAS_PATH = Path(__file__).parent / "tarifas_ejemplo.json"


def _cargar_tarifas() -> dict:
    with open(TARIFAS_PATH, encoding="utf-8") as f:
        return json.load(f)


@dataclass
class EstimacionCosto:
    proveedor: str
    modelo: str
    tokens_entrada: int
    tokens_salida: int
    costo_entrada_usd: float
    costo_salida_usd: float
    costo_total_usd: float
    fecha_referencia_tarifa: str
    nota: str


def calcular_costo_llamada(
    proveedor: str, modelo: str, tokens_entrada: int, tokens_salida: int
) -> EstimacionCosto:
    tarifas = _cargar_tarifas()
    clave = f"{proveedor}:{modelo}"
    tarifa = tarifas.get(clave) or tarifas.get(f"{proveedor}:__default__")
    if tarifa is None:
        return EstimacionCosto(
            proveedor=proveedor,
            modelo=modelo,
            tokens_entrada=tokens_entrada,
            tokens_salida=tokens_salida,
            costo_entrada_usd=0.0,
            costo_salida_usd=0.0,
            costo_total_usd=0.0,
            fecha_referencia_tarifa="N/A",
            nota=f"Sin tarifa registrada para '{clave}' — costo reportado como 0.",
        )
    costo_entrada = (tokens_entrada / 1_000_000) * tarifa["usd_por_millon_entrada"]
    costo_salida = (tokens_salida / 1_000_000) * tarifa["usd_por_millon_salida"]
    return EstimacionCosto(
        proveedor=proveedor,
        modelo=modelo,
        tokens_entrada=tokens_entrada,
        tokens_salida=tokens_salida,
        costo_entrada_usd=round(costo_entrada, 8),
        costo_salida_usd=round(costo_salida, 8),
        costo_total_usd=round(costo_entrada + costo_salida, 8),
        fecha_referencia_tarifa=tarifa.get("fecha_referencia", "sin fecha"),
        nota=tarifa.get("nota", ""),
    )


def _percentil(valores_ordenados: list[float], p: float) -> float:
    """Percentil por interpolación lineal (método "nearest-rank" suavizado,
    equivalente al que usan numpy/pandas por defecto) — suficiente para el
    tamaño de muestra de un PoC (decenas a cientos de llamadas), sin
    necesitar una dependencia estadística adicional."""
    if not valores_ordenados:
        return 0.0
    if len(valores_ordenados) == 1:
        return valores_ordenados[0]
    indice = (len(valores_ordenados) - 1) * (p / 100)
    piso = math.floor(indice)
    techo = math.ceil(indice)
    if piso == techo:
        return valores_ordenados[int(indice)]
    peso = indice - piso
    return valores_ordenados[piso] * (1 - peso) + valores_ordenados[techo] * peso


@dataclass
class PerfilLatencia:
    proveedor: str
    modelo: str
    muestras: int
    p50_segundos: float
    p95_segundos: float
    p99_segundos: float
    minimo_segundos: float
    maximo_segundos: float


def calcular_perfil_latencia(proveedor: str, modelo: str, latencias_segundos: list[float]) -> PerfilLatencia:
    valores = sorted(latencias_segundos)
    return PerfilLatencia(
        proveedor=proveedor,
        modelo=modelo,
        muestras=len(valores),
        p50_segundos=round(_percentil(valores, 50), 4),
        p95_segundos=round(_percentil(valores, 95), 4),
        p99_segundos=round(_percentil(valores, 99), 4),
        minimo_segundos=round(min(valores), 4) if valores else 0.0,
        maximo_segundos=round(max(valores), 4) if valores else 0.0,
    )


@dataclass
class ResultadoCostoEfectivo:
    costo_promedio_usd: float
    umbral_sla_segundos: float
    llamadas_totales: int
    llamadas_incumplen_sla: int
    tasa_incumplimiento_sla: float
    interpretacion: str


def calcular_costo_efectivo(
    costo_promedio_usd: float,
    latencias_segundos: list[float],
    umbral_sla_segundos: float = 3.0,
) -> ResultadoCostoEfectivo:
    """Combina costo monetario y cumplimiento de SLA en un solo reporte:
    el 'costo efectivo' de un proveedor no es solo su precio por token,
    también es qué tan seguido rompe la expectativa de tiempo de
    respuesta que el negocio necesita."""
    total = len(latencias_segundos)
    incumplen = sum(1 for lat in latencias_segundos if lat > umbral_sla_segundos)
    tasa = round(incumplen / total, 4) if total else 0.0

    if tasa == 0:
        interpretacion = "Cumple el SLA en el 100% de la muestra — el costo por token es la única variable relevante."
    elif tasa < 0.05:
        interpretacion = "Incumplimiento marginal (<5%) — aceptable para la mayoría de los casos de uso de PoC."
    elif tasa < 0.20:
        interpretacion = "Incumplimiento notable (5-20%) — evaluar si el caso de uso tolera esa variabilidad antes de elegir este proveedor."
    else:
        interpretacion = "Incumplimiento alto (>20%) — el costo por token puede ser engañosamente bajo si 1 de cada 5 respuestas rompe la experiencia del usuario."

    return ResultadoCostoEfectivo(
        costo_promedio_usd=costo_promedio_usd,
        umbral_sla_segundos=umbral_sla_segundos,
        llamadas_totales=total,
        llamadas_incumplen_sla=incumplen,
        tasa_incumplimiento_sla=tasa,
        interpretacion=interpretacion,
    )


def proyectar_costo_poc(
    costo_por_llamada_usd: float, usuarios_estimados: int, llamadas_por_usuario_mes: int
) -> dict:
    llamadas_mes = usuarios_estimados * llamadas_por_usuario_mes
    costo_mes = llamadas_mes * costo_por_llamada_usd
    return {
        "usuarios_estimados": usuarios_estimados,
        "llamadas_por_usuario_mes": llamadas_por_usuario_mes,
        "llamadas_totales_mes": llamadas_mes,
        "costo_estimado_mes_usd": round(costo_mes, 2),
        "costo_estimado_anio_usd": round(costo_mes * 12, 2),
        "advertencia": (
            "Proyección lineal simple — no incluye descuentos por volumen, infraestructura, "
            "reintentos, ni el costo de degradación de experiencia por incumplimiento de SLA "
            "(ver calcular_costo_efectivo)."
        ),
    }
