from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.assistant_service import AssistantService
from app.providers.openrouter import OpenRouterProvider
from app.providers.base import LLMProviderError
import os

router = APIRouter()

# Initialize provider and service
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key:
    provider = OpenRouterProvider(api_key=api_key)
    assistant_service = AssistantService(provider=provider)
else:
    # Fallback to bootstrap if no API key
    from app.services.bootstrap_service import BootstrapService
    assistant_service = BootstrapService()


@router.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that processes user questions using LLM.

    Accepts a JSON with question, model, temperature, top_p, and max_tokens.
    Returns a response with 'answer' and 'provider' fields.

    Provider errors (LLMProviderError) return HTTP 502.
    """
    try:
        # Check if using LLM provider or bootstrap
        if hasattr(assistant_service, 'provider'):
            answer, provider = await assistant_service.process_question(
                question=request.question,
                model=request.model,
                temperature=request.temperature,
                top_p=request.top_p,
                max_tokens=request.max_tokens,
            )
        else:
            # Bootstrap fallback
            response = assistant_service.process_question(request.question)
            answer = response.answer
            provider = response.provider

        return ChatResponse(answer=answer, provider=provider)

    except LLMProviderError as e:
        # Provider errors return 502 (didactic implementation)
        raise HTTPException(status_code=502, detail="Provider error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
