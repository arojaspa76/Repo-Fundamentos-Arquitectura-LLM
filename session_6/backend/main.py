"""
main.py
=======
Backend FastAPI de la Sesión 6 — Modelo de Costos por Tokens/Latencia,
Riesgos y Sesgos, y Selección de Alternativa Base.

Endpoints:
- POST /api/costos/perfil        → corre N llamadas contra un proveedor y calcula costo promedio + percentiles de latencia (P50/P95/P99) + costo efectivo vs. un umbral de SLA
- GET  /api/riesgos/taxonomia    → taxonomía de riesgo de Weidinger et al. (2021)
- GET  /api/riesgos/mitigacion   → los 3 momentos de mitigación de Gallegos et al. (2024)
- GET  /api/riesgos/dataset-sesgo→ el dataset de pares para el bias probe
- POST /api/riesgos/bias-probe   → corre el dataset de pares contra un proveedor y compara respuestas
- POST /api/seleccion/ranking    → matriz de decisión ponderada (AHP-lite) sobre una lista de candidatos
- GET  /api/registro             → historial de corridas (costeo, bias probe, selección)

Misma disciplina de las sesiones anteriores: credenciales vía variables
de entorno, rate limiting con slowapi, CORS solo al frontend de
desarrollo, modo simulado automático sin API keys (ver proveedores.py).
"""
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

import modelo_costos
import os
import proveedores
import registro
import riesgos_sesgos
import seleccion_alternativa

DATASET_SESGO_PATH = Path(__file__).parent / "dataset_sesgo.json"

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Sesión 6 — Costos por Tokens/Latencia, Riesgos y Sesgos, Selección de Alternativa",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origenes_permitidos = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _cargar_dataset_sesgo() -> dict:
    with open(DATASET_SESGO_PATH, encoding="utf-8") as f:
        return json.load(f)


PROMPTS_MUESTRA_LATENCIA = [
    "¿Cuál es la política de devoluciones de Tienda Andina?",
    "¿Hacen envíos internacionales?",
    "¿Puedo pagar en cuotas sin intereses?",
    "¿Qué hacen con mis datos de tarjeta al comprar?",
    "¿Tienen la mochila Andina Trek en stock?",
]


# ---------------------------------------------------------------------------
# Modelos Pydantic
# ---------------------------------------------------------------------------
class SolicitudPerfilCosto(BaseModel):
    proveedor: str
    modelo: Optional[str] = None
    num_llamadas: int = Field(10, ge=3, le=50)
    umbral_sla_segundos: float = Field(3.0, gt=0)
    aprobado_por: Optional[str] = None


class SolicitudBiasProbe(BaseModel):
    proveedor: str
    modelo: Optional[str] = None
    aprobado_por: Optional[str] = None


class CandidatoEntrada(BaseModel):
    proveedor: str
    modelo: str
    puntaje_calidad: float = Field(..., ge=0, le=1)
    costo_promedio_usd: float = Field(..., ge=0)
    latencia_p95_segundos: float = Field(..., ge=0)
    tasa_alerta_sesgo: float = Field(..., ge=0, le=1)


class SolicitudRanking(BaseModel):
    candidatos: list[CandidatoEntrada]
    pesos: Optional[dict[str, float]] = None
    aprobado_por: Optional[str] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def raiz():
    return {"servicio": "Sesión 6 — Costos, Riesgos/Sesgos y Selección de Alternativa", "estado": "ok"}


@app.post("/api/costos/perfil")
@limiter.limit("10/minute")
def perfil_costo(request: Request, solicitud: SolicitudPerfilCosto):
    if solicitud.proveedor not in proveedores.PROVEEDORES:
        raise HTTPException(
            status_code=400,
            detail=f"Proveedor '{solicitud.proveedor}' no soportado. Use uno de: {list(proveedores.PROVEEDORES)}",
        )
    latencias = []
    costos = []
    modelo_usado = solicitud.modelo
    for i in range(solicitud.num_llamadas):
        prompt = PROMPTS_MUESTRA_LATENCIA[i % len(PROMPTS_MUESTRA_LATENCIA)]
        respuesta = proveedores.invocar(solicitud.proveedor, prompt, solicitud.modelo)
        modelo_usado = respuesta.modelo
        latencias.append(respuesta.latencia_segundos)
        estimacion = modelo_costos.calcular_costo_llamada(
            solicitud.proveedor, respuesta.modelo, respuesta.tokens_entrada, respuesta.tokens_salida
        )
        costos.append(estimacion.costo_total_usd)

    perfil = modelo_costos.calcular_perfil_latencia(solicitud.proveedor, modelo_usado or "desconocido", latencias)
    costo_promedio = round(sum(costos) / len(costos), 8) if costos else 0.0
    costo_efectivo = modelo_costos.calcular_costo_efectivo(costo_promedio, latencias, solicitud.umbral_sla_segundos)

    resultado = {
        "perfil_latencia": perfil.__dict__,
        "costo_promedio_usd": costo_promedio,
        "costo_efectivo": costo_efectivo.__dict__,
    }
    run = registro.registrar_corrida("costeo_latencia", resultado, solicitud.aprobado_por)
    return {"run": run, "detalle": resultado}


@app.get("/api/riesgos/taxonomia")
@limiter.limit("30/minute")
def taxonomia_riesgo(request: Request):
    return {"taxonomia": riesgos_sesgos.TAXONOMIA_RIESGO_WEIDINGER}


@app.get("/api/riesgos/mitigacion")
@limiter.limit("30/minute")
def momentos_mitigacion(request: Request):
    return {"momentos": riesgos_sesgos.MOMENTOS_MITIGACION}


@app.get("/api/riesgos/dataset-sesgo")
@limiter.limit("30/minute")
def dataset_sesgo(request: Request):
    return _cargar_dataset_sesgo()


@app.post("/api/riesgos/bias-probe")
@limiter.limit("10/minute")
def bias_probe(request: Request, solicitud: SolicitudBiasProbe):
    if solicitud.proveedor not in proveedores.PROVEEDORES:
        raise HTTPException(
            status_code=400,
            detail=f"Proveedor '{solicitud.proveedor}' no soportado. Use uno de: {list(proveedores.PROVEEDORES)}",
        )
    dataset = _cargar_dataset_sesgo()
    resultados = []
    for par in dataset["pares"]:
        prompt_a = par["plantilla"].format(nombre=par["variante_a"]["nombre"])
        prompt_b = par["plantilla"].format(nombre=par["variante_b"]["nombre"])
        resp_a = proveedores.invocar(solicitud.proveedor, prompt_a, solicitud.modelo)
        resp_b = proveedores.invocar(solicitud.proveedor, prompt_b, solicitud.modelo)
        comparacion = riesgos_sesgos.comparar_par(
            par_id=par["id"],
            categoria=par["categoria"],
            nombre_a=par["variante_a"]["nombre"],
            nombre_b=par["variante_b"]["nombre"],
            respuesta_a=resp_a.texto,
            respuesta_b=resp_b.texto,
        )
        resultados.append(comparacion)

    resumen = riesgos_sesgos.resumen_bias_probe(resultados)
    payload = {
        "proveedor": solicitud.proveedor,
        "resumen": resumen,
        "detalle": [r.__dict__ for r in resultados],
    }
    run = registro.registrar_corrida("bias_probe", payload, solicitud.aprobado_por)
    return {"run": run, "detalle": payload}


@app.post("/api/seleccion/ranking")
@limiter.limit("30/minute")
def ranking_alternativas(request: Request, solicitud: SolicitudRanking):
    candidatos = [
        seleccion_alternativa.CandidatoAlternativa(
            proveedor=c.proveedor,
            modelo=c.modelo,
            puntaje_calidad=c.puntaje_calidad,
            costo_promedio_usd=c.costo_promedio_usd,
            latencia_p95_segundos=c.latencia_p95_segundos,
            tasa_alerta_sesgo=c.tasa_alerta_sesgo,
        )
        for c in solicitud.candidatos
    ]
    try:
        resultados = seleccion_alternativa.calcular_ranking(candidatos, solicitud.pesos)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    recomendacion_final = seleccion_alternativa.recomendacion(resultados)
    payload = {
        "ranking": [
            {
                "proveedor": r.proveedor,
                "modelo": r.modelo,
                "puntaje_calidad_normalizado": r.puntaje_calidad_normalizado,
                "puntaje_costo_normalizado": r.puntaje_costo_normalizado,
                "puntaje_latencia_normalizado": r.puntaje_latencia_normalizado,
                "puntaje_riesgo_normalizado": r.puntaje_riesgo_normalizado,
                "puntaje_ponderado_total": r.puntaje_ponderado_total,
            }
            for r in resultados
        ],
        "recomendacion": recomendacion_final,
        "pesos_usados": solicitud.pesos or seleccion_alternativa.PESOS_DEFECTO,
    }
    run = registro.registrar_corrida("seleccion", payload, solicitud.aprobado_por)
    return {"run": run, "detalle": payload}


@app.get("/api/registro")
@limiter.limit("30/minute")
def obtener_registro(request: Request, tipo: Optional[str] = None):
    return {"corridas": registro.listar_corridas(tipo)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
