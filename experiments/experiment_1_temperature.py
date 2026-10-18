"""
Experiment 1: Temperature

Observes the effect of temperature on response variation.
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
QUESTION = "Explica el concepto de IA usando una analogía comprensible para un aprendiz de software."
MODEL = "openai/gpt-3.5-turbo"
TOP_P = 1.0
MAX_TOKENS = 300


async def send_request(temperature: float, repetition: int):
    """Send a request with specific temperature."""
    payload = {
        "question": QUESTION,
        "model": MODEL,
        "temperature": temperature,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
    }

    start_time = datetime.now()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{BASE_URL}/api/v1/chat", json=payload)
    duration = (datetime.now() - start_time).total_seconds()

    return {
        "timestamp": datetime.now().isoformat(),
        "temperature": temperature,
        "repetition": repetition,
        "request": payload,
        "status_code": response.status_code,
        "response": response.json() if response.status_code == 200 else response.text,
        "duration_seconds": duration,
    }


async def run_experiment_1():
    """Run Experiment 1: Temperature."""
    print("=" * 60)
    print("EXPERIMENT 1: Temperature")
    print("=" * 60)
    print(f"Fixed Question: {QUESTION}")
    print(f"Model: {MODEL}")
    print(f"Top-p: {TOP_P}")
    print(f"Max Tokens: {MAX_TOKENS}")
    print("=" * 60)

    temperatures = [0.1, 0.5, 1.0]
    repetitions = 5
    results = []

    for temp in temperatures:
        print(f"\nTemperature: {temp}")
        for i in range(1, repetitions + 1):
            print(f"  Repetition {i}/{repetitions}...", end=" ")
            result = await send_request(temp, i)
            results.append(result)
            print(f"Status: {result['status_code']}, Duration: {result['duration_seconds']:.2f}s")

    # Save results
    with open("experiments/logs/experiment_1_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print("Results saved to experiments/logs/experiment_1_results.json")
    print("=" * 60)

    # Print summary table
    print("\nExperiment Table:")
    print(f"{'Temp.':<10} {'Repetitions':<12} {'Distinct Responses':<25}")
    print("-" * 47)

    for temp in temperatures:
        temp_results = [r for r in results if r["temperature"] == temp]
        distinct_responses = len(set(r["response"]["answer"] for r in temp_results))
        print(f"{temp:<10} {repetitions:<12} {distinct_responses:<25}")


if __name__ == "__main__":
    asyncio.run(run_experiment_1())
