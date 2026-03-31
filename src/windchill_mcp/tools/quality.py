"""Quality management tools for Windchill MCP Server."""

from __future__ import annotations

import json

from windchill.odata.query import Query

from windchill_mcp.server import get_client, mcp


@mcp.tool()
async def windchill_list_nonconformances(top: int = 50) -> str:
    """List Nonconformance records in Windchill.

    Nonconformances track deviations from specifications, standards,
    or requirements in products or processes.

    Args:
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of Nonconformance records with their properties.
    """
    try:
        client = await get_client()
        query = Query().top(top)
        result = await client.nc.list_nonconformances(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_list_capas(top: int = 50) -> str:
    """List Corrective and Preventive Actions (CAPAs) in Windchill.

    CAPAs are structured processes for investigating root causes and
    implementing corrective/preventive measures for quality issues.

    Args:
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of CAPA records with their properties.
    """
    try:
        client = await get_client()
        query = Query().top(top)
        result = await client.capa.list_capas(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_list_audits(top: int = 50) -> str:
    """List Quality Audits in Windchill.

    Audits are systematic reviews of quality management systems,
    processes, or products for compliance verification.

    Args:
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of Audit records with their properties.
    """
    try:
        client = await get_client()
        query = Query().top(top)
        result = await client.qms.list_audits(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
