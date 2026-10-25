"""Muestra un resumen de las respuestas guardadas en lab/respuestas/.

Uso:
    python scripts/ver_respuestas.py 6 20        # IDs del 6 al 20
    python scripts/ver_respuestas.py 6 20 400    # igual, mostrando 400 caracteres por respuesta
"""
import json
import sys
from pathlib import Path

desde, hasta = int(sys.argv[1]), int(sys.argv[2])
largo = int(sys.argv[3]) if len(sys.argv) > 3 else 250

for i in range(desde, hasta + 1):
    archivo = Path("lab/respuestas") / f"{i:03d}.json"
    if not archivo.exists():
        continue
    d = json.loads(archivo.read_text(encoding="utf-8"))
    req, resp = d["request"], d["response"]
    texto = (resp.get("answer") or "").replace("\n", " ").strip()
    print("=" * 78)
    print(f"[{i:03d}] T={req['temperature']} max={req['max_tokens']} "
          f"HTTP {d['status']} {d['segundos']}s "
          f"finish={resp.get('finish_reason')} caracteres={len(texto)}")
    print(texto[:largo] + ("..." if len(texto) > largo else "") if texto else "(respuesta vacía)")
    