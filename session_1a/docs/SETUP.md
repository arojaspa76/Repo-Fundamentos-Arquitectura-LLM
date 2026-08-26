# Setup — Sesión 1a: Python para IA/LLM

## Requisitos previos

- Python 3.10 o superior
- Git (opcional)
- Ollama (para el ejemplo 07)

---

## Instalación en 3 pasos

### Paso 1 — Clonar o descargar el repositorio

```bash
git clone https://github.com/<tu-usuario>/nivelacion-llm.git
cd nivelacion-llm
```

O descargar el ZIP desde GitHub y descomprimirlo.

### Paso 2 — Instalar dependencias Python

```bash
pip install -r requirements.txt
```

### Paso 3 — Instalar y configurar Ollama (para el Bloque 3)

Ollama permite correr modelos LLM **gratis y localmente**, sin API key.

**macOS / Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**  
Descargar desde https://ollama.ai/download

**Iniciar el servidor:**
```bash
ollama serve
```

**Descargar el modelo llama3.2 (2.0 GB):**
```bash
ollama pull llama3.2
```

**Verificar que funciona:**
```bash
ollama run llama3.2 "Hola, que eres?"
```

---

## Ejecutar los ejemplos

Desde la carpeta `session_1a/ejemplos/`:

```bash
cd session_1a/ejemplos

python 01_variables_tipos.py       # Variables y tipos
python 02_estructuras_control.py   # if/for/while
python 03_funciones.py             # Funciones
python 04_listas_diccionarios.py   # Listas y diccionarios
python 05_json_archivos.py         # JSON y archivos
python 06_oop_basico.py            # Clases y OOP
python 07_primera_api_call.py      # API call a Ollama
```

---

## Configurar variables de entorno (opcional)

Para el ejemplo 07 y proyectos futuros:

```bash
cp .env.example .env
# Edita .env con tu editor favorito
```

Variables disponibles:
- `OLLAMA_URL` — URL de Ollama (default: `http://localhost:11434`)
- `OPENAI_API_KEY` — Clave de OpenAI (si usas modelos cloud)
- `DEFAULT_MODEL` — Modelo por defecto (default: `llama3.2`)

---

## Resolución de problemas

### "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests
# o con el entorno virtual:
pip install -r requirements.txt
```

### "Error: No se puede conectar a Ollama"
```bash
# Verificar que Ollama está corriendo:
ollama serve

# En otra terminal, verificar:
curl http://localhost:11434/api/tags
```

### Python no encontrado (Windows)
Asegúrate de instalar Python con la opción "Add to PATH" marcada.  
Verifica con: `python --version` o `python3 --version`

---

## Estructura del repositorio

```
nivelacion/
├── README.md              ← Descripción general
├── requirements.txt       ← Dependencias Python
├── .env.example           ← Plantilla de variables de entorno
│
├── session_1a/            ← Esta sesión (Python)
│   ├── README.md
│   ├── docs/
│   │   └── SETUP.md       ← Este archivo
│   └── ejemplos/
│       ├── 01_variables_tipos.py
│       ├── 02_estructuras_control.py
│       ├── 03_funciones.py
│       ├── 04_listas_diccionarios.py
│       ├── 05_json_archivos.py
│       ├── 06_oop_basico.py
│       └── 07_primera_api_call.py
│
└── session_1b/            ← Sesión 1b (APIs + LLMs)
    ├── README.md
    ├── docs/
    │   └── SETUP.md
    ├── ejemplos/
    └── backend/
```
