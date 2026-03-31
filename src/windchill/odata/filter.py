"""OData v4 filter expression builder for Windchill REST API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _quote_value(value: Any) -> str:
    """Format a value for OData filter expressions."""
    if isinstance(value, str):
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)


@dataclass(frozen=True)
class FilterExpr:
    """An OData filter expression that can be combined with & (and), | (or), ~ (not)."""

    expression: str

    def __and__(self, other: FilterExpr) -> FilterExpr:
        return FilterExpr(f"({self.expression} and {other.expression})")

    def __or__(self, other: FilterExpr) -> FilterExpr:
        return FilterExpr(f"({self.expression} or {other.expression})")

    def __invert__(self) -> FilterExpr:
        return FilterExpr(f"not ({self.expression})")

    def __str__(self) -> str:
        return self.expression


class F:
    """Factory for OData v4 filter expressions.

    Usage:
        F.eq("State", "INWORK")
        F.contains("Name", "bracket") & F.eq("Source", "MAKE")
        F.any("Documents", "d", F.eq("d/State", "RELEASED"))
    """

    @staticmethod
    def eq(prop: str, value: Any) -> FilterExpr:
        return FilterExpr(f"{prop} eq {_quote_value(value)}")

    @staticmethod
    def ne(prop: str, value: Any) -> FilterExpr:
        return FilterExpr(f"{prop} ne {_quote_value(value)}")

    @staticmethod
    def gt(prop: str, value: Any) -> FilterExpr:
        return FilterExpr(f"{prop} gt {_quote_value(value)}")

    @staticmethod
    def ge(prop: str, value: Any) -> FilterExpr:
        return FilterExpr(f"{prop} ge {_quote_value(value)}")

    @staticmethod
    def lt(prop: str, value: Any) -> FilterExpr:
        return FilterExpr(f"{prop} lt {_quote_value(value)}")

    @staticmethod
    def le(prop: str, value: Any) -> FilterExpr:
        return FilterExpr(f"{prop} le {_quote_value(value)}")

    @staticmethod
    def contains(prop: str, value: str) -> FilterExpr:
        return FilterExpr(f"contains({prop},{_quote_value(value)})")

    @staticmethod
    def startswith(prop: str, value: str) -> FilterExpr:
        return FilterExpr(f"startswith({prop},{_quote_value(value)})")

    @staticmethod
    def endswith(prop: str, value: str) -> FilterExpr:
        return FilterExpr(f"endswith({prop},{_quote_value(value)})")

    @staticmethod
    def any(nav_prop: str, alias: str, expr: FilterExpr) -> FilterExpr:
        """Lambda any() filter on a collection navigation property.

        Example: F.any("Documents", "d", F.eq("d/State", "RELEASED"))
        Generates: Documents/any(d: d/State eq 'RELEASED')
        """
        return FilterExpr(f"{nav_prop}/any({alias}: {expr.expression})")

    @staticmethod
    def all(nav_prop: str, alias: str, expr: FilterExpr) -> FilterExpr:
        """Lambda all() filter on a collection navigation property.

        Example: F.all("Documents", "d", F.eq("d/State", "RELEASED"))
        Generates: Documents/all(d: d/State eq 'RELEASED')
        """
        return FilterExpr(f"{nav_prop}/all({alias}: {expr.expression})")

    @staticmethod
    def raw(expression: str) -> FilterExpr:
        """Create a filter from a raw OData expression string."""
        return FilterExpr(expression)
