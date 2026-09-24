# Sesión 6 — Costos por Tokens/Latencia, Riesgos y Sesgos, Selección de Alternativa

**Curso:** Fundamentos de Arquitectura LLM · Capítulo 3: Evaluación, Costeo y Ética en el Uso de LLM
**Objetivo de desempeño:** Diseñar una evaluación inicial y un estimado de costos/tiempos para un PoC simple con LLM, incluyendo consideraciones éticas básicas.

## Temas cubiertos

1. **Modelo de costos por tokens/latencia (cálculo simple).**
2. **Riesgos y sesgos: principios de mitigación.**
3. **Selección de alternativa base para un caso simple.**

## Qué construye este repositorio

Esta sesión cierra la decisión que las Sesiones 5 y 6 vienen preparando sobre el mismo dominio del curso ("Tienda Andina"): **¿qué proveedor de LLM usar como base para el PoC?** — respondida con evidencia, no con intuición.

- Un **modelo de costos por tokens y latencia** (`backend/modelo_costos.py`) que reporta percentiles (P50/P95/P99), no solo promedios — siguiendo la práctica estándar de sistemas distribuidos en producción (Dean & Barroso, 2013) — y calcula un "costo efectivo" que combina precio con cumplimiento de un SLA definido por el equipo.
- Un módulo de **riesgos y sesgos** (`backend/riesgos_sesgos.py`) con la taxonomía completa de 6 categorías de riesgo de Weidinger et al. (2021), los tres momentos de mitigación de Gallegos et al. (2024), y un **bias probe pareado** ejecutable: 6 pares de prompts idénticos salvo por el nombre del cliente, comparados automáticamente para detectar trato diferencial.
- Una **matriz de decisión ponderada** (`backend/seleccion_alternativa.py`), versión simplificada del método AHP de Saaty (1980), que combina calidad, costo, latencia y riesgo de sesgo de cada proveedor candidato en un solo puntaje comparable, con una recomendación final explícita.
- Un **dashboard en React** (`frontend/`) con cuatro pestañas, una por cada pieza anterior, incluyendo una tabla editable de candidatos para experimentar con los pesos de la decisión en vivo durante la clase.
- La **guía de Ollama** de la Sesión 5, reutilizada sin cambios, para correr todo el ejercicio sin costo ni credenciales.

Ver `docs/marco_teorico.md` para el fundamento completo (con citas verificables) de cada decisión de diseño, y `docs/SETUP.md` para instrucciones de instalación y ejecución.

## Por qué está diseñado así (resumen para el estudiante)

El objetivo de desempeño del curso pide explícitamente "un estimado de costos/tiempos [...] incluyendo consideraciones éticas básicas" — tres cosas, no una. Este repositorio las trata como tres módulos independientes que se combinan al final, no como una sola métrica confusa. La idea central de la sesión: **una decisión de "qué proveedor usar" tomada mirando solo el precio por token, o solo un puntaje de calidad, es una decisión incompleta** — la matriz de decisión ponderada existe precisamente para que el equipo tenga que ser explícito sobre qué está priorizando, en vez de decidir "a ojo" y racionalizarlo después.

## Stack técnico

- Python 3.12 + FastAPI (backend, puerto 8001)
- React 18 + Vite 6 (frontend, puerto 5174)
- Ollama (modelo local opcional, reutiliza la guía de la Sesión 5)
- Sin base de datos: registro en JSON append-only
- Todas las credenciales vía variables de entorno

## Inicio rápido

```bash
# Backend
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && cp .env.example .env
uvicorn main:app --reload --port 8001

# Frontend (en otra terminal)
cd frontend && npm install && npm run dev
```

Ver `docs/SETUP.md` para el flujo completo recomendado en clase.
