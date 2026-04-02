"""Tests for the BOM enrichment and Levels generation."""

import pytest

from windchill_spm.enricher import (
    _classify_part,
    _safe_sort_int,
    explode_boms,
    generate_levels,
    match_assembly_drawings,
)
from windchill_spm.models import ExplosionLevel, PartKind, SapBomRow


def _make_row(**overrides) -> SapBomRow:
    """Create a SapBomRow with sensible defaults (16-column format)."""
    defaults = {
        "level": 2,
        "parent_name": "Parent",
        "parent_number": "WH100000",
        "document": "",
        "item_number": "10",
        "item_category": "L",
        "sort_string": "100",
        "component_number": "WH200000",
        "object_description": "Test Part",
        "item_text": "",
        "document_sort_string": "",
        "special_procurement": "",
        "document_type": "",
        "parent_drawing_number": "",
        "document_version": "",
        "document_part": "",
    }
    defaults.update(overrides)
    return SapBomRow(**defaults)


class TestClassifyPart:
    def test_mechanical(self):
        assert _classify_part("WH200000") == PartKind.MECHANICAL

    def test_electrical(self):
        assert _classify_part("WH700000") == PartKind.ELECTRICAL

    def test_electrical_prefix(self):
        assert _classify_part("WH734145") == PartKind.ELECTRICAL

    def test_manual_excluded(self):
        # WH8* parts are mechanical but get excluded later
        assert _classify_part("WH800000") == PartKind.MECHANICAL


class TestSafeSortInt:
    def test_valid_number(self):
        assert _safe_sort_int("42") == 42

    def test_empty_string(self):
        assert _safe_sort_int("") == 999999

    def test_non_numeric(self):
        assert _safe_sort_int("abc") == 999999


class TestExplodeBoms:
    def test_no_explosion_needed(self):
        """Level 2 followed by Level 3 → already has children, no explosion."""
        rows = [
            _make_row(level=2, component_number="WH100000"),
            _make_row(level=3, component_number="WH200000", parent_number="WH100000"),
        ]
        result = explode_boms(rows, {})
        assert len(result) == 2

    def test_explosion_from_service_boms(self):
        """Level 2 without children → add from Service BOMs."""
        rows = [
            _make_row(level=2, component_number="WH100000"),
            _make_row(level=2, component_number="WH300000"),
        ]
        service_boms = {
            "WH100000": [
                {"pos_number": "10", "child_number": "WH111111", "child_name": "Bolt", "item_text": ""},
                {"pos_number": "20", "child_number": "WH222222", "child_name": "Nut", "item_text": ""},
            ]
        }
        result = explode_boms(rows, service_boms)
        assert len(result) == 4  # 2 original + 2 children
        assert result[1].level == 3
        assert result[1].component_number == "WH111111"
        assert result[2].level == 3
        assert result[2].component_number == "WH222222"

    def test_no_service_bom_available(self):
        """Level 2 without children and no Service BOM → no change."""
        rows = [
            _make_row(level=2, component_number="WH100000"),
            _make_row(level=2, component_number="WH300000"),
        ]
        result = explode_boms(rows, {})
        assert len(result) == 2

    def test_last_row_is_level2(self):
        """Last row being Level 2 should be checked for explosion."""
        rows = [
            _make_row(level=2, component_number="WH100000"),
        ]
        service_boms = {
            "WH100000": [
                {"pos_number": "10", "child_number": "WH111111", "child_name": "Part", "item_text": ""},
            ]
        }
        result = explode_boms(rows, service_boms)
        assert len(result) == 2


class TestMatchAssemblyDrawings:
    def test_fills_missing_drawing(self):
        rows = [_make_row(level=2, component_number="WH200000", parent_drawing_number="")]
        master = {"WH200000": "WH999999"}
        result = match_assembly_drawings(rows, master)
        assert result[0].parent_drawing_number == "WH999999"

    def test_preserves_existing_drawing(self):
        rows = [_make_row(level=2, component_number="WH200000", parent_drawing_number="WH888888")]
        master = {"WH200000": "WH999999"}
        result = match_assembly_drawings(rows, master)
        assert result[0].parent_drawing_number == "WH888888"

    def test_no_match_in_master(self):
        rows = [_make_row(level=2, component_number="WH200000", parent_drawing_number="")]
        result = match_assembly_drawings(rows, {})
        assert result[0].parent_drawing_number == ""


class TestGenerateLevels:
    def test_basic_levels(self):
        rows = [
            _make_row(level=2, component_number="WH200000", item_category="L",
                       sort_string="001", parent_drawing_number="WH400000"),
            _make_row(level=3, component_number="WH300000", parent_number="WH200000"),
        ]
        levels = generate_levels(rows)
        # Should have 1 entry (the Level 2 item)
        mech = [l for l in levels if l.kind == PartKind.MECHANICAL]
        assert len(mech) == 1
        assert mech[0].legend_number == "WH200000"
        assert mech[0].explosion_level == ExplosionLevel.WITH_DRAWING

    def test_standalone_part(self):
        """Level 2 without children → explosion level 2 (standalone)."""
        rows = [
            _make_row(level=2, component_number="WH200000", item_category="R"),
        ]
        levels = generate_levels(rows)
        mech = [l for l in levels if l.kind == PartKind.MECHANICAL]
        assert len(mech) == 1
        assert mech[0].explosion_level == ExplosionLevel.STANDALONE

    def test_without_drawing(self):
        """Level 2 with children but no drawing → explosion level 4."""
        rows = [
            _make_row(level=2, component_number="WH200000", item_category="L",
                       parent_drawing_number=""),
            _make_row(level=3, component_number="WH300000", parent_number="WH200000"),
        ]
        levels = generate_levels(rows)
        mech = [l for l in levels if l.kind == PartKind.MECHANICAL]
        assert len(mech) == 1
        assert mech[0].explosion_level == ExplosionLevel.WITHOUT_DRAWING

    def test_electrical_classification(self):
        rows = [
            _make_row(level=2, component_number="WH700000", item_category="R"),
        ]
        levels = generate_levels(rows)
        ela = [l for l in levels if l.kind == PartKind.ELECTRICAL]
        assert len(ela) == 1

    def test_excludes_wh8_manuals(self):
        rows = [
            _make_row(level=2, component_number="WH800000", item_category="L"),
        ]
        levels = generate_levels(rows)
        wh8 = [l for l in levels if l.legend_number == "WH800000"]
        assert len(wh8) == 1
        assert wh8[0].explosion_level is None  # Excluded

    def test_main_overview_drawing(self):
        rows = [
            _make_row(level=1, component_number="WH100000",
                       document="WH999000", item_category=""),
        ]
        levels = generate_levels(rows)
        mod = [l for l in levels if l.kind == PartKind.MAIN_OVERVIEW_DRAWING]
        assert len(mod) == 1
        assert mod[0].legend_number == "WH999000"

    def test_general_overview_drawings(self):
        rows = [
            _make_row(level=3, component_number="WH555000 Rev A",
                       item_category="D"),
        ]
        levels = generate_levels(rows)
        god = [l for l in levels if l.kind == PartKind.GENERAL_OVERVIEW_DRAWING]
        assert len(god) == 1
        assert god[0].legend_number == "WH555000"  # Before space

    def test_filters_non_lr_categories(self):
        rows = [
            _make_row(level=2, component_number="WH200000", item_category="D"),
        ]
        levels = generate_levels(rows)
        mech = [l for l in levels if l.kind == PartKind.MECHANICAL]
        assert len(mech) == 0

    def test_filters_todo_entries(self):
        rows = [
            _make_row(level=2, component_number="WHTODO", item_category="L"),
        ]
        levels = generate_levels(rows)
        assert len([l for l in levels if l.legend_number == "WHTODO"]) == 0
