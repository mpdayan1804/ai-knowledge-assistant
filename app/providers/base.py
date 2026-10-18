"""
Base provider contract for LLM providers.

This module defines the abstraction layer for LLM providers without
depending on any specific implementation (OpenRouter, OpenAI, etc.).
"""

from abc import ABC, abstractmethod
from typing import Optional


class LLMProviderError(Exception):
    """Custom exception for LLM provider errors."""
    pass


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    This defines the contract that all LLM providers must implement,
    allowing the application to switch providers without changing
    the service layer.
    """

    @abstractmethod
    async def generate(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages: List of message dictionaries (system, user, assistant)
            model: Model identifier
            temperature: Sampling temperature (0.0 to 2.0)
            top_p: Nucleus sampling parameter (0.0 to 1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response

        Raises:
            LLMProviderError: If the provider fails to generate a response
        """
        pass
