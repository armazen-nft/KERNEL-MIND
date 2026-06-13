# KernelMind Windows App Integration

> Transformar KernelMind em uma aplicação Windows nativa com interface gráfica e web.

## 📦 Opções Disponíveis

### Opção A: App Desktop (Recomendado)

**Arquivo:** `kernelmind_wrapper.py`

Aplicação GUI desktop com:
- Interface moderna em Tkinter
- Monitoramento em tempo real (CPU, RAM, Disco)
- Sugestões da IA integradas
- Controle ético via EthicsLock
- Integração automática com WSL

#### Uso:
```bash
python kernelmind_wrapper.py
```

### Opção B: App Web

**Arquivo:** `kernelmind_web.py`

Interface web responsiva com:
- Dashboard em Flask
- Acesso via navegador (http://localhost:5000)
- Sugestões da IA em tempo real
- API REST integrada

#### Uso:
```bash
python kernelmind_web.py
```

## 🔨 Build para Executável Windows

### Requisitos
- Python 3.10+
- WSL (Windows Subsystem for Linux) instalado
- KernelMind instalado no WSL

### Passo 1: Instalar Dependências

```bash
pip install pyinstaller flask psutil
```

### Passo 2: Executar Build

#### Opção A: Script Batch (Windows Command Prompt)
```bash
build_kernelmind_app.bat
```

#### Opção B: Comandos Manuais

**Versão GUI:**
```bash
pyinstaller --onefile --windowed --name "KernelMind_GUI" kernelmind_wrapper.py
```

**Versão Web:**
```bash
pyinstaller --onefile --name "KernelMind_Web" kernelmind_web.py
```

### Passo 3: Criar Instalador (Opcional)

Utilize o **Inno Setup** com o arquivo `setup_kernelmind.iss`:

1. Instale [Inno Setup](https://jrsoftware.org/isdl.php)
2. Abra `setup_kernelmind.iss`
3. Compile para gerar o instalador profissional

## 🚀 Instalação Rápida

### Opção 1: PowerShell (Automático)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install_kernelmind_app.ps1
```

### Opção 2: Manual

1. Copie os arquivos para `C:\Program Files\KernelMind`
2. Crie um atalho no Desktop apontando para o .exe
3. Execute

## 📋 Arquitetura

```
windows/
├── kernelmind_wrapper.py      # GUI Desktop (Tkinter)
├── kernelmind_web.py          # Web App (Flask)
├── setup_kernelmind.iss       # Instalador (Inno Setup)
├── build_kernelmind_app.bat   # Script de build
├── install_kernelmind_app.ps1 # Instalação automática
└── README.md                   # Este arquivo
```

## 🔧 Integração com WSL

O app verifica automaticamente se WSL está instalado e se KernelMind já foi instalado no subsistema.

Se não encontrar:
1. Solicita confirmação do usuário
2. Instala KernelMind automaticamente via `git clone`
3. Instala dependências Python necessárias
4. Inicia monitoramento

## 🛡️ EthicsLock em Ação

Todas as ações que modificam o sistema requerem confirmação:

```
[EthicsLock] KernelMind sugere otimizar a memória RAM.

Isso pode melhorar o desempenho do sistema.

Deseja permitir esta ação?
  [SIM] [NÃO]
```

## 🐛 Troubleshooting

### "WSL não encontrado"

Instale o WSL:
```powershell
wsl --install
```

### "KernelMind não encontrado no WSL"

O app oferecerá instalar automaticamente, mas você também pode instalar manualmente:

```bash
wsl bash
git clone https://github.com/armazen-nft/KERNEL-MIND.git ~/kernelmind
cd ~/kernelmind
pip3 install -e .
```

### Porta 5000 já está em uso (Web App)

Altere a porta em `kernelmind_web.py`:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)  # Mude 5000 para 5001
```

## 📊 Funcionalidades

✅ Monitoramento em tempo real de CPU, RAM e Disco
✅ Sugestões da IA para otimização
✅ Interface ética com EthicsLock obrigatório
✅ Integração com API REST do KernelMind
✅ Log de auditoria imutável
✅ Instalação automatizada
✅ Versão Desktop e Web
✅ Executável Windows nativo (.exe)

## 📝 Licença

AGPL-3.0 — Código aberto, modificações devem ser compartilhadas.
Ver [LICENSE](../LICENSE) para detalhes.
