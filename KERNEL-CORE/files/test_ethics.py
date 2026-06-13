"""Tests for EthicsLock."""
import pytest
from kernelmind.ethics.lock import EthicsLock, ActionType


@pytest.fixture
def lock_deny():
    return EthicsLock(audit_path="/tmp/km_test_audit.jsonl",
                      confirmation_fn=lambda _: False)


@pytest.fixture
def lock_allow():
    return EthicsLock(audit_path="/tmp/km_test_audit.jsonl",
                      confirmation_fn=lambda _: True)


def test_read_always_allowed(lock_deny):
    assert lock_deny.evaluate(ActionType.READ, "test").allowed is True


def test_suggest_always_allowed(lock_deny):
    assert lock_deny.evaluate(ActionType.SUGGEST, "test").allowed is True


def test_network_always_blocked(lock_allow):
    assert lock_allow.evaluate(ActionType.NETWORK, "test").allowed is False


def test_tune_denied(lock_deny):
    v = lock_deny.evaluate(ActionType.TUNE, "test")
    assert v.allowed is False
    assert v.requires_confirmation is True


def test_tune_allowed(lock_allow):
    assert lock_allow.evaluate(ActionType.TUNE, "test").allowed is True


def test_kill_denied(lock_deny):
    assert lock_deny.evaluate(ActionType.KILL, "test").allowed is False


def test_delete_denied(lock_deny):
    assert lock_deny.evaluate(ActionType.DELETE, "test").allowed is False


def test_audit_grows(lock_deny):
    n = len(lock_deny.recent_log())
    lock_deny.evaluate(ActionType.READ, "a")
    lock_deny.evaluate(ActionType.READ, "b")
    assert len(lock_deny.recent_log()) >= n + 2


def test_fingerprint_present(lock_deny):
    lock_deny.evaluate(ActionType.READ, "fp test")
    entry = lock_deny.recent_log()[-1]
    assert "fp" in entry
    assert len(entry["fp"]) == 16


def test_status_structure(lock_deny):
    st = lock_deny.status()
    assert st["network_blocked"] is True
    assert "tune" in st["confirmation_required_for"]
    assert "kill" in st["confirmation_required_for"]
    assert "delete" in st["confirmation_required_for"]
