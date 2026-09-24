# Guía: pruebas locales con Ollama

Esta guía permite a cualquier estudiante correr **todo el PoC de las Sesiones 5 y 6 sin gastar un centavo ni tener ninguna API key**, usando un modelo local con [Ollama](https://ollama.com/).

## 1. ¿Por qué un modelo local en esta sesión?

El objetivo de desempeño de la sesión es "diseñar una evaluación inicial y un estimado de costos/tiempos para un PoC simple". Ollama es la herramienta perfecta para esa primera iteración porque:

- El costo por token es **$0** — solo hay costo de infraestructura (CPU/GPU, energía), no de API.
- Permite comparar "¿vale la pena pagar por un proveedor gestionado, o un modelo local ya es suficiente para este caso de uso?" — exactamente el tipo de decisión de costeo que la sesión pide justificar.
- No depende de conectividad ni de cuentas de facturación, ideal para practicar en clase.

Este PoC lo trata como **un proveedor más** dentro de `proveedores.py` (`llamar_ollama`), evaluado con el mismo harness y el mismo dataset dorado que OpenAI, Anthropic o Google — la comparación es justa porque las condiciones (mismo prompt, mismo dataset) son las mismas.

## 2. Instalación (Ubuntu 24.04+)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verificar que el servicio quedó activo:

```bash
systemctl status ollama --no-pager
# o, si no se usa systemd:
ollama serve &
```

Por defecto Ollama expone su API en `http://localhost:11434`, que es lo que lee `OLLAMA_BASE_URL` en `backend/.env.example`.

## 3. Descargar un modelo

Para esta sesión se recomienda un modelo pequeño (corre razonablemente bien en una laptop sin GPU dedicada):

```bash
ollama pull llama3.2
```

Modelos alternativos más livianos si el equipo tiene poca RAM:

```bash
ollama pull llama3.2:1b
ollama pull qwen2.5:3b
```

## 4. Probar el modelo manualmente

```bash
ollama run llama3.2 "Resume en una frase qué es un PoC de LLM."
```

Si responde, el servidor local está funcionando y el backend de la Sesión 5 o de la Sesión 6 podrá usarlo automáticamente.

## 5. Conectarlo al backend (Sesión 5 o Sesión 6)

No se necesita ninguna API key. Solo asegúrese de que `backend/.env` tenga:

```
OLLAMA_BASE_URL=http://localhost:11434
```

Y luego, desde la pestaña "Evaluar proveedor" del dashboard (o directamente contra la API), seleccione `proveedor=ollama`. El backend llamará a `POST /api/generate` de Ollama y el resto del pipeline (evaluación, costeo con tarifa $0, registro) funciona exactamente igual que con un proveedor pagado.

## 6. El costo real de "gratis"

Un punto importante a discutir en la sesión: Ollama no cobra por token, pero **no es gratis en un sentido más amplio**:

- Consume CPU/GPU y memoria del equipo o servidor donde corre — si se despliega en la nube (por ejemplo, una VM con GPU en GCP), ese cómputo sí tiene un costo por hora, independiente de cuánto se use.
- Los modelos pequeños que corren razonablemente rápido en una laptop suelen tener menor calidad que los modelos de frontera de los proveedores gestionados — el trade-off costo-calidad hay que medirlo con el mismo harness de `evaluacion.py`, no asumirlo.
- La latencia en CPU suele ser notablemente mayor que la de un proveedor gestionado con GPUs dedicadas — es una de las métricas que el dashboard reporta junto al puntaje y el costo.

Esta es la razón por la que el módulo de costeo (`costeo.py`) documenta explícitamente que el costo de Ollama en `tarifas_ejemplo.json` es "$0 por token, pero costo real de infraestructura" — para que el estudiante no concluya erróneamente que un modelo local siempre es la opción más barata en términos totales.
