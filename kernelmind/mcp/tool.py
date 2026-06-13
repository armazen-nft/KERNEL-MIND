"""
KernelMind :: MCP Tool
Integração com o Model Context Protocol da Anthropic.
Namespace: io.github.armazen-nft/kernelmind

Expõe as ferramentas KernelMind para uso por IAs (Claude, Melissa, etc.)
dentro do ecossistema PoE.

Para usar com FastMCP:
    python3 mcp/tool.py

Para usar com servidor MCP existente, importe McpKernelMind e registre.
"""

import json
import time
from dataclasses import asdict

from kernelmind.core.sensor import KernelSense
from kernelmind.core.memory import MemoryWeaver
from kernelmind.core.storage import StorageGuard
from kernelmind.core.threat import ThreatRadar
from kernelmind.ethics.lock import EthicsLock, ActionType

# ── Instâncias singleton ──
_sensor  = KernelSense()
_memory  = MemoryWeaver()
_storage = StorageGuard()
_threat  = ThreatRadar()
_ethics  = EthicsLock()


# ── Tool handlers ──

def kernel_snapshot(args: dict = None) -> dict:
    """Retorna snapshot completo do sistema: CPU, RAM, disco, processos."""
    verdict = _ethics.evaluate(ActionType.READ, "kernel_snapshot via MCP")
    if not verdict.allowed:
        return {"error": verdict.reason}
    snap = _sensor.snapshot()
    return {
        "timestamp": snap.timestamp,
        "kernel_version": snap.kernel_version,
        "uptime_hours": snap.uptime_hours,
        "cpu": asdict(snap.cpu),
        "memory": asdict(snap.memory),
        "disks": snap.disks,
        "top_processes": snap.top_processes[:5],
        "temperature_c": snap.temperature_c,
    }


def kernel_memory_suggest(args: dict = None) -> dict:
    """Analisa RAM e retorna sugestões de otimização priorizadas."""
    verdict = _ethics.evaluate(ActionType.SUGGEST, "memory_suggest via MCP")
    if not verdict.allowed:
        return {"error": verdict.reason}
    suggestions = _memory.analyze()
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


def kernel_storage_suggest(args: dict = None) -> dict:
    """Analisa disco e retorna sugestões de limpeza."""
    verdict = _ethics.evaluate(ActionType.SUGGEST, "storage_suggest via MCP")
    if not verdict.allowed:
        return {"error": verdict.reason}
    suggestions = _storage.analyze()
    return {
        "count": len(suggestions),
        "suggestions": [
            {
                "priority": s.priority,
                "title": s.title,
                "description": s.description,
                "command": s.command,
                "estimated_gain_mb": s.estimated_gain_mb,
            }
            for s in suggestions
        ],
    }


def kernel_threat_scan(args: dict = None) -> dict:
    """Escaneia anomalias comportamentais do sistema."""
    verdict = _ethics.evaluate(ActionType.READ, "threat_scan via MCP")
    if not verdict.allowed:
        return {"error": verdict.reason}
    anomalies = _threat.scan()
    return {
        "count": len(anomalies),
        "clean": len(anomalies) == 0,
        "anomalies": [
            {
                "severity": a.severity,
                "category": a.category,
                "description": a.description,
                "pid": a.pid,
                "process_name": a.process_name,
                "recommendation": a.recommendation,
            }
            for a in anomalies
        ],
    }


def kernel_ethics_status(args: dict = None) -> dict:
    """Retorna status completo do EthicsLock e audit log recente."""
    return {
        "status": _ethics.status(),
        "recent_log": _ethics.recent_log(20),
    }


# ── MCP Tool Registry ──

TOOLS = {
    "kernel_snapshot": {
        "fn": kernel_snapshot,
        "description": "Retorna snapshot completo do sistema: CPU, RAM, disco, processos, temperatura.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "kernel_memory_suggest": {
        "fn": kernel_memory_suggest,
        "description": "Analisa memória RAM e retorna sugestões de otimização priorizadas.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "kernel_storage_suggest": {
        "fn": kernel_storage_suggest,
        "description": "Analisa uso de disco e sugere limpezas seguras.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "kernel_threat_scan": {
        "fn": kernel_threat_scan,
        "description": "Escaneia o sistema em busca de anomalias comportamentais.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "kernel_ethics_status": {
        "fn": kernel_ethics_status,
        "description": "Retorna status do EthicsLock e audit log das últimas ações.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
}


# ── Stdio MCP server (sem dependência externa) ──

def stdio_server():
    """
    Servidor MCP mínimo via stdio.
    Compatível com Claude Desktop e qualquer cliente MCP padrão.
    """
    import sys

    def send(obj: dict):
        line = json.dumps(obj)
        sys.stdout.write(line + "\n")
        sys.stdout.flush()

    def handle(req: dict) -> dict:
        method = req.get("method", "")
        req_id = req.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0", "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "kernelmind",
                        "version": "0.9.1",
                        "namespace": "io.github.armazen-nft/kernelmind",
                    },
                },
            }

        if method == "tools/list":
            tools_list = [
                {
                    "name": name,
                    "description": info["description"],
                    "inputSchema": info["inputSchema"],
                }
                for name, info in TOOLS.items()
            ]
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}}

        if method == "tools/call":
            tool_name = req.get("params", {}).get("name", "")
            tool_args = req.get("params", {}).get("arguments", {})
            if tool_name not in TOOLS:
                return {
                    "jsonrpc": "2.0", "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"},
                }
            try:
                result = TOOLS[tool_name]["fn"](tool_args)
                return {
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                    },
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0", "id": req_id,
                    "error": {"code": -32603, "message": str(e)},
                }

        return {
            "jsonrpc": "2.0", "id": req_id,
            "error": {"code": -32601, "message": f"Method '{method}' not found"},
        }

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle(req)
            send(resp)
        except json.JSONDecodeError:
            pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description="KernelMind MCP Server")
    parser.add_argument("--test", action="store_true", help="Testar todas as ferramentas")
    parser.add_argument("--tool", help="Testar ferramenta específica")
    args = parser.parse_args()

    if args.test or args.tool:
        tools_to_test = [args.tool] if args.tool else list(TOOLS.keys())
        for name in tools_to_test:
            if name not in TOOLS:
                print(f"Ferramenta '{name}' não encontrada.")
                continue
            print(f"\n── {name} ──")
            result = TOOLS[name]["fn"]({})
            print(json.dumps(result, indent=2, default=str))
    else:
        # Modo servidor MCP via stdio
        stdio_server()


if __name__ == "__main__":
    main()
