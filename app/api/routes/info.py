from fastapi import APIRouter
from app.schemas.info import InfoResponse
from app.config import config

router = APIRouter()


@router.get("/api/v1/info", response_model=InfoResponse)
async def info() -> InfoResponse:
    """
    Info endpoint that returns basic project information.
    Includes application name, version, environment, and LLM status.
    """
    return InfoResponse(
        name=config.name,
        version=config.version,
        environment=config.environment,
        llm_enabled=config.llm_enabled
    )
