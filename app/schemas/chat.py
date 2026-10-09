from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="User question to be processed"
    )

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty_or_whitespace(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Question cannot be empty or whitespace only")
        return v.strip()


class ChatResponse(BaseModel):
    answer: str
    provider: str = "bootstrap-local"
