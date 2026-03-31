"""PTC Common domain - shared operations across all domains."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class Common(BaseDomain):
    """PTC Common domain providing cross-domain operations.

    Includes nonce token management, lifecycle operations, type definitions,
    and object lookup by ID.
    """

    domain = "PTC"
    namespace = "PTC"

    # ── Functions (GET, read-only) ──

    async def get_nonce_token(self) -> str:
        """Fetch a CSRF nonce token for write operations.

        Tries GetCSRFToken (newer servers) then GetNonceToken (older servers).
        """
        for func_name in ["GetCSRFToken", "GetNonceToken"]:
            try:
                data = await self.unbound_function(func_name)
                token = (
                    data.get("NonceValue")
                    or data.get("NonceToken")
                    or data.get("value", "")
                )
                if token:
                    return token
            except Exception:
                continue
        raise ValueError("Could not obtain CSRF nonce token")

    async def get_type_definitions(self) -> ODataResponse:
        """Get all type definitions."""
        return await self.list("TypeDefinitions")

    async def get_object_by_id(self, object_id: str) -> dict[str, Any]:
        """Look up any business object by its Object Reference ID."""
        data = await self.unbound_function(
            "GetObjectByID",
            params={"ID": f"'{object_id}'"},
        )
        return data

    async def get_lifecycle_states(self, template_name: str) -> list[dict[str, Any]]:
        """Get all lifecycle states for a given lifecycle template."""
        data = await self.unbound_function(
            "GetLifeCycleStates",
            params={"TemplateName": f"'{template_name}'"},
        )
        return data.get("value", [])

    async def get_containers(self, query: Query | None = None) -> ODataResponse:
        """Get all accessible containers (Products, Libraries, Projects).

        Tries unbound GetContainers function first, falls back to DataAdmin/Containers entity set.
        """
        try:
            data = await self.unbound_function("GetContainers")
            return ODataResponse.from_dict(data)
        except Exception:
            # Fall back to DataAdmin domain Containers entity set
            url = f"{self._http._config.odata_base}/DataAdmin/Containers"
            params = query.to_params() if query else None
            data = await self._http.get_json(url, params=params)
            return ODataResponse.from_dict(data)

    async def search_by_keyword(
        self,
        keyword: str,
        query: Query | None = None,
    ) -> ODataResponse:
        """Full-text search across all business objects."""
        params = {"Keyword": f"'{keyword}'"}
        if query:
            params.update(query.to_params())
        data = await self.unbound_function("SearchByKeyword", params=params)
        return ODataResponse.from_dict(data)

    async def get_lifecycle_templates(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List all lifecycle templates."""
        return await self.list("LifeCycleTemplates", query)

    async def get_business_objects(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List business objects in the common domain."""
        return await self.list("BusinessObjects", query)

    # ── Bound Functions (on entity instances) ──

    async def get_versions(
        self, entity_set: str, entity_id: str
    ) -> ODataResponse:
        """Get all versions of a versioned entity."""
        data = await self.function(entity_set, entity_id, "GetVersions")
        return ODataResponse.from_dict(data)

    async def get_iterations(
        self, entity_set: str, entity_id: str
    ) -> ODataResponse:
        """Get all iterations of a versioned entity."""
        data = await self.function(entity_set, entity_id, "GetIterations")
        return ODataResponse.from_dict(data)

    async def get_lifecycle_history(
        self, entity_set: str, entity_id: str
    ) -> ODataResponse:
        """Get lifecycle state change history for an entity."""
        data = await self.function(entity_set, entity_id, "GetLifeCycleHistory")
        return ODataResponse.from_dict(data)

    async def get_access_permissions(
        self, entity_set: str, entity_id: str
    ) -> dict[str, Any]:
        """Get access permissions for an entity."""
        return await self.function(entity_set, entity_id, "GetAccessPermissions")

    # ── Bound Actions (POST, state-changing) ──

    async def checkout(self, entity_set: str, entity_id: str) -> dict[str, Any]:
        """Check out an entity, returning the working copy."""
        return await self.action(entity_set, entity_id, "CheckOut", {})

    async def checkin(
        self,
        entity_set: str,
        entity_id: str,
        comment: str | None = None,
    ) -> dict[str, Any]:
        """Check in a working copy."""
        body: dict[str, Any] = {}
        if comment:
            body["Comment"] = comment
        return await self.action(entity_set, entity_id, "CheckIn", body)

    async def undo_checkout(
        self, entity_set: str, entity_id: str
    ) -> dict[str, Any]:
        """Undo checkout of a working copy."""
        return await self.action(entity_set, entity_id, "UndoCheckOut", {})

    async def revise(self, entity_set: str, entity_id: str) -> dict[str, Any]:
        """Create a new revision of an entity."""
        return await self.action(entity_set, entity_id, "Revise", {})

    async def set_lifecycle_state(
        self,
        entity_set: str,
        entity_id: str,
        state: str,
    ) -> dict[str, Any]:
        """Set the lifecycle state of an entity.

        Args:
            state: Internal state name, e.g. "INWORK", "RELEASED", "CANCELLED".
        """
        return await self.action(
            entity_set, entity_id, "SetLifeCycleState", {"State": state}
        )
