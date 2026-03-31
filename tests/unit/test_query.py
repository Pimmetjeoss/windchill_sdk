"""Tests for OData query builder."""

from windchill.odata.query import ExpandOption, Query


class TestQuery:
    def test_empty_query(self):
        q = Query()
        assert q.to_params() == {}

    def test_select(self):
        q = Query().select("ID", "Name", "State")
        assert q.to_params() == {"$select": "ID,Name,State"}

    def test_top(self):
        q = Query().top(50)
        assert q.to_params() == {"$top": "50"}

    def test_skip(self):
        q = Query().skip(100)
        assert q.to_params() == {"$skip": "100"}

    def test_count(self):
        q = Query().count()
        assert q.to_params() == {"$count": "true"}

    def test_search(self):
        q = Query().search("bracket")
        assert q.to_params() == {"$search": "bracket"}

    def test_orderby_ascending(self):
        q = Query().orderby("Name")
        assert q.to_params() == {"$orderby": "Name asc"}

    def test_orderby_descending(self):
        q = Query().orderby("CreatedOn", ascending=False)
        assert q.to_params() == {"$orderby": "CreatedOn desc"}

    def test_orderby_multiple(self):
        q = Query().orderby("Name asc", "CreatedOn desc")
        assert q.to_params() == {"$orderby": "Name asc,CreatedOn desc"}

    def test_expand_simple(self):
        q = Query().expand("Context", "Attachments")
        assert q.to_params() == {"$expand": "Context,Attachments"}

    def test_expand_nested(self):
        q = Query().expand(
            ExpandOption(
                property="Context",
                expand=(ExpandOption(property="Folders"),),
            )
        )
        assert q.to_params() == {"$expand": "Context($expand=Folders)"}

    def test_expand_with_select(self):
        q = Query().expand(
            ExpandOption(property="Context", select=("ID", "Name"))
        )
        assert q.to_params() == {"$expand": "Context($select=ID,Name)"}

    def test_latest_version(self):
        q = Query().latest_version()
        assert q.to_params() == {"ptc.search.latestversion": "true"}

    def test_latest_version_disabled(self):
        q = Query().latest_version().latest_version(enabled=False)
        assert "ptc.search.latestversion" not in q.to_params()

    def test_custom_param(self):
        q = Query().custom("myParam", "myValue")
        assert q.to_params() == {"myParam": "myValue"}

    def test_combined_query(self):
        from windchill.odata.filter import F

        q = (
            Query()
            .select("ID", "Name")
            .filter(F.eq("State", "INWORK"))
            .top(10)
            .count()
            .latest_version()
        )
        params = q.to_params()
        assert params["$select"] == "ID,Name"
        assert params["$filter"] == "State eq 'INWORK'"
        assert params["$top"] == "10"
        assert params["$count"] == "true"
        assert params["ptc.search.latestversion"] == "true"

    def test_immutability(self):
        q1 = Query()
        q2 = q1.top(10)
        q3 = q1.top(20)
        assert q1.to_params() == {}
        assert q2.to_params() == {"$top": "10"}
        assert q3.to_params() == {"$top": "20"}

    def test_query_string(self):
        q = Query().select("ID").top(5)
        qs = q.to_query_string()
        assert "$select=ID" in qs
        assert "$top=5" in qs
        assert qs.startswith("?")
