"""Event Management domain - Event subscriptions and event history."""

from __future__ import annotations

from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class EventMgmt(BaseDomain):
    """Event Management domain (EventMgmt).

    Manages event subscriptions for object lifecycle notifications and
    provides access to the event log.
    """

    domain = "EventMgmt"
    namespace = "PTC.EventMgmt"

    # ── EventSubscriptions ──

    async def list_subscriptions(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List event subscriptions with optional OData query."""
        return await self.list("EventSubscriptions", query)

    async def get_subscription(self, subscription_id: str) -> dict[str, Any]:
        """Get a single event subscription by Object Reference ID."""
        return await self.get("EventSubscriptions", subscription_id)

    async def create_subscription(
        self,
        *,
        event_type: str,
        target_type: str | None = None,
        target_id: str | None = None,
        context_id: str | None = None,
        callback_url: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new event subscription.

        Args:
            event_type: Type of event to subscribe to
                (e.g., "STATE_CHANGE", "CHECKIN", "CHECKOUT").
            target_type: OData type of the target entity.
            target_id: Object Reference ID of the specific target entity.
            context_id: Container Object Reference ID to scope the subscription.
            callback_url: URL to receive event notifications.
            **attributes: Additional subscription properties.
        """
        data: dict[str, Any] = {"EventType": event_type, **attributes}
        if target_type:
            data["TargetType"] = target_type
        if target_id:
            data["TargetID"] = target_id
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if callback_url:
            data["CallbackURL"] = callback_url
        return await self.create("EventSubscriptions", data)

    async def delete_subscription(self, subscription_id: str) -> None:
        """Delete an event subscription."""
        await self.delete("EventSubscriptions", subscription_id)

    # ── Events ──

    async def list_events(
        self, query: Query | None = None
    ) -> ODataResponse:
        """List events from the event log with optional OData query."""
        return await self.list("Events", query)

    async def get_event(self, event_id: str) -> dict[str, Any]:
        """Get a single event by Object Reference ID."""
        return await self.get("Events", event_id)

    # ── Pagination Helpers ──

    async def get_all_subscriptions(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all event subscriptions across all pages."""
        return await self.list_all("EventSubscriptions", query, max_items)

    async def get_all_events(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all events across all pages."""
        return await self.list_all("Events", query, max_items)
