"""
KernelMind :: EthicsLock
Camada de restrições éticas — núcleo de política dos módulos oficiais.
Nenhuma ação oficial do sistema deve contornar ou desativar este módulo.
Inspirado no princípio PoE: transparência, consentimento, reversibilidade.
"""

import hashlib
import json
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Optional


class ActionType(Enum):
    READ = "read"  # leitura de métricas — sempre permitida
    SUGGEST = "suggest"  # sugestão ao usuário — sempre permitida
    TUNE = "tune"  # ajuste de parâmetro kernel — requer confirmação
    KILL = "kill"  # encerrar processo — requer confirmação
    DELETE = "delete"  # excluir arquivo/cache — requer confirmação explícita
    NETWORK = "network"  # qualquer operação de rede — bloqueada por padrão


@dataclass
class EthicsVerdict:
    allowed: bool
    reason: str
    requires_confirmation: bool = False
    log_entry: Optional[str] = None


@dataclass
class AuditEntry:
    timestamp: float
    action_type: str
    description: str
    verdict: str
    fingerprint: str
    previous_fingerprint: Optional[str] = None


class EthicsLock:
    """
    Toda ação oficial do KernelMind passa por aqui antes de ser executada.
    Regras são declarativas e auditáveis; ações destrutivas exigem consentimento.
    """

    VERSION = "1.0.0"
    RULES = {
        # Ação           permitida  confirmação  bloqueada
        ActionType.READ: (True, False, False),
        ActionType.SUGGEST: (True, False, False),
        ActionType.TUNE: (True, True, False),
        ActionType.KILL: (True, True, False),
        ActionType.DELETE: (True, True, False),
        ActionType.NETWORK: (False, False, True),  # bloqueada por padrão
    }

    def __init__(
        self,
        audit_path: str = "/tmp/kernelmind_audit.jsonl",
        confirmation_fn: Optional[Callable[[str], bool]] = None,
    ):
        self.audit_path = audit_path
        # confirmation_fn: função que pergunta ao usuário (CLI, GUI, API).
        # Se None, usa modo seguro: não confirma automaticamente nada.
        self._confirm = confirmation_fn or (lambda _: False)
        self._audit_log: list[AuditEntry] = []
        self._last_fingerprint: Optional[str] = None

    def evaluate(
        self,
        action: ActionType,
        description: str,
        auto_confirm: bool = False,
    ) -> EthicsVerdict:
        """
        Avalia se uma ação pode ser executada.
        Registra em audit log independente do resultado.
        """
        allowed_base, needs_confirm, blocked = self.RULES[action]

        if blocked:
            verdict = EthicsVerdict(
                allowed=False,
                reason=(
                    f"Ação '{action.value}' bloqueada pela política ética. "
                    "Requer habilitação explícita do usuário."
                ),
                requires_confirmation=False,
            )
        elif needs_confirm and not auto_confirm:
            confirmed = self._confirm(
                f"KernelMind solicita permissão para: {description}\n"
                f"Tipo: {action.value.upper()} | Confirmar? [s/N] "
            )
            verdict = EthicsVerdict(
                allowed=confirmed,
                reason="Confirmado pelo usuário." if confirmed else "Negado pelo usuário.",
                requires_confirmation=True,
            )
        else:
            verdict = EthicsVerdict(
                allowed=allowed_base,
                reason="Ação de leitura/sugestão — sempre permitida.",
                requires_confirmation=needs_confirm,
            )

        entry = self._audit(action, description, verdict)
        verdict.log_entry = entry.fingerprint
        return verdict

    def _audit(self, action: ActionType, description: str, verdict: EthicsVerdict) -> AuditEntry:
        timestamp = time.time()
        previous = self._last_fingerprint
        content = {
            "ts": timestamp,
            "action": action.value,
            "desc": description,
            "allowed": verdict.allowed,
            "reason": verdict.reason,
            "prev_fp": previous,
        }
        fingerprint = hashlib.sha256(
            json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        entry = AuditEntry(
            timestamp=timestamp,
            action_type=action.value,
            description=description,
            verdict="PERMITIDO" if verdict.allowed else "BLOQUEADO",
            fingerprint=fingerprint,
            previous_fingerprint=previous,
        )
        self._audit_log.append(entry)
        self._last_fingerprint = fingerprint

        try:
            path = Path(self.audit_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as audit_file:
                audit_file.write(json.dumps(self._entry_to_dict(entry), ensure_ascii=False) + "\n")
                audit_file.flush()
        except OSError:
            # A auditoria em memória permanece disponível; falhas de filesystem
            # não devem mascarar o veredito ético já calculado.
            pass

        return entry

    def _entry_to_dict(self, entry: AuditEntry) -> dict:
        return {
            "ts": entry.timestamp,
            "action": entry.action_type,
            "desc": entry.description,
            "verdict": entry.verdict,
            "fp": entry.fingerprint,
            "prev_fp": entry.previous_fingerprint,
        }

    def recent_log(self, n: int = 20) -> list[dict]:
        return [self._entry_to_dict(entry) for entry in self._audit_log[-n:]]

    def status(self) -> dict:
        return {
            "ethics_lock_version": self.VERSION,
            "rules_active": len(self.RULES),
            "network_blocked": True,
            "confirmation_required_for": [
                action.value for action, (_, needs, _blocked) in self.RULES.items() if needs
            ],
            "always_allowed": [
                action.value
                for action, (ok, needs, _blocked) in self.RULES.items()
                if ok and not needs
            ],
            "audit_entries": len(self._audit_log),
            "last_fingerprint": self._last_fingerprint,
        }


if __name__ == "__main__":

    def cli_confirm(msg: str) -> bool:
        return input(msg).strip().lower() in ("s", "sim", "y", "yes")

    lock = EthicsLock(confirmation_fn=cli_confirm)

    print("=== EthicsLock Test ===")
    print(json.dumps(lock.status(), indent=2))

    # READ sempre passa
    v = lock.evaluate(ActionType.READ, "Leitura de CPU/RAM")
    print(f"\nREAD: {v.allowed} — {v.reason}")

    # NETWORK sempre bloqueia
    v = lock.evaluate(ActionType.NETWORK, "Enviar métricas para servidor externo")
    print(f"NETWORK: {v.allowed} — {v.reason}")
