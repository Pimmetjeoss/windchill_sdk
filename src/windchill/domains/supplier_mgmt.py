"""Supplier Management domain - Sourcing contexts (AML/AVL data)."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class SupplierMgmt(BaseDomain):
    """Supplier Management domain (SupplierMgmt).

    Manages sourcing context data including Approved Manufacturer Lists (AML)
    and Approved Vendor Lists (AVL) associated with parts.
    """

    domain = "SupplierMgmt"
    namespace = "PTC.SupplierMgmt"

    # ── SourcingContext ──

    async def list_sourcing_contexts(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List sourcing contexts (AML/AVL records) with optional OData query."""
        return await self.list("SourcingContext", query)

    async def get_sourcing_context(
        self, sourcing_context_id: str
    ) -> dict[str, Any]:
        """Get a single sourcing context by Object Reference ID."""
        return await self.get("SourcingContext", sourcing_context_id)

    async def create_sourcing_context(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new sourcing context record."""
        return await self.create("SourcingContext", data)

    async def update_sourcing_context(
        self, sourcing_context_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing sourcing context record."""
        return await self.update(
            "SourcingContext", sourcing_context_id, data
        )

    async def delete_sourcing_context(
        self, sourcing_context_id: str
    ) -> None:
        """Delete a sourcing context record."""
        await self.delete("SourcingContext", sourcing_context_id)

    # ── Pagination Helpers ──

    async def get_all_sourcing_contexts(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all sourcing contexts across all pages."""
        return await self.list_all("SourcingContext", query, max_items)
