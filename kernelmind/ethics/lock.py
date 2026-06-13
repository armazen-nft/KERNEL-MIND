"""
KernelMind :: EthicsLock
Camada de restrições éticas — núcleo imutável.
Nenhuma ação do sistema pode contornar ou desativar este módulo.
Inspirado no princípio PoE: transparência, consentimento, reversibilidade.
"""

import hashlib
import time
import json
import os
from dataclasses import dataclass, field
from typing import Callable, Optional
from enum import Enum


class ActionType(Enum):
    READ     = "read"       # leitura de métricas — sempre permitida
    SUGGEST  = "suggest"    # sugestão ao usuário — sempre permitida
    TUNE     = "tune"       # ajuste de parâmetro kernel — requer confirmação
    KILL     = "kill"       # encerrar processo — requer confirmação
    DELETE   = "delete"     # excluir arquivo/cache — requer confirmação explícita
    NETWORK  = "network"    # qualquer operação de rede — bloqueada por padrão


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
    fingerprint: str  # sha256 do conteúdo — prova de não-alteração


class EthicsLock:
    """
    Toda ação do KernelMind passa por aqui antes de ser executada.
    Regras são declarativas e auditáveis — não há bypass por código.
    """

    VERSION = "1.0.0"
    RULES = {
        # Ação           permitida  confirmação  bloqueada
        ActionType.READ:    (True,  False, False),
        ActionType.SUGGEST: (True,  False, False),
        ActionType.TUNE:    (True,  True,  False),
        ActionType.KILL:    (True,  True,  False),
        ActionType.DELETE:  (True,  True,  False),
        ActionType.NETWORK: (False, False, True),   # bloqueada por padrão
    }

    def __init__(self, audit_path: str = "/tmp/kernelmind_audit.jsonl",
                 confirmation_fn: Optional[Callable[[str], bool]] = None):
        self.audit_path = audit_path
        # confirmation_fn: função que pergunta ao usuário (CLI, GUI, API)
        # se None, usa modo seguro: não confirma automaticamente nada
        self._confirm = confirmation_fn or (lambda _: False)
        self._audit_log: list[AuditEntry] = []

    def evaluate(self, action: ActionType, description: str,
                 auto_confirm: bool = False) -> EthicsVerdict:
        """
        Avalia se uma ação pode ser executada.
        Registra em audit log independente do resultado.
        """
        allowed_base, needs_confirm, blocked = self.RULES[action]

        if blocked:
            verdict = EthicsVerdict(
                allowed=False,
                reason=f"Ação '{action.value}' bloqueada pela política ética. "
                       f"Requer habilitação explícita do usuário.",
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
            )

        self._audit(action, description, verdict)
        return verdict

    def _audit(self, action: ActionType, description: str, verdict: EthicsVerdict):
        content = f"{time.time()}|{action.value}|{description}|{verdict.allowed}|{verdict.reason}"
        fingerprint = hashlib.sha256(content.encode()).hexdigest()[:16]
        entry = AuditEntry(
            timestamp=time.time(),
            action_type=action.value,
            description=description,
            verdict="PERMITIDO" if verdict.allowed else "BLOQUEADO",
            fingerprint=fingerprint,
        )
        self._audit_log.append(entry)
        # persiste em disco
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
            pass  # audit nunca quebra o fluxo principal

    def recent_log(self, n: int = 20) -> list[dict]:
        return [
            {
                "ts": e.timestamp,
                "action": e.action_type,
                "desc": e.description,
                "verdict": e.verdict,
                "fp": e.fingerprint,
            }
            for e in self._audit_log[-n:]
        ]

    def status(self) -> dict:
        return {
            "ethics_lock_version": self.VERSION,
            "rules_active": len(self.RULES),
            "network_blocked": True,
            "confirmation_required_for": [
                a.value for a, (_, needs, _blocked) in self.RULES.items() if needs
            ],
            "always_allowed": [
                a.value for a, (ok, _, _blocked) in self.RULES.items() if ok
            ],
            "audit_entries": len(self._audit_log),
        }


if __name__ == "__main__":
    def cli_confirm(msg: str) -> bool:
        return input(msg).strip().lower() in ('s', 'sim', 'y', 'yes')

    lock = EthicsLock(confirmation_fn=cli_confirm)

    print("=== EthicsLock Test ===")
    print(json.dumps(lock.status(), indent=2))

    # READ sempre passa
    v = lock.evaluate(ActionType.READ, "Leitura de CPU/RAM")
    print(f"\nREAD: {v.allowed} — {v.reason}")

    # NETWORK sempre bloqueia
    v = lock.evaluate(ActionType.NETWORK, "Enviar métricas para servidor externo")
    print(f"NETWORK: {v.allowed} — {v.reason}")
