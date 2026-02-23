"""FastMCP server entrypoint for log-recon-mcp."""

from mcp_app import mcp
from tools import file_reckoning, health, script_runna

__all__ = ["mcp", "file_reckoning", "script_runna", "health"]


if __name__ == "__main__":
    # Default transport is STDIO, which is ideal for local MCP clients.
    mcp.run()
