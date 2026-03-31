"""Manufacturing Process Management domain - Process Plans, Operations, and Consumed Parts."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class MfgProcessMgmt(BaseDomain):
    """Manufacturing Process Management domain (MfgProcessMgmt).

    Manages process plans, operations, operation sequences, and consumed
    parts for manufacturing process definition and planning.
    """

    domain = "MfgProcessMgmt"
    namespace = "PTC.MfgProcessMgmt"

    # ── Process Plans CRUD ──

    async def list_process_plans(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List process plans with optional OData query."""
        return await self.list("ProcessPlans", query)

    async def get_process_plan(self, plan_id: str) -> dict[str, Any]:
        """Get a single process plan by ID."""
        return await self.get("ProcessPlans", plan_id)

    async def create_process_plan(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new process plan.

        Args:
            name: Process plan name.
            context_id: Container Object Reference ID.
            description: Process plan description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("ProcessPlans", data)

    async def update_process_plan(
        self, plan_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing process plan."""
        return await self.update("ProcessPlans", plan_id, data)

    async def delete_process_plan(self, plan_id: str) -> None:
        """Delete a process plan."""
        await self.delete("ProcessPlans", plan_id)

    # ── Operations CRUD ──

    async def list_operations(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List operations with optional OData query."""
        return await self.list("Operations", query)

    async def get_operation(self, operation_id: str) -> dict[str, Any]:
        """Get a single operation by ID."""
        return await self.get("Operations", operation_id)

    async def create_operation(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new operation.

        Args:
            name: Operation name.
            context_id: Container Object Reference ID.
            description: Operation description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("Operations", data)

    async def update_operation(
        self, operation_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing operation."""
        return await self.update("Operations", operation_id, data)

    async def delete_operation(self, operation_id: str) -> None:
        """Delete an operation."""
        await self.delete("Operations", operation_id)

    # ── Operation Sequences CRUD ──

    async def list_operation_sequences(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List operation sequences with optional OData query."""
        return await self.list("OperationSequences", query)

    async def get_operation_sequence(self, sequence_id: str) -> dict[str, Any]:
        """Get a single operation sequence by ID."""
        return await self.get("OperationSequences", sequence_id)

    async def create_operation_sequence(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new operation sequence."""
        return await self.create("OperationSequences", data)

    async def update_operation_sequence(
        self, sequence_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing operation sequence."""
        return await self.update("OperationSequences", sequence_id, data)

    async def delete_operation_sequence(self, sequence_id: str) -> None:
        """Delete an operation sequence."""
        await self.delete("OperationSequences", sequence_id)

    # ── Consumed Parts CRUD ──

    async def list_consumed_parts(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List consumed parts with optional OData query."""
        return await self.list("ConsumedParts", query)

    async def get_consumed_part(self, consumed_part_id: str) -> dict[str, Any]:
        """Get a single consumed part by ID."""
        return await self.get("ConsumedParts", consumed_part_id)

    async def create_consumed_part(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new consumed part record."""
        return await self.create("ConsumedParts", data)

    async def update_consumed_part(
        self, consumed_part_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing consumed part."""
        return await self.update("ConsumedParts", consumed_part_id, data)

    async def delete_consumed_part(self, consumed_part_id: str) -> None:
        """Delete a consumed part record."""
        await self.delete("ConsumedParts", consumed_part_id)

    # ── Navigation: ProcessPlans -> Operations ──

    async def get_plan_operations(
        self, plan_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get operations belonging to a process plan."""
        return await self.navigate("ProcessPlans", plan_id, "Operations", query)

    # ── Navigation: Operations -> ConsumedParts ──

    async def get_operation_consumed_parts(
        self, operation_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get consumed parts for an operation."""
        return await self.navigate(
            "Operations", operation_id, "ConsumedParts", query
        )
