"""Change management tools for Windchill MCP Server."""

from __future__ import annotations

import json

from windchill.odata.filter import F
from windchill.odata.query import Query

from windchill_mcp.server import get_client, mcp


@mcp.tool()
async def windchill_list_change_requests(
    filter_expr: str | None = None,
    top: int = 50,
) -> str:
    """List Change Requests (ECRs) in Windchill.

    Change Requests document proposed changes to products. They typically
    precede Change Notices in the formal change process.

    Args:
        filter_expr: OData filter expression (e.g. "State eq 'OPEN'",
            "contains(Name,'update')"). Supports standard OData operators.
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of Change Requests with their properties.
    """
    try:
        client = await get_client()
        query = Query().top(top)
        if filter_expr:
            query = query.filter(F.raw(filter_expr))
        result = await client.change_mgmt.list_change_requests(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_create_change_request(
    name: str,
    context_id: str | None = None,
    description: str | None = None,
) -> str:
    """Create a new Change Request (ECR) in Windchill.

    A Change Request documents a proposed change and its justification.

    Args:
        name: Change Request name (required).
        context_id: Container Object Reference ID. Use
            windchill_list_containers to find available containers.
        description: Description of the proposed change and its rationale.

    Returns:
        JSON object of the newly created Change Request.
    """
    try:
        client = await get_client()
        result = await client.change_mgmt.create_change_request(
            name, context_id=context_id, description=description
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_list_change_notices(
    filter_expr: str | None = None,
    top: int = 50,
) -> str:
    """List Change Notices (ECNs) in Windchill.

    Change Notices authorize and track the implementation of changes
    to products or documents.

    Args:
        filter_expr: OData filter expression (e.g. "State eq 'APPROVED'",
            "contains(Name,'release')"). Supports standard OData operators.
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of Change Notices with their properties.
    """
    try:
        client = await get_client()
        query = Query().top(top)
        if filter_expr:
            query = query.filter(F.raw(filter_expr))
        result = await client.change_mgmt.list_change_notices(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_create_problem_report(
    name: str,
    context_id: str | None = None,
    description: str | None = None,
) -> str:
    """Create a new Problem Report in Windchill.

    Problem Reports document issues found with products, parts, or
    processes. They often initiate the formal change management workflow.

    Args:
        name: Problem Report name (required).
        context_id: Container Object Reference ID. Use
            windchill_list_containers to find available containers.
        description: Detailed description of the problem.

    Returns:
        JSON object of the newly created Problem Report.
    """
    try:
        client = await get_client()
        result = await client.change_mgmt.create_problem_report(
            name, context_id=context_id, description=description
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
