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


@mcp.tool()
async def windchill_get_change_task(
    ct_number: str,
) -> str:
    """Look up a Change Task by its CT number and return full details.

    Change Tasks (CT) are the work items within a Change Notice that
    track specific changes to parts and documents.

    Args:
        ct_number: The Change Task number (e.g., "CT015630").

    Returns:
        JSON object with Change Task details including name, state,
        SAP text, creator, and Contiweb-specific fields.
    """
    try:
        client = await get_client()
        query = Query().filter(F.eq("Number", ct_number)).top(1)
        result = await client.change_mgmt.list_change_tasks(query)

        if not result.items:
            return json.dumps({"error": f"Change Task {ct_number} not found"})

        ct = result.first
        return json.dumps(ct, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_change_impact_analysis(
    ct_number: str,
) -> str:
    """Perform a full change impact analysis for a Change Task.

    Looks up the Change Task by CT number and retrieves:
    - Change Task details (name, state, SAP text, creator)
    - Affected Objects (parts/documents being changed)
    - Resulting Objects (new/revised parts/documents created)
    - Summary statistics by object type

    This is useful for understanding the scope and impact of an
    engineering change before validation or approval.

    Args:
        ct_number: The Change Task number (e.g., "CT015630").

    Returns:
        JSON object with change_task details, affected_objects,
        resulting_objects, and a summary with counts per type.
    """
    try:
        client = await get_client()
        config = client.config

        # Step 1: Find the Change Task
        query = Query().filter(F.eq("Number", ct_number)).top(1)
        result = await client.change_mgmt.list_change_tasks(query)

        if not result.items:
            return json.dumps({"error": f"Change Task {ct_number} not found"})

        ct = result.first
        ct_id = ct["ID"]

        # Step 2: Get Affected Objects
        affected_url = (
            f"{config.odata_base}/ChangeMgmt/ChangeTasks('{ct_id}')/AffectedObjects"
        )
        affected_data = await client.http.get_json(affected_url)
        affected = affected_data.get("value", [])

        # Step 3: Get Resulting Objects
        resulting_url = (
            f"{config.odata_base}/ChangeMgmt/ChangeTasks('{ct_id}')/ResultingObjects"
        )
        resulting_data = await client.http.get_json(resulting_url)
        resulting = resulting_data.get("value", [])

        # Step 4: Build summary
        affected_types: dict[str, int] = {}
        for obj in affected:
            obj_type = obj.get("ObjectType", "Unknown")
            affected_types[obj_type] = affected_types.get(obj_type, 0) + 1

        resulting_types: dict[str, int] = {}
        for obj in resulting:
            obj_type = obj.get("ObjectType", "Unknown")
            resulting_types[obj_type] = resulting_types.get(obj_type, 0) + 1

        # Step 5: Extract SAP replacement info if available
        sap_text = ct.get("CWSAPsalestext", "")
        replacements = []
        if sap_text:
            for line in sap_text.replace("\r\n", "\n").split("\n"):
                line = line.strip()
                if "REPLACED BY" in line:
                    parts = line.split("REPLACED BY")
                    if len(parts) == 2:
                        replacements.append({
                            "old_number": parts[0].strip(),
                            "new_number": parts[1].strip(),
                        })

        report = {
            "change_task": {
                "number": ct.get("Number"),
                "name": ct.get("Name"),
                "state": ct.get("State"),
                "created_by": ct.get("CreatedBy"),
                "created_on": ct.get("CreatedOn"),
                "sap_obsolete": ct.get("CWSAPObsolete"),
                "wc_obsolete": ct.get("CWWCObsolete"),
                "documentation_update": ct.get("CWDocumentationupdate"),
                "service_validation": ct.get("CWSERVICEVALIDATION"),
                "change_effect_new_order": ct.get("CWChangeEffectNewOrder"),
                "change_effect_running_orders": ct.get("CWChangeEffectRunningOrders"),
            },
            "affected_objects": [
                {
                    "number": obj.get("Number", obj.get("Name", "?")),
                    "name": obj.get("Name", ""),
                    "type": obj.get("ObjectType", "?"),
                    "state": obj.get("State"),
                    "id": obj.get("ID"),
                }
                for obj in affected
            ],
            "resulting_objects": [
                {
                    "number": obj.get("Number", obj.get("Name", "?")),
                    "name": obj.get("Name", ""),
                    "type": obj.get("ObjectType", "?"),
                    "state": obj.get("State"),
                    "id": obj.get("ID"),
                }
                for obj in resulting
            ],
            "sap_replacements": replacements,
            "summary": {
                "total_affected": len(affected),
                "total_resulting": len(resulting),
                "total_sap_replacements": len(replacements),
                "affected_by_type": affected_types,
                "resulting_by_type": resulting_types,
            },
        }

        return json.dumps(report, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
