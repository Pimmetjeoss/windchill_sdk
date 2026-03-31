"""Classification Structure domain - Nodes, Attributes, and Classified Objects."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class ClfStructure(BaseDomain):
    """Classification Structure domain (ClfStructure).

    Manages classification hierarchies including nodes, attributes,
    and classified objects. Provides unbound functions for traversing
    the classification tree.
    """

    domain = "ClfStructure"
    namespace = "PTC.ClfStructure"

    # ── Classification Nodes CRUD ──

    async def list_classification_nodes(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List classification nodes with optional OData query."""
        return await self.list("ClassificationNodes", query)

    async def get_classification_node(self, node_id: str) -> dict[str, Any]:
        """Get a single classification node by ID."""
        return await self.get("ClassificationNodes", node_id)

    async def create_classification_node(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new classification node."""
        return await self.create("ClassificationNodes", data)

    async def update_classification_node(
        self, node_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing classification node."""
        return await self.update("ClassificationNodes", node_id, data)

    async def delete_classification_node(self, node_id: str) -> None:
        """Delete a classification node."""
        await self.delete("ClassificationNodes", node_id)

    # ── Classification Attributes CRUD ──

    async def list_classification_attributes(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List classification attributes with optional OData query."""
        return await self.list("ClassificationAttributes", query)

    async def get_classification_attribute(
        self, attribute_id: str
    ) -> dict[str, Any]:
        """Get a single classification attribute by ID."""
        return await self.get("ClassificationAttributes", attribute_id)

    async def create_classification_attribute(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new classification attribute."""
        return await self.create("ClassificationAttributes", data)

    async def update_classification_attribute(
        self, attribute_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing classification attribute."""
        return await self.update("ClassificationAttributes", attribute_id, data)

    async def delete_classification_attribute(
        self, attribute_id: str
    ) -> None:
        """Delete a classification attribute."""
        await self.delete("ClassificationAttributes", attribute_id)

    # ── Classified Objects CRUD ──

    async def list_classified_objects(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List classified objects with optional OData query."""
        return await self.list("ClassifiedObjects", query)

    async def get_classified_object(
        self, classified_object_id: str
    ) -> dict[str, Any]:
        """Get a single classified object by ID."""
        return await self.get("ClassifiedObjects", classified_object_id)

    async def create_classified_object(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new classified object record."""
        return await self.create("ClassifiedObjects", data)

    async def update_classified_object(
        self, classified_object_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing classified object."""
        return await self.update(
            "ClassifiedObjects", classified_object_id, data
        )

    async def delete_classified_object(
        self, classified_object_id: str
    ) -> None:
        """Delete a classified object record."""
        await self.delete("ClassifiedObjects", classified_object_id)

    # ── Unbound Functions ──

    async def get_child_nodes(self, node_id: str) -> dict[str, Any]:
        """Get child nodes of a classification node.

        Args:
            node_id: The parent classification node ID.
        """
        return await self.unbound_function(
            "GetChildNodes",
            params={"NodeID": f"'{node_id}'"},
        )

    async def get_classification_attributes_for_node(
        self, node_id: str
    ) -> dict[str, Any]:
        """Get classification attributes defined on a node.

        Args:
            node_id: The classification node ID.
        """
        return await self.unbound_function(
            "GetClassificationAttributes",
            params={"NodeID": f"'{node_id}'"},
        )

    async def get_root_nodes(self, hierarchy_name: str) -> dict[str, Any]:
        """Get root nodes of a classification hierarchy.

        Args:
            hierarchy_name: The name of the classification hierarchy.
        """
        return await self.unbound_function(
            "GetRootNodes",
            params={"HierarchyName": f"'{hierarchy_name}'"},
        )
