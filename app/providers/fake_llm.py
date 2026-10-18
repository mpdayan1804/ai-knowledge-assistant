"""
Fake LLM Provider for testing error scenarios.

This provider simulates various error conditions without making
actual HTTP requests to external services.
"""

import asyncio
from app.providers.base import BaseLLMProvider, LLMProviderError


class FakeLLMProvider(BaseLLMProvider):
    """
    Fake LLM provider for testing error scenarios.

    Can simulate:
    - HTTP timeout
    - HTTP 429 (rate limit)
    - Response without choices
    """

    def __init__(self, simulate_error: str = "none"):
        """
        Initialize the fake provider.

        Args:
            simulate_error: Type of error to simulate
                - "none": No error (returns fake response)
                - "timeout": Simulate HTTP timeout
                - "429": Simulate HTTP 429
                - "no_choices": Simulate response without choices
        """
        self.simulate_error = simulate_error

    async def generate(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: int = None,
    ) -> str:
        """
        Generate a response (fake) or simulate an error.

        Args:
            messages: List of message dictionaries
            model: Model identifier
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response (if no error)

        Raises:
            LLMProviderError: If simulating an error
        """
        if self.simulate_error == "timeout":
            await asyncio.sleep(35)  # Exceed default timeout
            raise LLMProviderError("Timeout simulated")

        elif self.simulate_error == "429":
            raise LLMProviderError("Rate limit exceeded (HTTP 429)")

        elif self.simulate_error == "no_choices":
            raise LLMProviderError("Provider response missing 'choices' field")

        else:
            # Return a fake response
            return "This is a fake response from the FakeLLMProvider."
