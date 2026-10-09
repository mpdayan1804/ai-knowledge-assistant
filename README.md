# AI Knowledge Assistant - Bootstrap API

Primer incremento funcional del proyecto AI Knowledge Assistant para el Módulo 0 del curso de Ingeniería de Sistemas de IA.

## Objetivo

Construir, probar y versionar la base técnica de una API asíncrona preparada para evolucionar en un sistema de IA real. Este proyecto NO integra ningún proveedor de LLM (OpenAI, Anthropic, etc.) en este módulo.

## Tecnologías

- Python 3.12+
- FastAPI (Framework web asíncrono)
- Pydantic (Validación de datos)
- AsyncIO (Programación asíncrona)
- HTTPX (Cliente HTTP asíncrono)
- pytest (Framework de pruebas)
- Git/GitHub (Control de versiones)

## Requisitos Previos

- Python 3.12 o superior instalado
- Git instalado
- Cuenta en GitHub

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd ai-knowledge-assistant
```

### 2. Crear el entorno virtual

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

**En Windows (Git Bash):**
```bash
source .venv/Scripts/activate
```

**En Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

**En Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -e .
```

## Ejecución de la API

### Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

### Documentación de la API

FastAPI genera automáticamente la documentación interactiva:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Endpoints Disponibles

### GET /health
Verifica que la API esté funcionando correctamente.

**Respuesta esperada:**
```json
{
  "status": "healthy"
}
```

### POST /api/v1/chat
Procesa una pregunta del usuario y retorna una respuesta de bootstrap.

**Request:**
```json
{
  "question": "¿Qué es FastAPI?"
}
```

**Respuesta esperada:**
```json
{
  "answer": "...",
  "provider": "bootstrap-local"
}
```

**Validaciones:**
- La pregunta debe tener entre 3 y 2000 caracteres
- Preguntas vacías o solo espacios retornan HTTP 422

### GET /api/v1/info
Retorna información básica del proyecto.

**Respuesta esperada:**
```json
{
  "name": "AI Knowledge Assistant",
  "version": "0.1.0",
  "environment": "development",
  "llm_enabled": false
}
```

## Ejecución de Pruebas

### Ejecutar todas las pruebas

```bash
python -m pytest -q
```

### Ejecutar pruebas con detalle

```bash
python -m pytest -v
```

### Ejecutar solo pruebas unitarias

```bash
python -m pytest tests/unit/
```

### Ejecutar solo pruebas de integración

```bash
python -m pytest tests/integration/
```

## Suite de Pruebas

El proyecto incluye las siguientes pruebas obligatorias:

- **T-01:** Unit test del servicio (respuesta a pregunta conocida)
- **T-02:** GET /health retorna HTTP 200
- **T-03:** POST /api/v1/chat con pregunta válida retorna HTTP 200
- **T-04:** POST /api/v1/chat con pregunta muy corta retorna HTTP 422
- **T-05:** GET /api/v1/info retorna HTTP 200 y llm_enabled = false

**Total de pruebas:** 16 (7 unitarias + 9 de integración)

## Demostración Asíncrona

El proyecto incluye un script de demostración que muestra el uso de AsyncIO y HTTPX:

```bash
python scripts/async_demo.py
```

Este script demuestra cómo hacer múltiples peticiones HTTP concurrentemente.

## Estructura del Proyecto

```
ai-knowledge-assistant/
├── app/
│   ├── main.py              # Aplicación FastAPI principal
│   ├── config.py            # Configuración de la aplicación
│   ├── api/
│   │   └── routes/
│   │       ├── health.py    # Endpoint /health
│   │       ├── chat.py      # Endpoint /api/v1/chat
│   │       └── info.py      # Endpoint /api/v1/info
│   ├── schemas/
│   │   ├── chat.py          # Modelos ChatRequest y ChatResponse
│   │   └── info.py          # Modelo InfoResponse
│   └── services/
│       └── bootstrap_service.py  # Lógica de negocio
├── scripts/
│   └── async_demo.py        # Demostración asíncrona
├── tests/
│   ├── unit/
│   │   └── test_bootstrap_service.py
│   └── integration/
│       └── test_api.py
├── .gitignore
├── pyproject.toml
├── pytest.ini
└── README.md
```

## Arquitectura

El proyecto sigue una arquitectura de capas con separación de responsabilidades:

1. **Capa HTTP (Routes):** Maneja las peticiones y respuestas HTTP
2. **Capa de Datos (Schemas):** Define y valida los modelos de datos con Pydantic
3. **Capa de Servicios:** Contiene la lógica de negocio independiente de la capa HTTP

Flujo: Cliente → FastAPI → Pydantic → Service → Pydantic → FastAPI → Cliente

## Restricciones

**NO se incluye en este módulo:**
- Integración con proveedores de LLM (OpenAI, Anthropic, Gemini, Ollama)
- Frameworks como LangChain o LangGraph
- Bases de datos (PostgreSQL, Redis, bases vectoriales)
- Sistemas RAG, agentes o memoria conversacional

Estas funcionalidades se agregarán en módulos posteriores.

## Calidad del Código

- Todas las pruebas pasan sin fallos
- Código asíncrono con async/await
- Validación de datos con Pydantic
- Documentación OpenAPI automática
- Commits coherentes y descriptivos
- Sin secretos o credenciales en el repositorio

## Estado del Proyecto

✅ Completado - Módulo 0 - Primer incremento funcional

## Autor

Desarrollado como proyecto del curso de Ingeniería de Sistemas de IA - Módulo 0.
