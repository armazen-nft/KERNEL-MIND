# KernelMind

> IA leve e ética para observação de kernel em notebooks e computadores.
> Observa. Sugere. Não executa ações destrutivas sem consentimento humano.

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Kernel: Linux 4.15+](https://img.shields.io/badge/Kernel-Linux%204.15%2B-orange.svg)](https://kernel.org)
[![Ethics: Active](https://img.shields.io/badge/EthicsLock-active-brightgreen.svg)](docs/ethics.md)
[![PoE Ecosystem](https://img.shields.io/badge/PoE-Ecosystem-blueviolet.svg)](https://proofofenergy.blogspot.com)

---

## O que é

KernelMind é um pacote Python para monitoramento e sugestão de otimização de sistema operacional. Ele lê métricas reais via `psutil`, `/proc` e interfaces do kernel, analisa padrões de CPU, RAM, disco e processos, e devolve sugestões auditáveis.

A regra de segurança do projeto é simples: os módulos oficiais podem **ler** e **sugerir** automaticamente, mas ações como ajuste de kernel, encerramento de processo, exclusão de arquivo/cache ou transmissão de dados exigem o fluxo do `EthicsLock`.

> Nota de escopo: o `EthicsLock` protege o fluxo oficial do KernelMind. Como todo software livre, forks ou alterações no código devem ser auditados por testes, revisão e hashes de release.

---

## Estrutura canônica

```text
kernelmind/
├── core/
│   ├── sensor.py        # KernelSense — leitura de métricas reais
│   ├── memory.py        # MemoryWeaver — análise/sugestões de RAM
│   ├── storage.py       # StorageGuard — análise/sugestões de disco
│   └── threat.py        # ThreatRadar — detecção de anomalias
├── ethics/
│   └── lock.py          # EthicsLock — política e auditoria
├── api/
│   └── server.py        # FastAPI REST — porta padrão 7771
├── cli/
│   └── km.py            # Interface de linha de comando
└── mcp/
    └── tool.py          # Servidor MCP stdio

tests/                   # Testes automatizados
config/defaults.toml     # Configuração padrão documentada
docs/                    # Documentação complementar
scripts/setup.sh         # Instalação local em modo editável
```

Diretórios e artefatos de staging/release não fazem parte da fonte de verdade. A implementação oficial fica no pacote `kernelmind`.

---

## Instalação rápida

### Desenvolvimento local

```bash
git clone https://github.com/armazen-nft/KERNEL-MIND.git
cd KERNEL-MIND
python -m pip install -e .[dev]
```

### Script auxiliar

```bash
bash scripts/setup.sh
```

### Via pip

```bash
pip install kernelmind
```

---

## Uso — CLI

```bash
km snapshot      # estado do sistema agora
km memory        # sugestões de otimização de RAM
km storage       # sugestões de otimização de disco
km threat        # scan de anomalias comportamentais
km watch         # monitor contínuo (Ctrl+C para parar)
km ethics        # status do EthicsLock e audit log da sessão
km --json        # snapshot JSON para integração
km --help        # ajuda completa
```

Também é possível executar sem instalar os entry points:

```bash
python -m kernelmind.cli.km --help
```

---

## Uso — API REST

```bash
km-api
# Acesse: http://localhost:7771/docs
```

Ou:

```bash
python -m kernelmind.api.server
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
| GET | `/ethics/log` | Audit log recente da sessão |
| GET | `/health` | Health check |

Por segurança, exponha a API apenas em redes confiáveis. Snapshots podem conter nomes de processos e métricas sensíveis do host.

---

## Princípios Éticos (EthicsLock)

| Ação | Política nos módulos oficiais |
|------|-------------------------------|
| Leitura de métricas | Sempre permitida |
| Sugestões ao usuário | Sempre permitidas |
| Ajuste de parâmetro kernel | Requer confirmação |
| Encerrar processo | Requer confirmação |
| Excluir arquivo/cache | Requer confirmação explícita |
| Operações de rede | Bloqueadas por padrão |

Toda avaliação é registrada em audit log JSONL com fingerprint SHA-256 e encadeamento simples por hash anterior. Veja [docs/ethics.md](docs/ethics.md).

---

## Integração PoE / MCP

KernelMind expõe ferramentas MCP sob o namespace `io.github.armazen-nft/kernelmind`:

- `kernel_snapshot` — estado completo do sistema
- `kernel_memory_suggest` — sugestões de RAM
- `kernel_storage_suggest` — sugestões de disco
- `kernel_threat_scan` — scan de anomalias comportamentais
- `kernel_ethics_status` — auditoria ética

Teste local:

```bash
km-mcp --test
python -m kernelmind.mcp.tool --tool kernel_snapshot
```

Ver [docs/mcp-integration.md](docs/mcp-integration.md) para configuração em clientes MCP.

---

## Qualidade e testes

```bash
python -m pytest
python -m ruff check kernelmind tests
python -m compileall kernelmind
```

O CI oficial usa a matriz Python 3.10, 3.11 e 3.12.

---

## Ecossistema PoE

KernelMind é parte da infraestrutura do [Proof of Energy](https://proofofenergy.blogspot.com) — ecossistema de coparticipação humano-IA desenvolvido por Daniel Estefani com Melissa Solari e coparticipantes Claude, GPT, DeepSeek, Qwen, Grok e Daizen.

> "A informação nunca se perde — apenas se recodi(fica)."

---

## Licença

[AGPL-3.0 com cláusula ética PoE](LICENSE) — código aberto; modificações e uso em rede devem respeitar os termos da licença.
