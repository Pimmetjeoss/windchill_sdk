"""SPM generation pipeline — orchestrates the full workflow.

SAP Excel → Parse → Enrich (Windchill BOMs + drawings) → PDF → Upload to Windchill.
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Any

from windchill_spm.enricher import (
    build_manual_content,
    explode_boms,
    fetch_drawings_from_windchill,
    fetch_service_boms_from_windchill,
    generate_levels,
    load_drawings_from_folder,
    match_assembly_drawings,
)
from windchill_spm.models import SpmResult
from windchill_spm.pdf_generator import generate_pdf
from windchill_spm.sap_reader import read_sap_export

logger = logging.getLogger(__name__)


async def generate_spm(
    sap_export_path: str | Path,
    *,
    client: Any | None = None,
    drawings_folder: str | Path | None = None,
    output_dir: str | Path | None = None,
    publish: bool = False,
    context_id: str | None = None,
    machine_name: str = "",
    service_boms_file: str | Path | None = None,
    drawing_master_file: str | Path | None = None,
) -> SpmResult:
    """Generate Spare Parts Manuals (MSPM + ESPM) from SAP BOM export.

    This is the main entry point for the full pipeline.

    Args:
        sap_export_path: Path to SAP BOM export Excel file.
        client: WindchillClient instance (optional — used for BOM enrichment,
            drawing downloads, and publishing).
        drawings_folder: Path to local folder with TIFF/PDF drawings.
            If None and client is provided, downloads from Windchill.
        output_dir: Where to save generated PDFs. Defaults to temp directory.
        publish: If True and client provided, upload PDFs to Windchill.
        context_id: Windchill container ID for new documents.
        machine_name: Machine name for document titles.
        service_boms_file: Path to legacy Service BOMs text file (optional fallback).
        drawing_master_file: Path to legacy Assembly Drawing master data (optional fallback).

    Returns:
        SpmResult with paths to generated PDFs and WH-numbers if published.
    """
    warnings: list[str] = []

    # ── Step 1: Read SAP Export ──
    logger.info("Step 1: Reading SAP export from %s", sap_export_path)
    sap_rows = read_sap_export(sap_export_path)
    logger.info("Read %d SAP BOM rows", len(sap_rows))

    # ── Step 2: Get Service BOMs for enrichment ──
    service_boms: dict[str, list[dict[str, str]]] = {}

    # Find Level-2 items that might need explosion
    level2_numbers = [
        row.component_number
        for row in sap_rows
        if row.level == 2
    ]

    if client:
        logger.info("Step 2: Fetching Service BOMs from Windchill (%d parts)", len(level2_numbers))
        service_boms = await fetch_service_boms_from_windchill(client, level2_numbers)
    elif service_boms_file:
        logger.info("Step 2: Loading Service BOMs from file: %s", service_boms_file)
        service_boms = _load_service_boms_file(service_boms_file)
    else:
        warnings.append("No Service BOMs source — BOM explosion skipped")

    # ── Step 3: Explode BOMs ──
    logger.info("Step 3: Exploding BOMs")
    enriched_rows = explode_boms(sap_rows, service_boms)
    logger.info("After explosion: %d rows (was %d)", len(enriched_rows), len(sap_rows))

    # ── Step 4: Match Assembly Drawings ──
    drawing_master: dict[str, str] = {}
    if drawing_master_file:
        drawing_master = _load_drawing_master_file(drawing_master_file)

    enriched_rows = match_assembly_drawings(enriched_rows, drawing_master)

    # ── Step 5: Generate Levels ──
    logger.info("Step 5: Generating Levels structure")
    levels = generate_levels(enriched_rows)
    logger.info("Generated %d level entries", len(levels))

    # ── Step 6: Get Drawings ──
    # Collect all unique drawing numbers needed
    drawing_numbers = set()
    for entry in levels:
        if entry.assembly_drawing_number and entry.assembly_drawing_number != "empty":
            drawing_numbers.add(entry.assembly_drawing_number)

    output_dir = Path(output_dir) if output_dir else Path(tempfile.mkdtemp(prefix="spm_"))
    output_dir.mkdir(parents=True, exist_ok=True)
    drawings_dir = output_dir / "drawings"

    drawings: dict[str, list] = {}
    if drawings_folder:
        logger.info("Step 6: Loading drawings from folder: %s", drawings_folder)
        drawings = load_drawings_from_folder(drawings_folder)
    elif client:
        logger.info("Step 6: Downloading %d drawings from Windchill", len(drawing_numbers))
        drawings = await fetch_drawings_from_windchill(
            client, list(drawing_numbers), drawings_dir
        )
    else:
        warnings.append("No drawing source — PDFs will have placeholder text for drawings")

    # Convert PDF/multi-page TIFF to single-page images for reportlab
    if drawings:
        from windchill_spm.drawing_utils import convert_drawings

        convert_dir = output_dir / "drawings_converted"
        drawings = convert_drawings(drawings, convert_dir)

    # Check for missing drawings
    for dwg_num in drawing_numbers:
        if dwg_num not in drawings:
            warnings.append(f"Drawing not found: {dwg_num}")

    # ── Step 7: Build Manual Content ──
    logger.info("Step 7: Building manual content structures")
    mspm_content = build_manual_content("mechanical", levels, enriched_rows, drawings)
    espm_content = build_manual_content("electrical", levels, enriched_rows, drawings)

    # ── Step 8: Generate PDFs ──
    name_prefix = f"{machine_name} - " if machine_name else ""

    mspm_path: Path | None = None
    espm_path: Path | None = None

    has_mech = (
        mspm_content.sections_with_drawing
        or mspm_content.general_parts
        or mspm_content.sections_without_drawing
        or mspm_content.main_overview_drawings
    )
    has_elec = (
        espm_content.sections_with_drawing
        or espm_content.general_parts
        or espm_content.sections_without_drawing
    )

    if has_mech:
        mspm_path = generate_pdf(
            mspm_content,
            output_dir / f"{name_prefix}MSPM.pdf",
        )
        logger.info("Generated MSPM: %s", mspm_path)
    else:
        warnings.append("No mechanical content found — MSPM not generated")

    if has_elec:
        espm_path = generate_pdf(
            espm_content,
            output_dir / f"{name_prefix}ESPM.pdf",
        )
        logger.info("Generated ESPM: %s", espm_path)
    else:
        warnings.append("No electrical content found — ESPM not generated")

    # ── Step 9: Publish to Windchill ──
    mspm_wh: str | None = None
    espm_wh: str | None = None

    if publish and client:
        from windchill_spm.publisher import publish_to_windchill

        if mspm_path:
            logger.info("Step 9: Publishing MSPM to Windchill")
            result = await publish_to_windchill(
                client,
                mspm_path,
                f"{name_prefix}Mechanical Spare Parts Manual",
                context_id=context_id,
            )
            mspm_wh = result.get("document_number")

        if espm_path:
            logger.info("Step 9: Publishing ESPM to Windchill")
            result = await publish_to_windchill(
                client,
                espm_path,
                f"{name_prefix}Electrical Spare Parts Manual",
                context_id=context_id,
            )
            espm_wh = result.get("document_number")

    for w in warnings:
        logger.warning(w)

    return SpmResult(
        mspm_pdf_path=mspm_path,
        espm_pdf_path=espm_path,
        mspm_wh_number=mspm_wh,
        espm_wh_number=espm_wh,
        warnings=tuple(warnings),
    )


# ── Legacy File Loaders ──


def _load_service_boms_file(
    file_path: str | Path,
) -> dict[str, list[dict[str, str]]]:
    """Load Service BOMs from legacy tab-delimited text file.

    File format (8 columns, tab-separated):
    Col 1: Parent WH-number
    Col 2: Child Position Number
    Col 3: Child WH-number
    Col 4: Child Name
    Col 5-6: Child Item Text
    Col 7-8: Additional data
    """
    file_path = Path(file_path)
    result: dict[str, list[dict[str, str]]] = {}

    with open(file_path, encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f, start=1):
            if line_no == 1:
                continue  # Skip header

            parts = line.strip().split("\t")
            if len(parts) < 4:
                continue

            parent = _normalize_wh(parts[0])
            child = {
                "pos_number": parts[1] if len(parts) > 1 else "",
                "child_number": _normalize_wh(parts[2]) if len(parts) > 2 else "",
                "child_name": parts[3] if len(parts) > 3 else "",
                "item_text": parts[5] if len(parts) > 5 else "",
            }
            result.setdefault(parent, []).append(child)

    logger.info("Loaded Service BOMs: %d parents, %d total children",
                len(result), sum(len(v) for v in result.values()))
    return result


def _load_drawing_master_file(
    file_path: str | Path,
) -> dict[str, str]:
    """Load Assembly Drawing master data from legacy tab-delimited text file.

    File format (3 columns, tab-separated):
    Col 1: WH-number
    Col 2: Assembly Drawing Type
    Col 3: Assembly Drawing Number
    """
    file_path = Path(file_path)
    result: dict[str, str] = {}

    with open(file_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                wh = _normalize_wh(parts[0])
                dwg = parts[2].strip()
                if wh and dwg:
                    result[wh] = dwg

    logger.info("Loaded drawing master: %d entries", len(result))
    return result


def _normalize_wh(value: str) -> str:
    """Remove dots from WH-numbers."""
    if value.startswith("WH."):
        return "WH" + value[3:]
    return value.strip()
