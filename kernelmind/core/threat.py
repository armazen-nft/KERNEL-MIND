"""
KernelMind :: ThreatRadar
Detecção de anomalias comportamentais no sistema.
Sem antivírus clássico — análise de padrões reais do kernel.
"""

import psutil
import os
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class Anomaly:
    severity: int          # 1=crítico, 2=suspeito, 3=atenção
    category: str          # privilege | io | network | process
    description: str
    pid: Optional[int]
    process_name: Optional[str]
    recommendation: str


class ThreatRadar:
    """
    Analisa padrões comportamentais para detectar anomalias.
    Não bloqueia — observa e alerta. A decisão é humana.
    """

    def __init__(self):
        self._baseline_io: dict = {}
        self._scan_time = time.time()

    def scan(self) -> list[Anomaly]:
        anomalies = []
        anomalies.extend(self._check_privilege_escalation())
        anomalies.extend(self._check_io_anomalies())
        anomalies.extend(self._check_zombie_processes())
        anomalies.extend(self._check_high_fd_usage())
        anomalies.extend(self._check_deleted_files_in_use())
        anomalies.sort(key=lambda a: a.severity)
        return anomalies

    def _check_privilege_escalation(self) -> list[Anomaly]:
        """Processos com UID/EUID diferentes — possível escalada."""
        anomalies = []
        try:
            for p in psutil.process_iter(['pid', 'name', 'uids', 'status']):
                try:
                    uids = p.info.get('uids')
                    if uids and uids.real != uids.effective and uids.effective == 0:
                        anomalies.append(Anomaly(
                            severity=1,
                            category="privilege",
                            description=f"Processo com EUID=root mas UID real={uids.real}",
                            pid=p.info['pid'],
                            process_name=p.info['name'],
                            recommendation="Verificar se este processo deveria ter privilégio root.",
                        ))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception:
            pass
        return anomalies

    def _check_io_anomalies(self) -> list[Anomaly]:
        """Processos com I/O muito acima da média — ransomware, miners."""
        anomalies = []
        try:
            high_io = []
            for p in psutil.process_iter(['pid', 'name', 'io_counters']):
                try:
                    io = p.info.get('io_counters')
                    if io and (io.read_bytes + io.write_bytes) > 500 * 1024 * 1024:
                        high_io.append({
                            'pid': p.info['pid'],
                            'name': p.info['name'],
                            'bytes': io.read_bytes + io.write_bytes,
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            for proc in high_io[:3]:
                mb = proc['bytes'] // (1024*1024)
                anomalies.append(Anomaly(
                    severity=2,
                    category="io",
                    description=f"I/O acumulado elevado: {mb} MB",
                    pid=proc['pid'],
                    process_name=proc['name'],
                    recommendation="Verificar se o processo está fazendo backup, "
                                   "indexação ou acesso anômalo a arquivos.",
                ))
        except Exception:
            pass
        return anomalies

    def _check_zombie_processes(self) -> list[Anomaly]:
        """Processos zumbis — indicam falha no gerenciamento de processos pai."""
        anomalies = []
        try:
            zombies = [
                p for p in psutil.process_iter(['pid', 'name', 'status'])
                if p.info.get('status') == psutil.STATUS_ZOMBIE
            ]
            if zombies:
                anomalies.append(Anomaly(
                    severity=3,
                    category="process",
                    description=f"{len(zombies)} processo(s) zumbi detectado(s): "
                                + ", ".join(p.info['name'] for p in zombies[:3]),
                    pid=None,
                    process_name=None,
                    recommendation="Reiniciar o processo pai ou reinicializar o sistema "
                                   "se o número crescer.",
                ))
        except Exception:
            pass
        return anomalies

    def _check_high_fd_usage(self) -> list[Anomaly]:
        """Processos com muitos file descriptors abertos — leak ou ataque."""
        anomalies = []
        try:
            for p in psutil.process_iter(['pid', 'name']):
                try:
                    fd_count = p.num_fds()
                    if fd_count > 1000:
                        anomalies.append(Anomaly(
                            severity=2 if fd_count > 5000 else 3,
                            category="process",
                            description=f"{fd_count} file descriptors abertos",
                            pid=p.pid,
                            process_name=p.info['name'],
                            recommendation="Possível file descriptor leak. "
                                           "Reiniciar o processo se o número continuar crescendo.",
                        ))
                except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                    pass
        except Exception:
            pass
        return anomalies

    def _check_deleted_files_in_use(self) -> list[Anomaly]:
        """Arquivos deletados ainda abertos por processos — técnica de rootkit."""
        anomalies = []
        try:
            result_path = "/proc"
            suspicious = []
            for pid_dir in os.listdir(result_path):
                if not pid_dir.isdigit():
                    continue
                fd_path = f"/proc/{pid_dir}/fd"
                try:
                    for fd in os.listdir(fd_path):
                        link = os.readlink(f"{fd_path}/{fd}")
                        if "(deleted)" in link and not link.startswith("/tmp"):
                            try:
                                name = open(f"/proc/{pid_dir}/comm").read().strip()
                            except Exception:
                                name = "?"
                            suspicious.append((int(pid_dir), name, link))
                            break
                except (PermissionError, FileNotFoundError):
                    pass
            if suspicious:
                for pid, name, fpath in suspicious[:3]:
                    anomalies.append(Anomaly(
                        severity=2,
                        category="process",
                        description=f"Arquivo deletado ainda em uso: {fpath[:60]}",
                        pid=pid,
                        process_name=name,
                        recommendation="Verificar se o processo é legítimo. "
                                       "Pode indicar tentativa de ocultar arquivos.",
                    ))
        except Exception:
            pass
        return anomalies


if __name__ == "__main__":
    tr = ThreatRadar()
    anomalies = tr.scan()
    prio = {1: "🔴 CRÍTICO", 2: "🟡 SUSPEITO", 3: "🔵 ATENÇÃO"}
    print(f"ThreatRadar — {len(anomalies)} anomalia(s)\n")
    if not anomalies:
        print("✓ Nenhuma anomalia detectada.")
    for a in anomalies:
        print(f"{prio.get(a.severity)} [{a.category}] {a.description}")
        if a.pid:
            print(f"  PID: {a.pid}  Processo: {a.process_name}")
        print(f"  → {a.recommendation}")
        print()
