"""
Experiment 5: Handling failures without external consumption

Tests error handling using FakeLLMProvider to simulate timeout, 429, and no choices errors.
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
QUESTION = "Test question for error handling"


async def test_with_fake_provider():
    """
    Test the API with FakeLLMProvider configured for different error scenarios.

    Note: This requires temporarily modifying the chat router to use FakeLLMProvider.
    For manual testing, change the provider in app/api/routes/chat.py to FakeLLMProvider.
    """
    print("=" * 60)
    print("EXPERIMENT 5: Handling failures without external consumption")
    print("=" * 60)
    print("\nNOTE: This experiment requires manual configuration.")
    print("Modify app/api/routes/chat.py to use FakeLLMProvider with different error scenarios.")
    print("\nScenarios to test:")
    print("1. FakeLLMProvider(simulate_error='timeout') -> Expected: 502")
    print("2. FakeLLMProvider(simulate_error='429') -> Expected: 502")
    print("3. FakeLLMProvider(simulate_error='no_choices') -> Expected: 502")
    print("=" * 60)

    # Example of how to test once configured
    print("\nExample test (assuming FakeLLMProvider is configured):")
    payload = {
        "question": QUESTION,
        "model": "fake",
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 300,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{BASE_URL}/api/v1/chat", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Create a template for manual testing results
    results_template = {
        "timeout": {
            "simulated_case": "Timeout HTTPX",
            "expected_output": "502 (implementación didáctica)",
            "result": "TO BE FILLED MANUALLY",
        },
        "429": {
            "simulated_case": "HTTP 429 del proveedor",
            "expected_output": "502 (implementación didáctica)",
            "result": "TO BE FILLED MANUALLY",
        },
        "no_choices": {
            "simulated_case": "JSON sin choices",
            "expected_output": "502 (implementación didáctica)",
            "result": "TO BE FILLED MANUALLY",
        },
    }

    with open("experiments/logs/experiment_5_template.json", "w") as f:
        json.dump(results_template, f, indent=2)

    print("\nTemplate saved to experiments/logs/experiment_5_template.json")
    print("Fill in the 'result' field after manual testing.")


if __name__ == "__main__":
    asyncio.run(test_with_fake_provider())
