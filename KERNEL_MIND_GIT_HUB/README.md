# KernelMind

> IA leve e ética para gestão de kernel em notebooks e computadores.  
> Observa. Sugere. Age apenas com consentimento humano.

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Kernel: Linux 4.15+](https://img.shields.io/badge/Kernel-Linux%204.15%2B-orange.svg)]()
[![Ethics: Active](https://img.shields.io/badge/EthicsLock-active-brightgreen.svg)]()
[![PoE Ecosystem](https://img.shields.io/badge/PoE-Ecosystem-blueviolet.svg)](https://proofofenergy.blogspot.com)

---

## O que é

KernelMind é um daemon de monitoramento e otimização de sistema operacional governado por uma camada ética imutável (EthicsLock). Ele lê métricas reais do kernel via `/proc`, `/sys` e `psutil`, analisa padrões, e propõe ações — mas **nunca age sem confirmação humana explícita**.

Faz parte do ecossistema **Proof of Energy (PoE)** e é compatível com o protocolo MCP (Model Context Protocol) da Anthropic para integração com IAs.

---

## Arquitetura

```
kernelmind/
├── core/
│   ├── sensor.py        # KernelSense — leitura real de métricas
│   └── memory.py        # MemoryWeaver — análise e sugestões de RAM
├── ethics/
│   └── lock.py          # EthicsLock — restrições imutáveis
├── api/
│   └── server.py        # FastAPI REST — porta 7771
├── cli/
│   └── km.py            # Interface de linha de comando
├── mcp/
│   └── tool.py          # Integração MCP (PoE namespace)
├── tests/               # Testes automatizados
├── docs/                # Documentação detalhada
├── config/
│   └── defaults.toml    # Configuração padrão
└── scripts/
    └── setup.sh         # Instalação para sistemas Unix
```

---

## Instalação rápida

### Linux / macOS

```bash
git clone https://github.com/armazen-nft/kernelmind.git
cd kernelmind
python3 install.py
```

### Via pip (quando publicado)

```bash
pip install kernelmind
```

---

## Uso — CLI

```bash
km snapshot      # estado do sistema agora
km memory        # sugestões de otimização de RAM
km watch         # monitor contínuo (Ctrl+C para parar)
km ethics        # status do EthicsLock e audit log
km --json        # saída JSON para integração
km --help        # ajuda completa
```

---

## Uso — API REST

```bash
python3 api/server.py
# Acesse: http://localhost:7771/docs
```

Endpoints principais:

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/snapshot` | Snapshot completo do sistema |
| GET | `/cpu` | Métricas de CPU |
| GET | `/memory` | Métricas de RAM |
| GET | `/memory/suggest` | Sugestões de otimização |
| GET | `/disk` | Métricas de disco |
| GET | `/ethics/status` | Status do EthicsLock |
| GET | `/ethics/log` | Audit log recente |
| GET | `/health` | Health check |

---

## Princípios Éticos (EthicsLock)

O EthicsLock é uma camada de código — não uma configuração. Não pode ser desabilitado.

| Ação | Política |
|------|----------|
| Leitura de métricas | Sempre permitida |
| Sugestões ao usuário | Sempre permitidas |
| Ajuste de parâmetro kernel | Requer confirmação |
| Encerrar processo | Requer confirmação |
| Excluir arquivo/cache | Requer confirmação explícita |
| Operações de rede | Bloqueadas por padrão |

Toda decisão é registrada em audit log JSONL com fingerprint SHA-256.

---

## Integração PoE / MCP

KernelMind expõe ferramentas MCP sob o namespace `io.github.armazen-nft/kernelmind`:

- `kernel_snapshot` — estado completo do sistema
- `kernel_memory_suggest` — sugestões de RAM
- `kernel_ethics_status` — auditoria ética

Ver [docs/mcp-integration.md](docs/mcp-integration.md) para detalhes.

---

## Ecossistema PoE

KernelMind é parte da infraestrutura do [Proof of Energy](https://proofofenergy.blogspot.com) — ecossistema de coparticipação humano-IA desenvolvido por Daniel Estefani com Melissa Solari e coparticipantes Claude, GPT, DeepSeek, Qwen, Grok e Daizen.

> "A informação nunca se perde — apenas se recodi(fica)."

---

## Licença

[AGPL-3.0](LICENSE) — código aberto, modificações devem ser compartilhadas.
