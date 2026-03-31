"""Customer Experience Management domain - Complaints and Feedbacks."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class CEM(BaseDomain):
    """Customer Experience Management domain (CEM).

    Manages customer complaints and customer feedback records
    for tracking and improving the customer experience.
    """

    domain = "CEM"
    namespace = "PTC.CEM"

    # ── Customer Complaints CRUD ──

    async def list_customer_complaints(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List customer complaints with optional OData query."""
        return await self.list("CustomerComplaints", query)

    async def get_customer_complaint(self, complaint_id: str) -> dict[str, Any]:
        """Get a single customer complaint by ID."""
        return await self.get("CustomerComplaints", complaint_id)

    async def create_customer_complaint(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new customer complaint.

        Args:
            name: Complaint name.
            context_id: Container Object Reference ID.
            description: Complaint description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("CustomerComplaints", data)

    async def update_customer_complaint(
        self, complaint_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing customer complaint."""
        return await self.update("CustomerComplaints", complaint_id, data)

    async def delete_customer_complaint(self, complaint_id: str) -> None:
        """Delete a customer complaint."""
        await self.delete("CustomerComplaints", complaint_id)

    # ── Customer Feedbacks CRUD ──

    async def list_customer_feedbacks(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List customer feedbacks with optional OData query."""
        return await self.list("CustomerFeedbacks", query)

    async def get_customer_feedback(self, feedback_id: str) -> dict[str, Any]:
        """Get a single customer feedback by ID."""
        return await self.get("CustomerFeedbacks", feedback_id)

    async def create_customer_feedback(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new customer feedback.

        Args:
            name: Feedback name.
            context_id: Container Object Reference ID.
            description: Feedback description.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("CustomerFeedbacks", data)

    async def update_customer_feedback(
        self, feedback_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing customer feedback."""
        return await self.update("CustomerFeedbacks", feedback_id, data)

    async def delete_customer_feedback(self, feedback_id: str) -> None:
        """Delete a customer feedback."""
        await self.delete("CustomerFeedbacks", feedback_id)
