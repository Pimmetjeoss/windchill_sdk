"""Shared type definitions for Windchill SDK."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ODataResponse:
    """Parsed OData response envelope."""

    context: str = ""
    value: list[dict[str, Any]] | dict[str, Any] = field(default_factory=list)
    next_link: str | None = None
    count: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ODataResponse:
        """Parse a raw OData JSON response into an ODataResponse."""
        return cls(
            context=data.get("@odata.context", ""),
            value=data.get("value", data),
            next_link=data.get("@odata.nextLink"),
            count=data.get("@odata.count"),
        )

    @property
    def items(self) -> list[dict[str, Any]]:
        """Return value as a list, wrapping single entities."""
        if isinstance(self.value, list):
            return self.value
        return [self.value]

    @property
    def first(self) -> dict[str, Any] | None:
        """Return the first item, or None if empty."""
        items = self.items
        return items[0] if items else None

    @property
    def has_more(self) -> bool:
        """Whether there are more pages available."""
        return self.next_link is not None


@dataclass(frozen=True)
class EntityRef:
    """Reference to a Windchill entity."""

    id: str
    entity_set: str
    domain: str

    @property
    def odata_id(self) -> str:
        """OData entity identifier path."""
        return f"{self.entity_set}('{self.id}')"

    def bind_path(self, property_name: str) -> dict[str, str]:
        """Generate an @odata.bind reference for linking entities."""
        return {f"{property_name}@odata.bind": f"{self.entity_set}('{self.id}')"}


@dataclass(frozen=True)
class BatchOperationResult:
    """Result of a single operation within a batch response."""

    content_id: str | None
    status_code: int
    headers: dict[str, str] = field(default_factory=dict)
    body: dict[str, Any] | None = None

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300


@dataclass(frozen=True)
class BatchResponse:
    """Parsed batch response containing individual operation results."""

    operations: list[BatchOperationResult] = field(default_factory=list)

    @property
    def all_successful(self) -> bool:
        return all(op.is_success for op in self.operations)

    @property
    def failed(self) -> list[BatchOperationResult]:
        return [op for op in self.operations if not op.is_success]
