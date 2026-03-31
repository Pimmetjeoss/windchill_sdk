"""Auto-paging support for OData v4 responses."""

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from windchill.types import ODataResponse

if TYPE_CHECKING:
    from windchill.http import HttpTransport


async def paginate(
    http: HttpTransport,
    url: str,
    params: dict[str, str] | None = None,
    max_page_size: int | None = None,
) -> AsyncIterator[ODataResponse]:
    """Async generator that follows @odata.nextLink for auto-paging.

    Yields one ODataResponse per page. Each page contains up to max_page_size items.

    Usage:
        async for page in paginate(http, url, params):
            for item in page.items:
                process(item)
    """
    headers: dict[str, str] = {}
    if max_page_size:
        headers["Prefer"] = f"odata.maxpagesize={max_page_size}"

    current_url = url
    current_params = params
    is_first = True

    while current_url:
        if is_first:
            data = await http.get_json(current_url, params=current_params)
            is_first = False
        else:
            # nextLink URLs are absolute and include query params
            data = await http.get_json(current_url)

        page = ODataResponse.from_dict(data)
        yield page

        current_url = page.next_link
        current_params = None  # nextLink includes all params


async def collect_all(
    http: HttpTransport,
    url: str,
    params: dict[str, str] | None = None,
    max_page_size: int | None = None,
    max_items: int | None = None,
) -> list[dict]:
    """Collect all items across all pages into a single list.

    Args:
        http: HTTP transport instance.
        url: Initial request URL.
        params: Query parameters for the first request.
        max_page_size: Server-side page size hint.
        max_items: Stop collecting after this many items (safety limit).

    Returns:
        List of all entity dicts across all pages.
    """
    items: list[dict] = []

    async for page in paginate(http, url, params, max_page_size):
        items.extend(page.items)
        if max_items and len(items) >= max_items:
            items = items[:max_items]
            break

    return items
