"""Aquí se CONSTRUYEN servicio y adaptador (inyección de dependencias con Depends)."""
import os

from app.providers.openrouter import OpenRouterProvider
from app.services.assistant_service import AssistantService


def get_assistant_service() -> AssistantService:
    provider = OpenRouterProvider(
        api_key=os.getenv("OPENROUTER_API_KEY"),            # la clave vive SOLO en el entorno
        default_model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        reasoning_off=os.getenv("OPENROUTER_REASONING_OFF") == "1",
        timeout=float(os.getenv("LLM_TIMEOUT_SECONDS", "30")),  # el timeout se define aquí/adaptador
    )
    return AssistantService(provider)