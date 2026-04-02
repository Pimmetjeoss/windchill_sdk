"""Read SAP BOM export from Excel file.

Parses the 16-column SAP EXPORT.XLSX (from ZPP262) into
a list of SapBomRow frozen dataclasses.
"""

from __future__ import annotations

import logging
from pathlib import Path

from windchill_spm.models import SapBomRow

logger = logging.getLogger(__name__)

# SAP EXPORT.XLSX column indices (0-based, 16 columns)
_COL_LEVEL = 0  # Explosion level
_COL_PARENT_NAME = 1  # Object description (parent)
_COL_PARENT_NO = 2  # Component number (parent)
_COL_DOCUMENT = 3  # Document (main overview drawing)
_COL_ITEM_NO = 4  # Item Number
_COL_ITEM_CAT = 5  # Item category
_COL_SORT_STRING = 6  # Sort String
_COL_COMPONENT_NO = 7  # Component number (child part)
_COL_OBJECT_DESC = 8  # Object description (child)
_COL_ITEM_TEXT = 9  # Item Text
_COL_DOC_SORT_STRING = 10  # Document Sort String
_COL_SPECIAL_PROC = 11  # Special procurement
_COL_DOC_TYPE = 12  # Document Type
_COL_PARENT_DWG_NO = 13  # Document (assembly drawing)
_COL_DOC_VERSION = 14  # Document Version
_COL_DOC_PART = 15  # Document Part

_NUM_COLUMNS = 16


def _normalize_wh(value: str) -> str:
    """Remove dots from WH-numbers: 'WH.123456' -> 'WH123456'."""
    if isinstance(value, str) and value.startswith("WH."):
        return "WH" + value[3:]
    return str(value) if value is not None else ""


def _cell_str(value: object) -> str:
    """Convert cell value to string, handling None and numeric types."""
    if value is None:
        return ""
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value).strip()


def _cell_int(value: object) -> int:
    """Convert cell value to int, defaulting to 0."""
    if value is None:
        return 0
    try:
        return int(float(str(value)))
    except (ValueError, TypeError):
        return 0


def read_sap_export(file_path: str | Path) -> list[SapBomRow]:
    """Read SAP BOM export from an Excel file.

    Supports the 16-column EXPORT.XLSX format from SAP ZPP262.

    Args:
        file_path: Path to the Excel file (.xls or .xlsx).

    Returns:
        List of SapBomRow, one per data row (header row skipped).

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file is empty.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"SAP export file not found: {file_path}")

    import openpyxl

    # Handle .xls files using xlrd
    if file_path.suffix.lower() == ".xls":
        rows = _read_xls(file_path)
    else:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        wb.close()

    if not rows:
        raise ValueError(f"SAP export file is empty: {file_path}")

    # Skip header row (row 1)
    data_rows = rows[1:]
    result: list[SapBomRow] = []

    for row in data_rows:
        # Pad row to 16 columns if needed
        cells = list(row) + [None] * max(0, _NUM_COLUMNS - len(row))

        if cells[_COL_COMPONENT_NO] is None or _cell_str(cells[_COL_COMPONENT_NO]) == "":
            continue  # Skip empty rows

        result.append(
            SapBomRow(
                level=_cell_int(cells[_COL_LEVEL]),
                parent_name=_cell_str(cells[_COL_PARENT_NAME]),
                parent_number=_normalize_wh(_cell_str(cells[_COL_PARENT_NO])),
                document=_normalize_wh(_cell_str(cells[_COL_DOCUMENT])),
                item_number=_cell_str(cells[_COL_ITEM_NO]),
                item_category=_cell_str(cells[_COL_ITEM_CAT]),
                sort_string=_cell_str(cells[_COL_SORT_STRING]),
                component_number=_normalize_wh(_cell_str(cells[_COL_COMPONENT_NO])),
                object_description=_cell_str(cells[_COL_OBJECT_DESC]),
                item_text=_cell_str(cells[_COL_ITEM_TEXT]),
                document_sort_string=_cell_str(cells[_COL_DOC_SORT_STRING]),
                special_procurement=_cell_str(cells[_COL_SPECIAL_PROC]),
                document_type=_cell_str(cells[_COL_DOC_TYPE]),
                parent_drawing_number=_normalize_wh(_cell_str(cells[_COL_PARENT_DWG_NO])),
                document_version=_cell_str(cells[_COL_DOC_VERSION]),
                document_part=_cell_str(cells[_COL_DOC_PART]),
            )
        )

    logger.info("Read %d rows from SAP export: %s", len(result), file_path.name)
    return result


def _read_xls(file_path: Path) -> list[tuple]:
    """Read .xls file using xlrd (legacy format)."""
    try:
        import xlrd
    except ImportError:
        raise ImportError(
            "xlrd is required to read .xls files. Install with: pip install xlrd"
        )

    wb = xlrd.open_workbook(str(file_path))
    ws = wb.sheet_by_index(0)
    rows = []
    for row_idx in range(ws.nrows):
        rows.append(tuple(ws.cell_value(row_idx, col) for col in range(ws.ncols)))
    return rows
