"""FastMCP server entrypoint for log-efficient-mcp."""

from mcp_app import mcp
from tools import health, log_explore, script_runna

__all__ = ["mcp", "log_explore", "script_runna", "health"]


if __name__ == "__main__":
    # Default transport is STDIO, which is ideal for local MCP clients.
    mcp.run()
