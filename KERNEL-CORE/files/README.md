# KernelMind

> **Lightweight ethical AI kernel manager — PoE Ecosystem**  
> Observa. Sugere. Age apenas com consentimento humano.

[![CI](https://github.com/armazen-nft/KERNEL-MIND/actions/workflows/ci.yml/badge.svg)](https://github.com/armazen-nft/KERNEL-MIND/actions)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![PoE](https://img.shields.io/badge/PoE-Ecosystem-blueviolet.svg)](https://proofofenergy.blogspot.com)

---

## Instalação

```bash
git clone https://github.com/armazen-nft/KERNEL-MIND.git
cd KERNEL-MIND
pip install -e .
km snapshot
```

Ou via script:

```bash
bash scripts/setup.sh
```

---

## Uso — CLI

```bash
km snapshot    # estado do sistema agora
km memory      # sugestões de RAM
km storage     # sugestões de disco
km threat      # anomalias comportamentais
km watch       # monitor contínuo (Ctrl+C para parar)
km ethics      # audit log ético
km --json      # saída JSON
```

---

## Uso — API REST

```bash
km-api
# http://127.0.0.1:7771/docs
```

| Rota | Descrição |
|------|-----------|
| `GET /snapshot` | CPU, RAM, disco, processos, temperatura |
| `GET /cpu` | Métricas de CPU |
| `GET /memory` | Métricas de RAM |
| `GET /memory/suggest` | Sugestões de otimização de RAM |
| `GET /disk` | Métricas de disco |
| `GET /storage/suggest` | Sugestões de limpeza de disco |
| `GET /threat/scan` | Anomalias comportamentais |
| `GET /ethics/status` | Status do EthicsLock |
| `GET /ethics/log` | Audit log recente |
| `GET /health` | Health check |

CORS padrão: `localhost` only. Expandir via env `KERNELMIND_CORS_ORIGINS`.

---

## Uso — MCP (PoE / Claude Desktop)

```bash
km-mcp --test   # testar ferramentas
km-mcp          # servidor stdio para Claude Desktop
```

Config `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "kernelmind": {
      "command": "km-mcp"
    }
  }
}
```

Ferramentas: `kernel_snapshot`, `kernel_memory_suggest`, `kernel_storage_suggest`, `kernel_threat_scan`, `kernel_ethics_status`.

---

## Arquitetura

```
kernelmind/              ← pacote Python importável
  core/
    sensor.py            KernelSense — CPU, RAM, disco, processos
    memory.py            MemoryWeaver — análise e sugestões de RAM
    storage.py           StorageGuard — análise de disco
    threat.py            ThreatRadar — anomalias comportamentais
  ethics/
    lock.py              EthicsLock — restrições imutáveis
  api/
    server.py            FastAPI REST (porta 7771)
  cli/
    km.py                CLI com cores e barras de progresso
  mcp/
    tool.py              MCP stdio server (PoE namespace)
tests/                   pytest — sensor, ethics, API
docs/                    Documentação
config/
  defaults.toml          Configuração padrão
scripts/
  setup.sh               Instalação automatizada
```

---

## EthicsLock

Camada de código no caminho crítico — não pode ser desabilitada por configuração.

| Ação | Política |
|------|----------|
| READ / SUGGEST | Sempre permitida |
| TUNE / KILL / DELETE | Requer confirmação humana |
| NETWORK | Permanentemente bloqueada |

Toda decisão é registrada em audit log JSONL com fingerprint SHA-256.

---

## Testes

```bash
pytest tests/ -v
```

---

## Ecossistema PoE

Parte da infraestrutura do [Proof of Energy](https://proofofenergy.blogspot.com).  
Namespace MCP: `io.github.armazen-nft/kernelmind`

> *"A informação nunca se perde — apenas se recodifica."*

---

## Licença

[AGPL-3.0](LICENSE) + Cláusula Ética PoE: nenhuma derivação pode remover ou enfraquecer o EthicsLock.
