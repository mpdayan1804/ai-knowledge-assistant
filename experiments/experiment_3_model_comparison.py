"""
Experiment 3: Comparison between two models

Compares two models from OpenRouter using a specific prompt about FastAPI.
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
QUESTION = "¿Qué es FastAPI y por qué es popular para construir APIs?"
TEMPERATURE = 0.7
TOP_P = 1.0
MAX_TOKENS = 300
MODELS = ["openai/gpt-3.5-turbo", "anthropic/claude-3-haiku"]


async def send_request(model: str, repetition: int):
    """Send a request with specific model."""
    payload = {
        "question": QUESTION,
        "model": model,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
    }

    start_time = datetime.now()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f"{BASE_URL}/api/v1/chat", json=payload)
    duration = (datetime.now() - start_time).total_seconds()

    response_data = response.json() if response.status_code == 200 else {"error": response.text}

    return {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "repetition": repetition,
        "request": payload,
        "status_code": response.status_code,
        "response": response_data,
        "duration_seconds": duration,
        "answer_length": len(response_data.get("answer", "")),
    }


async def run_experiment_3():
    """Run Experiment 3: Model Comparison."""
    print("=" * 60)
    print("EXPERIMENT 3: Comparison between two models")
    print("=" * 60)
    print(f"Question: {QUESTION}")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Top-p: {TOP_P}")
    print(f"Max Tokens: {MAX_TOKENS}")
    print("=" * 60)

    results = []

    for model in MODELS:
        print(f"\nModel: {model}")
        for i in range(1, 4):  # 3 repetitions per model
            print(f"  Repetition {i}/3...", end=" ")
            result = await send_request(model, i)
            results.append(result)
            print(f"Status: {result['status_code']}, Duration: {result['duration_seconds']:.2f}s")

    # Save results
    with open("experiments/logs/experiment_3_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print("Results saved to experiments/logs/experiment_3_results.json")
    print("=" * 60)

    # Print summary table
    print("\nComparative Table:")
    print(f"{'Model':<30} {'Avg Time (s)':<15} {'Avg Length':<15}")
    print("-" * 60)

    for model in MODELS:
        model_results = [r for r in results if r["model"] == model]
        avg_time = sum(r["duration_seconds"] for r in model_results) / len(model_results)
        avg_length = sum(r["answer_length"] for r in model_results) / len(model_results)
        print(f"{model:<30} {avg_time:<15.2f} {avg_length:<15.0f}")


if __name__ == "__main__":
    asyncio.run(run_experiment_3())
