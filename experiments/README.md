# Experiments - Module I

This directory contains the experiments for Module I of the AI Knowledge Assistant course.

## Setup

1. Ensure you have an OpenRouter API key: https://openrouter.ai/keys
2. Create a `.env` file in the project root:
   ```
   cp .env.example .env
   ```
3. Add your API key to `.env`:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

## Running the API

```bash
# Activate virtual environment
.venv/Scripts/activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .

# Start the server
uvicorn app.main:app --reload
```

## Experiments

### Experiment 0: Baseline and Validation

Validates input data and distinguishes internal errors from model responses.

```bash
python experiments/experiment_0_baseline.py
```

**Tests:**
- Baseline (valid request) → Expected: 200
- question = "A" → Expected: 422
- temperature = -1 → Expected: 422

### Experiment 1: Temperature

Observes the effect of temperature on response variation.

```bash
python experiments/experiment_1_temperature.py
```

**Parameters:**
- Temperatures: 0.1, 0.5, 1.0
- 5 repetitions per temperature
- Fixed question, model, top_p, max_tokens

### Experiment 2: Output Limit

Tests the effect of max_tokens on response completion.

```bash
python experiments/experiment_2_output_limit.py
```

**Parameters:**
- Max tokens: 50, 150, 500
- 3 repetitions per value
- Fixed temperature, model, question

### Experiment 3: Model Comparison

Compares two models from OpenRouter.

```bash
python experiments/experiment_3_model_comparison.py
```

**Models:**
- openai/gpt-3.5-turbo
- anthropic/claude-3-haiku

### Experiment 4: Hallucinations

Investigates model hallucinations by asking about a fictitious concept.

```bash
python experiments/experiment_4_hallucinations.py
```

**Question:** About a fictitious quantum optimization algorithm.

### Experiment 5: Failure Handling

Tests error handling using FakeLLMProvider.

```bash
python experiments/experiment_5_failure_handling.py
```

**Scenarios:**
- Timeout HTTPX → Expected: 502
- HTTP 429 from provider → Expected: 502
- JSON without choices → Expected: 502

**Note:** This requires manual configuration of the router to use FakeLLMProvider.

## Results

All experiment results are saved in `experiments/logs/` as JSON files.

## Deliverables

1. Complete log and integral responses (TXT/JSON)
2. Swagger captures with valid and 422 requests
3. Comparative table between two models
4. Evidence of hallucination or uncertainty
5. Evidence of simulated failures and tests
6. Annotated flow diagram identifying routes, files, errors, and response returns
7. Technical conclusions (at least 300 words) - See `analisis_y_conclusiones.md`
