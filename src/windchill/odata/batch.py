"""OData v4 batch request builder for Windchill REST API.

Generates multipart/mixed batch requests with support for:
- Independent GET/POST/PATCH/DELETE operations
- Atomic changesets (grouped writes with rollback)
- Content-ID cross-referencing within changesets
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from typing import Any

from windchill.odata.query import Query

NEWLINE = "\r\n"


@dataclass(frozen=True)
class BatchOperation:
    """A single HTTP operation within a batch request."""

    method: str
    path: str
    body: dict[str, Any] | None = None
    content_id: str | None = None
    headers: dict[str, str] = field(default_factory=dict)

    def to_http_part(self) -> str:
        """Serialize this operation as an HTTP message within a multipart part."""
        lines = [
            "Content-Type: application/http",
            "Content-Transfer-Encoding: binary",
        ]
        if self.content_id:
            lines.append(f"Content-ID: {self.content_id}")
        lines.append("")

        # HTTP request line
        lines.append(f"{self.method} {self.path} HTTP/1.1")

        # Headers
        all_headers = dict(self.headers)
        if self.body is not None:
            all_headers.setdefault("Content-Type", "application/json")
        for key, value in all_headers.items():
            lines.append(f"{key}: {value}")

        lines.append("")

        # Body
        if self.body is not None:
            lines.append(json.dumps(self.body))
        else:
            lines.append("")

        return NEWLINE.join(lines)


@dataclass
class Changeset:
    """An atomic changeset within a batch - all operations succeed or all roll back."""

    boundary: str = field(default_factory=lambda: f"changeset_{uuid.uuid4().hex[:12]}")
    operations: list[BatchOperation] = field(default_factory=list)

    def to_multipart(self) -> str:
        """Serialize the changeset as a multipart/mixed section."""
        parts = []
        for op in self.operations:
            parts.append(f"--{self.boundary}")
            parts.append(op.to_http_part())
        parts.append(f"--{self.boundary}--")
        return NEWLINE.join(parts)


class Batch:
    """Builder for OData v4 batch requests.

    Usage:
        batch = (
            Batch(domain="ProdMgmt")
            .begin_changeset()
            .post("Parts", {"Name": "New Part"}, content_id="1_1")
            .post("Parts('$1_1')/PTC.ProdMgmt.CheckOut", {}, content_id="2_1")
            .end_changeset()
            .get("Parts", query=Query().top(5))
        )
        content_type, body = batch.build()
    """

    def __init__(self, domain: str):
        self.domain = domain
        self._boundary = f"batch_{uuid.uuid4().hex[:12]}"
        self._parts: list[BatchOperation | Changeset] = []
        self._current_changeset: Changeset | None = None

    def begin_changeset(self) -> Batch:
        """Start a new atomic changeset."""
        if self._current_changeset is not None:
            raise ValueError("Cannot nest changesets")
        self._current_changeset = Changeset()
        return self

    def end_changeset(self) -> Batch:
        """Close the current changeset and add it to the batch."""
        if self._current_changeset is None:
            raise ValueError("No changeset is open")
        self._parts.append(self._current_changeset)
        self._current_changeset = None
        return self

    def get(
        self,
        path: str,
        *,
        query: Query | None = None,
        content_id: str | None = None,
    ) -> Batch:
        """Add a GET operation (not allowed inside changesets)."""
        if self._current_changeset is not None:
            raise ValueError("GET operations are not allowed inside changesets")
        full_path = self._build_path(path, query)
        op = BatchOperation(method="GET", path=full_path, content_id=content_id)
        self._parts.append(op)
        return self

    def post(
        self,
        path: str,
        body: dict[str, Any] | None = None,
        *,
        content_id: str | None = None,
    ) -> Batch:
        """Add a POST operation."""
        op = BatchOperation(method="POST", path=path, body=body, content_id=content_id)
        if self._current_changeset is not None:
            self._current_changeset.operations.append(op)
        else:
            self._parts.append(op)
        return self

    def patch(
        self,
        path: str,
        body: dict[str, Any],
        *,
        content_id: str | None = None,
    ) -> Batch:
        """Add a PATCH operation."""
        op = BatchOperation(method="PATCH", path=path, body=body, content_id=content_id)
        if self._current_changeset is not None:
            self._current_changeset.operations.append(op)
        else:
            self._parts.append(op)
        return self

    def delete(
        self,
        path: str,
        *,
        content_id: str | None = None,
    ) -> Batch:
        """Add a DELETE operation."""
        op = BatchOperation(method="DELETE", path=path, content_id=content_id)
        if self._current_changeset is not None:
            self._current_changeset.operations.append(op)
        else:
            self._parts.append(op)
        return self

    def _build_path(self, path: str, query: Query | None) -> str:
        """Build a path with optional query parameters."""
        if query:
            qs = query.to_query_string()
            return f"{path}{qs}"
        return path

    def build(self) -> tuple[str, str]:
        """Build the batch request body and content type.

        Returns:
            Tuple of (content_type, body_string).
        """
        if self._current_changeset is not None:
            raise ValueError("Unclosed changeset - call end_changeset() first")

        sections = []
        for part in self._parts:
            sections.append(f"--{self._boundary}")
            if isinstance(part, Changeset):
                sections.append(
                    f"Content-Type: multipart/mixed;boundary={part.boundary}"
                )
                sections.append("")
                sections.append(part.to_multipart())
            else:
                sections.append(part.to_http_part())

        sections.append(f"--{self._boundary}--")

        body = NEWLINE.join(sections)
        content_type = f"multipart/mixed;boundary={self._boundary}"
        return content_type, body

    @property
    def batch_url(self) -> str:
        """The $batch endpoint path for this domain."""
        return f"{self.domain}/$batch"
