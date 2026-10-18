# Análisis y Conclusiones Individuales - Módulo I

## Preguntas de Análisis

### 1. ¿Qué variable causó las diferencias más visibles y cómo lo verificaste?

**Respuesta:** La **temperatura**. Verifiqué con el Experimento 1: a temperatura 0.1 las respuestas eran muy consistentes, a 1.0 mostraban mayor variación en vocabulario y estructura.

### 2. ¿Por qué una temperatura más alta no demuestra automáticamente mayor calidad?

**Respuesta:** Porque aumenta la variación aleatoria, puede introducir incoherencias, y la calidad depende de precisión técnica no de creatividad. Para respuestas educativas, precisión > creatividad.

### 3. ¿Qué diferencia observaste entre un error 422 local y un error del proveedor remoto?

**Respuesta:**
- **422 local**: Ocurre en Pydantic ANTES de invocar el LLM. No consume tokens, es rápido, error claro.
- **502 remoto**: Ocurre DESPUÉS de enviar al LLM. Consume tiempo y potencialmente tokens. Error genérico por seguridad.

El 422 es validación preventiva, el 502 es error de infraestructura que ya incurrió en consumo.

### 4. ¿Qué evidencia demuestra que el servicio está desacoplado del proveedor?

**Respuesta:**
- El servicio depende de `BaseLLMProvider` (abstracción), no de `OpenRouterProvider` (implementación)
- Podemos reemplazar el proveedor sin modificar el servicio
- `FakeLLMProvider` permite testing sin peticiones HTTP reales
- El router es agnóstico al proveedor

El desacoplamiento permite cambiar de proveedor modificando solo el adaptador.

### 5. Si la respuesta toma 20 segundos, ¿qué capa es responsable de esperar y cuál de definir el timeout?

**Respuesta:**
- **Responsable de esperar**: Capa de Infraestructura/Adaptador (`providers/openrouter.py`) con `httpx.AsyncClient`
- **Responsable de timeout**: Capa de Infraestructura/Adaptador (define 30 segundos)

El servicio y router delegan esta responsabilidad a la capa de infraestructura.

### 6. ¿Qué modificarías para medir tokens usados y el costo real sin alterar la API pública?

**Respuesta:**
1. Modificar adaptador para extraer tokens/costo de la respuesta del proveedor
2. Extender contrato `generate()` para retornar metadatos
3. Actualizar servicio para capturar metadatos
4. Agregar campos opcionales `tokens_used` y `cost` en `ChatResponse`
5. Logging interno sin exponer al cliente

La API no cambia si los campos son opcionales.

---

## Conclusiones Generales

Este laboratorio permitió comprender:
1. La validación preventiva (422) evita consumo innecesario
2. Los hiperparámetros (temperatura, max_tokens) impactan la calidad y variación
3. La arquitectura en capas facilita testing, mantenimiento y evolución
4. El desacoplamiento servicio-proveedor es fundamental para flexibilidad
5. El manejo de errores debe ser controlado y no revelar información sensible
6. La experimentación sistemática es necesaria para entender el comportamiento de LLMs
