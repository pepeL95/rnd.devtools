"""Workspace handoff instructions tool."""

import os
from pathlib import Path

from mcp_app import mcp

WORKSPACE_ROOT_ENV_VAR = "LOG_EFFICIENT_MCP_WORKSPACE_ROOT"
WORKSPACE_MARKERS = (".git", "HANDOFF.md", ".hg", ".svn")

def _find_workspace_root(start: Path) -> Path | None:
    """Walk upward from `start` until a likely workspace root marker is found."""
    current = start.resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in WORKSPACE_MARKERS):
            return candidate
    return None

def _resolve_workspace_root() -> Path:
    """Resolve the best workspace root for locating HANDOFF.md."""
    env_root = os.environ.get(WORKSPACE_ROOT_ENV_VAR, "").strip()
    if env_root:
        return Path(env_root).expanduser().resolve()

    cwd_root = _find_workspace_root(Path.cwd())
    if cwd_root is not None:
        return cwd_root

    module_root = _find_workspace_root(Path(__file__))
    if module_root is not None:
        return module_root

    return Path.cwd().resolve()

@mcp.tool(name="handoffInstructions")
def handoff_instructions() -> str:
    """Collect any final human instructions before you end your turn.

    Always call this tool immediately before finishing a session turn, but after you have completed your tasks and responded, to check for residual user instructions.
    Skip it only if the user explicitly says not to call `handoffInstructions`.

    Use this tool to:
    - Ask the human for any last instructions or corrections.
    - Then follow those instructions, immediately, before ending your turn.

    Input:
    - None. This tool does not take any input parameters.

    Output:
    - `instructions`: the instruction text the agent must follow next.
    """
    workspace_root = _resolve_workspace_root()
    handoff_path = workspace_root / "HANDOFF.md"
    if not handoff_path.exists():
        return "No instruction provided .. ending turn without handoff instructions."

    instructions = handoff_path.read_text(encoding="utf-8").strip()
    if not instructions:
        return "No instruction provided .. ending turn without handoff instructions."

    return f"User >> {instructions}"
