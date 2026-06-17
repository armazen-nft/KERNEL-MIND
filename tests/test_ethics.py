import json

from kernelmind.ethics.lock import ActionType, EthicsLock


def test_read_and_suggest_are_allowed(tmp_path):
    lock = EthicsLock(audit_path=str(tmp_path / "audit.jsonl"))

    read = lock.evaluate(ActionType.READ, "ler métricas")
    suggest = lock.evaluate(ActionType.SUGGEST, "sugerir otimização")

    assert read.allowed is True
    assert suggest.allowed is True
    assert read.log_entry
    assert suggest.log_entry


def test_network_is_always_blocked_even_with_auto_confirm(tmp_path):
    lock = EthicsLock(
        audit_path=str(tmp_path / "audit.jsonl"),
        confirmation_fn=lambda _msg: True,
    )

    verdict = lock.evaluate(ActionType.NETWORK, "enviar métricas", auto_confirm=True)

    assert verdict.allowed is False
    assert verdict.requires_confirmation is False


def test_destructive_actions_require_human_confirmation(tmp_path):
    denied = EthicsLock(
        audit_path=str(tmp_path / "denied.jsonl"),
        confirmation_fn=lambda _msg: False,
    )
    allowed = EthicsLock(
        audit_path=str(tmp_path / "allowed.jsonl"),
        confirmation_fn=lambda _msg: True,
    )

    assert denied.evaluate(ActionType.TUNE, "ajustar kernel").allowed is False
    assert allowed.evaluate(ActionType.KILL, "encerrar processo").allowed is True
    assert allowed.evaluate(ActionType.DELETE, "limpar cache").requires_confirmation is True


def test_audit_log_is_persisted_and_hash_chained(tmp_path):
    audit_path = tmp_path / "audit.jsonl"
    lock = EthicsLock(audit_path=str(audit_path))

    first = lock.evaluate(ActionType.READ, "snapshot")
    second = lock.evaluate(ActionType.SUGGEST, "memory")

    entries = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines()]

    assert len(entries) == 2
    assert entries[0]["fp"] == first.log_entry
    assert entries[1]["fp"] == second.log_entry
    assert entries[1]["prev_fp"] == entries[0]["fp"]
    assert len(entries[0]["fp"]) == 64


def test_status_reports_active_policy(tmp_path):
    lock = EthicsLock(audit_path=str(tmp_path / "audit.jsonl"))
    lock.evaluate(ActionType.READ, "status warmup")

    status = lock.status()

    assert status["network_blocked"] is True
    assert set(status["confirmation_required_for"]) == {"tune", "kill", "delete"}
    assert "read" in status["always_allowed"]
    assert status["audit_entries"] == 1
    assert status["last_fingerprint"]
