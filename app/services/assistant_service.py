"""
Assistant service for LLM-powered responses.

This service coordinates the LLM provider, manages system prompts,
and orchestrates the inference process.
"""

from app.providers.base import BaseLLMProvider, LLMProviderError


class AssistantService:
    """
    Service layer for the AI assistant.

    Responsibilities:
    - Add system prompt
    - Coordinate provider contract
    - Handle provider errors
    """

    def __init__(self, provider: BaseLLMProvider):
        """
        Initialize the assistant service.

        Args:
            provider: LLM provider instance (e.g., OpenRouterProvider)
        """
        self.provider = provider
        self.system_prompt = (
            "Eres un asistente de IA educativo y claro. "
            "Explica conceptos técnicos de manera que sean comprensibles "
            "para aprendices de ingeniería de software. "
            "Usa analogías cuando sea apropiado."
        )

    async def process_question(
        self,
        question: str,
        model: str = "openai/gpt-3.5-turbo",
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: int = 300,
    ) -> tuple[str, str]:
        """
        Process a user question using the LLM provider.

        Args:
            question: User's question
            model: Model identifier
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens to generate

        Returns:
            Tuple of (answer, provider_name)

        Raises:
            LLMProviderError: If the provider fails
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": question},
        ]

        try:
            answer = await self.provider.generate(
                messages=messages,
                model=model,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            provider_name = model.split("/")[0] if "/" in model else model
            return answer, provider_name
        except LLMProviderError as e:
            # Re-raise to be handled by the router
            raise
