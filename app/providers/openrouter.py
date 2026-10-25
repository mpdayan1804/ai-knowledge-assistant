"""Adaptador de OpenRouter: aquí vive TODO lo que es infraestructura HTTP."""
import httpx

from app.providers.base import LLMProviderError, LLMResult


class OpenRouterProvider:
    name = "openrouter"

    def __init__(
        self,
        api_key: str | None,
        default_model: str,
        base_url: str = "https://openrouter.ai/api/v1",
        timeout: float = 30.0,
        reasoning_off: bool = False,   # intenta apagar el razonamiento (no todos los modelos lo permiten)
        transport: httpx.AsyncBaseTransport | None = None,  # para simular fallos en pruebas
    ) -> None:
        self._api_key = api_key
        self._default_model = default_model
        self._base_url = base_url
        self._timeout = timeout
        self._reasoning_off = reasoning_off
        self._transport = transport

    async def generate(
        self,
        messages: list[dict],
        *,
        temperature: float,
        top_p: float,
        max_tokens: int,
        model: str | None = None,
    ) -> LLMResult:
        if not self._api_key:
            raise LLMProviderError("API key no configurada")

        used_model = model or self._default_model
        payload = {
            "model": used_model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
        }
        if self._reasoning_off:
            payload["reasoning"] = {"enabled": False}
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(
                timeout=self._timeout, transport=self._transport
            ) as client:
                response = await client.post(
                    f"{self._base_url}/chat/completions", json=payload, headers=headers
                )
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException as exc:
            raise LLMProviderError("Timeout al llamar al proveedor") from exc
        except httpx.HTTPStatusError as exc:
            # Solo guardamos el código, NUNCA el cuerpo ni los headers (pueden ser sensibles)
            raise LLMProviderError(
                f"El proveedor respondió HTTP {exc.response.status_code}"
            ) from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise LLMProviderError("Error de comunicación con el proveedor") from exc

        try:
            choice = data["choices"][0]
            content = choice["message"].get("content")
            finish_reason = choice.get("finish_reason")
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            raise LLMProviderError("Respuesta del proveedor sin 'choices'") from exc

        served_model = data.get("model", used_model)

        if not content:
            # Caso típico de modelos de razonamiento: gastaron TODO max_tokens pensando.
            # No es una falla del proveedor, es un truncamiento: lo reportamos como tal.
            if finish_reason == "length":
                return LLMResult(content="", model=served_model, finish_reason="length")
            raise LLMProviderError("El proveedor devolvió contenido vacío")

        return LLMResult(content=content, model=served_model, finish_reason=finish_reason)