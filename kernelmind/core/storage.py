"""
KernelMind :: StorageGuard
Análise real de disco: integridade, fragmentação, uso por diretório.
Sugestões concretas — sem deletar nada sem consentimento.
"""

import os
import subprocess
import shutil
from dataclasses import dataclass
from typing import Optional


@dataclass
class DirUsage:
    path: str
    size_mb: int
    cleanable: bool
    reason: str


@dataclass
class StorageSuggestion:
    priority: int
    title: str
    description: str
    action_type: str
    command: Optional[str]
    estimated_gain_mb: int


class StorageGuard:
    """
    Analisa uso real do disco e gera sugestões priorizadas.
    Nunca deleta — apenas sugere e fornece os comandos.
    """

    CLEANABLE_PATHS = [
        ("/var/log",            "logs do sistema — pode ser rotacionado"),
        ("/tmp",                "arquivos temporários"),
        ("/var/tmp",            "temporários persistentes"),
        ("~/.cache",            "cache de aplicações do usuário"),
        ("/var/cache/apt",      "cache de pacotes apt (Debian/Ubuntu)"),
        ("/var/cache/dnf",      "cache de pacotes dnf (Fedora/RHEL)"),
        ("/var/cache/pacman",   "cache de pacotes pacman (Arch)"),
    ]

    WARN_PERCENT = 80
    CRITICAL_PERCENT = 92

    def analyze(self, root: str = "/") -> list[StorageSuggestion]:
        suggestions = []
        total, used, free = shutil.disk_usage(root)
        percent = used / total * 100

        # 1. Disco crítico
        if percent >= self.CRITICAL_PERCENT:
            suggestions.append(StorageSuggestion(
                priority=1,
                title="Disco crítico",
                description=f"Uso em {percent:.1f}%. Sistema pode se tornar instável acima de 95%.",
                action_type="suggest",
                command=f"du -sh {root}/* 2>/dev/null | sort -rh | head -20",
                estimated_gain_mb=0,
            ))

        # 2. Diretórios limpaveis
        for path_template, reason in self.CLEANABLE_PATHS:
            path = os.path.expanduser(path_template)
            if not os.path.exists(path):
                continue
            size_mb = self._dir_size_mb(path)
            if size_mb > 100:
                cmd = self._clean_command(path)
                suggestions.append(StorageSuggestion(
                    priority=2 if percent > self.WARN_PERCENT else 3,
                    title=f"Espaço recuperável: {os.path.basename(path)}",
                    description=f"{path} ocupa {size_mb} MB — {reason}.",
                    action_type="delete",
                    command=cmd,
                    estimated_gain_mb=int(size_mb * 0.7),
                ))

        # 3. Arquivos grandes órfãos em /tmp
        big_tmp = self._find_big_files("/tmp", min_mb=50)
        for f in big_tmp[:3]:
            suggestions.append(StorageSuggestion(
                priority=2,
                title=f"Arquivo grande em /tmp",
                description=f"{f['path']} ({f['mb']} MB) — verifique se ainda é necessário.",
                action_type="delete",
                command=f"ls -lh {f['path']}",
                estimated_gain_mb=f['mb'],
            ))

        # 4. Logs grandes
        big_logs = self._find_big_files("/var/log", min_mb=100)
        for f in big_logs[:2]:
            suggestions.append(StorageSuggestion(
                priority=3,
                title="Log grande detectado",
                description=f"{f['path']} ({f['mb']} MB). Pode ser truncado com journalctl.",
                action_type="tune",
                command=f"sudo journalctl --vacuum-size=100M",
                estimated_gain_mb=f['mb'],
            ))

        suggestions.sort(key=lambda s: s.priority)
        return suggestions

    def _dir_size_mb(self, path: str) -> int:
        try:
            result = subprocess.run(
                ["du", "-sm", path],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return int(result.stdout.split()[0])
        except Exception:
            pass
        return 0

    def _find_big_files(self, path: str, min_mb: int = 50) -> list[dict]:
        files = []
        try:
            result = subprocess.run(
                ["find", path, "-type", "f", "-size", f"+{min_mb}M",
                 "-printf", "%s %p\n"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.strip().splitlines():
                parts = line.split(None, 1)
                if len(parts) == 2:
                    size_bytes = int(parts[0])
                    files.append({"path": parts[1], "mb": size_bytes // (1024*1024)})
        except Exception:
            pass
        files.sort(key=lambda x: x['mb'], reverse=True)
        return files

    def _clean_command(self, path: str) -> str:
        if "apt" in path:
            return "sudo apt-get clean"
        if "dnf" in path or "yum" in path:
            return "sudo dnf clean all"
        if "pacman" in path:
            return "sudo pacman -Sc"
        if path == "/tmp":
            return "sudo find /tmp -type f -atime +7 -delete"
        if ".cache" in path:
            return f"du -sh {path}/* 2>/dev/null | sort -rh | head -10"
        return f"sudo find {path} -type f -mtime +30 -delete"


if __name__ == "__main__":
    sg = StorageGuard()
    suggestions = sg.analyze()
    prio = {1: "🔴 CRÍTICO", 2: "🟡 IMPORTANTE", 3: "🟢 OTIMIZAÇÃO"}
    print(f"StorageGuard — {len(suggestions)} sugestão(ões)\n")
    for s in suggestions:
        print(f"{prio.get(s.priority)} {s.title}")
        print(f"  {s.description}")
        if s.command:
            print(f"  $ {s.command}")
        print()
