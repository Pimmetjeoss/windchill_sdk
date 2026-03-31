"""Base domain service with shared CRUD, action, and function patterns."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from windchill.odata.paging import collect_all, paginate
from windchill.odata.query import Query
from windchill.types import ODataResponse

if TYPE_CHECKING:
    from windchill.http import HttpTransport


class BaseDomain:
    """Base class for all Windchill domain services.

    Provides standard CRUD operations, bound/unbound actions and functions,
    navigation property traversal, and auto-paging support.

    Subclasses must set `domain` and `namespace` class attributes.
    """

    domain: str = ""
    namespace: str = ""

    def __init__(self, http: HttpTransport):
        self._http = http

    def _entity_set_url(self, entity_set: str) -> str:
        """Build URL for an entity set: {base}/{domain}/{entity_set}."""
        return f"{self._http._config.domain_url(self.domain)}/{entity_set}"

    def _entity_url(self, entity_set: str, entity_id: str) -> str:
        """Build URL for a single entity: {base}/{domain}/{entity_set}('{id}')."""
        return f"{self._entity_set_url(entity_set)}('{entity_id}')"

    def _bound_action_url(
        self, entity_set: str, entity_id: str, action_name: str
    ) -> str:
        """Build URL for a bound action on a specific entity."""
        return f"{self._entity_url(entity_set, entity_id)}/{self.namespace}.{action_name}"

    def _bound_function_url(
        self, entity_set: str, entity_id: str, function_name: str
    ) -> str:
        """Build URL for a bound function on a specific entity."""
        return f"{self._entity_url(entity_set, entity_id)}/{self.namespace}.{function_name}()"

    def _unbound_action_url(self, action_name: str) -> str:
        """Build URL for an unbound action on the domain."""
        return f"{self._http._config.domain_url(self.domain)}/{action_name}"

    def _unbound_function_url(self, function_name: str) -> str:
        """Build URL for an unbound function on the domain."""
        return f"{self._http._config.domain_url(self.domain)}/{function_name}()"

    def _navigation_url(
        self, entity_set: str, entity_id: str, nav_prop: str
    ) -> str:
        """Build URL for a navigation property."""
        return f"{self._entity_url(entity_set, entity_id)}/{nav_prop}"

    # ── CRUD Operations ──

    async def list(
        self,
        entity_set: str,
        query: Query | None = None,
    ) -> ODataResponse:
        """GET collection of entities with optional OData query."""
        url = self._entity_set_url(entity_set)
        params = query.to_params() if query else None
        data = await self._http.get_json(url, params=params)
        return ODataResponse.from_dict(data)

    async def get(self, entity_set: str, entity_id: str) -> dict[str, Any]:
        """GET a single entity by ID."""
        url = self._entity_url(entity_set, entity_id)
        return await self._http.get_json(url)

    async def create(
        self, entity_set: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """POST to create a new entity."""
        url = self._entity_set_url(entity_set)
        return await self._http.post_json(url, data)

    async def update(
        self, entity_set: str, entity_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """PATCH to update an existing entity."""
        url = self._entity_url(entity_set, entity_id)
        return await self._http.patch_json(url, data)

    async def delete(self, entity_set: str, entity_id: str) -> None:
        """DELETE an entity."""
        url = self._entity_url(entity_set, entity_id)
        await self._http.delete(url)

    # ── Bound Actions & Functions ──

    async def action(
        self,
        entity_set: str,
        entity_id: str,
        action_name: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST to invoke a bound action on a specific entity."""
        url = self._bound_action_url(entity_set, entity_id, action_name)
        return await self._http.post_json(url, body or {})

    async def function(
        self,
        entity_set: str,
        entity_id: str,
        function_name: str,
    ) -> dict[str, Any]:
        """GET to invoke a bound function on a specific entity."""
        url = self._bound_function_url(entity_set, entity_id, function_name)
        return await self._http.get_json(url)

    # ── Unbound Actions & Functions ──

    async def unbound_action(
        self,
        action_name: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST to invoke an unbound action on the domain."""
        url = self._unbound_action_url(action_name)
        return await self._http.post_json(url, body or {})

    async def unbound_function(
        self,
        function_name: str,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """GET to invoke an unbound function on the domain."""
        url = self._unbound_function_url(function_name)
        return await self._http.get_json(url, params=params)

    # ── Navigation Properties ──

    async def navigate(
        self,
        entity_set: str,
        entity_id: str,
        nav_prop: str,
        query: Query | None = None,
    ) -> ODataResponse:
        """GET related entities via a navigation property."""
        url = self._navigation_url(entity_set, entity_id, nav_prop)
        params = query.to_params() if query else None
        data = await self._http.get_json(url, params=params)
        return ODataResponse.from_dict(data)

    # ── Pagination ──

    async def list_all(
        self,
        entity_set: str,
        query: Query | None = None,
        max_items: int | None = None,
    ) -> list[dict[str, Any]]:
        """Collect all items across all pages for an entity set."""
        url = self._entity_set_url(entity_set)
        params = query.to_params() if query else None
        return await collect_all(
            self._http,
            url,
            params=params,
            max_page_size=self._http._config.max_page_size,
            max_items=max_items,
        )

    async def paginate(
        self,
        entity_set: str,
        query: Query | None = None,
    ):
        """Async generator yielding pages for an entity set."""
        url = self._entity_set_url(entity_set)
        params = query.to_params() if query else None
        async for page in paginate(
            self._http,
            url,
            params=params,
            max_page_size=self._http._config.max_page_size,
        ):
            yield page
