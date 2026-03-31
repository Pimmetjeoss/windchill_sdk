"""Change Management domain - Problem Reports, Change Requests/Notices/Tasks, Variances."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class ChangeMgmt(BaseDomain):
    """Change Management domain (ChangeMgmt).

    Manages change processes including Problem Reports, Change Requests (ECR),
    Change Notices (ECN), Change Tasks, and Variances.
    """

    domain = "ChangeMgmt"
    namespace = "PTC.ChangeMgmt"

    # ── Problem Reports ──

    async def list_problem_reports(self, query: Query | None = None) -> ODataResponse:
        return await self.list("ProblemReports", query)

    async def get_problem_report(self, pr_id: str) -> dict[str, Any]:
        return await self.get("ProblemReports", pr_id)

    async def create_problem_report(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("ProblemReports", data)

    # ── Change Requests (ECR) ──

    async def list_change_requests(self, query: Query | None = None) -> ODataResponse:
        return await self.list("ChangeRequests", query)

    async def get_change_request(self, ecr_id: str) -> dict[str, Any]:
        return await self.get("ChangeRequests", ecr_id)

    async def create_change_request(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("ChangeRequests", data)

    # ── Change Notices (ECN) ──

    async def list_change_notices(self, query: Query | None = None) -> ODataResponse:
        return await self.list("ChangeNotices", query)

    async def get_change_notice(self, ecn_id: str) -> dict[str, Any]:
        return await self.get("ChangeNotices", ecn_id)

    async def create_change_notice(
        self,
        name: str,
        *,
        context_id: str | None = None,
        description: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        return await self.create("ChangeNotices", data)

    # ── Change Tasks ──

    async def list_change_tasks(self, query: Query | None = None) -> ODataResponse:
        return await self.list("ChangeTasks", query)

    async def get_change_task(self, task_id: str) -> dict[str, Any]:
        return await self.get("ChangeTasks", task_id)

    # ── Variances ──

    async def list_variances(self, query: Query | None = None) -> ODataResponse:
        return await self.list("Variances", query)

    async def get_variance(self, variance_id: str) -> dict[str, Any]:
        return await self.get("Variances", variance_id)

    async def create_variance(
        self,
        name: str,
        *,
        context_id: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {"Name": name, **attributes}
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        return await self.create("Variances", data)

    # ── Common Actions ──

    async def set_state(
        self, entity_set: str, entity_id: str, state: str
    ) -> dict[str, Any]:
        """Set lifecycle state on any change management entity."""
        return await self.action(
            entity_set, entity_id, "SetLifeCycleState", {"State": state}
        )

    # ── Navigation ──

    async def get_affected_objects(
        self, entity_set: str, entity_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get objects affected by a change object."""
        return await self.navigate(entity_set, entity_id, "AffectedObjects", query)

    async def get_resulting_objects(
        self, entity_set: str, entity_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get resulting objects of a change object."""
        return await self.navigate(entity_set, entity_id, "ResultingObjects", query)
