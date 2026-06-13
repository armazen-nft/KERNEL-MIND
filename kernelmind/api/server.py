"""
KernelMind :: API Server
FastAPI — expõe métricas reais do kernel via HTTP/JSON
Porta padrão: 7771
"""

import time
from dataclasses import asdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from kernelmind.core.memory import MemoryWeaver
from kernelmind.core.sensor import KernelSense
from kernelmind.ethics.lock import ActionType, EthicsLock

app = FastAPI(
    title="KernelMind API",
    description="IA leve de gestão de kernel — dados reais, ética embutida",
    version="0.9.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringir em produção
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Instâncias globais
sensor = KernelSense()
weaver = MemoryWeaver()
ethics = EthicsLock()  # modo somente-leitura: sem confirmation_fn


@app.get("/")
def root():
    return {
        "name": "KernelMind",
        "version": "0.9.1",
        "status": "online",
        "ethics": ethics.status(),
        "endpoints": ["/snapshot", "/memory/suggest", "/ethics/log", "/health"],
    }


@app.get("/snapshot")
def snapshot():
    """Snapshot completo do sistema — CPU, RAM, disco, processos."""
    verdict = ethics.evaluate(ActionType.READ, "snapshot completo do sistema")
    if not verdict.allowed:
        return JSONResponse(status_code=403, content={"error": verdict.reason})

    snap = sensor.snapshot()
    return {
        "timestamp": snap.timestamp,
        "os": snap.os_name,
        "kernel": snap.kernel_version,
        "uptime_hours": snap.uptime_hours,
        "cpu": asdict(snap.cpu),
        "memory": asdict(snap.memory),
        "disks": snap.disks,
        "top_processes": snap.top_processes,
        "temperature_c": snap.temperature_c,
    }


@app.get("/cpu")
def cpu():
    ethics.evaluate(ActionType.READ, "leitura de CPU")
    m = sensor.cpu()
    return asdict(m)


@app.get("/memory")
def memory():
    ethics.evaluate(ActionType.READ, "leitura de memória")
    m = sensor.memory()
    return asdict(m)


@app.get("/memory/suggest")
def memory_suggest():
    """Sugestões concretas de otimização de RAM — sem executar nada."""
    ethics.evaluate(ActionType.SUGGEST, "análise de memória para sugestões")
    suggestions = weaver.analyze()
    return {
        "count": len(suggestions),
        "suggestions": [
            {
                "priority": s.priority,
                "priority_label": {1: "critico", 2: "importante", 3: "otimizacao"}.get(s.priority),
                "title": s.title,
                "description": s.description,
                "action_type": s.action_type,
                "command": s.command,
                "estimated_gain_mb": s.estimated_gain_mb,
            }
            for s in suggestions
        ],
    }


@app.get("/disk")
def disk():
    ethics.evaluate(ActionType.READ, "leitura de disco")
    m = sensor.disk()
    return asdict(m)


@app.get("/ethics/status")
def ethics_status():
    return ethics.status()


@app.get("/ethics/log")
def ethics_log():
    return {"entries": ethics.recent_log(50)}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "ts": time.time(),
        "ethics_lock": "active",
    }


def main():
    import uvicorn

    print("KernelMind API iniciando em http://localhost:7771")
    print("Documentação: http://localhost:7771/docs")
    uvicorn.run(app, host="0.0.0.0", port=7771, log_level="warning")


if __name__ == "__main__":
    main()
