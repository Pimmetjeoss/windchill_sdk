"""Tests for auto-paging support."""

import pytest

from windchill.odata.paging import collect_all, paginate
from windchill.types import ODataResponse


class MockHttpTransport:
    """Mock HTTP transport that returns predefined pages."""

    def __init__(self, pages: list[dict]):
        self._pages = pages
        self._call_index = 0

    async def get_json(self, url: str, params: dict | None = None) -> dict:
        if self._call_index >= len(self._pages):
            return {"value": []}
        page = self._pages[self._call_index]
        self._call_index += 1
        return page


class TestPaginate:
    @pytest.mark.asyncio
    async def test_single_page(self):
        http = MockHttpTransport([
            {"value": [{"ID": "1"}, {"ID": "2"}]}
        ])
        pages = []
        async for page in paginate(http, "http://test/Parts"):
            pages.append(page)

        assert len(pages) == 1
        assert len(pages[0].items) == 2

    @pytest.mark.asyncio
    async def test_multiple_pages(self):
        http = MockHttpTransport([
            {
                "value": [{"ID": "1"}],
                "@odata.nextLink": "http://test/Parts?$skip=1",
            },
            {
                "value": [{"ID": "2"}],
                "@odata.nextLink": "http://test/Parts?$skip=2",
            },
            {"value": [{"ID": "3"}]},
        ])
        pages = []
        async for page in paginate(http, "http://test/Parts"):
            pages.append(page)

        assert len(pages) == 3
        assert pages[0].items[0]["ID"] == "1"
        assert pages[2].items[0]["ID"] == "3"

    @pytest.mark.asyncio
    async def test_empty_result(self):
        http = MockHttpTransport([{"value": []}])
        pages = []
        async for page in paginate(http, "http://test/Parts"):
            pages.append(page)

        assert len(pages) == 1
        assert len(pages[0].items) == 0


class TestCollectAll:
    @pytest.mark.asyncio
    async def test_collect_all_pages(self):
        http = MockHttpTransport([
            {
                "value": [{"ID": "1"}, {"ID": "2"}],
                "@odata.nextLink": "http://test/next",
            },
            {"value": [{"ID": "3"}]},
        ])
        items = await collect_all(http, "http://test/Parts")
        assert len(items) == 3

    @pytest.mark.asyncio
    async def test_max_items_limit(self):
        http = MockHttpTransport([
            {
                "value": [{"ID": "1"}, {"ID": "2"}, {"ID": "3"}],
                "@odata.nextLink": "http://test/next",
            },
            {"value": [{"ID": "4"}, {"ID": "5"}]},
        ])
        items = await collect_all(http, "http://test/Parts", max_items=2)
        assert len(items) == 2
