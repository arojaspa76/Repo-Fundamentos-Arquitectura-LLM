"""
Pruebas de humo — Sesión 6. Ejecutar con: pytest -v (desde backend/)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import modelo_costos
import riesgos_sesgos
import seleccion_alternativa


# --- modelo_costos ---------------------------------------------------------
def test_calcular_costo_llamada_no_negativo():
    est = modelo_costos.calcular_costo_llamada("openai", "gpt-4o-mini", 1000, 500)
    assert est.costo_total_usd >= 0


def test_percentiles_latencia():
    perfil = modelo_costos.calcular_perfil_latencia(
        "openai", "gpt-4o-mini", [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 5.0]
    )
    assert perfil.p50_segundos <= perfil.p95_segundos <= perfil.p99_segundos
    assert perfil.maximo_segundos == 5.0
    assert perfil.minimo_segundos == 0.5


def test_percentil_muestra_unica():
    perfil = modelo_costos.calcular_perfil_latencia("ollama", "llama3.2", [1.2])
    assert perfil.p50_segundos == perfil.p95_segundos == perfil.p99_segundos == 1.2


def test_costo_efectivo_sin_incumplimiento():
    resultado = modelo_costos.calcular_costo_efectivo(0.002, [0.5, 0.6, 0.7], umbral_sla_segundos=3.0)
    assert resultado.tasa_incumplimiento_sla == 0.0
    assert "100%" in resultado.interpretacion


def test_costo_efectivo_con_incumplimiento_alto():
    resultado = modelo_costos.calcular_costo_efectivo(
        0.002, [5.0, 6.0, 7.0, 0.5], umbral_sla_segundos=3.0
    )
    assert resultado.tasa_incumplimiento_sla == 0.75
    assert "alto" in resultado.interpretacion.lower()


def test_proyeccion_costo_poc():
    proy = modelo_costos.proyectar_costo_poc(0.002, 500, 10)
    assert proy["llamadas_totales_mes"] == 5000
    assert proy["costo_estimado_mes_usd"] == 10.0


# --- riesgos_sesgos ----------------------------------------------------------
def test_comparar_par_sin_diferencia():
    resultado = riesgos_sesgos.comparar_par(
        "p1", "test", "Ana", "Juan",
        respuesta_a="Con gusto le ayudo a resolver su solicitud de inmediato.",
        respuesta_b="Con gusto le ayudo a resolver su solicitud de inmediato hoy mismo.",
    )
    assert resultado.diferencia_tono_detectada is False


def test_comparar_par_con_diferencia_tono():
    resultado = riesgos_sesgos.comparar_par(
        "p2", "test", "Ana", "Juan",
        respuesta_a="Con gusto, claro que sí, aprobamos su solicitud de inmediato, excelente.",
        respuesta_b="Lamentablemente no es posible, no podemos aprobar esto, no aplica.",
    )
    assert resultado.diferencia_tono_detectada is True
    assert "POSIBLE" in resultado.veredicto


def test_resumen_bias_probe_detecta_alertas():
    resultados = [
        riesgos_sesgos.comparar_par(
            "p1", "test", "Ana", "Juan",
            respuesta_a="Con gusto, claro que sí, excelente, aprobamos.",
            respuesta_b="Lamentablemente no podemos, no aplica, no es posible.",
        ),
        riesgos_sesgos.comparar_par(
            "p2", "test", "Ana", "Juan",
            respuesta_a="Con gusto le ayudamos.",
            respuesta_b="Con gusto le ayudamos también.",
        ),
    ]
    resumen = riesgos_sesgos.resumen_bias_probe(resultados)
    assert resumen["pares_evaluados"] == 2
    assert resumen["alertas"] == 1


def test_taxonomia_tiene_seis_categorias():
    assert len(riesgos_sesgos.TAXONOMIA_RIESGO_WEIDINGER) == 6


def test_momentos_mitigacion_tiene_tres():
    assert len(riesgos_sesgos.MOMENTOS_MITIGACION) == 3


# --- seleccion_alternativa ----------------------------------------------------
def test_ranking_ordena_por_puntaje_descendente():
    candidatos = [
        seleccion_alternativa.CandidatoAlternativa("openai", "gpt-4o-mini", 0.9, 0.002, 1.5, 0.0),
        seleccion_alternativa.CandidatoAlternativa("ollama", "llama3.2", 0.6, 0.0, 3.0, 0.1),
    ]
    ranking = seleccion_alternativa.calcular_ranking(candidatos)
    assert ranking[0].puntaje_ponderado_total >= ranking[1].puntaje_ponderado_total


def test_ranking_pesos_invalidos_lanza_error():
    candidatos = [seleccion_alternativa.CandidatoAlternativa("openai", "gpt-4o-mini", 0.9, 0.002, 1.5, 0.0)]
    import pytest

    with pytest.raises(ValueError):
        seleccion_alternativa.calcular_ranking(candidatos, pesos={"calidad": 0.5, "costo": 0.6, "latencia": 0.0, "riesgo_sesgo": 0.0})


def test_recomendacion_identifica_ganador():
    candidatos = [
        seleccion_alternativa.CandidatoAlternativa("openai", "gpt-4o-mini", 0.95, 0.001, 1.0, 0.0),
        seleccion_alternativa.CandidatoAlternativa("ollama", "llama3.2", 0.4, 0.0, 5.0, 0.3),
    ]
    ranking = seleccion_alternativa.calcular_ranking(candidatos)
    rec = seleccion_alternativa.recomendacion(ranking)
    assert rec["alternativa_recomendada"] == "openai:gpt-4o-mini"


def test_ranking_vacio_no_falla():
    assert seleccion_alternativa.calcular_ranking([]) == []
    assert "Sin candidatos" in seleccion_alternativa.recomendacion([])["recomendacion"]
