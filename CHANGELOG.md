# Changelog

## [0.9.1] — 2026-06-11

### Adicionado
- `KernelSense` — leitura real de CPU, RAM, disco, temperatura, processos via psutil + /proc
- `MemoryWeaver` — análise de swappiness, page cache, OOM scores, sugestões priorizadas
- `StorageGuard` — análise de uso de disco, arquivos grandes, caches de pacotes
- `ThreatRadar` — detecção de escalada de privilégio, I/O anômalo, zumbis, fd leaks, deleted files
- `EthicsLock` — camada ética imutável com audit log SHA-256
- API REST FastAPI (porta 7771) com 8 endpoints
- CLI `km` com snapshot, memory, watch, ethics
- Servidor MCP stdio compatível com Claude Desktop e FastMCP
- 5 ferramentas MCP: kernel_snapshot, kernel_memory_suggest, kernel_storage_suggest, kernel_threat_scan, kernel_ethics_status
- Testes automatizados (pytest) para EthicsLock, API, CLI e MCP
- GitHub Actions: CI (Python 3.10/3.11/3.12), release automation
- Script de instalação `scripts/setup.sh` para Linux/macOS
- Configuração `config/defaults.toml`
- Documentação: MCP integration, EthicsLock

### Fundamentos PoE
- Namespace MCP: `io.github.armazen-nft/kernelmind`
- EthicsLock integrado com cláusula adicional AGPL para proteção da camada ética
- Pronto para integração com MELISSA_AI e ecossistema PoE

---

## [Próximas versões]

### [0.9.2] — Planejado
- `DialogKernel` — LLM local quantizado (GGUF/llama.cpp) para consultas em linguagem natural
- Modo daemon com systemd unit
- Compressão zram via MemoryWeaver (ação com confirmação)
- Windows: suporte via wmi/psutil

### [1.0.0] — Planejado
- Integração formal com SBL (Semantic Bridge Layer) do PoE
- qualyas_meter para métricas semânticas de carga computacional
- Suporte multi-máquina (MELISSA_AI como hub)
