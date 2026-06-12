#!/usr/bin/env python3
"""
KernelMind :: CLI
Interface de linha de comando — leve, direta, sem dependências extras.
Uso: python3 cli.py [snapshot|memory|watch|ethics]
"""

import sys
import os
import time
import json
import argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataclasses import asdict
from core.sensor import KernelSense
from core.memory import MemoryWeaver
from ethics.lock import EthicsLock, ActionType

# ── CORES ANSI ──
R  = "\033[0m"
G  = "\033[92m"
Y  = "\033[93m"
RE = "\033[91m"
B  = "\033[94m"
DIM= "\033[2m"
BD = "\033[1m"
CYN= "\033[96m"

def bar(pct: float, width: int = 20) -> str:
    filled = int(pct / 100 * width)
    color = G if pct < 60 else (Y if pct < 85 else RE)
    return color + "█" * filled + DIM + "░" * (width - filled) + R


def pct_color(pct: float) -> str:
    c = G if pct < 60 else (Y if pct < 85 else RE)
    return f"{c}{pct:.1f}%{R}"


def cmd_snapshot(sensor: KernelSense):
    print(f"\n{BD}{CYN}── KernelMind :: Snapshot ──────────────────{R}")
    snap = sensor.snapshot()

    # CPU
    cpu = snap.cpu
    print(f"\n{BD}CPU{R}  {bar(cpu.percent)} {pct_color(cpu.percent)}", end="")
    if cpu.freq_mhz:
        print(f"  {DIM}{cpu.freq_mhz} MHz{R}", end="")
    print(f"  {DIM}load: {cpu.load_avg_1m} {cpu.load_avg_5m} {cpu.load_avg_15m}{R}")

    # RAM
    mem = snap.memory
    print(f"{BD}RAM{R}  {bar(mem.percent)} {pct_color(mem.percent)}"
          f"  {DIM}{mem.used_mb} / {mem.total_mb} MB{R}")

    if mem.swap_total_mb > 0:
        print(f"{BD}SWAP{R} {bar(mem.swap_percent)} {pct_color(mem.swap_percent)}"
              f"  {DIM}{mem.swap_used_mb} / {mem.swap_total_mb} MB{R}")

    # Disco
    for d in snap.disks:
        print(f"{BD}DISK{R} {bar(d['percent'])} {pct_color(d['percent'])}"
              f"  {DIM}{d['free_gb']} GB livres / {d['total_gb']} GB{R}"
              f"  {DIM}↑{d['write_mb_s']} ↓{d['read_mb_s']} MB/s{R}")

    # Temperatura
    if snap.temperature_c:
        tc = snap.temperature_c
        col = G if tc < 65 else (Y if tc < 80 else RE)
        print(f"{BD}TEMP{R} {col}{tc}°C{R}")

    # Top processos
    print(f"\n{BD}Top processos{R}")
    for p in snap.top_processes[:5]:
        cpu_c = G if p['cpu_percent'] < 20 else (Y if p['cpu_percent'] < 50 else RE)
        print(f"  {DIM}{p['pid']:>6}{R}  {p['name']:<22}"
              f" cpu:{cpu_c}{p['cpu_percent']:>5.1f}%{R}"
              f"  mem:{DIM}{p['mem_mb']:>6.1f}MB{R}")

    print(f"\n{DIM}kernel {snap.kernel_version}  uptime {snap.uptime_hours:.1f}h{R}")


def cmd_memory(weaver: MemoryWeaver):
    print(f"\n{BD}{CYN}── KernelMind :: MemoryWeaver ───────────────{R}")
    suggestions = weaver.analyze()

    if not suggestions:
        print(f"\n{G}✓ Memória saudável — nenhuma ação necessária.{R}")
        return

    prio_icons = {1: f"{RE}● CRÍTICO {R}", 2: f"{Y}● IMPORTANTE{R}", 3: f"{G}● OTIMIZAÇÃO{R}"}

    for s in suggestions:
        print(f"\n{prio_icons.get(s.priority, '●')} {BD}{s.title}{R}")
        print(f"  {s.description}")
        if s.command:
            print(f"  {DIM}Comando sugerido:{R}")
            print(f"  {CYN}$ {s.command}{R}")
        if s.estimated_gain_mb:
            print(f"  {DIM}Ganho estimado: ~{s.estimated_gain_mb} MB{R}")

    print(f"\n{DIM}Nenhuma ação foi executada. Revise e aplique manualmente.{R}")


def cmd_watch(sensor: KernelSense, interval: int = 3):
    print(f"{BD}{CYN}KernelMind :: Watch — Ctrl+C para parar{R}")
    try:
        while True:
            os.system('clear')
            cmd_snapshot(sensor)
            print(f"\n{DIM}Atualizando em {interval}s...{R}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{DIM}Watch encerrado.{R}")


def cmd_ethics(lock: EthicsLock):
    print(f"\n{BD}{CYN}── KernelMind :: EthicsLock ─────────────────{R}")
    st = lock.status()
    print(f"\n{G}✓ EthicsLock v{st['ethics_lock_version']} ativo{R}")
    print(f"  Regras ativas:      {st['rules_active']}")
    print(f"  Rede bloqueada:     {G}sim{R}")
    print(f"  Requer confirmação: {', '.join(st['confirmation_required_for'])}")
    print(f"  Sempre permitido:   {', '.join(st['always_allowed'])}")
    print(f"  Entradas no audit:  {st['audit_entries']}")

    log = lock.recent_log(10)
    if log:
        print(f"\n{BD}Últimas ações auditadas:{R}")
        for e in log[-5:]:
            ts = time.strftime('%H:%M:%S', time.localtime(e['ts']))
            col = G if e['verdict'] == 'PERMITIDO' else RE
            print(f"  {DIM}{ts}{R}  {col}{e['verdict']:<10}{R}  {e['action']:<8}  {e['desc'][:50]}")


def main():
    parser = argparse.ArgumentParser(
        description="KernelMind CLI — gestão de kernel leve e ética",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandos:
  snapshot   Estado atual do sistema
  memory     Sugestões de otimização de RAM
  watch      Monitor contínuo (Ctrl+C para parar)
  ethics     Status do EthicsLock e audit log
        """,
    )
    parser.add_argument("command", nargs="?", default="snapshot",
                        choices=["snapshot", "memory", "watch", "ethics"])
    parser.add_argument("--interval", type=int, default=3,
                        help="Intervalo em segundos para watch (padrão: 3)")
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args()

    sensor = KernelSense()
    weaver = MemoryWeaver()
    ethics_lock = EthicsLock()

    if args.json:
        snap = sensor.snapshot()
        print(json.dumps(asdict(snap), indent=2, default=str))
        return

    if args.command == "snapshot":
        cmd_snapshot(sensor)
    elif args.command == "memory":
        cmd_memory(weaver)
    elif args.command == "watch":
        cmd_watch(sensor, args.interval)
    elif args.command == "ethics":
        cmd_ethics(ethics_lock)


if __name__ == "__main__":
    main()
