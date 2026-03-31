"""Quality Management System domain - Audits, Findings, and Quality Actions."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class QMS(BaseDomain):
    """Quality Management System domain (QMS).

    Manages audits, audit findings, and quality actions for
    quality management processes.
    """

    domain = "QMS"
    namespace = "PTC.QMS"

    # ── Audits CRUD ──

    async def list_audits(self, query: Query | None = None) -> ODataResponse:
        """List audits with optional OData query."""
        return await self.list("Audits", query)

    async def get_audit(self, audit_id: str) -> dict[str, Any]:
        """Get a single audit by ID."""
        return await self.get("Audits", audit_id)

    async def create_audit(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new audit.

        Args:
            name: Audit name.
            context_id: Container Object Reference ID.
            description: Audit description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("Audits", data)

    async def update_audit(
        self, audit_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing audit."""
        return await self.update("Audits", audit_id, data)

    async def delete_audit(self, audit_id: str) -> None:
        """Delete an audit."""
        await self.delete("Audits", audit_id)

    # ── Audit Findings CRUD ──

    async def list_audit_findings(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List audit findings with optional OData query."""
        return await self.list("AuditFindings", query)

    async def get_audit_finding(self, finding_id: str) -> dict[str, Any]:
        """Get a single audit finding by ID."""
        return await self.get("AuditFindings", finding_id)

    async def create_audit_finding(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new audit finding.

        Args:
            name: Finding name.
            context_id: Container Object Reference ID.
            description: Finding description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("AuditFindings", data)

    async def update_audit_finding(
        self, finding_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing audit finding."""
        return await self.update("AuditFindings", finding_id, data)

    async def delete_audit_finding(self, finding_id: str) -> None:
        """Delete an audit finding."""
        await self.delete("AuditFindings", finding_id)

    # ── Quality Actions CRUD ──

    async def list_quality_actions(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List quality actions with optional OData query."""
        return await self.list("QualityActions", query)

    async def get_quality_action(self, action_id: str) -> dict[str, Any]:
        """Get a single quality action by ID."""
        return await self.get("QualityActions", action_id)

    async def create_quality_action(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new quality action.

        Args:
            name: Quality action name.
            context_id: Container Object Reference ID.
            description: Quality action description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("QualityActions", data)

    async def update_quality_action(
        self, action_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing quality action."""
        return await self.update("QualityActions", action_id, data)

    async def delete_quality_action(self, action_id: str) -> None:
        """Delete a quality action."""
        await self.delete("QualityActions", action_id)
