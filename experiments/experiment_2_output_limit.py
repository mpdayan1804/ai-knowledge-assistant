"""
Experiment 2: Output Limit

Tests the effect of max_tokens on response completion.
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
QUESTION = "Explica qué es una API REST con un ejemplo educativo detallado."
MODEL = "openai/gpt-3.5-turbo"
TEMPERATURE = 0.3
TOP_P = 1.0


async def send_request(max_tokens: int, repetition: int):
    """Send a request with specific max_tokens."""
    payload = {
        "question": QUESTION,
        "model": MODEL,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": max_tokens,
    }

    start_time = datetime.now()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{BASE_URL}/api/v1/chat", json=payload)
    duration = (datetime.now() - start_time).total_seconds()

    response_data = response.json() if response.status_code == 200 else {"error": response.text}

    return {
        "timestamp": datetime.now().isoformat(),
        "max_tokens": max_tokens,
        "repetition": repetition,
        "request": payload,
        "status_code": response.status_code,
        "response": response_data,
        "duration_seconds": duration,
        "answer_length": len(response_data.get("answer", "")),
    }


async def run_experiment_2():
    """Run Experiment 2: Output Limit."""
    print("=" * 60)
    print("EXPERIMENT 2: Output Limit")
    print("=" * 60)
    print(f"Fixed Question: {QUESTION}")
    print(f"Model: {MODEL}")
    print(f"Temperature: {TEMPERATURE}")
    print("=" * 60)

    max_tokens_values = [50, 150, 500]
    results = []

    for max_tok in max_tokens_values:
        print(f"\nMax Tokens: {max_tok}")
        for i in range(1, 4):  # 3 repetitions
            print(f"  Repetition {i}/3...", end=" ")
            result = await send_request(max_tok, i)
            results.append(result)
            print(f"Status: {result['status_code']}, Duration: {result['duration_seconds']:.2f}s, Length: {result['answer_length']}")

    # Save results
    with open("experiments/logs/experiment_2_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print("Results saved to experiments/logs/experiment_2_results.json")
    print("=" * 60)

    # Print summary table
    print("\nExperiment Table:")
    print(f"{'Max Tokens':<12} {'Status':<10} {'Duration (s)':<15} {'Answer Length':<15}")
    print("-" * 52)

    for max_tok in max_tokens_values:
        max_tok_results = [r for r in results if r["max_tokens"] == max_tok]
        for r in max_tok_results:
            print(f"{max_tok:<12} {r['status_code']:<10} {r['duration_seconds']:<15.2f} {r['answer_length']:<15}")


if __name__ == "__main__":
    asyncio.run(run_experiment_2())
