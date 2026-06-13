"""
KernelMind :: KernelSense
Leitura real de métricas do sistema via psutil + /proc
Sem simulação. Sem mock. Dados do kernel agora.
"""

import psutil
import os
import time
import platform
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class CPUMetrics:
    percent: float
    freq_mhz: Optional[float]
    cores_logical: int
    cores_physical: int
    load_avg_1m: float
    load_avg_5m: float
    load_avg_15m: float


@dataclass
class MemoryMetrics:
    total_mb: int
    used_mb: int
    available_mb: int
    percent: float
    swap_total_mb: int
    swap_used_mb: int
    swap_percent: float


@dataclass
class DiskMetrics:
    path: str
    total_gb: float
    used_gb: float
    free_gb: float
    percent: float
    read_mb_s: float
    write_mb_s: float


@dataclass
class ProcessSummary:
    pid: int
    name: str
    cpu_percent: float
    mem_mb: float
    status: str


@dataclass
class SystemSnapshot:
    timestamp: float
    os_name: str
    kernel_version: str
    cpu: CPUMetrics
    memory: MemoryMetrics
    disks: list
    top_processes: list
    temperature_c: Optional[float]
    uptime_hours: float


class KernelSense:
    """
    Lê o estado real do sistema operacional.
    Cada chamada a snapshot() retorna dados frescos do kernel.
    """

    def __init__(self, disk_path: str = "/"):
        self.disk_path = disk_path
        self._last_disk_io = None
        self._last_disk_time = None

    def cpu(self) -> CPUMetrics:
        freq = psutil.cpu_freq()
        load = os.getloadavg() if hasattr(os, 'getloadavg') else (0.0, 0.0, 0.0)
        return CPUMetrics(
            percent=psutil.cpu_percent(interval=0.3),
            freq_mhz=round(freq.current, 1) if freq else None,
            cores_logical=psutil.cpu_count(logical=True),
            cores_physical=psutil.cpu_count(logical=False) or 1,
            load_avg_1m=round(load[0], 2),
            load_avg_5m=round(load[1], 2),
            load_avg_15m=round(load[2], 2),
        )

    def memory(self) -> MemoryMetrics:
        vm = psutil.virtual_memory()
        sw = psutil.swap_memory()
        return MemoryMetrics(
            total_mb=vm.total // (1024 * 1024),
            used_mb=vm.used // (1024 * 1024),
            available_mb=vm.available // (1024 * 1024),
            percent=vm.percent,
            swap_total_mb=sw.total // (1024 * 1024),
            swap_used_mb=sw.used // (1024 * 1024),
            swap_percent=sw.percent,
        )

    def disk(self) -> DiskMetrics:
        usage = psutil.disk_usage(self.disk_path)
        read_s, write_s = 0.0, 0.0

        try:
            io_now = psutil.disk_io_counters(perdisk=False)
            t_now = time.monotonic()
            if self._last_disk_io and io_now:
                dt = t_now - self._last_disk_time
                if dt > 0:
                    read_s = (io_now.read_bytes - self._last_disk_io.read_bytes) / dt / (1024*1024)
                    write_s = (io_now.write_bytes - self._last_disk_io.write_bytes) / dt / (1024*1024)
            self._last_disk_io = io_now
            self._last_disk_time = t_now
        except Exception:
            pass

        return DiskMetrics(
            path=self.disk_path,
            total_gb=round(usage.total / (1024**3), 2),
            used_gb=round(usage.used / (1024**3), 2),
            free_gb=round(usage.free / (1024**3), 2),
            percent=usage.percent,
            read_mb_s=round(read_s, 2),
            write_mb_s=round(write_s, 2),
        )

    def temperature(self) -> Optional[float]:
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return None
            for key in ('coretemp', 'cpu_thermal', 'acpitz', 'k10temp'):
                if key in temps and temps[key]:
                    return round(temps[key][0].current, 1)
            # fallback: first available
            first = next(iter(temps.values()))
            if first:
                return round(first[0].current, 1)
        except Exception:
            pass
        return None

    def top_processes(self, n: int = 5) -> list:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status']):
            try:
                info = p.info
                procs.append(ProcessSummary(
                    pid=info['pid'],
                    name=info['name'] or '?',
                    cpu_percent=info['cpu_percent'] or 0.0,
                    mem_mb=round((info['memory_info'].rss if info['memory_info'] else 0) / (1024*1024), 1),
                    status=info['status'] or 'unknown',
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        procs.sort(key=lambda x: x.cpu_percent, reverse=True)
        return procs[:n]

    def snapshot(self) -> SystemSnapshot:
        boot_time = psutil.boot_time()
        uptime_h = round((time.time() - boot_time) / 3600, 2)
        return SystemSnapshot(
            timestamp=time.time(),
            os_name=f"{platform.system()} {platform.version()[:40]}",
            kernel_version=platform.release(),
            cpu=self.cpu(),
            memory=self.memory(),
            disks=[asdict(self.disk())],
            top_processes=[asdict(p) for p in self.top_processes()],
            temperature_c=self.temperature(),
            uptime_hours=uptime_h,
        )


if __name__ == "__main__":
    import json
    ks = KernelSense()
    snap = ks.snapshot()
    print(json.dumps(asdict(snap) if hasattr(snap, '__dataclass_fields__') else snap.__dict__, indent=2, default=str))
