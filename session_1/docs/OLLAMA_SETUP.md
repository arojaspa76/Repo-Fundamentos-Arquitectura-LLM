# 🦙 Guía de Instalación de Ollama

## Ejecuta LLMs localmente — Gratis y sin límites

---

## ¿Qué es Ollama?

Ollama es una herramienta que permite ejecutar Large Language Models directamente
en tu computadora, sin necesidad de:
- ❌ API keys
- ❌ Conexión a internet (una vez descargado el modelo)
- ❌ Costos por token
- ❌ Enviar datos a terceros

Es ideal para desarrollo, aprendizaje y prototipos rápidos.

---

## Requisitos de Hardware

| Modelo | RAM Mínima | GPU (Opcional) | Velocidad |
|--------|-----------|----------------|-----------|
| llama3.2 (3B) | 4 GB | No necesaria | Rápido |
| llama3.2 (1B) | 2 GB | No necesaria | Muy rápido |
| mistral (7B) | 8 GB | Recomendada | Medio |
| llama3.1 (8B) | 8 GB | Recomendada | Medio |
| llama3.1 (70B) | 48 GB | Necesaria | Lento sin GPU |

> **Para este curso:** llama3.2 (3B) funciona bien en cualquier laptop moderna.

---

## Instalación

### macOS

```bash
# Opción 1: Homebrew
brew install ollama

# Opción 2: Descargar desde el sitio
# https://ollama.com/download/mac
# Abrir el .dmg y arrastrar a Aplicaciones
```

### Linux (Ubuntu/Debian/Fedora)

```bash
# Script de instalación oficial
curl -fsSL https://ollama.com/install.sh | sh

# Verificar instalación
ollama --version
```

### Windows

1. Descargar el instalador desde: https://ollama.com/download/windows
2. Ejecutar `OllamaSetup.exe`
3. Seguir el asistente de instalación
4. Ollama se iniciará automáticamente en la bandeja del sistema

---

## Primeros Pasos

### 1. Iniciar el servidor Ollama

```bash
# El servidor escucha en http://localhost:11434
ollama serve
```

> En macOS/Windows con la app instalada, el servidor inicia automáticamente.

### 2. Descargar modelos recomendados para el curso

```bash
# Modelo principal del curso (~2 GB)
ollama pull llama3.2

# Para embeddings (requerido para Ejemplo 03)
ollama pull nomic-embed-text

# Alternativas que puedes explorar:
ollama pull mistral      # Muy buena calidad (~4 GB)
ollama pull phi3         # Rápido y eficiente (~2.3 GB)
ollama pull gemma2       # De Google (~5 GB)
```

### 3. Verificar que todo funciona

```bash
# Listar modelos instalados
ollama list

# Probar chat interactivo en terminal
ollama run llama3.2

# Salir del chat interactivo
/bye
```

### 4. Probar la API directamente

```bash
# Test básico de la API REST
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "¿Qué es un transformer en 1 oración?",
    "stream": false
  }'
```

Deberías ver una respuesta JSON con el campo `"response"`.

---

## Comandos Útiles

```bash
# Ver modelos instalados
ollama list

# Ver modelos corriendo en memoria
ollama ps

# Descargar modelo
ollama pull <nombre>

# Eliminar modelo
ollama rm <nombre>

# Información del modelo
ollama show llama3.2

# Chat en terminal
ollama run llama3.2

# Parar un modelo de la memoria
ollama stop llama3.2
```

---

## Gestión de Memoria

Ollama carga los modelos en RAM (o VRAM si tienes GPU).
Para optimizar:

```bash
# Ver cuánta memoria usa cada modelo
ollama ps

# Descargar un modelo de la memoria (sin borrarlo del disco)
ollama stop llama3.2

# Configurar tiempo de inactividad antes de liberar memoria
# (variable de entorno, en segundos, 0 = nunca liberar)
OLLAMA_KEEP_ALIVE=300 ollama serve
```

---

## API Reference

Ollama expone una API REST en `http://localhost:11434`.

### Endpoints principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/generate` | POST | Generar texto (completion) |
| `/api/chat` | POST | Chat con historial |
| `/api/embeddings` | POST | Generar embeddings |
| `/api/tags` | GET | Listar modelos |
| `/api/show` | POST | Info de un modelo |
| `/api/pull` | POST | Descargar modelo |

### Compatibilidad OpenAI

Ollama también tiene un endpoint compatible con la API de OpenAI:

```bash
# Usar el cliente de Python de OpenAI apuntando a Ollama
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # cualquier string
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hola!"}]
)
```

---

## Solución de Problemas

### "connection refused" al hacer requests

```bash
# El servidor no está corriendo
ollama serve

# Si ya está corriendo, verificar el puerto
curl http://localhost:11434/api/tags
```

### "model not found"

```bash
# El modelo no está descargado
ollama pull llama3.2
```

### Muy lento

```bash
# Ver qué está usando los recursos
ollama ps

# Usar un modelo más pequeño
ollama pull llama3.2:1b   # versión 1B (más pequeña y rápida)
```

### Sin GPU en macOS con Apple Silicon

Ollama usa automáticamente el chip M1/M2/M3 vía Metal.
Debería ser notablemente más rápido que en CPU Intel.

---

## Explorar más Modelos

Navega el catálogo completo en: **https://ollama.com/library**

Modelos destacados para desarrollo:

| Modelo | Tamaño | Especialidad |
|--------|--------|-------------|
| `codellama` | 4-7 GB | Generación de código |
| `llava` | 4 GB | Visión + texto |
| `deepseek-coder` | 1-7 GB | Código de alta calidad |
| `dolphin-mixtral` | 26 GB | Sin censura para investigación |
| `starcoder2` | 2-9 GB | Code completion |

---

*Guía de instalación de Ollama — Sesión 1, Fundamentos de Arquitectura LLM*
