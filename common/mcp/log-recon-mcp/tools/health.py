"""Health tool for server liveness checks."""

from datetime import datetime, timezone

from mcp_app import mcp


@mcp.tool(name="health")
def health() -> dict[str, str]:
    """Ping server health/liveness for readiness checks.

    When to use:
    - Service readiness/liveness probes.
    - Fast smoke checks before running other tools.
    - Monitoring endpoints that need a lightweight status signal.

    When not to use:
    - Deep diagnostics or dependency checks.
    - Performance, capacity, or functional validation.
    - Any workflow requiring details beyond basic availability.
    """
    return {
        "status": "ok",
        "service": "log-recon-mcp",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
