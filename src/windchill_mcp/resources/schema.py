"""MCP Resources exposing Windchill domain and API information."""

from __future__ import annotations

import json

from windchill_mcp.server import mcp

# ── Static domain reference data exposed as MCP resources ──

_DOMAINS = {
    "PTC": {
        "description": "Common domain - shared operations, lifecycle, type definitions",
        "entity_sets": [
            "BusinessObjects",
            "TypeDefinitions",
            "LifeCycleTemplates",
        ],
        "functions": [
            "GetNonceToken",
            "GetObjectByID",
            "GetLifeCycleStates",
            "GetContainers",
            "SearchByKeyword",
        ],
    },
    "ProdMgmt": {
        "description": "Product Management - parts, BOMs, product data",
        "entity_sets": ["Parts", "BOMs"],
        "actions": [
            "CheckOut",
            "CheckIn",
            "UndoCheckOut",
            "Revise",
            "SaveAs",
            "SetLifeCycleState",
        ],
        "functions": ["GetPartsList", "GetPartStructure", "GetWhereUsed"],
    },
    "DocMgmt": {
        "description": "Document Management - documents, content upload/download",
        "entity_sets": ["Documents"],
        "actions": [
            "CheckOut",
            "CheckIn",
            "UndoCheckOut",
            "Revise",
            "SetLifeCycleState",
            "UploadContent",
            "UpdateCommonProperties",
        ],
        "navigation": ["PrimaryContent", "Attachments"],
    },
    "ChangeMgmt": {
        "description": "Change Management - problem reports, ECRs, ECNs, variances",
        "entity_sets": [
            "ProblemReports",
            "ChangeRequests",
            "ChangeNotices",
            "ChangeTasks",
            "Variances",
        ],
        "actions": ["SetLifeCycleState"],
        "navigation": ["AffectedObjects", "ResultingObjects"],
    },
    "Workflow": {
        "description": "Workflow - work items, task routing, process management",
        "entity_sets": ["WorkItems"],
        "actions": ["Complete", "Save", "Reassign"],
        "functions": ["GetRoutingOptions", "GetValidReassignUsers"],
        "navigation": ["Subject", "Activities"],
    },
    "DataAdmin": {
        "description": "Data Administration - containers, folders, cabinets, teams",
        "entity_sets": ["Containers", "Folders", "Cabinets", "Teams"],
        "navigation": ["SubFolders"],
    },
    "PrincipalMgmt": {
        "description": "Principal Management - users and groups",
        "entity_sets": ["Users", "Groups"],
        "navigation": ["Members"],
    },
    "QMS": {
        "description": "Quality Management System - audits, findings, quality actions",
        "entity_sets": ["Audits", "AuditFindings", "QualityActions"],
    },
    "NC": {
        "description": "Nonconformance - nonconformance records and dispositions",
        "entity_sets": ["Nonconformances", "Dispositions"],
    },
    "CAPA": {
        "description": "Corrective and Preventive Actions",
        "entity_sets": ["CAPAs", "CAPAActions"],
    },
    "SavedSearch": {
        "description": "Saved Search - stored search definitions and execution",
        "entity_sets": ["SavedSearches"],
        "functions": ["ExecuteSavedSearch"],
    },
}

_ODATA_FILTER_GUIDE = {
    "description": "OData v4 filter expression syntax for Windchill queries",
    "operators": {
        "eq": "Equal: State eq 'RELEASED'",
        "ne": "Not equal: Source ne 'BUY'",
        "gt": "Greater than: CreatedOn gt 2024-01-01T00:00:00Z",
        "ge": "Greater than or equal",
        "lt": "Less than",
        "le": "Less than or equal",
    },
    "string_functions": {
        "contains": "contains(Name,'bracket')",
        "startswith": "startswith(Number,'00')",
        "endswith": "endswith(Name,'.pdf')",
    },
    "logical": {
        "and": "State eq 'RELEASED' and Source eq 'MAKE'",
        "or": "State eq 'INWORK' or State eq 'UNDERREVIEW'",
        "not": "not contains(Name,'obsolete')",
    },
    "common_part_properties": [
        "ID",
        "Name",
        "Number",
        "State",
        "Version",
        "Iteration",
        "Source",
        "DefaultUnit",
        "CreatedOn",
        "ModifiedOn",
        "CheckedOut",
    ],
    "common_document_properties": [
        "ID",
        "Name",
        "Number",
        "State",
        "Version",
        "Iteration",
        "Description",
        "CreatedOn",
        "ModifiedOn",
    ],
    "common_lifecycle_states": [
        "INWORK",
        "UNDERREVIEW",
        "RELEASED",
        "CANCELLED",
    ],
}

_TOOLS_GUIDE = {
    "description": "Quick reference for available Windchill MCP tools",
    "parts": {
        "search": "windchill_search_parts - Find parts by filter",
        "get": "windchill_get_part - Get part details by ID",
        "create": "windchill_create_part - Create a new part",
        "checkout": "windchill_checkout_part - Check out for editing",
        "checkin": "windchill_checkin_part - Check in after editing",
        "revise": "windchill_revise_part - Create new revision",
        "state": "windchill_set_part_state - Change lifecycle state",
        "bom": "windchill_get_bom - Get bill of materials",
        "where_used": "windchill_get_where_used - Find parent assemblies",
    },
    "documents": {
        "search": "windchill_search_documents - Find documents by filter",
        "create": "windchill_create_document - Create a new document",
        "checkout": "windchill_checkout_document - Check out for editing",
        "checkin": "windchill_checkin_document - Check in after editing",
        "upload": "windchill_upload_file - Upload file to working copy",
        "download": "windchill_download_file - Download primary content",
    },
    "changes": {
        "list_ecr": "windchill_list_change_requests - List ECRs",
        "create_ecr": "windchill_create_change_request - Create ECR",
        "list_ecn": "windchill_list_change_notices - List ECNs",
        "create_pr": "windchill_create_problem_report - Create Problem Report",
    },
    "workflow": {
        "list": "windchill_list_workitems - List work items",
        "get": "windchill_get_workitem - Get work item details",
        "complete": "windchill_complete_workitem - Complete a task",
        "reassign": "windchill_reassign_workitem - Reassign to another user",
        "options": "windchill_get_routing_options - Get routing options",
    },
    "search": {
        "global": "windchill_search - Full-text search across all objects",
        "saved": "windchill_execute_saved_search - Run a saved search",
    },
    "admin": {
        "containers": "windchill_list_containers - List Products/Libraries/Projects",
        "folders": "windchill_list_folders - List folders in a container",
        "users": "windchill_search_users - Search for users",
        "lifecycle": "windchill_get_lifecycle_states - Get states for a template",
        "set_state": "windchill_set_lifecycle_state - Set state on any entity",
    },
    "quality": {
        "nc": "windchill_list_nonconformances - List nonconformances",
        "capa": "windchill_list_capas - List CAPAs",
        "audits": "windchill_list_audits - List quality audits",
    },
}


@mcp.resource("windchill://domains")
async def get_domains() -> str:
    """List all Windchill API domains and their entity sets, actions, and functions."""
    return json.dumps(_DOMAINS, indent=2)


@mcp.resource("windchill://odata-filter-guide")
async def get_odata_filter_guide() -> str:
    """OData v4 filter expression syntax reference for building Windchill queries."""
    return json.dumps(_ODATA_FILTER_GUIDE, indent=2)


@mcp.resource("windchill://tools-guide")
async def get_tools_guide() -> str:
    """Quick reference for all available Windchill MCP tools organized by category."""
    return json.dumps(_TOOLS_GUIDE, indent=2)
