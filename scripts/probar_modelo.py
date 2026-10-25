"""Llama DIRECTO a OpenRouter (sin pasar por tu API) para ver la respuesta cruda.

Uso:
    python scripts/probar_modelo.py ID_DEL_MODELO 300
    python scripts/probar_modelo.py ID_DEL_MODELO 300 sin-razonamiento
(2.º argumento: max_tokens, por defecto 50. 3.º, opcional: intenta apagar el razonamiento)

La clave se lee de la variable de entorno OPENROUTER_API_KEY y NUNCA se imprime.
"""
import json
import os
import sys

import httpx

modelo = sys.argv[1]
max_tokens = int(sys.argv[2]) if len(sys.argv) > 2 else 50
sin_razonamiento = len(sys.argv) > 3 and sys.argv[3] == "sin-razonamiento"
clave = os.getenv("OPENROUTER_API_KEY")
if not clave:
    raise SystemExit("Falta definir la variable OPENROUTER_API_KEY en esta terminal")

payload = {
    "model": modelo,
    "messages": [{"role": "user", "content": "Explica qué es una API REST con un ejemplo educativo."}],
    "max_tokens": max_tokens,
    "temperature": 0.3,
}
if sin_razonamiento:
    payload["reasoning"] = {"enabled": False}
r = httpx.post(
    "https://openrouter.ai/api/v1/chat/completions",
    json=payload,
    headers={"Authorization": f"Bearer {clave}"},
    timeout=120,
)
print("HTTP", r.status_code)
try:
    data = r.json()
except ValueError:
    raise SystemExit(r.text[:500])

if "choices" in data:
    choice = data["choices"][0]
    msg = choice.get("message", {})
    print("modelo servido :", data.get("model"))
    print("finish_reason  :", choice.get("finish_reason"))
    print("content        :", repr(msg.get("content")))
    print("tiene reasoning:", bool(msg.get("reasoning")))
    usage = data.get("usage") or {}
    detalles = usage.get("completion_tokens_details") or {}
    print("tokens generados:", usage.get("completion_tokens"),
          "| de razonamiento:", detalles.get("reasoning_tokens"))
else:
    print(json.dumps(data, ensure_ascii=False, indent=2)[:1500])