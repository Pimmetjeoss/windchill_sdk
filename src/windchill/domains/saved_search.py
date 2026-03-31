"""Saved Search domain - Saved searches and execution."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class SavedSearch(BaseDomain):
    """Saved Search domain.

    Manages saved search definitions and provides the ability to
    execute saved searches by ID, returning result collections.
    """

    domain = "SavedSearch"
    namespace = "PTC.SavedSearch"

    # ── Saved Searches CRUD ──

    async def list_saved_searches(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List saved searches with optional OData query."""
        return await self.list("SavedSearches", query)

    async def get_saved_search(self, search_id: str) -> dict[str, Any]:
        """Get a single saved search definition by ID."""
        return await self.get("SavedSearches", search_id)

    async def create_saved_search(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new saved search."""
        return await self.create("SavedSearches", data)

    async def update_saved_search(
        self, search_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing saved search."""
        return await self.update("SavedSearches", search_id, data)

    async def delete_saved_search(self, search_id: str) -> None:
        """Delete a saved search."""
        await self.delete("SavedSearches", search_id)

    # ── Unbound Functions ──

    async def execute_saved_search(
        self, saved_search_id: str
    ) -> dict[str, Any]:
        """Execute a saved search and return the result collection.

        Args:
            saved_search_id: The ID of the saved search to execute.

        Returns:
            Raw response dict containing the search results collection.
        """
        return await self.unbound_function(
            "ExecuteSavedSearch",
            params={"SavedSearchID": f"'{saved_search_id}'"},
        )
