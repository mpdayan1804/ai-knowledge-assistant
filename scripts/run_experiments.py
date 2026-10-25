"""Ejecuta los experimentos del laboratorio y llena la bitácora automáticamente.

Uso (con uvicorn corriendo en otra terminal y la clave de OpenRouter configurada):
    python scripts/run_experiments.py exp0
    python scripts/run_experiments.py exp1 --model ID_EXACTO
    python scripts/run_experiments.py exp2 --model ID_EXACTO
    python scripts/run_experiments.py exp3 --model ID_MODELO_A
    python scripts/run_experiments.py exp3 --model ID_MODELO_B
    python scripts/run_experiments.py exp4 --model ID_EXACTO
    # corrida adicional con más tokens (para modelos de razonamiento):
    python scripts/run_experiments.py exp1 --model ID_EXACTO --max-tokens 1000
    python scripts/run_experiments.py exp2 --model ID_EXACTO --max-tokens 2000   # respuesta de referencia

Genera: lab/bitacora.csv  y  lab/respuestas/<ID>.json (respuesta íntegra).
"""
import argparse
import csv
import json
import time
from datetime import datetime
from pathlib import Path

import httpx

URL = "http://localhost:8000/api/v1/chat"
LAB = Path("lab")
RESP = LAB / "respuestas"
CSV_PATH = LAB / "bitacora.csv"
CAMPOS = ["id", "fecha_hora", "experimento", "modelo_solicitado", "modelo_real",
          "temperature", "top_p", "max_tokens", "status", "finish_reason", "segundos",
          "pregunta", "archivo"]

Q_BASE = "Explica qué es una API REST con un ejemplo educativo."
Q_TEMP = "Explica el concepto de IA usando una analogía comprensible para un aprendiz de software."
Q_TOK = ("Explica los componentes de una API REST, con ejemplo de request y response, "
         "diferencias entre GET y POST y buenas prácticas.")
Q_MODELS = "Explica qué es FastAPI, presenta tres ventajas reales y escribe un ejemplo sencillo de endpoint."
Q_HALLU = ("Explica el algoritmo Zafiro-Delta de optimización cuántica publicado por el "
           "Instituto Algorítmico de Marte en 2024 e incluye su DOI.")


def plan(exp: str):
    """Devuelve lista de (pregunta, temperature, top_p, max_tokens)."""
    if exp == "exp0":
        return ([(Q_BASE, 0.3, 1.0, 300)] * 3
                + [("A", 0.3, 1.0, 300), (Q_BASE, -1, 1.0, 300)])
    if exp == "exp1":
        return [(Q_TEMP, t, 1.0, 300) for t in (0.1, 0.5, 1.0) for _ in range(5)]
    if exp == "exp2":
        return [(Q_TOK, 0.3, 1.0, m) for m in (50, 150, 500)]
    if exp == "exp3":
        return [(Q_MODELS, 0.3, 1.0, 400)] * 3
    if exp == "exp4":
        return [(Q_HALLU, 0.3, 1.0, 400)] * 3
    raise SystemExit("Experimento desconocido")


def siguiente_id() -> int:
    if not CSV_PATH.exists():
        return 1
    with CSV_PATH.open(encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.DictReader(f)) + 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("exp", choices=["exp0", "exp1", "exp2", "exp3", "exp4"])
    ap.add_argument("--model", default=None, help="ID exacto del modelo en OpenRouter")
    ap.add_argument("--max-tokens", type=int, default=None,
                    help="Corrida adicional: reemplaza max_tokens en exp1/exp3/exp4; en exp2 hace UNA llamada de referencia")
    ap.add_argument("--pausa", type=float, default=3.0, help="segundos entre llamadas (evita 429)")
    args = ap.parse_args()

    RESP.mkdir(parents=True, exist_ok=True)
    nuevo = not CSV_PATH.exists()
    n = siguiente_id()

    with CSV_PATH.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if nuevo:
            w.writeheader()

        etiqueta = args.exp
        llamadas = plan(args.exp)
        if args.max_tokens and args.exp != "exp0":
            etiqueta = f"{args.exp}+max{args.max_tokens}"   # distingue la corrida adicional
            if args.exp == "exp2":
                # una sola llamada de referencia con el límite indicado
                llamadas = [(Q_TOK, 0.3, 1.0, args.max_tokens)]

        for pregunta, temp, top_p, max_tok in llamadas:
            if args.max_tokens and args.exp in ("exp1", "exp3", "exp4"):
                max_tok = args.max_tokens
            body = {"question": pregunta, "temperature": temp,
                    "top_p": top_p, "max_tokens": max_tok}
            if args.model:
                body["model"] = args.model

            inicio = time.perf_counter()
            try:
                r = httpx.post(URL, json=body, timeout=120)
                status, payload = r.status_code, r.json()
            except Exception as exc:  # servidor caído, timeout del cliente...
                status, payload = 0, {"error_cliente": repr(exc)}
            segundos = round(time.perf_counter() - inicio, 2)

            rid = f"{n:03d}"
            archivo = RESP / f"{rid}.json"
            archivo.write_text(json.dumps(
                {"request": body, "status": status, "segundos": segundos,
                 "response": payload}, ensure_ascii=False, indent=2), encoding="utf-8")

            w.writerow({
                "id": rid,
                "fecha_hora": datetime.now().isoformat(timespec="seconds"),
                "experimento": etiqueta,
                "modelo_solicitado": args.model or "(default del servidor)",
                "modelo_real": payload.get("model", "") if isinstance(payload, dict) else "",
                "temperature": temp, "top_p": top_p, "max_tokens": max_tok,
                "status": status,
                "finish_reason": payload.get("finish_reason", "") if isinstance(payload, dict) else "",
                "segundos": segundos,
                "pregunta": pregunta, "archivo": str(archivo),
            })
            f.flush()
            print(f"[{rid}] {etiqueta} T={temp} max={max_tok} -> HTTP {status} en {segundos}s")
            n += 1
            time.sleep(args.pausa)


if __name__ == "__main__":
    main()