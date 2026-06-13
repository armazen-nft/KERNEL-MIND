#!/usr/bin/env bash
# KernelMind — setup.sh
# Instala o pacote Python em modo editável e verifica a instalação.
set -euo pipefail

G="\033[92m"; Y="\033[93m"; RE="\033[91m"; CYN="\033[96m"; NC="\033[0m"; BD="\033[1m"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "\n${BD}${CYN}KernelMind — Instalação${NC}\n"

# Python 3.10+
PY=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
if [ "$MAJOR" -lt 3 ] || [ "$MINOR" -lt 10 ]; then
  echo -e "${RE}✗ Python $PY encontrado — necessário 3.10+${NC}"; exit 1
fi
echo -e "${G}✓ Python $PY${NC}"

# Instalar pacote
echo -e "${Y}Instalando kernelmind...${NC}"
pip install -e "$REPO" --quiet
echo -e "${G}✓ kernelmind instalado${NC}"

# Verificar entry points
for cmd in km km-api km-mcp; do
  if command -v "$cmd" &>/dev/null; then
    echo -e "${G}✓ $cmd disponível${NC}"
  else
    echo -e "${Y}⚠ $cmd não encontrado no PATH — adicione ~/.local/bin ao PATH${NC}"
  fi
done

# Teste rápido
echo -e "\n${Y}Teste rápido...${NC}"
python3 -c "
from kernelmind.core.sensor import KernelSense
snap = KernelSense().snapshot()
print(f'✓ Kernel: {snap.kernel_version} | RAM: {snap.memory.percent:.1f}% | CPU: {snap.cpu.percent:.1f}%')
"

echo -e "\n${BD}${G}Instalação concluída!${NC}"
echo -e "\n  ${CYN}km snapshot${NC}   — estado agora"
echo -e "  ${CYN}km memory${NC}     — sugestões de RAM"
echo -e "  ${CYN}km storage${NC}    — sugestões de disco"
echo -e "  ${CYN}km threat${NC}     — scan de anomalias"
echo -e "  ${CYN}km watch${NC}      — monitor contínuo"
echo -e "  ${CYN}km ethics${NC}     — audit log"
echo -e "  ${CYN}km-api${NC}        — API REST (porta 7771)"
echo -e "  ${CYN}km-mcp --test${NC} — testar ferramentas MCP\n"
