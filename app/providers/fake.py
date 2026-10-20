"""Proveedor falso: sirve para probar sin gastar llamadas reales."""
from app.providers.base import LLMProviderError, LLMResult
 
 
class FakeLLMProvider:
    name = "fake"
 
    def __init__(self, answer: str = "respuesta falsa", fail_with: str | None = None):
        self._answer = answer
        self._fail_with = fail_with
        self.calls: list[dict] = []   # para verificar qué recibió
 
    async def generate(self, messages, *, temperature, top_p, max_tokens, model=None):
        self.calls.append(
            {"messages": messages, "temperature": temperature,
             "top_p": top_p, "max_tokens": max_tokens, "model": model}
        )
        if self._fail_with:
            raise LLMProviderError(self._fail_with)
        return LLMResult(content=self._answer, model="fake-model")
  