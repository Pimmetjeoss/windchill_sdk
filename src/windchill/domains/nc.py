"""Nonconformance domain - Nonconformances and Dispositions."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class NC(BaseDomain):
    """Nonconformance domain (NC).

    Manages nonconformance records and their dispositions for
    tracking and resolving product or process deviations.
    """

    domain = "NC"
    namespace = "PTC.NC"

    # ── Nonconformances ──

    async def list_nonconformances(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List nonconformances with optional OData query."""
        return await self.list("Nonconformances", query)

    async def get_nonconformance(self, nc_id: str) -> dict[str, Any]:
        """Get a single nonconformance by ID."""
        return await self.get("Nonconformances", nc_id)

    async def create_nonconformance(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new nonconformance.

        Args:
            name: Nonconformance name.
            context_id: Container Object Reference ID.
            description: Nonconformance description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("Nonconformances", data)

    async def update_nonconformance(
        self, nc_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing nonconformance."""
        return await self.update("Nonconformances", nc_id, data)

    async def delete_nonconformance(self, nc_id: str) -> None:
        """Delete a nonconformance."""
        await self.delete("Nonconformances", nc_id)

    # ── Dispositions ──

    async def list_dispositions(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List dispositions with optional OData query."""
        return await self.list("Dispositions", query)

    async def get_disposition(self, disposition_id: str) -> dict[str, Any]:
        """Get a single disposition by ID."""
        return await self.get("Dispositions", disposition_id)

    async def create_disposition(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new disposition.

        Args:
            name: Disposition name.
            context_id: Container Object Reference ID.
            description: Disposition description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("Dispositions", data)

    async def update_disposition(
        self, disposition_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing disposition."""
        return await self.update("Dispositions", disposition_id, data)

    async def delete_disposition(self, disposition_id: str) -> None:
        """Delete a disposition."""
        await self.delete("Dispositions", disposition_id)
