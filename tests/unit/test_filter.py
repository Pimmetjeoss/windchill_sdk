"""Tests for OData filter expressions."""

from windchill.odata.filter import F, FilterExpr


class TestFilterExpr:
    def test_eq_string(self):
        expr = F.eq("State", "INWORK")
        assert str(expr) == "State eq 'INWORK'"

    def test_eq_number(self):
        expr = F.eq("Quantity", 5)
        assert str(expr) == "Quantity eq 5"

    def test_eq_bool(self):
        expr = F.eq("LatestIteration", True)
        assert str(expr) == "LatestIteration eq true"

    def test_eq_null(self):
        expr = F.eq("Description", None)
        assert str(expr) == "Description eq null"

    def test_ne(self):
        expr = F.ne("State", "CANCELLED")
        assert str(expr) == "State ne 'CANCELLED'"

    def test_gt(self):
        expr = F.gt("Quantity", 10)
        assert str(expr) == "Quantity gt 10"

    def test_ge(self):
        expr = F.ge("Quantity", 10)
        assert str(expr) == "Quantity ge 10"

    def test_lt(self):
        expr = F.lt("Quantity", 5)
        assert str(expr) == "Quantity lt 5"

    def test_le(self):
        expr = F.le("Quantity", 5)
        assert str(expr) == "Quantity le 5"

    def test_contains(self):
        expr = F.contains("Name", "bracket")
        assert str(expr) == "contains(Name,'bracket')"

    def test_startswith(self):
        expr = F.startswith("Number", "000")
        assert str(expr) == "startswith(Number,'000')"

    def test_endswith(self):
        expr = F.endswith("Name", "assy")
        assert str(expr) == "endswith(Name,'assy')"

    def test_and(self):
        expr = F.eq("State", "INWORK") & F.contains("Name", "bracket")
        assert str(expr) == "(State eq 'INWORK' and contains(Name,'bracket'))"

    def test_or(self):
        expr = F.eq("State", "INWORK") | F.eq("State", "RELEASED")
        assert str(expr) == "(State eq 'INWORK' or State eq 'RELEASED')"

    def test_not(self):
        expr = ~F.eq("State", "CANCELLED")
        assert str(expr) == "not (State eq 'CANCELLED')"

    def test_complex_combination(self):
        expr = (F.eq("State", "INWORK") & F.contains("Name", "bracket")) | F.eq(
            "Source", "MAKE"
        )
        assert "and" in str(expr)
        assert "or" in str(expr)

    def test_any_lambda(self):
        expr = F.any("Documents", "d", F.eq("d/State", "RELEASED"))
        assert str(expr) == "Documents/any(d: d/State eq 'RELEASED')"

    def test_all_lambda(self):
        expr = F.all("Documents", "d", F.eq("d/State", "RELEASED"))
        assert str(expr) == "Documents/all(d: d/State eq 'RELEASED')"

    def test_any_with_contains(self):
        expr = F.any("Attachments", "a", F.contains("a/FileName", "spec"))
        assert str(expr) == "Attachments/any(a: contains(a/FileName,'spec'))"

    def test_raw(self):
        expr = F.raw("custom_field gt 42")
        assert str(expr) == "custom_field gt 42"

    def test_string_escaping(self):
        expr = F.eq("Name", "O'Brien")
        assert str(expr) == "Name eq 'O''Brien'"

    def test_frozen_dataclass(self):
        expr = F.eq("State", "INWORK")
        assert isinstance(expr, FilterExpr)
