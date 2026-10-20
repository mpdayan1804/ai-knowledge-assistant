"""Contrato (Protocol) que cualquier proveedor de LLM debe cumplir.
 
El servicio SOLO conoce este archivo: no sabe nada de OpenRouter,
de URLs ni de headers HTTP. Eso es el desacoplamiento.
"""
from dataclasses import dataclass
from typing import Protocol
 
 
class LLMProviderError(Exception):
    """Error controlado del proveedor (timeout, 429, JSON sin choices...)."""
 
 
@dataclass
class LLMResult:
    content: str          # texto generado por el modelo
    model: str | None     # modelo realmente servido (si el proveedor lo informa)
 
 
class LLMProvider(Protocol):
    name: str
 
    async def generate(
        self,
        messages: list[dict],
        *,
        temperature: float,
        top_p: float,
        max_tokens: int,
        model: str | None = None,
    ) -> LLMResult: ...