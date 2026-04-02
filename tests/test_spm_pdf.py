"""Tests for the PDF generator."""

import tempfile
from pathlib import Path

import pytest

from windchill_spm.models import BomLine, DrawingFile, ManualContent
from windchill_spm.pdf_generator import _calculate_col_widths, _escape, generate_pdf


class TestEscape:
    def test_ampersand(self):
        assert _escape("A & B") == "A &amp; B"

    def test_angle_brackets(self):
        assert _escape("<test>") == "&lt;test&gt;"

    def test_plain_text(self):
        assert _escape("hello world") == "hello world"


class TestCalculateColWidths:
    def test_basic_widths(self):
        data = [["Pos no", "Part no"], ["10", "WH123456"]]
        widths = _calculate_col_widths(data)
        assert len(widths) == 2
        assert all(w > 0 for w in widths)

    def test_respects_header_length(self):
        data = [["Part name", "X"], ["Short", "Y"]]
        widths = _calculate_col_widths(data)
        # First column should be wider (header "Part name" > data "Short")
        assert widths[0] > widths[1]


class TestGeneratePdf:
    def test_generates_empty_manual(self):
        """Should handle empty content gracefully."""
        content = ManualContent(title="Test Manual")
        with tempfile.TemporaryDirectory() as tmpdir:
            path = generate_pdf(content, Path(tmpdir) / "test.pdf")
            assert path.exists()
            assert path.stat().st_size > 0

    def test_generates_with_bom_lines(self):
        """Should generate a PDF with BOM tables."""
        content = ManualContent(
            title="Mechanical Spare Parts Manual",
            general_parts=(
                BomLine("10", "001", "WH123456", "Test Bolt M8x20", ""),
                BomLine("20", "002", "WH789012", "Test Nut M8", "TAG1"),
            ),
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = generate_pdf(content, Path(tmpdir) / "mspm.pdf")
            assert path.exists()
            assert path.stat().st_size > 1000  # Should have real content

    def test_output_dir_created(self):
        """Should create output directory if it doesn't exist."""
        content = ManualContent(title="Test Manual")
        with tempfile.TemporaryDirectory() as tmpdir:
            nested = Path(tmpdir) / "sub" / "dir"
            path = generate_pdf(content, nested / "test.pdf")
            assert path.exists()
