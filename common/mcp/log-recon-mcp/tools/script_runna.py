"""Script runner tool with context-window aware return modes."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Literal

from mcp_app import mcp


def _resolve_script_log_dir(requested_dir: str) -> tuple[Path, bool]:
    target = Path(requested_dir).expanduser()
    try:
        target.mkdir(parents=True, exist_ok=True)
        return target.resolve(), False
    except OSError:
        fallback = Path("/tmp/script-runna/logs")
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback.resolve(), True


@mcp.tool(name="script_runna")
def script_runna(
    script: str,
    output_dir: str = "/temp/script-runna/logs",
    inline_output_epsilon: int = 4000,
    timeout_seconds: int = 1800,
    cwd: str = "",
    return_mode: Literal["auto", "path_only", "inline_only"] = "auto",
) -> dict[str, object]:
    """Run a bash script while controlling context-window impact for agents.

    When to use:
    - Installs, builds, tests, migrations, or commands that may emit large output.
    - Tasks where you need durable logs and controllable inline response size.
    - Multi-step scripts where captured output must be reviewed after execution.

    When not to use:
    - Very short shell checks (`pwd`, `ls`, simple `rg`) better handled directly.
    - Interactive commands requiring a TTY/session input loop.
    - Cases where command output must never be written to disk.

    Agent-oriented guidance:
    - Default to this tool for installs, builds, tests, migrations, or any command likely to emit more than ~50 lines.
    - Prefer this tool over direct shell execution when raw output is not the final deliverable.
    - Use `return_mode="path_only"` for noisy tasks (installs, builds, tests, long logs).
    - Use `return_mode="auto"` for normal tasks; only small outputs are returned inline.
    - Use `return_mode="inline_only"` only when immediate text output is required.
    - For large outputs, chain with `file_reckoning` on the returned `output_file`.
    - Reserve direct shell execution (`exec_command`) for short checks like `pwd`, `ls`, and compact `rg` queries.

    Core behavior:
    - Combined `stdout` + `stderr` is always persisted to a log file.
    - Response payload is controlled by `return_mode` and `inline_output_epsilon`.
    """
    if not script.strip():
        raise ValueError("`script` cannot be empty.")

    inline_output_epsilon = max(0, min(inline_output_epsilon, 200_000))
    timeout_seconds = max(1, min(timeout_seconds, 86_400))

    log_dir, used_fallback_dir = _resolve_script_log_dir(output_dir)
    timestamp_ms = int(time.time() * 1000)
    output_file = log_dir / f"script-{timestamp_ms}.log"

    run_cwd = Path(cwd).expanduser().resolve() if cwd else None
    if run_cwd and not run_cwd.exists():
        raise FileNotFoundError(f"`cwd` does not exist: {run_cwd}")
    if run_cwd and not run_cwd.is_dir():
        raise ValueError(f"`cwd` is not a directory: {run_cwd}")

    timed_out = False
    exit_code = -1
    with output_file.open("w", encoding="utf-8", errors="replace") as out:
        try:
            completed = subprocess.run(
                ["bash", "-lc", script],
                stdout=out,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout_seconds,
                cwd=str(run_cwd) if run_cwd else None,
                check=False,
            )
            exit_code = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            out.write(f"\n[script_runna] timeout after {timeout_seconds}s\n")

    size_bytes = output_file.stat().st_size
    if return_mode == "path_only":
        return {
            "exit_code": exit_code,
            "timed_out": timed_out,
            "output_file": str(output_file),
            "output_size_bytes": size_bytes,
            "used_fallback_output_dir": used_fallback_dir,
            "return_mode": return_mode,
        }

    if return_mode == "auto" and size_bytes <= inline_output_epsilon:
        output = output_file.read_text(encoding="utf-8", errors="replace")
        return {
            "exit_code": exit_code,
            "timed_out": timed_out,
            "output": output,
            "output_size_bytes": size_bytes,
            "output_file": str(output_file),
            "used_fallback_output_dir": used_fallback_dir,
            "return_mode": return_mode,
        }

    if return_mode == "inline_only":
        output = output_file.read_text(encoding="utf-8", errors="replace")
        return {
            "exit_code": exit_code,
            "timed_out": timed_out,
            "output": output,
            "output_size_bytes": size_bytes,
            "output_file": str(output_file),
            "used_fallback_output_dir": used_fallback_dir,
            "return_mode": return_mode,
        }

    return {
        "exit_code": exit_code,
        "timed_out": timed_out,
        "output_file": str(output_file),
        "output_size_bytes": size_bytes,
        "used_fallback_output_dir": used_fallback_dir,
        "return_mode": return_mode,
    }
