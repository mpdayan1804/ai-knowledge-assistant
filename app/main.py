from fastapi import FastAPI
from app.api.routes import health, chat, info

app = FastAPI(
    title="AI Knowledge Assistant",
    description="Bootstrap API for AI Knowledge Assistant - Module 0",
    version="0.1.0"
)

# Include routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(info.router)


@app.get("/")
async def root():
    """
    Root endpoint with basic information.
    """
    return {
        "message": "AI Knowledge Assistant - Bootstrap API",
        "docs": "/docs",
        "version": "0.1.0"
    }
