"""KernelMind :: CLI — interface de linha de comando."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict

from kernelmind.core.sensor import KernelSense
from kernelmind.core.memory import MemoryWeaver
from kernelmind.core.storage import StorageGuard
from kernelmind.core.threat import ThreatRadar
from kernelmind.ethics.lock import EthicsLock, ActionType

R   = "\033[0m"
G   = "\033[92m"
Y   = "\033[93m"
RE  = "\033[91m"
B   = "\033[94m"
DIM = "\033[2m"
BD  = "\033[1m"
CYN = "\033[96m"


def bar(pct: float, w: int = 20) -> str:
    filled = int(pct / 100 * w)
    color = G if pct < 60 else (Y if pct < 85 else RE)
    return color + "█" * filled + DIM + "░" * (w - filled) + R


def pcolor(pct: float) -> str:
    c = G if pct < 60 else (Y if pct < 85 else RE)
    return f"{c}{pct:.1f}%{R}"


def cmd_snapshot(sensor: KernelSense) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: Snapshot ──────────────────{R}")
    snap = sensor.snapshot()
    cpu = snap.cpu
    print(f"\n{BD}CPU {R} {bar(cpu.percent)} {pcolor(cpu.percent)}", end="")
    if cpu.freq_mhz:
        print(f"  {DIM}{cpu.freq_mhz} MHz{R}", end="")
    print(f"  {DIM}load: {cpu.load_avg_1m} {cpu.load_avg_5m} {cpu.load_avg_15m}{R}")

    mem = snap.memory
    print(f"{BD}RAM  {R}{bar(mem.percent)} {pcolor(mem.percent)}"
          f"  {DIM}{mem.used_mb}/{mem.total_mb} MB{R}")
    if mem.swap_total_mb > 0:
        print(f"{BD}SWAP {R}{bar(mem.swap_percent)} {pcolor(mem.swap_percent)}"
              f"  {DIM}{mem.swap_used_mb}/{mem.swap_total_mb} MB{R}")

    for d in snap.disks:
        print(f"{BD}DISK {R}{bar(d['percent'])} {pcolor(d['percent'])}"
              f"  {DIM}{d['free_gb']} GB livres / {d['total_gb']} GB{R}")

    if snap.temperature_c:
        tc = snap.temperature_c
        col = G if tc < 65 else (Y if tc < 80 else RE)
        print(f"{BD}TEMP {R}{col}{tc}°C{R}")

    print(f"\n{BD}Top processos{R}")
    for p in snap.top_processes[:5]:
        cc = G if p["cpu_percent"] < 20 else (Y if p["cpu_percent"] < 50 else RE)
        print(f"  {DIM}{p['pid']:>6}{R}  {p['name']:<22}"
              f" cpu:{cc}{p['cpu_percent']:>5.1f}%{R}"
              f"  mem:{DIM}{p['mem_mb']:>6.1f} MB{R}")

    print(f"\n{DIM}kernel {snap.kernel_version}  uptime {snap.uptime_hours:.1f}h{R}")


def cmd_memory(weaver: MemoryWeaver) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: MemoryWeaver ───────────────{R}")
    sugs = weaver.analyze()
    if not sugs:
        print(f"\n{G}✓ Memória saudável.{R}")
        return
    icons = {1: f"{RE}● CRÍTICO   {R}", 2: f"{Y}● IMPORTANTE{R}", 3: f"{G}● OTIMIZAÇÃO{R}"}
    for s in sugs:
        print(f"\n{icons.get(s.priority, '●')} {BD}{s.title}{R}")
        print(f"  {s.description}")
        if s.command:
            print(f"  {DIM}Comando:{R} {CYN}$ {s.command}{R}")
            print(f"  {DIM}Root: {'sim' if s.requires_root else 'não'} | "
                  f"Reversível: {'sim' if s.reversible else 'não'} | "
                  f"Risco: {s.risk_level}{R}")
    print(f"\n{DIM}Nenhuma ação executada. Aplique manualmente após revisão.{R}")


def cmd_storage(guard: StorageGuard) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: StorageGuard ───────────────{R}")
    sugs = guard.analyze()
    if not sugs:
        print(f"\n{G}✓ Disco saudável.{R}")
        return
    icons = {1: f"{RE}● CRÍTICO   {R}", 2: f"{Y}● IMPORTANTE{R}", 3: f"{G}● OTIMIZAÇÃO{R}"}
    for s in sugs:
        print(f"\n{icons.get(s.priority, '●')} {BD}{s.title}{R}")
        print(f"  {s.description}")
        if s.estimated_gain_mb:
            print(f"  {DIM}Ganho estimado: ~{s.estimated_gain_mb} MB{R}")
        if s.command:
            print(f"  {CYN}$ {s.command}{R}")


def cmd_threat(radar: ThreatRadar) -> None:
    print(f"\n{BD}{CYN}── KernelMind :: ThreatRadar ────────────────{R}")
    anomalies = radar.scan()
    if not anomalies:
        print(f"\n{G}✓ Nenhuma anomalia detectada.{R}")
        return
    icons = {1: f"{RE}● CRÍTICO {R}", 2: f"{Y}● SUSPEITO{R}", 3: f"{B}● ATENÇÃO  {R}"}
    for a in anomalies:
        print(f"\n{icons.get(a.severity, '●')} [{a.category}] {a.description}")
        if a.pid:
            print(f"  PID: {a.pid}  Processo: {a.process_name}")
        print(f"  → {a.recommendation}")


def cmd_watch(sensor: KernelSense, interval: int = 3) -> None:
    print(f"{BD}{CYN}KernelMind :: Watch (Ctrl+C para parar){R}")
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
    st = lock.status()
    print(f"\n{G}✓ EthicsLock v{st['ethics_lock_version']} ativo{R}")
    print(f"  Regras:             {st['rules_active']}")
    print(f"  Rede bloqueada:     {G}sempre{R}")
    print(f"  Requer confirmação: {', '.join(st['confirmation_required_for'])}")
    print(f"  Sempre permitido:   {', '.join(st['always_allowed'])}")
    print(f"  Audit entries:      {st['audit_entries']}")
    log = lock.recent_log(5)
    if log:
        print(f"\n{BD}Últimas ações:{R}")
        for e in log:
            ts = time.strftime("%H:%M:%S", time.localtime(e["ts"]))
            col = G if e["verdict"] == "PERMITIDO" else RE
            print(f"  {DIM}{ts}{R}  {col}{e['verdict']:<10}{R}  {e['action']:<8}  {e['desc'][:50]}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="km",
        description="KernelMind CLI — gestão de kernel leve e ética",
    )
    parser.add_argument(
        "command", nargs="?", default="snapshot",
        choices=["snapshot", "memory", "storage", "threat", "watch", "ethics"],
    )
    parser.add_argument("--interval", type=int, default=3)
    parser.add_argument("--json", action="store_true", help="Saída JSON")
    args = parser.parse_args()

    sensor  = KernelSense()
    weaver  = MemoryWeaver()
    guard   = StorageGuard()
    radar   = ThreatRadar()
    lock    = EthicsLock()

    if args.json:
        print(json.dumps(asdict(sensor.snapshot()), indent=2, default=str))
        return

    dispatch = {
        "snapshot": lambda: cmd_snapshot(sensor),
        "memory":   lambda: cmd_memory(weaver),
        "storage":  lambda: cmd_storage(guard),
        "threat":   lambda: cmd_threat(radar),
        "watch":    lambda: cmd_watch(sensor, args.interval),
        "ethics":   lambda: cmd_ethics(lock),
    }
    dispatch[args.command]()


if __name__ == "__main__":
    main()
