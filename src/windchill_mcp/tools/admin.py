"""Administration tools for Windchill MCP Server."""

from __future__ import annotations

import json

from windchill.odata.filter import F
from windchill.odata.query import Query

from windchill_mcp.server import get_client, mcp


@mcp.tool()
async def windchill_list_containers() -> str:
    """List all accessible containers (Products, Libraries, Projects).

    Containers are the top-level organizational structures in Windchill.
    Use container IDs when creating parts, documents, or other objects
    to specify where they should be stored.

    Returns:
        JSON array of containers with ID, Name, Type, and other properties.
    """
    try:
        client = await get_client()
        result = await client.data_admin.list_containers()
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_list_folders(container_id: str) -> str:
    """List folders within a specific container.

    Args:
        container_id: The Object Reference ID of the container.
            Use windchill_list_containers to find container IDs.

    Returns:
        JSON array of folders within the container.
    """
    try:
        client = await get_client()
        query = Query().filter(
            F.raw(f"Context@odata.bind eq 'Containers(\\'{container_id}\\')'")
        )
        result = await client.data_admin.list_folders(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_search_users(
    name: str | None = None,
    top: int = 50,
) -> str:
    """Search for users in Windchill.

    Args:
        name: Name or partial name to search for. If omitted, lists all users.
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of matching users with ID, Name, Email, and other properties.
    """
    try:
        client = await get_client()
        if name:
            query = Query().top(top)
            result = await client.principal_mgmt.search_users(name, query=query)
        else:
            query = Query().top(top)
            result = await client.principal_mgmt.list_users(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_get_lifecycle_states(template_name: str) -> str:
    """Get all lifecycle states for a given lifecycle template.

    Lifecycle templates define the valid states and transitions for
    objects (e.g., INWORK -> UNDERREVIEW -> RELEASED).

    Args:
        template_name: Name of the lifecycle template (e.g. "Basic",
            "Default Lifecycle").

    Returns:
        JSON array of lifecycle states with their properties.
    """
    try:
        client = await get_client()
        result = await client.common.get_lifecycle_states(template_name)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_set_lifecycle_state(
    entity_set: str,
    entity_id: str,
    state: str,
) -> str:
    """Set the lifecycle state of any Windchill entity.

    This is a generic lifecycle state setter that works with any entity
    type. For parts specifically, prefer windchill_set_part_state.

    Args:
        entity_set: The OData entity set name (e.g. "Parts", "Documents",
            "ChangeRequests", "ChangeNotices", "ProblemReports").
        entity_id: The Object Reference ID of the entity.
        state: Target lifecycle state name (e.g. "INWORK", "RELEASED",
            "APPROVED", "CANCELLED").

    Returns:
        JSON object confirming the state change.
    """
    try:
        client = await get_client()
        result = await client.common.set_lifecycle_state(
            entity_set, entity_id, state
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
