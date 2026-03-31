"""Product Management domain - Parts, BOMs, and product data."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class ProdMgmt(BaseDomain):
    """Product Management domain (ProdMgmt).

    Manages parts, bills of materials, supplier/manufacturer parts,
    and product-related actions like checkout, checkin, and revise.
    """

    domain = "ProdMgmt"
    namespace = "PTC.ProdMgmt"

    # ── Parts CRUD ──

    async def list_parts(self, query: Query | None = None) -> ODataResponse:
        """List parts with optional OData query."""
        return await self.list("Parts", query)

    async def get_part(self, part_id: str) -> dict[str, Any]:
        """Get a single part by Object Reference ID."""
        return await self.get("Parts", part_id)

    async def create_part(
        self,
        name: str,
        *,
        number: str | None = None,
        context_id: str | None = None,
        source: str | None = None,
        default_unit: str | None = None,
        odata_type: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new part.

        Args:
            name: Part name.
            number: Part number (auto-generated if omitted).
            context_id: Container Object Reference ID to bind the part to.
            source: Part source type (e.g., "MAKE", "BUY").
            default_unit: Default unit of measure (e.g., "ea", "kg").
            odata_type: OData type for soft types (e.g., "PTC.ProdMgmt.Capacitor").
            **attributes: Additional properties to set on the part.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if number:
            data["Number"] = number
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if source:
            data["Source"] = source
        if default_unit:
            data["DefaultUnit"] = default_unit
        if odata_type:
            data["@odata.type"] = odata_type
        return await self.create("Parts", data)

    async def update_part(
        self, part_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing part."""
        return await self.update("Parts", part_id, data)

    async def delete_part(self, part_id: str) -> None:
        """Delete a part."""
        await self.delete("Parts", part_id)

    # ── Part Actions (bound, single object) ──

    async def checkout_part(self, part_id: str) -> dict[str, Any]:
        """Check out a part. Returns the working copy entity."""
        return await self.action("Parts", part_id, "CheckOut", {})

    async def checkin_part(
        self, working_copy_id: str, comment: str | None = None
    ) -> dict[str, Any]:
        """Check in a part working copy."""
        body: dict[str, Any] = {}
        if comment:
            body["Comment"] = comment
        return await self.action("Parts", working_copy_id, "CheckIn", body)

    async def undo_checkout_part(self, working_copy_id: str) -> dict[str, Any]:
        """Undo checkout of a part working copy."""
        return await self.action("Parts", working_copy_id, "UndoCheckOut", {})

    async def revise_part(self, part_id: str) -> dict[str, Any]:
        """Create a new revision of a part."""
        return await self.action("Parts", part_id, "Revise", {})

    async def save_as_part(
        self, part_id: str, new_attributes: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a copy of a part with new attributes."""
        return await self.action("Parts", part_id, "SaveAs", new_attributes)

    async def set_part_state(self, part_id: str, state: str) -> dict[str, Any]:
        """Set the lifecycle state of a part."""
        return await self.action(
            "Parts", part_id, "SetLifeCycleState", {"State": state}
        )

    # ── Multi-Object Actions (unbound) ──

    async def checkout_parts(self, part_ids: list[str]) -> dict[str, Any]:
        """Check out multiple parts in one request."""
        objects = [{"ID": pid} for pid in part_ids]
        return await self.unbound_action("CheckOut", {"Objects": objects})

    async def checkin_parts(
        self, working_copy_ids: list[str]
    ) -> dict[str, Any]:
        """Check in multiple part working copies."""
        objects = [{"ID": wid} for wid in working_copy_ids]
        return await self.unbound_action("CheckIn", {"Objects": objects})

    async def undo_checkout_parts(
        self, working_copy_ids: list[str]
    ) -> dict[str, Any]:
        """Undo checkout for multiple parts."""
        objects = [{"ID": wid} for wid in working_copy_ids]
        return await self.unbound_action("UndoCheckOut", {"Objects": objects})

    async def revise_parts(
        self, objects: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Revise multiple parts. Each object dict should have 'ID' and optionally 'Number'."""
        return await self.unbound_action("Revise", {"Objects": objects})

    async def delete_parts(self, part_ids: list[str]) -> dict[str, Any]:
        """Delete multiple parts."""
        objects = [{"ID": pid} for pid in part_ids]
        return await self.unbound_action("Delete", {"Objects": objects})

    # ── BOM Functions (bound) ──

    async def get_bom(
        self, part_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get bill of materials (BOM) via Uses navigation property."""
        return await self.navigate("Parts", part_id, "Uses", query)

    async def get_parts_list(self, part_id: str) -> dict[str, Any]:
        """Get flattened parts list (GetPartsList bound function)."""
        return await self.function("Parts", part_id, "GetPartsList")

    async def get_part_structure(self, part_id: str) -> dict[str, Any]:
        """Get multi-level part structure (GetPartStructure bound function)."""
        return await self.function("Parts", part_id, "GetPartStructure")

    async def get_where_used(self, part_id: str) -> dict[str, Any]:
        """Get where-used relationships for a part."""
        return await self.function("Parts", part_id, "GetWhereUsed")

    # ── BOM Modification ──

    async def add_part_usage(
        self,
        parent_part_id: str,
        child_part_id: str,
        *,
        quantity: float | None = None,
        unit: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Add a part usage link (BOM line) between parent and child parts.

        The parent part must be checked out first.
        """
        data: dict[str, Any] = {
            "Uses@odata.bind": f"Parts('{child_part_id}')",
            **attributes,
        }
        if quantity is not None:
            data["Quantity"] = quantity
        if unit:
            data["Unit"] = unit
        url = self._navigation_url("Parts", parent_part_id, "Uses")
        return await self._http.post_json(url, data)

    # ── BOMs Entity Set ──

    async def list_boms(self, query: Query | None = None) -> ODataResponse:
        """List BOMs with optional query."""
        return await self.list("BOMs", query)

    async def get_all_parts(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all parts across all pages."""
        return await self.list_all("Parts", query, max_items)

    # ── Content Download ──

    async def get_part_content_info(self, part_id: str) -> Any:
        """Get content info for a part's linked document.

        Follows: Part -> DescribedBy -> Document -> PrimaryContent.
        Returns ContentInfo or None if no content found.
        """
        from windchill.content.download import get_part_document_content

        return await get_part_document_content(
            self._http, self._http._config.odata_base, part_id
        )

    async def download_part_content(
        self,
        part_id: str,
        output_path: str | None = None,
    ) -> str:
        """Download the primary content file associated with a Part.

        Follows the full chain: Part -> DescribedBy -> Document -> PrimaryContent -> Download.

        Args:
            part_id: Part Object Reference ID.
            output_path: Where to save. If None, uses the original filename.

        Returns:
            Path to the downloaded file as string.
        """
        from pathlib import Path

        from windchill.content.download import download_part_content

        out = Path(output_path) if output_path else None
        result = await download_part_content(
            self._http, self._http._config.odata_base, part_id, out
        )
        return str(result)
