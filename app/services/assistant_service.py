"""Lógica de aplicación: arma los mensajes system + user y delega al proveedor."""
from app.providers.base import LLMProvider, LLMResult
 
SYSTEM_PROMPT = (
    "Eres AI Knowledge Assistant, un asistente educativo para aprendices de software. "
    "Responde en español, de forma clara y con ejemplos sencillos. "
    "Si no conoces algo o no estás seguro, dilo explícitamente. "
    "No inventes datos, citas, DOI ni referencias."
)
 
 
class AssistantService:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider
 
    @property
    def provider_name(self) -> str:
        return self._provider.name
 
    async def ask(
        self,
        question: str,
        *,
        temperature: float,
        top_p: float,
        max_tokens: int,
        model: str | None = None,
    ) -> LLMResult:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
        return await self._provider.generate(
            messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            model=model,
        )