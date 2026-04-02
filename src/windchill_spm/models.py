"""Immutable data models for the SPM pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class PartKind(Enum):
    """Part categorization."""

    MECHANICAL = "M"
    ELECTRICAL = "E"
    MAIN_OVERVIEW_DRAWING = "MOD"
    GENERAL_OVERVIEW_DRAWING = "GOD"


class ExplosionLevel(Enum):
    """How a BOM assembly is displayed in the manual."""

    STANDALONE = 2  # No children — listed in General Parts section
    WITH_DRAWING = 3  # Has children AND an assembly drawing
    WITHOUT_DRAWING = 4  # Has children but NO assembly drawing


# ── SAP BOM Data ──


@dataclass(frozen=True)
class SapBomRow:
    """One row from the SAP BOM export (16 columns, EXPORT.XLSX format).

    Column mapping from SAP ZPP262 export:
      1: Explosion level       8: Component number
      2: Object description    9: Object description (child)
      3: Component number     10: Item Text
      4: Document             11: Document Sort String
      5: Item Number          12: Special procurement
      6: Item category        13: Document Type
      7: Sort String          14: Document (assembly drawing)
                              15: Document Version
                              16: Document Part
    """

    level: int  # Col 1: hierarchy level (1=root, 2=assembly, 3=child)
    parent_name: str  # Col 2: Object description (parent)
    parent_number: str  # Col 3: Component number (parent WH-number)
    document: str  # Col 4: Document number (main overview drawing)
    item_number: str  # Col 5: Item Number (position in BOM)
    item_category: str  # Col 6: Item category (L=Layout, R=Regular, D=Drawing)
    sort_string: str  # Col 7: Sort String (sorting sequence)
    component_number: str  # Col 8: Component number (WH-number of this part)
    object_description: str  # Col 9: Object description (part name)
    item_text: str  # Col 10: Item Text
    document_sort_string: str  # Col 11: Document Sort String
    special_procurement: str  # Col 12: Special procurement
    document_type: str  # Col 13: Document Type (e.g. ZAS)
    parent_drawing_number: str  # Col 14: Document (assembly drawing number)
    document_version: str  # Col 15: Document Version
    document_part: str  # Col 16: Document Part

    @property
    def main_overview_drawing(self) -> str:
        """Alias for backward compat — Col 4 Document."""
        return self.document

    @property
    def tsl_number(self) -> str:
        """TSL number — derived from sort_string (Col 7) for sorting."""
        return self.sort_string

    @property
    def device_tag(self) -> str:
        """Device tag — mapped from Item Text (Col 10)."""
        return self.item_text


# ── Enriched / Intermediate Data ──


@dataclass(frozen=True)
class LevelEntry:
    """One entry in the Levels structure (replaces VBA Levels file).

    Represents a Level-2 assembly from the SAP BOM with its
    categorization and explosion metadata.
    """

    legend_number: str  # WH-number of the assembly
    name: str  # Part name
    assembly_drawing_number: str  # Drawing number or "empty"
    kind: PartKind  # E, M, MOD, or GOD
    explosion_level: ExplosionLevel | None  # 2, 3, 4, or None (excluded)
    tsl_number: str  # TSL number (mechanical sort key)
    sort_string: str  # Sort string (electrical sort key)
    bom_start_row: int | None  # Start row index in enriched SAP data
    bom_end_row: int | None  # End row index in enriched SAP data


@dataclass(frozen=True)
class DrawingFile:
    """A drawing file (TIFF/PDF) downloaded from Windchill or local disk."""

    wh_number: str  # Short name, e.g. "WH806239"
    file_path: Path  # Local path to the downloaded file
    page_number: int = 1  # Page number within a multi-page drawing


@dataclass(frozen=True)
class BomLine:
    """One line in a Bill of Materials table."""

    pos_number: str  # Position number
    function_number: str  # TSL / function number
    part_number: str  # WH-number
    part_name: str  # Description
    device_tag: str  # Electrical device tag


@dataclass(frozen=True)
class AssemblySection:
    """A complete assembly section for the manual.

    Groups a drawing with its BOM lines, ready for PDF rendering.
    """

    legend_number: str  # WH-number of the assembly
    name: str  # Assembly name
    kind: PartKind  # M or E
    sort_key: str  # TSL number (M) or Sort String (E)
    assembly_drawing_number: str  # Drawing WH-number
    drawings: tuple[DrawingFile, ...] = ()  # Drawing pages (may be multi-page)
    bom_lines: tuple[BomLine, ...] = ()  # BOM table rows
    explosion_level: ExplosionLevel | None = None


@dataclass(frozen=True)
class ManualContent:
    """Complete content for one Spare Parts Manual (MSPM or ESPM)."""

    title: str  # e.g. "Mechanical Spare Parts Manual"
    main_overview_drawings: tuple[DrawingFile, ...] = ()
    general_overview_drawings: tuple[DrawingFile, ...] = ()
    sections_with_drawing: tuple[AssemblySection, ...] = ()  # Explosion level 3
    general_parts: tuple[BomLine, ...] = ()  # Explosion level 2
    sections_without_drawing: tuple[AssemblySection, ...] = ()  # Explosion level 4


@dataclass(frozen=True)
class SpmResult:
    """Result of the full SPM generation pipeline."""

    mspm_pdf_path: Path | None = None
    espm_pdf_path: Path | None = None
    mspm_wh_number: str | None = None  # WH-number in Windchill
    espm_wh_number: str | None = None  # WH-number in Windchill
    warnings: tuple[str, ...] = ()
