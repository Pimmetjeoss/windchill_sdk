"""Tests for OData batch request builder."""

import pytest

from windchill.odata.batch import Batch
from windchill.odata.query import Query


class TestBatch:
    def test_simple_get(self):
        batch = Batch(domain="ProdMgmt")
        batch.get("Parts")
        content_type, body = batch.build()

        assert "multipart/mixed" in content_type
        assert "GET Parts HTTP/1.1" in body

    def test_simple_post(self):
        batch = Batch(domain="ProdMgmt")
        batch.post("Parts", {"Name": "Test Part"})
        _, body = batch.build()

        assert "POST Parts HTTP/1.1" in body
        assert '"Name": "Test Part"' in body

    def test_changeset(self):
        batch = (
            Batch(domain="ProdMgmt")
            .begin_changeset()
            .post("Parts", {"Name": "Part 1"}, content_id="1_1")
            .post("Parts", {"Name": "Part 2"}, content_id="2_1")
            .end_changeset()
        )
        content_type, body = batch.build()

        assert "Content-ID: 1_1" in body
        assert "Content-ID: 2_1" in body
        assert "changeset_" in body

    def test_mixed_operations(self):
        batch = (
            Batch(domain="ProdMgmt")
            .begin_changeset()
            .post("Parts", {"Name": "New Part"}, content_id="1_1")
            .end_changeset()
            .get("Parts", query=Query().top(5))
        )
        _, body = batch.build()

        assert "POST Parts HTTP/1.1" in body
        assert "GET Parts" in body

    def test_get_in_changeset_raises(self):
        batch = Batch(domain="ProdMgmt").begin_changeset()
        with pytest.raises(ValueError, match="not allowed inside changesets"):
            batch.get("Parts")

    def test_nested_changeset_raises(self):
        batch = Batch(domain="ProdMgmt").begin_changeset()
        with pytest.raises(ValueError, match="Cannot nest"):
            batch.begin_changeset()

    def test_end_without_begin_raises(self):
        batch = Batch(domain="ProdMgmt")
        with pytest.raises(ValueError, match="No changeset"):
            batch.end_changeset()

    def test_build_with_unclosed_changeset_raises(self):
        batch = Batch(domain="ProdMgmt").begin_changeset()
        batch.post("Parts", {"Name": "Test"})
        with pytest.raises(ValueError, match="Unclosed changeset"):
            batch.build()

    def test_batch_url(self):
        batch = Batch(domain="ProdMgmt")
        assert batch.batch_url == "ProdMgmt/$batch"

    def test_delete_operation(self):
        batch = (
            Batch(domain="ProdMgmt")
            .begin_changeset()
            .delete("Parts('abc123')")
            .end_changeset()
        )
        _, body = batch.build()
        assert "DELETE Parts('abc123') HTTP/1.1" in body

    def test_patch_operation(self):
        batch = (
            Batch(domain="ProdMgmt")
            .begin_changeset()
            .patch("Parts('abc')", {"Name": "Updated"})
            .end_changeset()
        )
        _, body = batch.build()
        assert "PATCH Parts('abc') HTTP/1.1" in body
        assert '"Name": "Updated"' in body
