"""Workflow tools for Windchill MCP Server."""

from __future__ import annotations

import json

from windchill.odata.filter import F
from windchill.odata.query import Query

from windchill_mcp.server import get_client, mcp


@mcp.tool()
async def windchill_list_workitems(
    filter_expr: str | None = None,
    top: int = 50,
) -> str:
    """List workflow work items (tasks) in Windchill.

    Work items represent tasks assigned to users as part of workflow
    processes (e.g., review tasks, approval tasks).

    Args:
        filter_expr: OData filter expression (e.g. "Status eq 'ACTIVE'",
            "contains(Name,'review')"). Supports standard OData operators.
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of work items with their properties.
    """
    try:
        client = await get_client()
        query = Query().top(top)
        if filter_expr:
            query = query.filter(F.raw(filter_expr))
        result = await client.workflow.list_workitems(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_get_workitem(workitem_id: str) -> str:
    """Get detailed information about a specific workflow work item.

    Args:
        workitem_id: The Object Reference ID of the work item.

    Returns:
        JSON object with all work item properties including Name, Status,
        AssignedTo, DueDate, Subject, and workflow context.
    """
    try:
        client = await get_client()
        result = await client.workflow.get_workitem(workitem_id)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_complete_workitem(
    workitem_id: str,
    routing_option: str | None = None,
    comment: str | None = None,
) -> str:
    """Complete (finish) a workflow work item.

    Use windchill_get_routing_options first to see available routing
    options for the work item.

    Args:
        workitem_id: The Object Reference ID of the work item.
        routing_option: Routing option name (e.g. "Approve", "Reject").
            Get available options from windchill_get_routing_options.
        comment: Completion comment visible in workflow history.

    Returns:
        JSON object confirming the work item completion.
    """
    try:
        client = await get_client()
        result = await client.workflow.complete_workitem(
            workitem_id, routing_option=routing_option, comment=comment
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_reassign_workitem(
    workitem_id: str,
    user_id: str,
    comment: str | None = None,
) -> str:
    """Reassign a workflow work item to a different user.

    Args:
        workitem_id: The Object Reference ID of the work item.
        user_id: The user ID or username to reassign the work item to.
        comment: Optional comment explaining the reassignment.

    Returns:
        JSON object confirming the reassignment.
    """
    try:
        client = await get_client()
        result = await client.workflow.reassign_workitem(
            workitem_id, user_id, comment=comment
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_get_routing_options(workitem_id: str) -> str:
    """Get available routing options for a workflow work item.

    Routing options define the possible outcomes when completing a
    work item (e.g., "Approve", "Reject", "Rework").

    Args:
        workitem_id: The Object Reference ID of the work item.

    Returns:
        JSON object listing available routing options.
    """
    try:
        client = await get_client()
        result = await client.workflow.get_routing_options(workitem_id)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
