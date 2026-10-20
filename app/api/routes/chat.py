"""Frontera HTTP: recibe, valida (vía schema), llama al servicio y traduce errores."""
from fastapi import APIRouter, Depends, HTTPException
 
from app.dependencies import get_assistant_service
from app.providers.base import LLMProviderError
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.assistant_service import AssistantService
 
# En main.py: app.include_router(chat.router, prefix="/api/v1")
router = APIRouter(tags=["chat"])
 
 
@router.post("/chat", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    service: AssistantService = Depends(get_assistant_service),
) -> ChatResponse:
    try:
        result = await service.ask(
            body.question,
            temperature=body.temperature,
            top_p=body.top_p,
            max_tokens=body.max_tokens,
            model=body.model,
        )
    except LLMProviderError:
        # Mensaje genérico: no filtramos API key ni cuerpo del proveedor
        raise HTTPException(
            status_code=502,
            detail="El proveedor de IA no pudo atender la solicitud.",
        )
    return ChatResponse(
        answer=result.content, provider=service.provider_name, model=result.model
    )