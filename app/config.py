from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class AppConfig(BaseModel):
    name: str = "AI Knowledge Assistant"
    version: str = "0.1.0"
    environment: str = "development"
    llm_enabled: bool = bool(os.getenv("OPENROUTER_API_KEY"))


config = AppConfig()
