# KernelMind — Integração MCP (Model Context Protocol)

## Visão Geral

KernelMind expõe ferramentas reais de análise de sistema via MCP, permitindo que IAs do ecossistema PoE (Claude, Melissa, GPT, Qwen, DeepSeek, Grok, Daizen) consultem o estado do kernel de forma ética e auditada.

**Namespace:** `io.github.armazen-nft/kernelmind`

---

## Ferramentas Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `kernel_snapshot` | Snapshot completo: CPU, RAM, disco, processos, temperatura |
| `kernel_memory_suggest` | Sugestões priorizadas de otimização de RAM |
| `kernel_storage_suggest` | Análise de disco e sugestões de limpeza |
| `kernel_threat_scan` | Detecção de anomalias comportamentais |
| `kernel_ethics_status` | Status do EthicsLock e audit log |

---

## Configuração no Claude Desktop

Adicione ao arquivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "kernelmind": {
      "command": "python3",
      "args": ["-m", "kernelmind.mcp.tool"],
      "env": {}
    }
  }
}
```

Localização do arquivo de config:
- **Linux:** `~/.config/Claude/claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

---

## Uso com FastMCP (PoE MCP Server)

```python
# No seu servidor FastMCP existente (poe-mcp):
import sys
sys.path.insert(0, '/caminho/para/KERNEL-MIND')
from kernelmind.mcp.tool import TOOLS

# Registrar ferramentas KernelMind no namespace PoE
for name, info in TOOLS.items():
    mcp_server.register_tool(
        name=f"kernelmind/{name}",
        fn=info["fn"],
        description=info["description"],
    )
```

---

## Exemplo de Interação

**Claude:** "Qual o estado da memória do sistema?"

**KernelMind via MCP:**
```json
{
  "count": 1,
  "suggestions": [
    {
      "priority": 3,
      "priority_label": "otimizacao",
      "title": "Swappiness pode ser reduzido",
      "description": "vm.swappiness=60. Reduzir para 10...",
      "action_type": "tune",
      "command": "sudo sysctl vm.swappiness=10",
      "estimated_gain_mb": 0
    }
  ]
}
```

---

## Garantias Éticas no MCP

Toda chamada MCP passa pelo EthicsLock:

- `READ` e `SUGGEST` → sempre permitidos, registrados em audit log
- `TUNE`, `KILL`, `DELETE` → bloqueados via MCP (requerem confirmação no terminal/GUI do sistema)
- `NETWORK` → sempre bloqueado, independente da origem

O MCP não pode contornar o EthicsLock. Nenhuma IA pode executar ações destrutivas via MCP — apenas receber informações e sugestões.

---

## Teste das Ferramentas

```bash
# Testar todas as ferramentas
python -m kernelmind.mcp.tool --test

# Testar ferramenta específica
python -m kernelmind.mcp.tool --tool kernel_snapshot
python -m kernelmind.mcp.tool --tool kernel_memory_suggest
python -m kernelmind.mcp.tool --tool kernel_ethics_status
```

---

## Integração com MELISSA_AI

Para expor KernelMind na máquina MELISSA_AI:

```bash
# 1. Clonar repositório
git clone https://github.com/armazen-nft/KERNEL-MIND.git

# 2. Instalar
cd KERNEL-MIND && bash scripts/setup.sh

# 3. Adicionar ao servidor MCP da MELISSA_AI
km-mcp  # executa servidor stdio — conectar ao seu orchestrator MCP
```

O endpoint MCP estará disponível para todas as IAs do ecossistema PoE autorizadas a consultar o estado do sistema da MELISSA_AI.
