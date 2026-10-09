from pydantic import BaseModel


class AppConfig(BaseModel):
    name: str = "AI Knowledge Assistant"
    version: str = "0.1.0"
    environment: str = "development"
    llm_enabled: bool = False


config = AppConfig()
