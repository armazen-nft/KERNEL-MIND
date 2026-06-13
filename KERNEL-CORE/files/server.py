"""KernelMind :: API REST — FastAPI porta 7771."""
from __future__ import annotations

import os
import time
from dataclasses import asdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from kernelmind.core.sensor import KernelSense
from kernelmind.core.memory import MemoryWeaver
from kernelmind.core.storage import StorageGuard
from kernelmind.core.threat import ThreatRadar
from kernelmind.ethics.lock import EthicsLock, ActionType

# ── CORS seguro: configurável por env var ──
_cors_env = os.environ.get("KERNELMIND_CORS_ORIGINS", "")
CORS_ORIGINS = (
    [o.strip() for o in _cors_env.split(",") if o.strip()]
    if _cors_env
    else ["http://localhost:7771", "http://127.0.0.1:7771", "http://localhost:3000"]
)

app = FastAPI(
    title="KernelMind API",
    description="IA leve e ética para gestão de kernel — dados reais, ética embutida.",
    version="0.9.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)

_sensor  = KernelSense()
_memory  = MemoryWeaver()
_storage = StorageGuard()
_threat  = ThreatRadar()
_ethics  = EthicsLock()


@app.get("/")
def root():
    return {"name": "KernelMind", "version": "0.9.1", "status": "online",
            "ethics": _ethics.status(),
            "endpoints": ["/snapshot", "/cpu", "/memory", "/memory/suggest",
                          "/disk", "/storage/suggest", "/threat/scan",
                          "/ethics/status", "/ethics/log", "/health"]}


@app.get("/snapshot")
def snapshot():
    v = _ethics.evaluate(ActionType.READ, "snapshot completo")
    if not v.allowed:
        return JSONResponse(status_code=403, content={"error": v.reason})
    snap = _sensor.snapshot()
    return asdict(snap)


@app.get("/cpu")
def cpu():
    _ethics.evaluate(ActionType.READ, "leitura CPU")
    return asdict(_sensor.cpu())


@app.get("/memory")
def memory():
    _ethics.evaluate(ActionType.READ, "leitura RAM")
    return asdict(_sensor.memory())


@app.get("/memory/suggest")
def memory_suggest():
    _ethics.evaluate(ActionType.SUGGEST, "sugestões de RAM")
    return {"suggestions": [vars(s) for s in _memory.analyze()]}


@app.get("/disk")
def disk():
    _ethics.evaluate(ActionType.READ, "leitura disco")
    return asdict(_sensor.disk())


@app.get("/storage/suggest")
def storage_suggest():
    _ethics.evaluate(ActionType.SUGGEST, "sugestões de disco")
    return {"suggestions": [vars(s) for s in _storage.analyze()]}


@app.get("/threat/scan")
def threat_scan():
    _ethics.evaluate(ActionType.READ, "scan de anomalias")
    anomalies = _threat.scan()
    return {"clean": len(anomalies) == 0, "count": len(anomalies),
            "anomalies": [vars(a) for a in anomalies]}


@app.get("/ethics/status")
def ethics_status():
    return _ethics.status()


@app.get("/ethics/log")
def ethics_log():
    return {"entries": _ethics.recent_log(50)}


@app.get("/health")
def health():
    return {"status": "ok", "ts": time.time(), "ethics_lock": "active"}


if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("KERNELMIND_HOST", "127.0.0.1")
    port = int(os.environ.get("KERNELMIND_PORT", "7771"))
    print(f"KernelMind API → http://{host}:{port}")
    print(f"Docs           → http://{host}:{port}/docs")
    uvicorn.run(app, host=host, port=port, log_level="warning")
