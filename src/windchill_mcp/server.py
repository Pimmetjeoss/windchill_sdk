"""Windchill MCP Server - exposes Windchill SDK as tools for AI agents."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Windchill PLM")

# ── Shared Client (lazy-initialized) ──

_client = None


async def get_client():
    """Return a shared WindchillClient, creating it on first use from env vars."""
    global _client
    if _client is None:
        from windchill import WindchillClient, WindchillConfig

        config = WindchillConfig.from_env()
        _client = WindchillClient(config)
    return _client


# ── Register tool modules (side-effect imports register @mcp.tool decorators) ──

import windchill_mcp.tools.admin  # noqa: E402, F401
import windchill_mcp.tools.changes  # noqa: E402, F401
import windchill_mcp.tools.documents  # noqa: E402, F401
import windchill_mcp.tools.parts  # noqa: E402, F401
import windchill_mcp.tools.quality  # noqa: E402, F401
import windchill_mcp.tools.search  # noqa: E402, F401
import windchill_mcp.tools.spm  # noqa: E402, F401
import windchill_mcp.tools.workflow  # noqa: E402, F401

# ── Register resource modules ──

import windchill_mcp.resources.schema  # noqa: E402, F401


def main():
    """Run the MCP server via stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
