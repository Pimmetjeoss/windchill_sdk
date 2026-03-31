"""CAD Document Management domain - CAD documents, structure, and content."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class CADDocMgmt(BaseDomain):
    """CAD Document Management domain (CADDocMgmt).

    Manages CAD documents, CAD document usage links, references,
    and CAD-specific actions like checkout, checkin, and structure retrieval.
    """

    domain = "CADDocMgmt"
    namespace = "PTC.CADDocMgmt"

    # ── CADDocuments CRUD ──

    async def list_cad_documents(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List CAD documents with optional OData query."""
        return await self.list("CADDocuments", query)

    async def get_cad_document(self, cad_doc_id: str) -> dict[str, Any]:
        """Get a single CAD document by Object Reference ID."""
        return await self.get("CADDocuments", cad_doc_id)

    async def create_cad_document(
        self,
        name: str,
        *,
        number: str | None = None,
        context_id: str | None = None,
        cad_name: str | None = None,
        doc_type: str | None = None,
        odata_type: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new CAD document.

        Args:
            name: CAD document name.
            number: CAD document number (auto-generated if omitted).
            context_id: Container Object Reference ID.
            cad_name: Native CAD file name.
            doc_type: CAD document type (e.g., "PROE", "CREO").
            odata_type: OData type for soft types.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if number:
            data["Number"] = number
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if cad_name:
            data["CADName"] = cad_name
        if doc_type:
            data["DocType"] = doc_type
        if odata_type:
            data["@odata.type"] = odata_type
        return await self.create("CADDocuments", data)

    # ── CAD Document Actions (bound) ──

    async def checkout_cad_document(self, cad_doc_id: str) -> dict[str, Any]:
        """Check out a CAD document. Returns the working copy entity."""
        return await self.action("CADDocuments", cad_doc_id, "CheckOut", {})

    async def checkin_cad_document(
        self, working_copy_id: str, comment: str | None = None
    ) -> dict[str, Any]:
        """Check in a CAD document working copy."""
        body: dict[str, Any] = {}
        if comment:
            body["Comment"] = comment
        return await self.action(
            "CADDocuments", working_copy_id, "CheckIn", body
        )

    async def undo_checkout_cad_document(
        self, working_copy_id: str
    ) -> dict[str, Any]:
        """Undo checkout of a CAD document working copy."""
        return await self.action(
            "CADDocuments", working_copy_id, "UndoCheckOut", {}
        )

    # ── Structure (bound action, POST) ──

    async def get_structure(
        self,
        cad_doc_id: str,
        *,
        navigation_criteria: dict[str, Any] | None = None,
        bom_members_only: bool | None = None,
    ) -> dict[str, Any]:
        """Get the CAD document structure via bound action (POST).

        Args:
            cad_doc_id: CAD document Object Reference ID.
            navigation_criteria: Criteria controlling structure traversal depth
                and filtering (e.g., ConfigSpec, PartUseFilter).
            bom_members_only: When True, returns only BOM-relevant members.
        """
        body: dict[str, Any] = {}
        if navigation_criteria is not None:
            body["NavigationCriteria"] = navigation_criteria
        if bom_members_only is not None:
            body["BOMMembersOnly"] = bom_members_only
        return await self.action(
            "CADDocuments", cad_doc_id, "GetStructure", body
        )

    # ── Navigation Properties ──

    async def get_all_primary_contents(
        self, cad_doc_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get all primary content files for a CAD document.

        Uses the AllPrimaryContents navigation property which returns content
        across all iterations, unlike PrimaryContent which returns only the
        latest iteration's content.
        """
        return await self.navigate(
            "CADDocuments", cad_doc_id, "AllPrimaryContents", query
        )

    async def get_uses(
        self, cad_doc_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get CAD document usage links (child components)."""
        return await self.navigate("CADDocuments", cad_doc_id, "Uses", query)

    # ── CADDocumentUse Entity Set ──

    async def list_cad_document_uses(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List CAD document use links with optional query."""
        return await self.list("CADDocumentUse", query)

    async def get_cad_document_use(self, use_id: str) -> dict[str, Any]:
        """Get a single CAD document use link by ID."""
        return await self.get("CADDocumentUse", use_id)

    # ── CADDocumentReference Entity Set ──

    async def list_cad_document_references(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List CAD document reference links with optional query."""
        return await self.list("CADDocumentReference", query)

    async def get_cad_document_reference(
        self, reference_id: str
    ) -> dict[str, Any]:
        """Get a single CAD document reference link by ID."""
        return await self.get("CADDocumentReference", reference_id)

    # ── Pagination Helpers ──

    async def get_all_cad_documents(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all CAD documents across all pages."""
        return await self.list_all("CADDocuments", query, max_items)
