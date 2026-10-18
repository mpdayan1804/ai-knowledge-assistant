"""
Experiment 0: Baseline and Validation

Validates input data and distinguishes internal errors from model responses.
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


async def send_request(question: str, temperature: float = 0.7, top_p: float = 1.0, max_tokens: int = 300, model: str = "openai/gpt-3.5-turbo"):
    """Send a request to the chat endpoint."""
    payload = {
        "question": question,
        "model": model,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }

    start_time = datetime.now()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{BASE_URL}/api/v1/chat", json=payload)
    duration = (datetime.now() - start_time).total_seconds()

    return {
        "timestamp": datetime.now().isoformat(),
        "request": payload,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "duration_seconds": duration,
    }


async def run_experiment_0():
    """Run Experiment 0: Baseline and Validation."""
    print("=" * 60)
    print("EXPERIMENT 0: Baseline and Validation")
    print("=" * 60)

    results = []

    # Test 1: Baseline (valid request)
    print("\n1. Baseline (valid request)...")
    result = await send_request(
        question="Explica qué es una API REST con un ejemplo educativo.",
        temperature=0.3,
        top_p=1.0,
        max_tokens=300,
    )
    results.append(("Baseline", result))
    print(f"   Status: {result['status_code']} (expected: 200)")
    print(f"   Duration: {result['duration_seconds']:.2f}s")

    # Test 2: Invalid question (too short)
    print("\n2. Invalid question (too short)...")
    result = await send_request(question="A")
    results.append(("question = A", result))
    print(f"   Status: {result['status_code']} (expected: 422)")

    # Test 3: Invalid temperature (negative)
    print("\n3. Invalid temperature (negative)...")
    try:
        result = await send_request(
            question="Test", temperature=-1.0
        )
        results.append(("temperature = -1", result))
        print(f"   Status: {result['status_code']} (expected: 422)")
    except Exception as e:
        print(f"   Error: {e}")

    # Save results
    with open("experiments/logs/experiment_0_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print("Results saved to experiments/logs/experiment_0_results.json")
    print("=" * 60)

    # Print summary
    print("\nValidation Table:")
    print(f"{'Test':<25} {'Expected HTTP':<15} {'Observed HTTP':<15}")
    print("-" * 55)
    for test_name, result in results:
        if test_name == "Baseline":
            expected = "200"
        else:
            expected = "422"
        print(f"{test_name:<25} {expected:<15} {result['status_code']:<15}")


if __name__ == "__main__":
    asyncio.run(run_experiment_0())
