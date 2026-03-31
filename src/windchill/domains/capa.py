"""CAPA domain - Corrective and Preventive Actions."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class CAPA(BaseDomain):
    """CAPA domain (Corrective and Preventive Actions).

    Manages CAPAs and their associated corrective/preventive actions
    for quality compliance and continuous improvement.
    """

    domain = "CAPA"
    namespace = "PTC.CAPA"

    # ── CAPAs ──

    async def list_capas(self, query: Query | None = None) -> ODataResponse:
        """List CAPAs with optional OData query."""
        return await self.list("CAPAs", query)

    async def get_capa(self, capa_id: str) -> dict[str, Any]:
        """Get a single CAPA by ID."""
        return await self.get("CAPAs", capa_id)

    async def create_capa(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new CAPA.

        Args:
            name: CAPA name.
            context_id: Container Object Reference ID.
            description: CAPA description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("CAPAs", data)

    async def update_capa(
        self, capa_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing CAPA."""
        return await self.update("CAPAs", capa_id, data)

    async def delete_capa(self, capa_id: str) -> None:
        """Delete a CAPA."""
        await self.delete("CAPAs", capa_id)

    # ── CAPA Actions ──

    async def list_capa_actions(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List CAPA actions with optional OData query."""
        return await self.list("CAPAActions", query)

    async def get_capa_action(self, action_id: str) -> dict[str, Any]:
        """Get a single CAPA action by ID."""
        return await self.get("CAPAActions", action_id)

    async def create_capa_action(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new CAPA action.

        Args:
            name: CAPA action name.
            context_id: Container Object Reference ID.
            description: CAPA action description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("CAPAActions", data)

    async def update_capa_action(
        self, action_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing CAPA action."""
        return await self.update("CAPAActions", action_id, data)

    async def delete_capa_action(self, action_id: str) -> None:
        """Delete a CAPA action."""
        await self.delete("CAPAActions", action_id)
