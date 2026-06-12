#!/usr/bin/env bash
# KernelMind — Setup Script
# Compatível com Linux (Debian/Ubuntu/Arch/Fedora) e macOS
set -euo pipefail

RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[0;33m'
CYN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="$HOME/.local/bin"
PYTHON="python3"

echo -e "\n${BOLD}${CYN}KernelMind — Instalação${NC}\n"

# ── Verificar Python ──
if ! command -v "$PYTHON" &>/dev/null; then
    echo -e "${RED}✗ Python 3 não encontrado. Instale Python 3.10+${NC}"
    exit 1
fi

PY_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$("$PYTHON" -c "import sys; print(sys.version_info.major)")
PY_MINOR=$("$PYTHON" -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
    echo -e "${RED}✗ Python $PY_VERSION encontrado, mas é necessário 3.10+${NC}"
    exit 1
fi
echo -e "${GRN}✓ Python $PY_VERSION${NC}"

# ── Verificar kernel (Linux) ──
if [ "$(uname -s)" = "Linux" ]; then
    KERNEL=$(uname -r | cut -d. -f1,2)
    echo -e "${GRN}✓ Kernel Linux $KERNEL${NC}"
fi

# ── Instalar dependências ──
echo -e "\n${YLW}Instalando dependências Python...${NC}"
DEPS=(psutil fastapi "uvicorn[standard]")
for dep in "${DEPS[@]}"; do
    if "$PYTHON" -m pip install "$dep" --break-system-packages -q 2>/dev/null || \
       "$PYTHON" -m pip install "$dep" --user -q 2>/dev/null; then
        echo -e "${GRN}✓ $dep${NC}"
    else
        echo -e "${RED}✗ Falha ao instalar $dep${NC}"
        exit 1
    fi
done

# ── Criar atalho km ──
mkdir -p "$BIN_DIR"
KM_SCRIPT="$BIN_DIR/km"
cat > "$KM_SCRIPT" << EOF
#!/usr/bin/env bash
exec $PYTHON "$REPO_DIR/cli/km.py" "\$@"
EOF
chmod +x "$KM_SCRIPT"
echo -e "${GRN}✓ Atalho km criado: $KM_SCRIPT${NC}"

# ── Criar atalho para servidor API ──
KM_API_SCRIPT="$BIN_DIR/km-api"
cat > "$KM_API_SCRIPT" << EOF
#!/usr/bin/env bash
exec $PYTHON "$REPO_DIR/api/server.py" "\$@"
EOF
chmod +x "$KM_API_SCRIPT"
echo -e "${GRN}✓ Atalho km-api criado: $KM_API_SCRIPT${NC}"

# ── Criar atalho para servidor MCP ──
KM_MCP_SCRIPT="$BIN_DIR/km-mcp"
cat > "$KM_MCP_SCRIPT" << EOF
#!/usr/bin/env bash
exec $PYTHON "$REPO_DIR/mcp/tool.py" "\$@"
EOF
chmod +x "$KM_MCP_SCRIPT"
echo -e "${GRN}✓ Atalho km-mcp criado: $KM_MCP_SCRIPT${NC}"

# ── Verificar PATH ──
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "\n${YLW}⚠ $BIN_DIR não está no PATH.${NC}"
    echo -e "Adicione ao seu ~/.bashrc ou ~/.zshrc:"
    echo -e "${CYN}  export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
fi

# ── Teste rápido ──
echo -e "\n${YLW}Verificando instalação...${NC}"
if "$PYTHON" "$REPO_DIR/cli/km.py" --json 2>/dev/null | "$PYTHON" -c "import sys,json; d=json.load(sys.stdin); print(f'✓ Kernel: {d[\"kernel_version\"]}')" 2>/dev/null; then
    echo -e "${GRN}✓ KernelMind funcionando${NC}"
else
    echo -e "${YLW}⚠ Teste rápido falhou — verifique manualmente com: python3 cli/km.py snapshot${NC}"
fi

echo -e "\n${BOLD}${GRN}KernelMind instalado com sucesso!${NC}\n"
echo -e "Comandos disponíveis:"
echo -e "  ${CYN}km snapshot${NC}     — estado do sistema agora"
echo -e "  ${CYN}km memory${NC}       — sugestões de RAM"
echo -e "  ${CYN}km watch${NC}        — monitor contínuo"
echo -e "  ${CYN}km ethics${NC}       — audit log ético"
echo -e "  ${CYN}km-api${NC}          — iniciar API REST (porta 7771)"
echo -e "  ${CYN}km-mcp --test${NC}   — testar ferramentas MCP"
echo ""
