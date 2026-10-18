from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="User question to be processed"
    )
    model: str = Field(
        default="openai/gpt-3.5-turbo",
        description="Model identifier (e.g., openai/gpt-3.5-turbo)"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature (0.0 to 2.0)"
    )
    top_p: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling parameter (0.0 to 1.0)"
    )
    max_tokens: int = Field(
        default=300,
        ge=1,
        le=4096,
        description="Maximum tokens to generate"
    )

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty_or_whitespace(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Question cannot be empty or whitespace only")
        return v.strip()


class ChatResponse(BaseModel):
    answer: str
    provider: str
