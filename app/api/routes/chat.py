from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.bootstrap_service import BootstrapService

router = APIRouter()
bootstrap_service = BootstrapService()


@router.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that processes user questions.

    Accepts a JSON with a 'question' field (3-2000 characters).
    Returns a response with 'answer' and 'provider' fields.

    The provider field will always be 'bootstrap-local' in this
    implementation, indicating no real LLM is integrated yet.
    """
    try:
        response = bootstrap_service.process_question(request.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
