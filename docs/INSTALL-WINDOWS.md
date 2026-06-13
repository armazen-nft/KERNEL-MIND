# 🪟 Instalação do KernelMind no Windows

> **KernelMind para Windows** — Monitoramento e otimização de kernel via WSL 2 ou nativo.

---

## Índice

1. [Via WSL 2 (Recomendado)](#via-wsl-2-recomendado)
2. [Via PowerShell Nativo (Python Direto)](#via-powershell-nativo)
3. [Via Docker Desktop](#via-docker-desktop)
4. [Acessar API do Windows](#acessar-api-do-windows)
5. [Troubleshooting](#troubleshooting)

---

## Via WSL 2 (Recomendado)

WSL 2 oferece acesso total ao kernel Linux e máxima compatibilidade com KernelMind.

### Passo 1: Instalar WSL 2

Abra **PowerShell como Administrador** e execute:

```powershell
# Instalar WSL com Ubuntu padrão
wsl --install

# Ou, para escolher distribuição manualmente:
wsl --install -d Ubuntu-24.04
```

**Reinicie o computador** quando solicitado. O Ubuntu abrirá automaticamente para criar seu usuário e senha.

Se já tem WSL instalado, atualize:

```powershell
wsl --update
wsl -l -v  # listar distros instaladas
```

### Passo 2: Dentro do WSL — Preparar Ambiente

Abra PowerShell ou CMD e digite:

```powershell
wsl
```

Dentro do terminal Ubuntu, execute:

```bash
# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install python3 python3-pip git curl wget build-essential -y

# Instalar bibliotecas Python necessárias
pip3 install --user psutil fastapi uvicorn pydantic toml
```

### Passo 3: Clonar e Instalar KernelMind

```bash
# Clonar repositório
git clone https://github.com/armazen-nft/KERNEL-MIND.git kernelmind

# Entrar na pasta
cd kernelmind

# Dar permissão de execução no script
chmod +x scripts/setup.sh

# Instalar via Python
python3 install.py

# Ou via script bash
bash scripts/setup.sh
```

### Passo 4: Verificar Instalação

```bash
# Testar comando CLI
km --version
km --help

# Fazer snapshot do sistema
km snapshot

# Verificar ética
km ethics

# Testar JSON
km snapshot --json
```

### Passo 5: Usar KernelMind no WSL

#### CLI (Linha de Comando)

```bash
# Monitor contínuo em tempo real
km watch

# Sugestões de otimização de RAM
km memory

# Sugestões de limpeza de disco
km storage

# Detectar ameaças/anomalias
km threat scan

# Ver logs éticos
km ethics --log

# Saída JSON (para integração)
km snapshot --json
```

#### API REST

```bash
# Terminal 1: Iniciar servidor API
python3 api/server.py

# Terminal 2 (novo WSL): Testar a API
curl http://localhost:7771/health
curl http://localhost:7771/snapshot
curl http://localhost:7771/memory/suggest

# Swagger UI (dentro do WSL)
# http://localhost:7771/docs
```

### Acessar API do Windows (Fora do WSL)

Para chamar a API KernelMind do Windows Host (PowerShell, navegador, etc.):

```bash
# Dentro do WSL, descobrir IP
ip addr show eth0 | grep inet

# Exemplo: 172.31.234.56
```

```powershell
# No PowerShell do Windows
# Substitua SEU_IP_WSL pelo IP obtido acima

curl.exe http://SEU_IP_WSL:7771/snapshot
# Ou abra no navegador:
# http://SEU_IP_WSL:7771/docs
```

**Firewall**: Se a porta 7771 não responder do Windows, configure o firewall:

```powershell
# PowerShell como Administrador
New-NetFirewallRule -DisplayName "KernelMind API" `
  -Direction Inbound `
  -Action Allow `
  -Protocol TCP `
  -LocalPort 7771
```

---

## Via PowerShell Nativo

Se preferir executar KernelMind **diretamente no Windows** (sem WSL):

### Passo 1: Instalar Python

1. Baixe Python 3.10+ em [python.org](https://www.python.org/downloads/)
2. **Marque**: "Add Python to PATH"
3. Instale

Verifique:

```powershell
python --version
pip --version
```

### Passo 2: Instalar KernelMind

```powershell
# Clonar repositório
git clone https://github.com/armazen-nft/KERNEL-MIND.git
cd KERNEL-MIND

# Instalar dependências
pip install psutil fastapi uvicorn pydantic toml windows-curses

# Instalar KernelMind
pip install -e .
```

### Passo 3: Usar KernelMind

```powershell
# Snapshot do sistema
km snapshot

# Monitor contínuo
km watch

# Sugestões de RAM
km memory

# API REST
python api/server.py

# Testar API (em outro PowerShell)
curl.exe http://localhost:7771/snapshot
```

### ⚠️ Limitações Nativas no Windows

| Funcionalidade | Windows | Motivo |
|---|---|---|
| Leitura de CPU/RAM | ✅ | `psutil` funciona bem |
| Leitura de disco | ✅ | Suportado |
| Monitoramento de processos | ✅ | Funciona |
| Ajuste kernel parâmetros | ❌ | Windows não permite via Python |
| Leitura de `/proc` | ❌ | Específico de Linux |
| MCP/PoE Integration | ⚠️ | Limitado |

**Recomendação**: Use WSL 2 para funcionalidade completa.

---

## Via Docker Desktop

Para isolamento total e sem WSL:

### Passo 1: Instalar Docker Desktop

1. Baixe em [docker.com](https://www.docker.com/products/docker-desktop)
2. Instale e inicie

### Passo 2: Executar KernelMind em Container

```powershell
# Pull da imagem (se disponível)
docker pull ghcr.io/armazen-nft/kernelmind:latest

# Ou, build local
git clone https://github.com/armazen-nft/KERNEL-MIND.git
cd KERNEL-MIND
docker build -t kernelmind:latest .

# Rodar container
docker run -it --rm -p 7771:7771 kernelmind:latest

# Em outro PowerShell, testar API
curl.exe http://localhost:7771/snapshot
```

**Nota**: Monitoramento de host é limitado em container; ideal para API REST apenas.

---

## Acessar API do Windows

### Via PowerShell (curl)

```powershell
# Health check
curl.exe http://localhost:7771/health

# Snapshot
curl.exe http://localhost:7771/snapshot

# Memory suggestions
curl.exe http://localhost:7771/memory/suggest

# Ethics status
curl.exe http://localhost:7771/ethics/status
```

### Via Navegador

Abra no Edge, Chrome, Firefox:

```
http://localhost:7771/docs
```

Você verá o Swagger UI interativo com todos os endpoints.

### Via Python

```python
import requests

response = requests.get("http://localhost:7771/snapshot")
print(response.json())
```

---

## Manter KernelMind Rodando em Background

### Via WSL + tmux (Recomendado)

```bash
# Dentro do WSL
sudo apt install tmux -y

# Criar nova sessão
tmux new -s kernelmind

# Dentro da sessão tmux
cd ~/kernelmind
python3 api/server.py

# Desanexar: Ctrl+B, depois D
# Reanexar: tmux attach -t kernelmind

# Listar sessões
tmux ls

# Matar sessão
tmux kill-session -t kernelmind
```

### Via PowerShell (Nativo Windows)

```powershell
# Criar task agendada
$trigger = New-ScheduledTaskTrigger -AtStartup
$action = New-ScheduledTaskAction -Execute "python" `
  -Argument "C:\caminho\para\kernelmind\api\server.py"
Register-ScheduledTask -TaskName "KernelMind" `
  -Trigger $trigger -Action $action -RunLevel Highest
```

### Via Windows Service (Avançado)

Use [NSSM](http://nssm.cc/) para converter script Python em serviço:

```powershell
# Baixar NSSM em http://nssm.cc/download
# Descompactar e:

nssm install KernelMind "python" "C:\path\to\api\server.py"
nssm start KernelMind
nssm status KernelMind
```

---

## Troubleshooting

### ❌ "Comando 'km' não encontrado"

**WSL:**
```bash
pip3 install --user -e .
export PATH=$PATH:~/.local/bin
# Adicione à ~/.bashrc para persistir
```

**Windows Nativo:**
```powershell
pip install -e .
refreshenv
```

### ❌ "ImportError: No module named 'psutil'"

```bash
# WSL
pip3 install psutil --user

# Windows
pip install psutil
```

### ❌ "Porta 7771 já em uso"

**WSL:**
```bash
sudo lsof -i :7771
sudo kill -9 <PID>
```

**Windows:**
```powershell
netstat -ano | findstr :7771
taskkill /PID <PID> /F
```

### ❌ "WSL não responde"

```powershell
# Reset WSL
wsl --shutdown

# Depois abra PowerShell e digite 'wsl' novamente
```

### ❌ "API não acessível do Windows"

1. Verifique IP do WSL:
   ```bash
   ip addr show eth0 | grep inet
   ```

2. Configure Firewall Windows:
   ```powershell
   New-NetFirewallRule -DisplayName "KernelMind" `
     -Direction Inbound -Action Allow -Protocol TCP -LocalPort 7771
   ```

3. Teste com `curl.exe http://IP_WSL:7771/health`

### ❌ "git não encontrado"

```bash
# WSL
sudo apt install git -y

# Windows Nativo
# Instale em https://git-scm.com/download/win
```

---

## Guia Rápido

### WSL (Recomendado)

```powershell
# PowerShell como Admin
wsl --install

# Reinicie, depois:
wsl
```

```bash
# Dentro do WSL
sudo apt update && sudo apt install python3 python3-pip git -y
pip3 install psutil fastapi uvicorn
git clone https://github.com/armazen-nft/KERNEL-MIND.git kernelmind
cd kernelmind
python3 install.py

# Usar
km snapshot
km watch
python3 api/server.py
```

### Windows Nativo

```powershell
# Instale Python 3.10+ com PATH marcado

python -m pip install psutil fastapi uvicorn
git clone https://github.com/armazen-nft/KERNEL-MIND.git
cd KERNEL-MIND
pip install -e .

km snapshot
km watch
python api/server.py
```

---

## Próximos Passos

- Leia [docs/mcp-integration.md](mcp-integration.md) para integrar com Claude Desktop
- Configure [EthicsLock](ethics.md) para suas preferências
- Consulte [API Reference](api.md) para endpoints completos

---

## Suporte

Dúvidas? Abra uma issue em [armazen-nft/KERNEL-MIND/issues](https://github.com/armazen-nft/KERNEL-MIND/issues)

---

**KernelMind** — Leve. Ético. Sempre com seu consentimento.
