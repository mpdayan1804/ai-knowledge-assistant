"""Pydantic valida tipos y rangos. Si algo no cumple -> HTTP 422 automático."""
from pydantic import BaseModel, ConfigDict, Field
 
 
class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, protected_namespaces=())
 
    question: str = Field(min_length=3, max_length=2000)
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    top_p: float = Field(default=1.0, gt=0.0, le=1.0)
    max_tokens: int = Field(default=300, ge=1, le=2000)
    model: str | None = Field(default=None, description="ID exacto del modelo (opcional)")
 
 
class ChatResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
 
    answer: str
    provider: str
    model: str | None = None