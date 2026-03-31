"""OData v4 query builder for Windchill REST API."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from windchill.odata.filter import FilterExpr


@dataclass(frozen=True)
class ExpandOption:
    """An $expand clause, optionally with nested options."""

    property: str
    select: tuple[str, ...] = ()
    expand: tuple[ExpandOption, ...] = ()
    filter: FilterExpr | None = None
    top: int | None = None

    def to_string(self) -> str:
        parts: list[str] = []
        if self.select:
            parts.append(f"$select={','.join(self.select)}")
        if self.expand:
            nested = ",".join(e.to_string() for e in self.expand)
            parts.append(f"$expand={nested}")
        if self.filter:
            parts.append(f"$filter={self.filter.expression}")
        if self.top is not None:
            parts.append(f"$top={self.top}")

        if parts:
            return f"{self.property}({';'.join(parts)})"
        return self.property


@dataclass(frozen=True)
class Query:
    """Immutable OData v4 query builder with fluent API.

    Usage:
        query = (
            Query()
            .select("ID", "Name", "State")
            .expand("Context")
            .filter(F.eq("State", "INWORK"))
            .orderby("Name")
            .top(50)
            .count()
            .latest_version()
        )
        params = query.to_params()  # dict for httpx params
    """

    _select: tuple[str, ...] = ()
    _expand: tuple[ExpandOption, ...] = ()
    _filter: FilterExpr | None = None
    _orderby: tuple[str, ...] = ()
    _top: int | None = None
    _skip: int | None = None
    _count: bool = False
    _search: str | None = None
    _custom: dict[str, str] = field(default_factory=dict)

    def select(self, *properties: str) -> Query:
        """Set $select to return only specific properties."""
        return replace(self, _select=properties)

    def expand(self, *properties: str | ExpandOption) -> Query:
        """Set $expand to inline related entities.

        Accepts property names (strings) or ExpandOption objects for nested expansions.
        """
        options = tuple(
            p if isinstance(p, ExpandOption) else ExpandOption(property=p)
            for p in properties
        )
        return replace(self, _expand=options)

    def filter(self, expr: FilterExpr) -> Query:
        """Set $filter expression."""
        return replace(self, _filter=expr)

    def orderby(self, *fields: str, ascending: bool = True) -> Query:
        """Set $orderby. Fields are sorted ascending by default.

        For mixed directions, pass full strings like "Name asc", "CreatedOn desc".
        """
        direction = "asc" if ascending else "desc"
        clauses = tuple(
            f if " " in f else f"{f} {direction}" for f in fields
        )
        return replace(self, _orderby=clauses)

    def top(self, n: int) -> Query:
        """Set $top to limit result count."""
        return replace(self, _top=n)

    def skip(self, n: int) -> Query:
        """Set $skip for pagination offset."""
        return replace(self, _skip=n)

    def count(self, enabled: bool = True) -> Query:
        """Enable $count to include total count in response."""
        return replace(self, _count=enabled)

    def search(self, keyword: str) -> Query:
        """Set $search for full-text search."""
        return replace(self, _search=keyword)

    def latest_version(self, enabled: bool = True) -> Query:
        """Set ptc.search.latestversion custom query option."""
        custom = dict(self._custom)
        if enabled:
            custom["ptc.search.latestversion"] = "true"
        else:
            custom.pop("ptc.search.latestversion", None)
        return replace(self, _custom=custom)

    def custom(self, key: str, value: str) -> Query:
        """Add a custom query parameter."""
        custom = dict(self._custom)
        custom[key] = value
        return replace(self, _custom=custom)

    def to_params(self) -> dict[str, str]:
        """Build query parameters dict for httpx."""
        params: dict[str, str] = {}

        if self._select:
            params["$select"] = ",".join(self._select)

        if self._expand:
            params["$expand"] = ",".join(e.to_string() for e in self._expand)

        if self._filter:
            params["$filter"] = self._filter.expression

        if self._orderby:
            params["$orderby"] = ",".join(self._orderby)

        if self._top is not None:
            params["$top"] = str(self._top)

        if self._skip is not None:
            params["$skip"] = str(self._skip)

        if self._count:
            params["$count"] = "true"

        if self._search:
            params["$search"] = self._search

        params.update(self._custom)
        return params

    def to_query_string(self) -> str:
        """Build the full query string (for debugging/logging)."""
        params = self.to_params()
        if not params:
            return ""
        return "?" + "&".join(f"{k}={v}" for k, v in params.items())
