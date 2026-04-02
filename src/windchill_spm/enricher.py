"""BOM enrichment and Levels generation.

Replaces the SPM File Generator VBA macro. Takes raw SAP BOM data,
enriches it with Windchill Service BOMs and assembly drawing data,
and produces the Levels structure needed by the PDF generator.
"""

from __future__ import annotations

import logging
from dataclasses import replace
from typing import Any

from windchill_spm.models import (
    AssemblySection,
    BomLine,
    DrawingFile,
    ExplosionLevel,
    LevelEntry,
    ManualContent,
    PartKind,
    SapBomRow,
)

logger = logging.getLogger(__name__)


# ── BOM Explosion ──


def explode_boms(
    sap_rows: list[SapBomRow],
    service_boms: dict[str, list[dict[str, str]]],
) -> list[SapBomRow]:
    """Enrich SAP BOM data by exploding missing children from Service BOMs.

    Mirrors the VBA ExplodeBoms logic: for each Level-2 assembly that
    has no Level-3 children in the SAP export, check if the Service BOMs
    file has children and add them.

    Args:
        sap_rows: Raw SAP BOM rows.
        service_boms: Dict mapping parent WH-number to list of children.
            Each child dict has keys: pos_number, child_number, child_name, item_text.

    Returns:
        New list of SapBomRow with exploded BOMs inserted.
    """
    result: list[SapBomRow] = []

    for i, row in enumerate(sap_rows):
        result.append(row)

        # Only check Level 2 items
        if row.level != 2:
            continue

        # Check if next row is Level 3 (has children already)
        has_children = (i + 1 < len(sap_rows)) and sap_rows[i + 1].level == 3
        if has_children:
            continue

        # No children — check Service BOMs
        children = service_boms.get(row.component_number, [])
        if not children:
            continue

        logger.info(
            "Exploding BOM for %s: adding %d children from Service BOMs",
            row.component_number,
            len(children),
        )

        for child in children:
            result.append(
                SapBomRow(
                    level=3,
                    parent_name=row.object_description,
                    parent_number=row.component_number,
                    document="",
                    item_number=child.get("pos_number", ""),
                    item_category="",
                    sort_string="",
                    component_number=child.get("child_number", ""),
                    object_description=child.get("child_name", ""),
                    item_text=child.get("item_text", ""),
                    document_sort_string="",
                    special_procurement="",
                    document_type="",
                    parent_drawing_number="",
                    document_version="",
                    document_part="",
                )
            )

    return result


# ── Assembly Drawing Matching ──


def match_assembly_drawings(
    sap_rows: list[SapBomRow],
    drawing_master: dict[str, str],
) -> list[SapBomRow]:
    """Fill missing assembly drawing numbers from master data.

    Mirrors the VBA FindAssDwg logic: for Level-2 items without a
    parent_drawing_number, look up the component_number in the
    drawing master data.

    Args:
        sap_rows: SAP BOM rows (possibly already exploded).
        drawing_master: Dict mapping WH-number to assembly drawing number.

    Returns:
        New list with drawing numbers filled in where found.
    """
    result: list[SapBomRow] = []

    for row in sap_rows:
        if row.level == 2 and not row.parent_drawing_number:
            dwg = drawing_master.get(row.component_number, "")
            if dwg:
                logger.info(
                    "Found assembly drawing %s for %s", dwg, row.component_number
                )
                row = replace(row, parent_drawing_number=dwg)
        result.append(row)

    return result


# ── Part Categorization ──


def _classify_part(wh_number: str) -> PartKind:
    """Classify part as Mechanical or Electrical based on WH-number prefix."""
    if wh_number.startswith("WH7"):
        return PartKind.ELECTRICAL
    return PartKind.MECHANICAL


# ── Levels Generation ──


def generate_levels(sap_rows: list[SapBomRow]) -> list[LevelEntry]:
    """Generate the Levels structure from enriched SAP data.

    Mirrors the VBA CreateLevelsFile logic. Processes Level-2 items
    with Item Category L or R, determines explosion level, and
    adds Main/General Overview Drawings.

    Args:
        sap_rows: Enriched SAP BOM rows.

    Returns:
        List of LevelEntry describing the manual structure.
    """
    levels: list[LevelEntry] = []
    num_rows = len(sap_rows)

    i = 0
    while i < num_rows:
        row = sap_rows[i]

        # Only process Level 2 items with category L or R
        if row.level != 2 or row.item_category not in ("L", "R"):
            i += 1
            continue

        # Filter out TODO entries (WH-number must start with digits after "WH")
        if len(row.component_number) < 3 or not row.component_number[2:3].isdigit():
            i += 1
            continue

        # Determine kind (E/M)
        kind = _classify_part(row.component_number)

        # Check for LAYOUT → Main Overview Drawing
        if row.object_description == "LAYOUT":
            kind = PartKind.MAIN_OVERVIEW_DRAWING

        # Determine explosion level and BOM row range
        has_children = (i + 1 < num_rows) and sap_rows[i + 1].level == 3
        has_drawing = bool(row.parent_drawing_number)

        if has_children and has_drawing:
            explosion = ExplosionLevel.WITH_DRAWING
        elif has_children and not has_drawing:
            explosion = ExplosionLevel.WITHOUT_DRAWING
        else:
            explosion = ExplosionLevel.STANDALONE

        # Find BOM row range (children)
        bom_start: int | None = None
        bom_end: int | None = None

        if has_children:
            bom_start = i + 1  # Index of first child
            bom_end = bom_start
            while (
                bom_end + 1 < num_rows
                and sap_rows[bom_end + 1].parent_number == sap_rows[bom_end].parent_number
                and sap_rows[bom_end + 1].level != 2
            ):
                bom_end += 1
            i = bom_end  # Skip past children

        # Exclude manuals (WH8*)
        if row.component_number.startswith("WH8"):
            explosion = None

        drawing_num = row.parent_drawing_number if row.parent_drawing_number else "empty"

        # Override for LAYOUT
        if kind == PartKind.MAIN_OVERVIEW_DRAWING:
            drawing_num = row.component_number
            explosion = ExplosionLevel.WITH_DRAWING

        levels.append(
            LevelEntry(
                legend_number=row.component_number,
                name=row.object_description,
                assembly_drawing_number=drawing_num,
                kind=kind,
                explosion_level=explosion,
                tsl_number=row.tsl_number,
                sort_string=row.sort_string,
                bom_start_row=bom_start,
                bom_end_row=bom_end,
            )
        )

        i += 1

    # Add Main Overview Drawing from row 1 (if present)
    if sap_rows and sap_rows[0].main_overview_drawing:
        mod_number = sap_rows[0].main_overview_drawing
        levels.append(
            LevelEntry(
                legend_number=mod_number,
                name="Main overview drawing",
                assembly_drawing_number=mod_number,
                kind=PartKind.MAIN_OVERVIEW_DRAWING,
                explosion_level=ExplosionLevel.WITH_DRAWING,
                tsl_number="",
                sort_string="",
                bom_start_row=None,
                bom_end_row=None,
            )
        )

    # Add General Overview Drawings (Item Category D, Level 3)
    for row in sap_rows:
        if row.item_category == "D" and row.level == 3:
            comp = row.component_number
            # Take part before first space (if any)
            if " " in comp:
                comp = comp[: comp.index(" ")]
            levels.append(
                LevelEntry(
                    legend_number=comp,
                    name="General overview drawing",
                    assembly_drawing_number=comp,
                    kind=PartKind.GENERAL_OVERVIEW_DRAWING,
                    explosion_level=ExplosionLevel.WITH_DRAWING,
                    tsl_number="",
                    sort_string="",
                    bom_start_row=None,
                    bom_end_row=None,
                )
            )

    logger.info("Generated %d level entries", len(levels))
    return levels


# ── Build Manual Content ──


def build_manual_content(
    manual_type: str,
    levels: list[LevelEntry],
    sap_rows: list[SapBomRow],
    drawings: dict[str, list[DrawingFile]],
) -> ManualContent:
    """Build the complete content structure for one manual (MSPM or ESPM).

    Args:
        manual_type: "mechanical" or "electrical"
        levels: Generated level entries.
        sap_rows: Enriched SAP BOM rows.
        drawings: Dict mapping WH-number to list of DrawingFile pages.

    Returns:
        ManualContent ready for PDF rendering.
    """
    target_kind = PartKind.MECHANICAL if manual_type == "mechanical" else PartKind.ELECTRICAL
    sort_key_attr = "tsl_number" if manual_type == "mechanical" else "sort_string"
    title = (
        "Mechanical Spare Parts Manual"
        if manual_type == "mechanical"
        else "Electrical Spare Parts Manual"
    )

    # Collect Main Overview Drawings
    mod_drawings: list[DrawingFile] = []
    for entry in levels:
        if entry.kind == PartKind.MAIN_OVERVIEW_DRAWING and entry.explosion_level:
            mod_drawings.extend(drawings.get(entry.legend_number, []))

    # Collect General Overview Drawings
    god_drawings: list[DrawingFile] = []
    for entry in levels:
        if entry.kind == PartKind.GENERAL_OVERVIEW_DRAWING and entry.explosion_level:
            god_drawings.extend(drawings.get(entry.legend_number, []))

    # Sections with drawing (explosion level 3)
    sections_with_dwg: list[AssemblySection] = []
    for entry in levels:
        if (
            entry.kind == target_kind
            and entry.explosion_level == ExplosionLevel.WITH_DRAWING
        ):
            bom_lines = _extract_bom_lines(sap_rows, entry.bom_start_row, entry.bom_end_row)
            dwg_files = drawings.get(entry.assembly_drawing_number, [])
            sections_with_dwg.append(
                AssemblySection(
                    legend_number=entry.legend_number,
                    name=entry.name,
                    kind=entry.kind,
                    sort_key=getattr(entry, sort_key_attr),
                    assembly_drawing_number=entry.assembly_drawing_number,
                    drawings=tuple(dwg_files),
                    bom_lines=tuple(bom_lines),
                    explosion_level=entry.explosion_level,
                )
            )

    # Sort: Mechanical by TSL number, Electrical by Sort String
    sections_with_dwg.sort(key=lambda s: _safe_sort_int(s.sort_key))

    # General parts (explosion level 2 — standalone, no children)
    general_parts: list[BomLine] = []
    for entry in levels:
        if (
            entry.kind == target_kind
            and entry.explosion_level == ExplosionLevel.STANDALONE
        ):
            # Find this part in SAP data
            for row in sap_rows:
                if row.component_number == entry.legend_number:
                    general_parts.append(
                        BomLine(
                            pos_number=row.item_number,
                            function_number=row.tsl_number,
                            part_number=row.component_number,
                            part_name=row.object_description,
                            device_tag=row.device_tag,
                        )
                    )
                    break

    # Sections without drawing (explosion level 4)
    sections_no_dwg: list[AssemblySection] = []
    for entry in levels:
        if (
            entry.kind == target_kind
            and entry.explosion_level == ExplosionLevel.WITHOUT_DRAWING
        ):
            bom_lines = _extract_bom_lines(sap_rows, entry.bom_start_row, entry.bom_end_row)
            sections_no_dwg.append(
                AssemblySection(
                    legend_number=entry.legend_number,
                    name=entry.name,
                    kind=entry.kind,
                    sort_key=getattr(entry, sort_key_attr),
                    assembly_drawing_number=entry.assembly_drawing_number,
                    drawings=(),
                    bom_lines=tuple(bom_lines),
                    explosion_level=entry.explosion_level,
                )
            )

    sections_no_dwg.sort(key=lambda s: _safe_sort_int(s.sort_key))

    return ManualContent(
        title=title,
        main_overview_drawings=tuple(mod_drawings),
        general_overview_drawings=tuple(god_drawings),
        sections_with_drawing=tuple(sections_with_dwg),
        general_parts=tuple(general_parts),
        sections_without_drawing=tuple(sections_no_dwg),
    )


def _extract_bom_lines(
    sap_rows: list[SapBomRow],
    start: int | None,
    end: int | None,
) -> list[BomLine]:
    """Extract BOM lines from SAP data for a given row range."""
    if start is None or end is None:
        return []

    return [
        BomLine(
            pos_number=sap_rows[i].item_number,
            function_number=sap_rows[i].tsl_number,
            part_number=sap_rows[i].component_number,
            part_name=sap_rows[i].object_description,
            device_tag=sap_rows[i].device_tag,
        )
        for i in range(start, end + 1)
        if i < len(sap_rows)
    ]


def _safe_sort_int(value: str) -> int:
    """Convert sort key to int for sorting, defaulting to 999999."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 999999


# ── Windchill Data Fetching ──


async def fetch_service_boms_from_windchill(
    client: Any,
    parent_wh_numbers: list[str],
) -> dict[str, list[dict[str, str]]]:
    """Fetch Service BOMs from Windchill for the given parent parts.

    Uses the Windchill SDK's get_bom method to retrieve children
    for each parent part, replacing the static SBOMs Export.txt file.

    Args:
        client: WindchillClient instance.
        parent_wh_numbers: List of parent WH-numbers to look up.

    Returns:
        Dict mapping parent WH-number to list of child dicts.
    """
    from windchill.odata.filter import F
    from windchill.odata.query import Query

    service_boms: dict[str, list[dict[str, str]]] = {}

    for wh_num in parent_wh_numbers:
        try:
            # Search for the part by number
            query = Query().filter(F.eq("Number", wh_num)).top(1)
            response = await client.prod_mgmt.list_parts(query)

            if not response.items:
                continue

            part = response.items[0]
            part_id = part.get("ID", "")

            if not part_id:
                continue

            # Get BOM (direct children)
            bom_response = await client.prod_mgmt.get_bom(part_id)

            children = []
            for idx, item in enumerate(bom_response.items, start=1):
                children.append(
                    {
                        "pos_number": str(idx * 10),
                        "child_number": item.get("Number", ""),
                        "child_name": item.get("Name", ""),
                        "item_text": "",
                    }
                )

            if children:
                service_boms[wh_num] = children
                logger.info("Fetched %d BOM children for %s", len(children), wh_num)

        except Exception as exc:
            logger.warning("Failed to fetch BOM for %s: %s", wh_num, exc)

    return service_boms


async def fetch_drawings_from_windchill(
    client: Any,
    drawing_numbers: list[str],
    output_dir: str | Any,
) -> dict[str, list[DrawingFile]]:
    """Download drawing files from Windchill for the given WH-numbers.

    Tries multiple strategies in order:
    1. Part -> DescribedBy -> Document -> PrimaryContent (for WTDocuments)
    2. CADDocumentMgmt -> <number>_DWG1 -> Representation -> AdditionalFiles PDF

    Args:
        client: WindchillClient instance.
        drawing_numbers: List of drawing WH-numbers.
        output_dir: Directory to save downloaded files.

    Returns:
        Dict mapping WH-number to list of DrawingFile (one per page).
    """
    from pathlib import Path

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    drawings: dict[str, list[DrawingFile]] = {}

    for wh_num in drawing_numbers:
        # Strategy 1: Part -> DescribedBy -> Document -> PrimaryContent
        result = await _try_download_via_described_by(client, wh_num, output_dir)
        if result:
            drawings[wh_num] = result
            continue

        # Strategy 2: CAD Drawing document (<number>_DWG1) -> Representation PDF
        result = await _try_download_via_cad_drawing(client, wh_num, output_dir)
        if result:
            drawings[wh_num] = result
            continue

        logger.warning("Drawing not found via any method: %s", wh_num)

    return drawings


async def _try_download_via_described_by(
    client: Any,
    wh_num: str,
    output_dir: Any,
) -> list[DrawingFile] | None:
    """Try downloading via Part -> DescribedBy -> Document -> PrimaryContent."""
    from pathlib import Path

    from windchill.odata.filter import F
    from windchill.odata.query import Query

    try:
        query = Query().filter(F.eq("Number", wh_num)).top(1)
        response = await client.prod_mgmt.list_parts(query)

        if not response.items:
            return None

        part = response.items[0]
        part_id = part.get("ID", "")
        if not part_id:
            return None

        file_path_str = await client.prod_mgmt.download_part_content(
            part_id, str(Path(output_dir) / f"{wh_num}.pdf")
        )
        file_path = Path(file_path_str)

        if file_path.exists():
            logger.info("Downloaded drawing %s via DescribedBy (%d KB)", wh_num, file_path.stat().st_size // 1024)
            return [DrawingFile(wh_number=wh_num, file_path=file_path, page_number=1)]

    except Exception:
        pass

    return None


async def _try_download_via_cad_drawing(
    client: Any,
    wh_num: str,
    output_dir: Any,
) -> list[DrawingFile] | None:
    """Try downloading the 2D drawing PDF via CADDocumentMgmt.

    Searches for <wh_num>_DWG1 CAD Document, gets its Representation,
    and downloads the PDF from AdditionalFiles.
    """
    from pathlib import Path

    http = client._http
    base_url = client._http._config.base_url

    dwg_number = f"{wh_num}_DWG1"

    try:
        # Step 1: Find the drawing CAD Document (v1 only for CADDocumentMgmt)
        url = f"{base_url}/v1/CADDocumentMgmt/CADDocuments?$filter=Number eq '{dwg_number}'"
        resp = await http.get_json(url)
        items = resp.get("value", [])

        if not items:
            return None

        cad_id = items[0].get("ID", "")
        if not cad_id:
            return None

        # Step 2: Get Representations on the CAD Document
        url = f"{base_url}/v1/CADDocumentMgmt/CADDocuments('{cad_id}')/Representations"
        resp = await http.get_json(url)
        reps = resp.get("value", [])

        if not reps:
            return None

        rep_id = reps[0].get("ID", "")
        if not rep_id:
            return None

        # Step 3: Get Representation details from Visualization domain
        url = f"{base_url}/v1/Visualization/Representations('{rep_id}')"
        resp = await http.get_json(url)

        additional_files = resp.get("AdditionalFiles", [])

        # Find a PDF or TIFF in AdditionalFiles
        download_file = None
        for af in additional_files:
            mime = (af.get("MimeType") or "").lower()
            fname = (af.get("FileName") or "").lower()
            if "pdf" in mime or fname.endswith(".pdf"):
                download_file = af
                break
            if "tiff" in mime or "tif" in mime or fname.endswith((".tif", ".tiff")):
                download_file = af
                break

        if not download_file or not download_file.get("URL"):
            # Fallback: try TwoDThumbnailURL (lower quality but better than nothing)
            thumb = resp.get("TwoDThumbnailURL")
            if isinstance(thumb, dict) and thumb.get("URL"):
                download_file = thumb

        if not download_file or not download_file.get("URL"):
            return None

        # Step 4: Download the file
        dl_url = download_file["URL"]
        file_name = download_file.get("FileName", f"{wh_num}.pdf")
        file_ext = Path(file_name).suffix or ".pdf"
        out_path = Path(output_dir) / f"{wh_num}{file_ext}"

        content, _headers = await http.download_content_url(dl_url)
        out_path.write_bytes(content)

        file_size_kb = len(content) // 1024
        logger.info("Downloaded drawing %s via CAD drawing (%d KB)", wh_num, file_size_kb)

        return [DrawingFile(wh_number=wh_num, file_path=out_path, page_number=1)]

    except Exception as exc:
        logger.debug("CAD drawing download failed for %s: %s", wh_num, exc)
        return None


def load_drawings_from_folder(folder: str | Any) -> dict[str, list[DrawingFile]]:
    """Load drawing files from a local folder (TIFF files).

    Handles the Contiweb naming convention:
    0000_WH1234567_2_D_Contiweb CAD Document_page1.tif

    Args:
        folder: Path to folder with TIFF/PDF files.

    Returns:
        Dict mapping WH-number to list of DrawingFile sorted by page number.
    """
    from pathlib import Path

    folder = Path(folder)
    drawings: dict[str, list[DrawingFile]] = {}

    if not folder.exists():
        logger.warning("Drawing folder does not exist: %s", folder)
        return drawings

    for file_path in sorted(folder.iterdir()):
        if file_path.suffix.lower() not in (".tif", ".tiff", ".pdf"):
            continue

        name = file_path.stem

        # Extract WH-number from DocumentMailer naming conventions:
        #   0000_WH1234567_2_D_Contiweb CAD Document.tif
        #   0096_WH7003043_2_-_EPLAN Document.pdf
        #   0096_WH7003043-B20_1_-_FRONT_PAGE.pdf
        #   WH1234567_page1.tif
        parts = name.split("_")

        # Find the first part that starts with "WH"
        short = ""
        for part in parts:
            if part.startswith("WH"):
                # Strip version suffix like "-B00", "-B20"
                short = part.split("-")[0] if "-" in part else part
                break

        if not short:
            continue

        # Extract page number from filename
        page_num = 1
        for part in reversed(name.split("_")):
            if part.startswith("page") and part[4:].isdigit():
                page_num = int(part[4:])
                break
            # Also check for trailing digits before extension
        # Fallback: look for number at end of filename
        stripped = name.rstrip("0123456789")
        if stripped != name:
            trailing = name[len(stripped):]
            if trailing.isdigit():
                page_num = int(trailing)

        drawings.setdefault(short, []).append(
            DrawingFile(wh_number=short, file_path=file_path, page_number=page_num)
        )

    # Sort each drawing's pages by page number
    for wh_num in drawings:
        drawings[wh_num].sort(key=lambda d: d.page_number)

    logger.info("Loaded %d drawings from %s", sum(len(v) for v in drawings.values()), folder)
    return drawings
