@echo off
echo ========================================
echo   Construindo KernelMind App para Windows
echo ========================================
echo.

REM Instalar dependências
echo [1/4] Instalando dependências Python...
pip install flask pyinstaller psutil

REM Criar executável da versão GUI
echo [2/4] Criando executável...
pyinstaller --onefile --windowed --name "KernelMind_GUI" kernelmind_wrapper.py

REM Criar executável da versão Web
echo [3/4] Criando versão web...
pyinstaller --onefile --name "KernelMind_Web" kernelmind_web.py

REM Criar pasta de distribuição
echo [4/4] Criando distribuição...
mkdir dist\KernelMind_Package
copy dist\KernelMind_GUI.exe dist\KernelMind_Package\
copy dist\KernelMind_Web.exe dist\KernelMind_Package\
copy README.txt dist\KernelMind_Package\

echo.
echo ✅ Build concluído!
echo 📁 Arquivos em: dist\KernelMind_Package\
pause
