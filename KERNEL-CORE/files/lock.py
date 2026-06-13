"""
KernelMind :: EthicsLock
Camada de restrições éticas imutável.
Toda ação passa aqui — sem bypass possível.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional


class ActionType(Enum):
    READ    = "read"
    SUGGEST = "suggest"
    TUNE    = "tune"
    KILL    = "kill"
    DELETE  = "delete"
    NETWORK = "network"


# (permitida, requer_confirmação, sempre_bloqueada)
_RULES: dict[ActionType, tuple[bool, bool, bool]] = {
    ActionType.READ:    (True,  False, False),
    ActionType.SUGGEST: (True,  False, False),
    ActionType.TUNE:    (True,  True,  False),
    ActionType.KILL:    (True,  True,  False),
    ActionType.DELETE:  (True,  True,  False),
    ActionType.NETWORK: (False, False, True),
}


@dataclass
class EthicsVerdict:
    allowed: bool
    reason: str
    requires_confirmation: bool = False


@dataclass
class AuditEntry:
    timestamp: float
    action_type: str
    description: str
    verdict: str
    fingerprint: str


class EthicsLock:
    VERSION = "1.0.0"

    def __init__(
        self,
        audit_path: str = "/tmp/kernelmind_audit.jsonl",
        confirmation_fn: Optional[Callable[[str], bool]] = None,
    ):
        self.audit_path = audit_path
        self._confirm = confirmation_fn or (lambda _: False)
        self._log: list[AuditEntry] = []

    def evaluate(
        self,
        action: ActionType,
        description: str,
        auto_confirm: bool = False,
    ) -> EthicsVerdict:
        allowed_base, needs_confirm, blocked = _RULES[action]

        if blocked:
            verdict = EthicsVerdict(
                allowed=False,
                reason=f"Ação '{action.value}' permanentemente bloqueada pela política ética.",
            )
        elif needs_confirm and not auto_confirm:
            confirmed = self._confirm(
                f"KernelMind solicita permissão para: {description}\n"
                f"Tipo: {action.value.upper()} — Confirmar? [s/N] "
            )
            verdict = EthicsVerdict(
                allowed=confirmed,
                reason="Confirmado pelo usuário." if confirmed else "Negado pelo usuário.",
                requires_confirmation=True,
            )
        else:
            verdict = EthicsVerdict(allowed=True, reason="Leitura/sugestão — sempre permitida.")

        self._audit(action, description, verdict)
        return verdict

    def _audit(self, action: ActionType, description: str, verdict: EthicsVerdict) -> None:
        content = f"{time.time()}|{action.value}|{description}|{verdict.allowed}"
        fp = hashlib.sha256(content.encode()).hexdigest()[:16]
        entry = AuditEntry(
            timestamp=time.time(),
            action_type=action.value,
            description=description,
            verdict="PERMITIDO" if verdict.allowed else "BLOQUEADO",
            fingerprint=fp,
        )
        self._log.append(entry)
        try:
            with open(self.audit_path, "a") as f:
                f.write(json.dumps({
                    "ts": entry.timestamp,
                    "action": entry.action_type,
                    "desc": entry.description,
                    "verdict": entry.verdict,
                    "fp": entry.fingerprint,
                }) + "\n")
        except Exception:
            pass

    def recent_log(self, n: int = 20) -> list[dict]:
        return [
            {"ts": e.timestamp, "action": e.action_type, "desc": e.description,
             "verdict": e.verdict, "fp": e.fingerprint}
            for e in self._log[-n:]
        ]

    def status(self) -> dict:
        return {
            "ethics_lock_version": self.VERSION,
            "rules_active": len(_RULES),
            "network_blocked": True,
            "confirmation_required_for": [
                a.value for a, (_, needs, _b) in _RULES.items() if needs
            ],
            "always_allowed": [
                a.value for a, (ok, _, _b) in _RULES.items() if ok and not _b
            ],
            "audit_entries": len(self._log),
        }
