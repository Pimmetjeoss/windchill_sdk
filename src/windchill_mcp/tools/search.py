"""Search tools for Windchill MCP Server."""

from __future__ import annotations

import json

from windchill.odata.query import Query

from windchill_mcp.server import get_client, mcp


@mcp.tool()
async def windchill_search(
    keyword: str,
    top: int = 50,
) -> str:
    """Full-text search across all Windchill business objects.

    Searches parts, documents, change objects, and other entities by
    keyword. This is the broadest search available.

    Args:
        keyword: Search keyword or phrase to find across all objects.
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of matching business objects from any domain.
    """
    try:
        client = await get_client()
        query = Query().top(top)
        result = await client.common.search_by_keyword(keyword, query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_execute_saved_search(saved_search_id: str) -> str:
    """Execute a previously saved search and return its results.

    Saved searches are pre-configured queries stored in Windchill.
    Use this to run a saved search by its ID.

    Args:
        saved_search_id: The Object Reference ID of the saved search to execute.

    Returns:
        JSON object containing the search results collection.
    """
    try:
        client = await get_client()
        result = await client.saved_search.execute_saved_search(saved_search_id)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
