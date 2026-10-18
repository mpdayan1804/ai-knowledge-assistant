"""
Experiment 4: Hallucinations and uncertainty management

Investigates model hallucinations by asking about a fictitious concept.
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
QUESTION = "Explica el algoritmo de optimización cuántica 'Q-Neural-Sync' inventado en 2023."
MODEL = "openai/gpt-3.5-turbo"
TEMPERATURE = 0.3
TOP_P = 1.0
MAX_TOKENS = 300


async def send_request(repetition: int):
    """Send a request about fictitious concept."""
    payload = {
        "question": QUESTION,
        "model": MODEL,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
    }

    start_time = datetime.now()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{BASE_URL}/api/v1/chat", json=payload)
    duration = (datetime.now() - start_time).total_seconds()

    response_data = response.json() if response.status_code == 200 else {"error": response.text}

    # Analyze behavior
    answer = response_data.get("answer", "").lower()
    behavior = "unknown"

    if "no tengo información" in answer or "no conozco" in answer or "no estoy seguro" in answer:
        behavior = "expresses_uncertainty"
    elif "no encontrado" in answer or "inventado" in answer or "ficticio" in answer:
        behavior = "states_fictitious"
    elif "referencia" in answer or "fuente" in answer:
        behavior = "requests_source"
    else:
        behavior = "invents_data"

    return {
        "timestamp": datetime.now().isoformat(),
        "repetition": repetition,
        "request": payload,
        "status_code": response.status_code,
        "response": response_data,
        "duration_seconds": duration,
        "behavior": behavior,
    }


async def run_experiment_4():
    """Run Experiment 4: Hallucinations."""
    print("=" * 60)
    print("EXPERIMENT 4: Hallucinations and Uncertainty")
    print("=" * 60)
    print(f"Question: {QUESTION}")
    print(f"Model: {MODEL}")
    print(f"Temperature: {TEMPERATURE}")
    print("=" * 60)

    results = []

    for i in range(1, 4):  # 3 repetitions
        print(f"\nAttempt {i}/3...", end=" ")
        result = await send_request(i)
        results.append(result)
        print(f"Status: {result['status_code']}, Behavior: {result['behavior']}")

    # Save results
    with open("experiments/logs/experiment_4_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print("Results saved to experiments/logs/experiment_4_results.json")
    print("=" * 60)

    # Print summary table
    print("\nBehavior Table:")
    print(f"{'Attempt':<10} {'Behavior':<30} {'Evidence Fragment':<30}")
    print("-" * 70)

    for r in results:
        answer = r["response"].get("answer", "")
        fragment = answer[:50] + "..." if len(answer) > 50 else answer
        print(f"{r['repetition']:<10} {r['behavior']:<30} {fragment:<30}")


if __name__ == "__main__":
    asyncio.run(run_experiment_4())
