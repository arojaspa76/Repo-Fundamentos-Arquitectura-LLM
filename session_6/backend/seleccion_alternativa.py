"""
seleccion_alternativa.py
=========================
Selección de alternativa base para un caso simple — Sesión 6.

Objetivo de desempeño del curso: "diseñar una evaluación inicial y un
estimado de costos/tiempos [...] incluyendo consideraciones éticas
básicas". Las Sesiones 5 y 6 construyeron, por separado, cuatro señales
sobre cada proveedor candidato: calidad/evaluación (Sesión 5), costo y
latencia (este módulo, `modelo_costos.py`), y riesgo/sesgo (este módulo,
`riesgos_sesgos.py`). Esta pieza final las combina en UNA decisión.

Por qué una matriz ponderada y no "elegir el más barato" o "elegir el
mejor puntaje de calidad"
--------------------------------------------------------------------
Ninguna de las cuatro señales por sí sola es suficiente: el proveedor
más barato puede tener la peor calidad; el de mejor calidad puede ser
inviable en costo; el más rápido puede tener señales de sesgo sin
revisar. Se necesita un método explícito para combinar criterios de
distinta naturaleza (calidad 0-1, costo en USD, latencia en segundos,
alertas de sesgo) en un solo puntaje comparable.

Este módulo implementa una versión simplificada ("AHP-lite") del
Proceso de Jerarquía Analítica de Saaty, T. L. (1980), "The Analytic
Hierarchy Process (AHP) for Decision Making", McGraw-Hill — el método
de referencia en investigación de operaciones para decisiones con
múltiples criterios. La simplificación deliberada frente al AHP
completo: en vez de pedir comparaciones por pares entre todos los
criterios (la matriz de comparación de Saaty), el equipo asigna
directamente un peso 0-1 a cada criterio (que deben sumar 1) — más
rápido de aplicar en un PoC, al costo de ser menos riguroso
matemáticamente que el AHP completo. Se documenta esta simplificación
explícitamente para que el estudiante entienda la diferencia y sepa
cuándo el AHP completo sí vale la pena (decisiones de alto impacto,
con múltiples stakeholders que pueden no estar de acuerdo en los pesos).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

PESOS_DEFECTO = {
    "calidad": 0.35,
    "costo": 0.30,
    "latencia": 0.20,
    "riesgo_sesgo": 0.15,
}


@dataclass
class CandidatoAlternativa:
    proveedor: str
    modelo: str
    puntaje_calidad: float  # 0-1, de la Sesión 5 (evaluacion.py)
    costo_promedio_usd: float  # de modelo_costos.py
    latencia_p95_segundos: float  # de modelo_costos.py
    tasa_alerta_sesgo: float  # 0-1, de riesgos_sesgos.py (0 = sin alertas)


@dataclass
class ResultadoRanking:
    proveedor: str
    modelo: str
    puntaje_calidad_normalizado: float
    puntaje_costo_normalizado: float
    puntaje_latencia_normalizado: float
    puntaje_riesgo_normalizado: float
    puntaje_ponderado_total: float
    datos_originales: CandidatoAlternativa


def _normalizar_mayor_es_mejor(valores: list[float]) -> list[float]:
    """Normaliza a 0-1 donde el valor más alto del conjunto = 1.0."""
    if not valores:
        return []
    maximo = max(valores)
    if maximo == 0:
        return [0.0 for _ in valores]
    return [round(v / maximo, 4) for v in valores]


def _normalizar_menor_es_mejor(valores: list[float]) -> list[float]:
    """Normaliza a 0-1 donde el valor más BAJO del conjunto = 1.0 (para
    costo, latencia y tasa de alerta de sesgo, donde menos es mejor)."""
    if not valores:
        return []
    maximo = max(valores)
    minimo = min(valores)
    if maximo == minimo:
        return [1.0 for _ in valores]
    return [round(1 - (v - minimo) / (maximo - minimo), 4) for v in valores]


def calcular_ranking(
    candidatos: list[CandidatoAlternativa],
    pesos: Optional[dict[str, float]] = None,
) -> list[ResultadoRanking]:
    pesos = pesos or PESOS_DEFECTO
    suma_pesos = sum(pesos.values())
    if not candidatos:
        return []
    if abs(suma_pesos - 1.0) > 0.01:
        raise ValueError(f"Los pesos deben sumar 1.0 (suman {suma_pesos})")

    calidades = _normalizar_mayor_es_mejor([c.puntaje_calidad for c in candidatos])
    costos = _normalizar_menor_es_mejor([c.costo_promedio_usd for c in candidatos])
    latencias = _normalizar_menor_es_mejor([c.latencia_p95_segundos for c in candidatos])
    riesgos = _normalizar_menor_es_mejor([c.tasa_alerta_sesgo for c in candidatos])

    resultados = []
    for i, candidato in enumerate(candidatos):
        puntaje_total = (
            pesos["calidad"] * calidades[i]
            + pesos["costo"] * costos[i]
            + pesos["latencia"] * latencias[i]
            + pesos["riesgo_sesgo"] * riesgos[i]
        )
        resultados.append(
            ResultadoRanking(
                proveedor=candidato.proveedor,
                modelo=candidato.modelo,
                puntaje_calidad_normalizado=calidades[i],
                puntaje_costo_normalizado=costos[i],
                puntaje_latencia_normalizado=latencias[i],
                puntaje_riesgo_normalizado=riesgos[i],
                puntaje_ponderado_total=round(puntaje_total, 4),
                datos_originales=candidato,
            )
        )
    resultados.sort(key=lambda r: -r.puntaje_ponderado_total)
    return resultados


def recomendacion(resultados: list[ResultadoRanking]) -> dict:
    if not resultados:
        return {"recomendacion": "Sin candidatos para evaluar."}
    ganador = resultados[0]
    margen = (
        round(ganador.puntaje_ponderado_total - resultados[1].puntaje_ponderado_total, 4)
        if len(resultados) > 1
        else None
    )
    if margen is not None and margen < 0.05:
        confianza = (
            f"Margen estrecho ({margen}) frente al segundo lugar ({resultados[1].proveedor}) — "
            "considerar factores cualitativos adicionales (soporte del proveedor, dependencia de "
            "vendor lock-in) antes de decidir, no solo el puntaje."
        )
    else:
        confianza = "Margen claro frente a las demás alternativas."

    return {
        "alternativa_recomendada": f"{ganador.proveedor}:{ganador.modelo}",
        "puntaje_ponderado_total": ganador.puntaje_ponderado_total,
        "margen_sobre_segundo_lugar": margen,
        "nota_confianza": confianza,
        "advertencia": (
            "Esta recomendación depende enteramente de los pesos asignados a cada criterio — "
            "cambiar los pesos puede cambiar el ganador. Siempre reportar los pesos usados junto "
            "con la recomendación (ver PESOS_DEFECTO)."
        ),
    }
