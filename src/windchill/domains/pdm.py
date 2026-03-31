"""PDM Conglomerate domain - Read-only BI domain for parts, documents, and changes."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class PDM(BaseDomain):
    """PDM Conglomerate domain (read-only BI domain).

    Provides read-only access to parts, documents, and change requests
    aggregated across the system. Intended for business intelligence
    and reporting use cases. No write operations are exposed.
    """

    domain = "PDM"
    namespace = "PTC.PDM"

    # ── Parts (read-only) ──

    async def list_parts(self, query: Query | None = None) -> ODataResponse:
        """List parts from the PDM conglomerate (read-only)."""
        return await self.list("Parts", query)

    async def get_part(self, part_id: str) -> dict[str, Any]:
        """Get a single part by ID (read-only)."""
        return await self.get("Parts", part_id)

    async def get_all_parts(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all parts across all pages (read-only)."""
        return await self.list_all("Parts", query, max_items)

    # ── Documents (read-only) ──

    async def list_documents(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List documents from the PDM conglomerate (read-only)."""
        return await self.list("Documents", query)

    async def get_document(self, document_id: str) -> dict[str, Any]:
        """Get a single document by ID (read-only)."""
        return await self.get("Documents", document_id)

    async def get_all_documents(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all documents across all pages (read-only)."""
        return await self.list_all("Documents", query, max_items)

    # ── Change Requests (read-only) ──

    async def list_change_requests(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List change requests from the PDM conglomerate (read-only)."""
        return await self.list("ChangeRequests", query)

    async def get_change_request(self, cr_id: str) -> dict[str, Any]:
        """Get a single change request by ID (read-only)."""
        return await self.get("ChangeRequests", cr_id)

    async def get_all_change_requests(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all change requests across all pages (read-only)."""
        return await self.list_all("ChangeRequests", query, max_items)
