"""Visualization domain - Representations, Files, and Thumbnails."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class Visualization(BaseDomain):
    """Visualization domain.

    Manages 3D/2D representations, representation files, and
    thumbnail images for visual content associated with business objects.
    """

    domain = "Visualization"
    namespace = "PTC.Visualization"

    # ── Representations CRUD ──

    async def list_representations(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List representations with optional OData query."""
        return await self.list("Representations", query)

    async def get_representation(
        self, representation_id: str
    ) -> dict[str, Any]:
        """Get a single representation by ID."""
        return await self.get("Representations", representation_id)

    async def create_representation(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new representation."""
        return await self.create("Representations", data)

    async def update_representation(
        self, representation_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing representation."""
        return await self.update("Representations", representation_id, data)

    async def delete_representation(self, representation_id: str) -> None:
        """Delete a representation."""
        await self.delete("Representations", representation_id)

    # ── Representation Files CRUD ──

    async def list_representation_files(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List representation files with optional OData query."""
        return await self.list("RepresentationFiles", query)

    async def get_representation_file(self, file_id: str) -> dict[str, Any]:
        """Get a single representation file by ID."""
        return await self.get("RepresentationFiles", file_id)

    async def create_representation_file(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new representation file."""
        return await self.create("RepresentationFiles", data)

    async def update_representation_file(
        self, file_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing representation file."""
        return await self.update("RepresentationFiles", file_id, data)

    async def delete_representation_file(self, file_id: str) -> None:
        """Delete a representation file."""
        await self.delete("RepresentationFiles", file_id)

    # ── Thumbnails CRUD ──

    async def list_thumbnails(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List thumbnails with optional OData query."""
        return await self.list("Thumbnails", query)

    async def get_thumbnail(self, thumbnail_id: str) -> dict[str, Any]:
        """Get a single thumbnail by ID."""
        return await self.get("Thumbnails", thumbnail_id)

    async def create_thumbnail(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new thumbnail."""
        return await self.create("Thumbnails", data)

    async def update_thumbnail(
        self, thumbnail_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing thumbnail."""
        return await self.update("Thumbnails", thumbnail_id, data)

    async def delete_thumbnail(self, thumbnail_id: str) -> None:
        """Delete a thumbnail."""
        await self.delete("Thumbnails", thumbnail_id)

    # ── Navigation: Representation -> Files ──

    async def get_representation_files(
        self, representation_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get files belonging to a representation via navigation property."""
        return await self.navigate(
            "Representations", representation_id, "RepresentationFiles", query
        )
