"""Document management tools for Windchill MCP Server."""

from __future__ import annotations

import json

from windchill.odata.filter import F
from windchill.odata.query import Query

from windchill_mcp.server import get_client, mcp


@mcp.tool()
async def windchill_search_documents(
    filter_expr: str | None = None,
    top: int = 50,
) -> str:
    """Search for documents in Windchill PLM.

    Args:
        filter_expr: OData filter expression (e.g. "contains(Name,'spec')",
            "State eq 'RELEASED'"). Supports standard OData operators:
            eq, ne, gt, lt, contains, startswith, endswith, and/or.
        top: Maximum number of results to return (default 50).

    Returns:
        JSON array of matching documents with their properties.
    """
    try:
        client = await get_client()
        query = Query().top(top)
        if filter_expr:
            query = query.filter(F.raw(filter_expr))
        result = await client.doc_mgmt.list_documents(query)
        return json.dumps(result.items, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_create_document(
    name: str,
    context_id: str | None = None,
) -> str:
    """Create a new document in Windchill.

    Args:
        name: Document name (required).
        context_id: Container Object Reference ID to create the document in.
            Use windchill_list_containers to find available containers.

    Returns:
        JSON object of the newly created document.
    """
    try:
        client = await get_client()
        result = await client.doc_mgmt.create_document(
            name, context_id=context_id
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_checkout_document(doc_id: str) -> str:
    """Check out a document for editing. Returns the working copy.

    The document must not already be checked out. After editing, use
    windchill_checkin_document with the working copy ID.

    Args:
        doc_id: The Object Reference ID of the document to check out.

    Returns:
        JSON object of the working copy (use its ID for upload/checkin).
    """
    try:
        client = await get_client()
        result = await client.doc_mgmt.checkout_document(doc_id)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_checkin_document(
    working_copy_id: str,
    comment: str | None = None,
) -> str:
    """Check in a document working copy after editing.

    Args:
        working_copy_id: The Object Reference ID of the working copy
            (returned from windchill_checkout_document).
        comment: Optional checkin comment describing the changes.

    Returns:
        JSON object of the checked-in document.
    """
    try:
        client = await get_client()
        result = await client.doc_mgmt.checkin_document(
            working_copy_id, comment=comment
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_upload_file(
    working_copy_id: str,
    file_path: str,
    role: str = "PRIMARY",
) -> str:
    """Upload a file to a document working copy.

    The document must be checked out first. Use windchill_checkout_document
    to get a working copy, then upload the file to it.

    Args:
        working_copy_id: The Object Reference ID of the document working copy.
        file_path: Absolute path to the file to upload.
        role: Content role - "PRIMARY" for the main file or "SECONDARY"
            for attachments. Default is "PRIMARY".

    Returns:
        JSON object confirming the upload, or empty object on success.
    """
    try:
        client = await get_client()
        result = await client.doc_mgmt.upload_content(
            working_copy_id, file_path, role=role
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def windchill_download_file(doc_id: str, output_path: str) -> str:
    """Download the primary content file of a document.

    Args:
        doc_id: The Object Reference ID of the document.
        output_path: Absolute path where the downloaded file should be saved.

    Returns:
        JSON object with the download path on success.
    """
    try:
        client = await get_client()
        saved_path = await client.doc_mgmt.download_primary(doc_id, output_path)
        return json.dumps(
            {"status": "downloaded", "path": str(saved_path)},
            indent=2,
            default=str,
        )
    except Exception as e:
        return json.dumps({"error": str(e)})
