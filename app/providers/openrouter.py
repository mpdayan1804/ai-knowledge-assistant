"""
OpenRouter provider implementation.

This module implements the LLM provider contract for OpenRouter,
handling authentication, HTTP requests, and response interpretation.
"""

import os
import httpx
from app.providers.base import BaseLLMProvider, LLMProviderError


class OpenRouterProvider(BaseLLMProvider):
    """
    OpenRouter implementation of the LLM provider.

    Handles:
    - Authentication via API key
    - HTTP requests to OpenRouter API
    - Response interpretation and error handling
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenRouter provider.

        Args:
            api_key: OpenRouter API key. If not provided, reads from OPENROUTER_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key not provided. "
                "Set OPENROUTER_API_KEY environment variable or pass api_key parameter."
            )
        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout = 30.0

    async def generate(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.7,
        top_p: float = 1.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response using OpenRouter.

        Args:
            messages: List of message dictionaries
            model: Model identifier (e.g., "openai/gpt-3.5-turbo")
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response

        Raises:
            LLMProviderError: If the request fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",  # Required by OpenRouter
            "X-Title": "AI Knowledge Assistant",
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )

                # Handle HTTP errors
                if response.status_code == 429:
                    raise LLMProviderError("Rate limit exceeded (HTTP 429)")
                elif response.status_code == 401:
                    raise LLMProviderError("Invalid API key (HTTP 401)")
                elif response.status_code >= 400:
                    raise LLMProviderError(
                        f"Provider error: HTTP {response.status_code} - {response.text}"
                    )

                data = response.json()

                # Check if response has choices
                if "choices" not in data or not data["choices"]:
                    raise LLMProviderError("Provider response missing 'choices' field")

                # Extract the generated content
                content = data["choices"][0].get("message", {}).get("content", "")

                if not content:
                    raise LLMProviderError("Provider returned empty content")

                return content

        except httpx.TimeoutException:
            raise LLMProviderError("Provider request timed out")
        except httpx.HTTPError as e:
            raise LLMProviderError(f"HTTP error: {str(e)}")
        except Exception as e:
            if isinstance(e, LLMProviderError):
                raise
            raise LLMProviderError(f"Unexpected error: {str(e)}")
