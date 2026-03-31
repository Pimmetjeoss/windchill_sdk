"""Workflow domain - WorkItems, task routing, and process management."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class Workflow(BaseDomain):
    """Workflow domain.

    Manages workflow work items, task completion, reassignment,
    and routing options.
    """

    domain = "Workflow"
    namespace = "PTC.Workflow"

    # ── WorkItems CRUD ──

    async def list_workitems(self, query: Query | None = None) -> ODataResponse:
        """List workflow work items."""
        return await self.list("WorkItems", query)

    async def get_workitem(self, workitem_id: str) -> dict[str, Any]:
        """Get a single work item by ID."""
        return await self.get("WorkItems", workitem_id)

    # ── Bound Functions ──

    async def get_routing_options(self, workitem_id: str) -> dict[str, Any]:
        """Get available routing options for a work item."""
        return await self.function("WorkItems", workitem_id, "GetRoutingOptions")

    async def get_valid_reassign_users(self, workitem_id: str) -> dict[str, Any]:
        """Get list of users the work item can be reassigned to."""
        return await self.function("WorkItems", workitem_id, "GetValidReassignUsers")

    # ── Bound Actions ──

    async def complete_workitem(
        self,
        workitem_id: str,
        *,
        routing_option: str | None = None,
        comment: str | None = None,
        user_event_list: list[str] | None = None,
        vote_action: str | None = None,
        automate_fast_track: bool | None = None,
        variables: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Complete (finish) a workflow work item.

        Args:
            workitem_id: Work item Object Reference ID.
            routing_option: Routing option name from GetRoutingOptions.
            comment: Completion comment.
            user_event_list: List of user events.
            vote_action: Vote action string.
            automate_fast_track: Whether to automate fast track.
            variables: List of variable dicts with Name/Value.
        """
        body: dict[str, Any] = {}
        if routing_option:
            body["RoutingOption"] = routing_option
        if comment:
            body["Comments"] = comment
        if user_event_list:
            body["UserEventList"] = user_event_list
        if vote_action:
            body["VoteAction"] = vote_action
        if automate_fast_track is not None:
            body["AutomateFastTrack"] = automate_fast_track
        if variables:
            body["Variables"] = variables
        return await self.action("WorkItems", workitem_id, "Complete", body)

    async def save_workitem(
        self,
        workitem_id: str,
        *,
        comment: str | None = None,
        variables: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Save (but not complete) a workflow work item."""
        body: dict[str, Any] = {}
        if comment:
            body["Comments"] = comment
        if variables:
            body["Variables"] = variables
        return await self.action("WorkItems", workitem_id, "Save", body)

    async def reassign_workitem(
        self,
        workitem_id: str,
        reassign_to: str,
        *,
        comment: str | None = None,
    ) -> dict[str, Any]:
        """Reassign a work item to another user.

        Args:
            workitem_id: Work item Object Reference ID.
            reassign_to: User ID or username to reassign to.
            comment: Reassignment comment.
        """
        body: dict[str, Any] = {"ReassignTo": reassign_to}
        if comment:
            body["Comments"] = comment
        return await self.action("WorkItems", workitem_id, "Reassign", body)

    # ── Unbound Actions ──

    async def reassign_workitems(
        self,
        workitem_ids: list[str],
        user_id: str,
        *,
        comment: str | None = None,
    ) -> dict[str, Any]:
        """Reassign multiple work items to a user (unbound action)."""
        body: dict[str, Any] = {
            "WorkItems": [{"ID": wid} for wid in workitem_ids],
            "User": {"ID": user_id},
        }
        if comment:
            body["Comment"] = comment
        return await self.unbound_action("ReassignWorkItems", body)

    # ── Unbound Functions ──

    async def get_workitem_reassign_user_list(
        self, workitem_ids: list[str]
    ) -> dict[str, Any]:
        """Get reassignable users for multiple work items (unbound function)."""
        wi_param = ",".join(f"'{wid}'" for wid in workitem_ids)
        return await self.unbound_function(
            "GetWorkItemReassignUserList",
            params={"@wi": f"[{wi_param}]"},
        )

    # ── Navigation ──

    async def get_workitem_subject(
        self, workitem_id: str
    ) -> ODataResponse:
        """Get the subject (business object) of a work item."""
        return await self.navigate("WorkItems", workitem_id, "Subject")

    async def get_workitem_activities(
        self, workitem_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get activities related to a work item."""
        return await self.navigate("WorkItems", workitem_id, "Activities", query)
