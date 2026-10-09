from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns HTTP 200 when the service is healthy.
    """
    return {"status": "healthy"}
