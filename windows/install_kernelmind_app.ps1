# Instalador Automático do KernelMind App
Write-Host "🧠 Instalando KernelMind App..." -ForegroundColor Green

# Baixar arquivos
$appPath = "$env:USERPROFILE\KernelMindApp"
New-Item -ItemType Directory -Force -Path $appPath

# Criar atalho no desktop
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut("$env:USERPROFILE\Desktop\KernelMind.lnk")
$Shortcut.TargetPath = "python.exe"
$Shortcut.Arguments = "$appPath\kernelmind_wrapper.py"
$Shortcut.Save()

Write-Host "✅ Instalação concluída!" -ForegroundColor Green
Write-Host "📌 Atalho criado no Desktop" -ForegroundColor Yellow
