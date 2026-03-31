"""Principal Management domain - Users and Groups."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.filter import FilterExpr
from windchill.odata.query import Query
from windchill.types import ODataResponse


class PrincipalMgmt(BaseDomain):
    """Principal Management domain (PrincipalMgmt).

    Manages user principals and group principals, including user search
    and group membership navigation.
    """

    domain = "PrincipalMgmt"
    namespace = "PTC.PrincipalMgmt"

    # ── Users ──

    async def list_users(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List users with optional OData query."""
        return await self.list("Users", query)

    async def get_user(self, user_id: str) -> dict[str, Any]:
        """Get a single user by Object Reference ID."""
        return await self.get("Users", user_id)

    async def search_users(
        self,
        name: str,
        *,
        query: Query | None = None,
    ) -> ODataResponse:
        """Search users by name using an OData filter.

        Applies a `contains(Name, '<name>')` filter. Additional query options
        (select, top, orderby, etc.) can be passed via the query parameter.

        Args:
            name: Name or partial name to search for.
            query: Additional OData query options to merge with the filter.
        """
        name_filter = FilterExpr(f"contains(Name,'{name}')")
        base_query = query if query is not None else Query()
        filtered_query = base_query.filter(name_filter)
        return await self.list("Users", filtered_query)

    # ── Groups ──

    async def list_groups(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List groups with optional OData query."""
        return await self.list("Groups", query)

    async def get_group(self, group_id: str) -> dict[str, Any]:
        """Get a single group by Object Reference ID."""
        return await self.get("Groups", group_id)

    # ── Group Members (navigation property) ──

    async def get_group_members(
        self, group_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get members of a group via the Members navigation property."""
        return await self.navigate("Groups", group_id, "Members", query)

    # ── Pagination Helpers ──

    async def get_all_users(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all users across all pages."""
        return await self.list_all("Users", query, max_items)

    async def get_all_groups(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all groups across all pages."""
        return await self.list_all("Groups", query, max_items)
