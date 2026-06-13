"""
KernelMind :: MCP Server
Namespace: io.github.armazen-nft/kernelmind
Compatível com Claude Desktop e qualquer cliente MCP stdio.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from kernelmind.core.sensor import KernelSense
from kernelmind.core.memory import MemoryWeaver
from kernelmind.core.storage import StorageGuard
from kernelmind.core.threat import ThreatRadar
from kernelmind.ethics.lock import EthicsLock, ActionType

_sensor  = KernelSense()
_memory  = MemoryWeaver()
_storage = StorageGuard()
_threat  = ThreatRadar()
_ethics  = EthicsLock()


def kernel_snapshot(_: dict) -> dict:
    v = _ethics.evaluate(ActionType.READ, "kernel_snapshot via MCP")
    if not v.allowed:
        return {"error": v.reason}
    return asdict(_sensor.snapshot())


def kernel_memory_suggest(_: dict) -> dict:
    _ethics.evaluate(ActionType.SUGGEST, "memory_suggest via MCP")
    return {"suggestions": [vars(s) for s in _memory.analyze()]}


def kernel_storage_suggest(_: dict) -> dict:
    _ethics.evaluate(ActionType.SUGGEST, "storage_suggest via MCP")
    return {"suggestions": [vars(s) for s in _storage.analyze()]}


def kernel_threat_scan(_: dict) -> dict:
    _ethics.evaluate(ActionType.READ, "threat_scan via MCP")
    anomalies = _threat.scan()
    return {"clean": len(anomalies) == 0, "count": len(anomalies),
            "anomalies": [vars(a) for a in anomalies]}


def kernel_ethics_status(_: dict) -> dict:
    return {"status": _ethics.status(), "recent_log": _ethics.recent_log(20)}


TOOLS: dict[str, dict] = {
    "kernel_snapshot": {
        "fn": kernel_snapshot,
        "description": "Snapshot completo: CPU, RAM, disco, processos, temperatura.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "kernel_memory_suggest": {
        "fn": kernel_memory_suggest,
        "description": "Sugestões priorizadas de otimização de RAM.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "kernel_storage_suggest": {
        "fn": kernel_storage_suggest,
        "description": "Análise de disco e sugestões de limpeza segura.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "kernel_threat_scan": {
        "fn": kernel_threat_scan,
        "description": "Detecta anomalias comportamentais no sistema.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "kernel_ethics_status": {
        "fn": kernel_ethics_status,
        "description": "Status do EthicsLock e audit log recente.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
}


def _send(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def _handle(req: dict) -> dict:
    method = req.get("method", "")
    rid = req.get("id")

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "kernelmind", "version": "0.9.1",
                           "namespace": "io.github.armazen-nft/kernelmind"},
        }}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": [
            {"name": n, "description": t["description"], "inputSchema": t["inputSchema"]}
            for n, t in TOOLS.items()
        ]}}

    if method == "tools/call":
        name = req.get("params", {}).get("name", "")
        args = req.get("params", {}).get("arguments", {})
        if name not in TOOLS:
            return {"jsonrpc": "2.0", "id": rid,
                    "error": {"code": -32601, "message": f"Tool '{name}' not found"}}
        try:
            result = TOOLS[name]["fn"](args)
            return {"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]
            }}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": rid,
                    "error": {"code": -32603, "message": str(e)}}

    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": -32601, "message": f"Method '{method}' not found"}}


def stdio_server() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            _send(_handle(json.loads(line)))
        except json.JSONDecodeError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="KernelMind MCP Server")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--tool", default="")
    args = parser.parse_args()

    if args.test or args.tool:
        names = [args.tool] if args.tool else list(TOOLS.keys())
        for name in names:
            if name not in TOOLS:
                print(f"Ferramenta '{name}' não encontrada.")
                continue
            print(f"\n── {name} ──")
            print(json.dumps(TOOLS[name]["fn"]({}), indent=2, default=str))
    else:
        stdio_server()


if __name__ == "__main__":
    main()
