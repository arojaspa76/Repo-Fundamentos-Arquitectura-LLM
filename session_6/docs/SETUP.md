# Guía de instalación y ejecución — Sesión 6

## Requisitos

- Python 3.12
- Node.js 20+ (React 18 / Vite 6)
- Ubuntu 24.04+ (o Linux/macOS/WSL2 equivalente)
- (Opcional) Ollama — ver `../ollama/GUIA_OLLAMA.md` (reutilizada de la Sesión 5)
- (Opcional) API keys de OpenAI/Anthropic/Google — sin ellas, todo corre en modo simulado

## 1. Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
uvicorn main:app --reload --port 8001
```

Nota: el backend de esta sesión corre en el puerto **8001** (no 8000) para poder tener el backend de la Sesión 5 corriendo en paralelo si se desea comparar ambas sesiones en clase.

```bash
curl http://localhost:8001/
```

Documentación interactiva: `http://localhost:8001/docs`.

### Pruebas

```bash
cd backend
pytest -v
```

Deben pasar 15 pruebas de humo (modelo de costos, riesgos/sesgos, selección de alternativa).

## 2. Frontend (React 18 + Vite 6)

```bash
cd frontend
npm install
npm run dev
```

Abrir `http://localhost:5174` (puerto 5174, distinto al 5173 de la Sesión 5). Configurable con `VITE_API_BASE`.

## 3. Flujo recomendado en clase

1. **Pestaña "1. Costo por Tokens/Latencia"**: correr el perfil contra `ollama` (funciona sin instalar nada) con 10-15 llamadas. Observar que P50, P95 y P99 casi nunca son iguales — y discutir qué significaría si lo fueran (muestra insuficiente, o un sistema extrañamente uniforme).
2. **Pestaña "2. Riesgos y Sesgos"**: revisar la taxonomía de Weidinger y los tres momentos de mitigación de Gallegos, luego correr el bias probe. Discutir: ¿una tasa de alerta de 0% significa "sin sesgo" o "la prueba heurística no lo detectó"? (Es lo segundo — remarcar la advertencia del resumen.)
3. **Pestaña "3. Selección de Alternativa"**: cargar los resultados reales de costo/latencia/sesgo de los pasos anteriores en la tabla de candidatos, ajustar los pesos, y calcular el ranking. Cambiar los pesos y observar si el ganador cambia — esa es la lección central: la "mejor" alternativa depende de lo que el equipo decida priorizar, y eso debe quedar explícito, no implícito.
4. **Pestaña "4. Registro de Corridas"**: revisar el historial completo, filtrando por tipo.

## 4. Estructura del repositorio

```
session_6/
├── README.md
├── docs/
│   ├── SETUP.md
│   └── marco_teorico.md
├── backend/
│   ├── main.py                    → API FastAPI (puerto 8001)
│   ├── modelo_costos.py           → costo por token + percentiles de latencia + costo efectivo
│   ├── riesgos_sesgos.py          → taxonomía Weidinger + bias probe pareado
│   ├── seleccion_alternativa.py   → matriz de decisión ponderada (AHP-lite)
│   ├── registro.py                → registro de corridas (JSON append-only)
│   ├── proveedores.py             → adaptadores de proveedor (reutilizado de la Sesión 5, sin cambios)
│   ├── dataset_sesgo.json         → 6 pares de prompts para el bias probe
│   ├── tarifas_ejemplo.json       → tabla de precios (reutilizada de la Sesión 5)
│   ├── requirements.txt
│   ├── .env.example
│   └── tests/test_sesion6.py      → 15 pruebas de humo
├── frontend/
│   ├── src/App.jsx                → dashboard con 4 pestañas
│   ├── src/components/            → un componente por pestaña
│   └── src/api.js                 → cliente HTTP hacia el backend
└── ollama/
    └── GUIA_OLLAMA.md             → reutilizada de la Sesión 5
```
