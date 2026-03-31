"""Product Platform Management domain - Platforms, Option Sets, Options, Choices, Expressions."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class ProdPlatformMgmt(BaseDomain):
    """Product Platform Management domain (ProdPlatformMgmt).

    Manages product platforms, option sets, options, choices, and
    expressions for configurable product platform definition.
    """

    domain = "ProdPlatformMgmt"
    namespace = "PTC.ProdPlatformMgmt"

    # ── Platforms CRUD ──

    async def list_platforms(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List platforms with optional OData query."""
        return await self.list("Platforms", query)

    async def get_platform(self, platform_id: str) -> dict[str, Any]:
        """Get a single platform by ID."""
        return await self.get("Platforms", platform_id)

    async def create_platform(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new platform.

        Args:
            name: Platform name.
            context_id: Container Object Reference ID.
            description: Platform description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("Platforms", data)

    async def update_platform(
        self, platform_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing platform."""
        return await self.update("Platforms", platform_id, data)

    async def delete_platform(self, platform_id: str) -> None:
        """Delete a platform."""
        await self.delete("Platforms", platform_id)

    # ── Option Sets CRUD ──

    async def list_option_sets(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List option sets with optional OData query."""
        return await self.list("OptionSets", query)

    async def get_option_set(self, option_set_id: str) -> dict[str, Any]:
        """Get a single option set by ID."""
        return await self.get("OptionSets", option_set_id)

    async def create_option_set(
        self,
        name: str,
        *,
        context_id: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new option set."""
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        return await self.create("OptionSets", data)

    async def update_option_set(
        self, option_set_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing option set."""
        return await self.update("OptionSets", option_set_id, data)

    async def delete_option_set(self, option_set_id: str) -> None:
        """Delete an option set."""
        await self.delete("OptionSets", option_set_id)

    # ── Options CRUD ──

    async def list_options(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List options with optional OData query."""
        return await self.list("Options", query)

    async def get_option(self, option_id: str) -> dict[str, Any]:
        """Get a single option by ID."""
        return await self.get("Options", option_id)

    async def create_option(
        self,
        name: str,
        *,
        context_id: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new option."""
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        return await self.create("Options", data)

    async def update_option(
        self, option_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing option."""
        return await self.update("Options", option_id, data)

    async def delete_option(self, option_id: str) -> None:
        """Delete an option."""
        await self.delete("Options", option_id)

    # ── Choices CRUD ──

    async def list_choices(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List choices with optional OData query."""
        return await self.list("Choices", query)

    async def get_choice(self, choice_id: str) -> dict[str, Any]:
        """Get a single choice by ID."""
        return await self.get("Choices", choice_id)

    async def create_choice(
        self,
        name: str,
        *,
        context_id: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new choice."""
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        return await self.create("Choices", data)

    async def update_choice(
        self, choice_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing choice."""
        return await self.update("Choices", choice_id, data)

    async def delete_choice(self, choice_id: str) -> None:
        """Delete a choice."""
        await self.delete("Choices", choice_id)

    # ── Expressions CRUD ──

    async def list_expressions(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List expressions with optional OData query."""
        return await self.list("Expressions", query)

    async def get_expression(self, expression_id: str) -> dict[str, Any]:
        """Get a single expression by ID."""
        return await self.get("Expressions", expression_id)

    async def create_expression(
        self,
        name: str,
        *,
        context_id: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new expression."""
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        return await self.create("Expressions", data)

    async def update_expression(
        self, expression_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing expression."""
        return await self.update("Expressions", expression_id, data)

    async def delete_expression(self, expression_id: str) -> None:
        """Delete an expression."""
        await self.delete("Expressions", expression_id)
