"""Data Administration domain - Containers, Folders, Cabinets, Teams."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class DataAdmin(BaseDomain):
    """Data Administration domain (DataAdmin).

    Manages organizational structure including containers (Products, Libraries,
    Projects), folders, cabinets, and team membership.
    """

    domain = "DataAdmin"
    namespace = "PTC.DataAdmin"

    # ── Containers ──

    async def list_containers(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List containers (Products, Libraries, Projects) with optional query."""
        return await self.list("Containers", query)

    async def get_container(self, container_id: str) -> dict[str, Any]:
        """Get a single container by Object Reference ID."""
        return await self.get("Containers", container_id)

    # ── Folders ──

    async def list_folders(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List folders with optional OData query."""
        return await self.list("Folders", query)

    async def get_folder(self, folder_id: str) -> dict[str, Any]:
        """Get a single folder by Object Reference ID."""
        return await self.get("Folders", folder_id)

    async def create_folder(
        self,
        name: str,
        *,
        context_id: str,
        parent_folder_path: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new folder within a container.

        Args:
            name: Folder name.
            context_id: Container Object Reference ID (required).
            parent_folder_path: Path to the parent folder (e.g., "/Default/Design").
                When omitted, the folder is created at the container root.
            description: Folder description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {
            "Name": name,
            "Context@odata.bind": f"Containers('{context_id}')",
            **attributes,
        }
        if parent_folder_path:
            data["ParentFolderPath"] = parent_folder_path
        if description:
            data["Description"] = description
        return await self.create("Folders", data)

    # ── SubFolders (navigation property) ──

    async def get_sub_folders(
        self, folder_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get immediate sub-folders of a folder."""
        return await self.navigate("Folders", folder_id, "SubFolders", query)

    # ── Cabinets ──

    async def list_cabinets(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List cabinets with optional OData query."""
        return await self.list("Cabinets", query)

    async def get_cabinet(self, cabinet_id: str) -> dict[str, Any]:
        """Get a single cabinet by Object Reference ID."""
        return await self.get("Cabinets", cabinet_id)

    # ── Teams ──

    async def list_teams(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List teams with optional OData query."""
        return await self.list("Teams", query)

    async def get_team(self, team_id: str) -> dict[str, Any]:
        """Get a single team by Object Reference ID."""
        return await self.get("Teams", team_id)

    # ── Pagination Helpers ──

    async def get_all_containers(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all containers across all pages."""
        return await self.list_all("Containers", query, max_items)

    async def get_all_folders(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all folders across all pages."""
        return await self.list_all("Folders", query, max_items)
