import subprocess
import sys

from kernelmind.mcp.tool import TOOLS, kernel_ethics_status

EXPECTED_TOOLS = {
    "kernel_snapshot",
    "kernel_memory_suggest",
    "kernel_storage_suggest",
    "kernel_threat_scan",
    "kernel_ethics_status",
}


def test_cli_help_runs():
    result = subprocess.run(
        [sys.executable, "-m", "kernelmind.cli.km", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "KernelMind CLI" in result.stdout
    assert "storage" in result.stdout
    assert "threat" in result.stdout


def test_mcp_registry_lists_expected_tools():
    assert EXPECTED_TOOLS <= set(TOOLS)
    for tool in EXPECTED_TOOLS:
        assert TOOLS[tool]["inputSchema"]["type"] == "object"
        assert callable(TOOLS[tool]["fn"])


def test_mcp_ethics_status_is_safe_and_structured():
    payload = kernel_ethics_status({})

    assert payload["status"]["network_blocked"] is True
    assert isinstance(payload["recent_log"], list)
