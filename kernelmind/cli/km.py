#!/usr/bin/env python3
"""
KernelMind :: CLI
Interface de linha de comando — leve, direta, sem dependências extras.
"""

import argparse
import json
import os
import time
from dataclasses import asdict

from kernelmind.core.memory import MemoryWeaver
from kernelmind.core.sensor import KernelSense
from kernelmind.core.storage import StorageGuard
from kernelmind.core.threat import ThreatRadar
from kernelmind.ethics.lock import EthicsLock

# ── CORES ANSI ──
R = "\033[0m"
G = "\033[92m"
Y = "\033[93m"
RE = "\033[91m"
DIM = "\033[2m"
BD = "\033[1m"
CYN = "\033[96m"


def bar(pct: float, width: int = 20) -> str:
    filled = int(pct / 100 * width)
    color = G if pct < 60 else (Y if pct < 85 else RE)
    return color + "█" * filled + DIM + "░" * (width - filled) + R


def pct_color(pct: float) -> str:
    c = G if pct < 60 else (Y if pct < 85 else RE)
    return f"{c}{pct:.1f}%{R}"


def cmd_snapshot(sensor: KernelSense) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: Snapshot ──────────────────{R}")
    snap = sensor.snapshot()

    cpu = snap.cpu
    print(f"\n{BD}CPU{R}  {bar(cpu.percent)} {pct_color(cpu.percent)}", end="")
    if cpu.freq_mhz:
        print(f"  {DIM}{cpu.freq_mhz} MHz{R}", end="")
    print(f"  {DIM}load: {cpu.load_avg_1m} {cpu.load_avg_5m} {cpu.load_avg_15m}{R}")

    mem = snap.memory
    print(
        f"{BD}RAM{R}  {bar(mem.percent)} {pct_color(mem.percent)}"
        f"  {DIM}{mem.used_mb} / {mem.total_mb} MB{R}"
    )

    if mem.swap_total_mb > 0:
        print(
            f"{BD}SWAP{R} {bar(mem.swap_percent)} {pct_color(mem.swap_percent)}"
            f"  {DIM}{mem.swap_used_mb} / {mem.swap_total_mb} MB{R}"
        )

    for disk in snap.disks:
        print(
            f"{BD}DISK{R} {bar(disk['percent'])} {pct_color(disk['percent'])}"
            f"  {DIM}{disk['free_gb']} GB livres / {disk['total_gb']} GB{R}"
            f"  {DIM}↑{disk['write_mb_s']} ↓{disk['read_mb_s']} MB/s{R}"
        )

    if snap.temperature_c:
        tc = snap.temperature_c
        col = G if tc < 65 else (Y if tc < 80 else RE)
        print(f"{BD}TEMP{R} {col}{tc}°C{R}")

    print(f"\n{BD}Top processos{R}")
    for proc in snap.top_processes[:5]:
        cpu_c = G if proc["cpu_percent"] < 20 else (Y if proc["cpu_percent"] < 50 else RE)
        print(
            f"  {DIM}{proc['pid']:>6}{R}  {proc['name']:<22}"
            f" cpu:{cpu_c}{proc['cpu_percent']:>5.1f}%{R}"
            f"  mem:{DIM}{proc['mem_mb']:>6.1f}MB{R}"
        )

    print(f"\n{DIM}kernel {snap.kernel_version}  uptime {snap.uptime_hours:.1f}h{R}")


def cmd_memory(weaver: MemoryWeaver) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: MemoryWeaver ───────────────{R}")
    suggestions = weaver.analyze()
    _print_suggestions(suggestions, empty_message="✓ Memória saudável — nenhuma ação necessária.")


def cmd_storage(storage: StorageGuard) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: StorageGuard ───────────────{R}")
    suggestions = storage.analyze()
    _print_suggestions(suggestions, empty_message="✓ Disco saudável — nenhuma ação necessária.")


def cmd_threat(threat: ThreatRadar) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: ThreatRadar ────────────────{R}")
    anomalies = threat.scan()
    if not anomalies:
        print(f"\n{G}✓ Nenhuma anomalia detectada.{R}")
        return

    labels = {1: f"{RE}● CRÍTICO {R}", 2: f"{Y}● SUSPEITO{R}", 3: f"{CYN}● ATENÇÃO {R}"}
    for anomaly in anomalies:
        print(f"\n{labels.get(anomaly.severity, '●')} {BD}[{anomaly.category}]{R}")
        print(f"  {anomaly.description}")
        if anomaly.pid:
            print(f"  {DIM}PID:{R} {anomaly.pid}  {DIM}Processo:{R} {anomaly.process_name}")
        print(f"  {DIM}Recomendação:{R} {anomaly.recommendation}")

    print(f"\n{DIM}Nenhuma ação foi executada. Revise e aplique manualmente.{R}")


def _print_suggestions(suggestions: list, empty_message: str) -> None:
    if not suggestions:
        print(f"\n{G}{empty_message}{R}")
        return

    prio_icons = {1: f"{RE}● CRÍTICO {R}", 2: f"{Y}● IMPORTANTE{R}", 3: f"{G}● OTIMIZAÇÃO{R}"}
    for suggestion in suggestions:
        print(f"\n{prio_icons.get(suggestion.priority, '●')} {BD}{suggestion.title}{R}")
        print(f"  {suggestion.description}")
        if suggestion.command:
            print(f"  {DIM}Comando sugerido:{R}")
            print(f"  {CYN}$ {suggestion.command}{R}")
        if suggestion.estimated_gain_mb:
            print(f"  {DIM}Ganho estimado: ~{suggestion.estimated_gain_mb} MB{R}")

    print(f"\n{DIM}Nenhuma ação foi executada. Revise e aplique manualmente.{R}")


def cmd_watch(sensor: KernelSense, interval: int = 3) -> None:
    print(f"{BD}{CYN}KernelMind :: Watch — Ctrl+C para parar{R}")
    try:
        while True:
            os.system("clear")
            cmd_snapshot(sensor)
            print(f"\n{DIM}Atualizando em {interval}s...{R}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{DIM}Watch encerrado.{R}")


def cmd_ethics(lock: EthicsLock) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: EthicsLock ─────────────────{R}")
    status = lock.status()
    print(f"\n{G}✓ EthicsLock v{status['ethics_lock_version']} ativo{R}")
    print(f"  Regras ativas:      {status['rules_active']}")
    print(f"  Rede bloqueada:     {G}sim{R}")
    print(f"  Requer confirmação: {', '.join(status['confirmation_required_for'])}")
    print(f"  Sempre permitido:   {', '.join(status['always_allowed'])}")
    print(f"  Entradas no audit:  {status['audit_entries']}")

    log = lock.recent_log(10)
    if log:
        print(f"\n{BD}Últimas ações auditadas:{R}")
        for entry in log[-5:]:
            ts = time.strftime("%H:%M:%S", time.localtime(entry["ts"]))
            col = G if entry["verdict"] == "PERMITIDO" else RE
            print(
                f"  {DIM}{ts}{R}  {col}{entry['verdict']:<10}{R}"
                f"  {entry['action']:<8}  {entry['desc'][:50]}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="KernelMind CLI — gestão de kernel leve e ética",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandos:
  snapshot   Estado atual do sistema
  memory     Sugestões de otimização de RAM
  storage    Sugestões de otimização de disco
  threat     Scan de anomalias comportamentais
  watch      Monitor contínuo (Ctrl+C para parar)
  ethics     Status do EthicsLock e audit log
        """,
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="snapshot",
        choices=["snapshot", "memory", "storage", "threat", "watch", "ethics"],
    )
    parser.add_argument("--interval", type=int, default=3, help="Intervalo em segundos para watch")
    parser.add_argument("--json", action="store_true", help="Saída em JSON")
    args = parser.parse_args()

    sensor = KernelSense()

    if args.json:
        snap = sensor.snapshot()
        print(json.dumps(asdict(snap), indent=2, default=str))
        return

    if args.command == "snapshot":
        cmd_snapshot(sensor)
    elif args.command == "memory":
        cmd_memory(MemoryWeaver())
    elif args.command == "storage":
        cmd_storage(StorageGuard())
    elif args.command == "threat":
        cmd_threat(ThreatRadar())
    elif args.command == "watch":
        cmd_watch(sensor, args.interval)
    elif args.command == "ethics":
        cmd_ethics(EthicsLock())


if __name__ == "__main__":
    main()
