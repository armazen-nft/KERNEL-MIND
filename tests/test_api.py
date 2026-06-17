from kernelmind.api import server


def test_health_endpoint():
    payload = server.health()

    assert payload["status"] == "ok"
    assert payload["ethics_lock"] == "active"


def test_ethics_status_endpoint_exposes_policy():
    payload = server.ethics_status()

    assert payload["network_blocked"] is True
    assert "tune" in payload["confirmation_required_for"]


def test_snapshot_endpoint_returns_expected_shape():
    payload = server.snapshot()

    assert {"timestamp", "kernel", "cpu", "memory", "disks", "top_processes"} <= payload.keys()
    assert "percent" in payload["cpu"]
    assert "total_mb" in payload["memory"]
    assert server.ethics.status()["audit_entries"] >= 1
