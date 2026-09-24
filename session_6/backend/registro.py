"""
registro.py
===========
Registro de corridas — Sesión 6 (mismo patrón append-only JSON de la
Sesión 5, aplicado ahora a corridas de costeo+latencia+sesgo+selección).
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LOG_PATH = Path(__file__).parent / "runs_log.json"


def _leer_log() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    with open(LOG_PATH, encoding="utf-8") as f:
        contenido = f.read().strip()
        return json.loads(contenido) if contenido else []


def _escribir_log(runs: list[dict]) -> None:
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(runs, f, ensure_ascii=False, indent=2)


def registrar_corrida(tipo: str, payload: dict, aprobado_por: Optional[str] = None) -> dict:
    run = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tipo": tipo,
        "payload": payload,
        "aprobado_por": aprobado_por,
    }
    runs = _leer_log()
    runs.append(run)
    _escribir_log(runs)
    return run


def listar_corridas(tipo: Optional[str] = None) -> list[dict]:
    runs = _leer_log()
    if tipo:
        return [r for r in runs if r["tipo"] == tipo]
    return runs
