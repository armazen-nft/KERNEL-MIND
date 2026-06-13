"""
KernelMind :: MemoryWeaver
Analisa RAM real e gera sugestões concretas e acionáveis.
Não age — sugere. A ação requer EthicsLock + confirmação humana.
"""

import os
import subprocess
from dataclasses import dataclass
from typing import Optional

import psutil


@dataclass
class MemorySuggestion:
    priority: int          # 1=crítico, 2=importante, 3=otimização
    title: str
    description: str
    action_type: str       # read | suggest | tune | kill | delete
    command: Optional[str] # comando que o usuário pode executar
    estimated_gain_mb: int


class MemoryWeaver:
    """
    Analisa o estado da memória e produz sugestões priorizadas.
    Cada sugestão é auditável, reversível e requer consentimento.
    """

    CRITICAL_PERCENT = 90
    WARN_PERCENT = 75
    SWAP_WARN_PERCENT = 40

    def analyze(self) -> list[MemorySuggestion]:
        suggestions = []
        vm = psutil.virtual_memory()
        sw = psutil.swap_memory()

        # 1. Estado crítico de RAM
        if vm.percent >= self.CRITICAL_PERCENT:
            top = self._top_consumers(3)
            suggestions.append(MemorySuggestion(
                priority=1,
                title="RAM crítica",
                description=f"Uso em {vm.percent:.1f}%. Processos maiores: "
                            + ", ".join(f"{p['name']}({p['mb']}MB)" for p in top),
                action_type="kill",
                command=None,  # requer seleção do usuário
                estimated_gain_mb=sum(p['mb'] for p in top[:2]),
            ))

        # 2. Page cache — pode ser liberado com segurança
        cached_mb = getattr(vm, 'cached', 0) // (1024*1024)
        buffers_mb = getattr(vm, 'buffers', 0) // (1024*1024)
        if cached_mb + buffers_mb > 500:
            suggestions.append(MemorySuggestion(
                priority=2 if vm.percent > self.WARN_PERCENT else 3,
                title="Cache de página liberável",
                description=f"{cached_mb + buffers_mb} MB em cache/buffers do kernel. "
                            f"Pode ser liberado sem perda de dados.",
                action_type="tune",
                command="sudo sh -c 'sync; echo 1 > /proc/sys/vm/drop_caches'",
                estimated_gain_mb=int((cached_mb + buffers_mb) * 0.6),
            ))

        # 3. Swap elevado
        if sw.total > 0 and sw.percent >= self.SWAP_WARN_PERCENT:
            suggestions.append(MemorySuggestion(
                priority=2,
                title="Swap elevado",
                description=f"Swap em {sw.percent:.1f}% ({sw.used//(1024*1024)} MB). "
                            f"Sistema usando disco como memória — desempenho degradado.",
                action_type="suggest",
                command=None,
                estimated_gain_mb=0,
            ))

        # 4. Swappiness alta (Linux)
        swappiness = self._read_kernel_param("vm.swappiness")
        if swappiness is not None and swappiness > 30:
            suggestions.append(MemorySuggestion(
                priority=3,
                title="Swappiness pode ser reduzido",
                description=f"vm.swappiness={swappiness}. Reduzir para 10 mantém "
                            f"mais dados em RAM para notebooks/desktops.",
                action_type="tune",
                command="sudo sysctl vm.swappiness=10",
                estimated_gain_mb=0,
            ))

        # 5. OOM killer candidates
        if vm.percent >= self.WARN_PERCENT:
            oom_candidates = self._oom_candidates(3)
            if oom_candidates:
                suggestions.append(MemorySuggestion(
                    priority=2,
                    title="Candidatos ao OOM killer",
                    description="Processos que o kernel encerraria sob pressão: "
                                + ", ".join(f"{p['name']}(score:{p['oom_score']})"
                                           for p in oom_candidates),
                    action_type="suggest",
                    command=None,
                    estimated_gain_mb=0,
                ))

        suggestions.sort(key=lambda s: s.priority)
        return suggestions

    def _top_consumers(self, n: int) -> list[dict]:
        procs = []
        for p in psutil.process_iter(['name', 'memory_info']):
            try:
                mb = p.info['memory_info'].rss // (1024*1024)
                procs.append({'name': p.info['name'], 'mb': mb, 'pid': p.pid})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        procs.sort(key=lambda x: x['mb'], reverse=True)
        return procs[:n]

    def _oom_candidates(self, n: int) -> list[dict]:
        candidates = []
        try:
            for p in psutil.process_iter(['pid', 'name']):
                try:
                    oom_path = f"/proc/{p.pid}/oom_score"
                    if os.path.exists(oom_path):
                        score = int(open(oom_path).read().strip())
                        if score > 100:
                            candidates.append({'name': p.info['name'],
                                               'pid': p.pid, 'oom_score': score})
                except Exception:
                    pass
        except Exception:
            pass
        candidates.sort(key=lambda x: x['oom_score'], reverse=True)
        return candidates[:n]

    def _read_kernel_param(self, param: str) -> Optional[int]:
        try:
            result = subprocess.run(
                ['sysctl', '-n', param],
                capture_output=True, text=True, timeout=2
            )
            return int(result.stdout.strip())
        except Exception:
            return None


if __name__ == "__main__":
    mw = MemoryWeaver()
    suggestions = mw.analyze()
    print(f"=== MemoryWeaver — {len(suggestions)} sugestão(ões) ===\n")
    for s in suggestions:
        prio_label = {1: "🔴 CRÍTICO", 2: "🟡 IMPORTANTE", 3: "🟢 OTIMIZAÇÃO"}
        print(f"{prio_label.get(s.priority, '⚪')} {s.title}")
        print(f"   {s.description}")
        if s.command:
            print(f"   Comando: {s.command}")
        if s.estimated_gain_mb:
            print(f"   Ganho estimado: ~{s.estimated_gain_mb} MB")
        print()
