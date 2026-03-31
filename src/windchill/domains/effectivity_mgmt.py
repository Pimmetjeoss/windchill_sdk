"""Effectivity Management domain - Date, Unit, and general effectivity."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class EffectivityMgmt(BaseDomain):
    """Effectivity Management domain (EffectivityMgmt).

    Manages effectivity definitions including general effectivity,
    date-based effectivity, unit-based effectivity, and part effectivity
    context associations.
    """

    domain = "EffectivityMgmt"
    namespace = "PTC.EffectivityMgmt"

    # ── Effectivity (general) ──

    async def list_effectivities(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List effectivity records with optional OData query."""
        return await self.list("Effectivity", query)

    async def get_effectivity(self, effectivity_id: str) -> dict[str, Any]:
        """Get a single effectivity record by Object Reference ID."""
        return await self.get("Effectivity", effectivity_id)

    async def create_effectivity(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new effectivity record."""
        return await self.create("Effectivity", data)

    async def update_effectivity(
        self, effectivity_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update an existing effectivity record."""
        return await self.update("Effectivity", effectivity_id, data)

    async def delete_effectivity(self, effectivity_id: str) -> None:
        """Delete an effectivity record."""
        await self.delete("Effectivity", effectivity_id)

    # ── DateEffectivity ──

    async def list_date_effectivities(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List date-based effectivity records."""
        return await self.list("DateEffectivity", query)

    async def get_date_effectivity(
        self, effectivity_id: str
    ) -> dict[str, Any]:
        """Get a single date effectivity record."""
        return await self.get("DateEffectivity", effectivity_id)

    async def create_date_effectivity(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new date-based effectivity record."""
        return await self.create("DateEffectivity", data)

    async def update_date_effectivity(
        self, effectivity_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a date-based effectivity record."""
        return await self.update("DateEffectivity", effectivity_id, data)

    async def delete_date_effectivity(self, effectivity_id: str) -> None:
        """Delete a date-based effectivity record."""
        await self.delete("DateEffectivity", effectivity_id)

    # ── UnitEffectivity ──

    async def list_unit_effectivities(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List unit-based effectivity records."""
        return await self.list("UnitEffectivity", query)

    async def get_unit_effectivity(
        self, effectivity_id: str
    ) -> dict[str, Any]:
        """Get a single unit effectivity record."""
        return await self.get("UnitEffectivity", effectivity_id)

    async def create_unit_effectivity(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new unit-based effectivity record."""
        return await self.create("UnitEffectivity", data)

    async def update_unit_effectivity(
        self, effectivity_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a unit-based effectivity record."""
        return await self.update("UnitEffectivity", effectivity_id, data)

    async def delete_unit_effectivity(self, effectivity_id: str) -> None:
        """Delete a unit-based effectivity record."""
        await self.delete("UnitEffectivity", effectivity_id)

    # ── PartEffectivityContext ──

    async def list_part_effectivity_contexts(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List part effectivity context associations."""
        return await self.list("PartEffectivityContext", query)

    async def get_part_effectivity_context(
        self, context_id: str
    ) -> dict[str, Any]:
        """Get a single part effectivity context association."""
        return await self.get("PartEffectivityContext", context_id)

    async def create_part_effectivity_context(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new part effectivity context association."""
        return await self.create("PartEffectivityContext", data)

    async def update_part_effectivity_context(
        self, context_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a part effectivity context association."""
        return await self.update("PartEffectivityContext", context_id, data)

    async def delete_part_effectivity_context(
        self, context_id: str
    ) -> None:
        """Delete a part effectivity context association."""
        await self.delete("PartEffectivityContext", context_id)
