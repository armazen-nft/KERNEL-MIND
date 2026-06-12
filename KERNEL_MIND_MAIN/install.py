#!/usr/bin/env python3
"""
KernelMind :: Instalador
Verifica dependências, instala, cria atalho 'km' no PATH.
"""
import subprocess, sys, os, shutil

REQUIRED = ["psutil", "fastapi", "uvicorn"]

def run(cmd, check=True):
    return subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)

def main():
    print("KernelMind — Instalação\n")

    # Python
    if sys.version_info < (3, 10):
        print("✗ Python 3.10+ necessário")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]}")

    # Dependências
    for pkg in REQUIRED:
        result = run(f"pip install {pkg} --break-system-packages -q", check=False)
        status = "✓" if result.returncode == 0 else "✗"
        print(f"{status} {pkg}")

    # Atalho km
    km_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cli", "km.py")
    link_target = os.path.expanduser("~/.local/bin/km")
    os.makedirs(os.path.dirname(link_target), exist_ok=True)

    wrapper = f"#!/bin/sh\npython3 {km_path} \"$@\"\n"
    with open(link_target, "w") as f:
        f.write(wrapper)
    os.chmod(link_target, 0o755)
    print(f"✓ Atalho criado: {link_target}")

    print("\n✓ KernelMind instalado.")
    print("\nUso:")
    print("  km snapshot     — estado do sistema agora")
    print("  km memory       — sugestões de RAM")
    print("  km watch        — monitor contínuo")
    print("  km ethics       — audit log ético")
    print("  km --json       — saída JSON para integração")
    print("\nAPI REST (porta 7771):")
    print("  python3 api/server.py")

if __name__ == "__main__":
    main()
