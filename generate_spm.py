"""CLI entry point for SPM generation.

Usage:
    # Via Windchill SDK (downloads drawings + service BOMs automatically):
    python generate_spm.py EXPORT.XLSX --name "CDN PASTER" --windchill

    # Via local drawings folder:
    python generate_spm.py EXPORT.XLSX --name "CDN PASTER" --drawings ./my_drawings/

    # Via DocumentMailer (wait for output on X-drive):
    python generate_spm.py EXPORT.XLSX --name "CDN PASTER" --wait

    # Only generate the Drawings list (to paste into DocumentMailer):
    python generate_spm.py EXPORT.XLSX --drawings-list-only
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Spare Parts Manuals (MSPM + ESPM)")
    parser.add_argument("sap_export", type=Path, help="SAP BOM export Excel file (.xls/.xlsx)")
    parser.add_argument("--output", "-o", type=Path, default=Path("output"), help="Output directory (default: ./output)")
    parser.add_argument("--name", "-n", default="", help="Machine name for titles")

    # Drawing source (mutually exclusive)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--windchill", action="store_true", help="Use Windchill SDK to download drawings and Service BOMs")
    source.add_argument("--drawings", "-d", type=Path, help="Local folder with drawings (TIFF/PDF)")
    source.add_argument("--drawings-list-only", action="store_true", help="Only output the Drawings list, then stop")
    source.add_argument("--wait", "-w", action="store_true", help="Wait for DocumentMailer output on X-drive")

    # Legacy file fallbacks
    parser.add_argument("--sboms", type=Path, help="Legacy Service BOMs text file")
    parser.add_argument("--dwg-master", type=Path, help="Legacy Assembly Drawing master data file")

    args = parser.parse_args()

    if not args.sap_export.exists():
        logger.error("SAP export file not found: %s", args.sap_export)
        sys.exit(1)

    asyncio.run(run(args))


async def run(args: argparse.Namespace) -> None:
    if args.windchill:
        await _run_windchill_pipeline(args)
    else:
        await _run_local_pipeline(args)


async def _run_windchill_pipeline(args: argparse.Namespace) -> None:
    """Run via Windchill SDK — downloads drawings + Service BOMs automatically."""
    from windchill_spm.pipeline import generate_spm

    logger.info("Running full pipeline via Windchill SDK")

    try:
        from windchill.client import WindchillClient
        from windchill.config import WindchillConfig

        config = WindchillConfig.from_env()
        client = WindchillClient(config)
    except Exception as exc:
        logger.error("Failed to create Windchill client: %s", exc)
        logger.error("Set WINDCHILL_BASE_URL, WINDCHILL_USERNAME, WINDCHILL_PASSWORD env vars")
        sys.exit(1)

    async with client:
        result = await generate_spm(
            sap_export_path=args.sap_export,
            client=client,
            output_dir=args.output,
            machine_name=args.name,
            service_boms_file=args.sboms,
            drawing_master_file=args.dwg_master,
        )

    if result.mspm_pdf_path:
        size_mb = result.mspm_pdf_path.stat().st_size / 1024 / 1024
        logger.info("MSPM: %s (%.1f MB)", result.mspm_pdf_path, size_mb)

    if result.espm_pdf_path:
        size_mb = result.espm_pdf_path.stat().st_size / 1024 / 1024
        logger.info("ESPM: %s (%.1f MB)", result.espm_pdf_path, size_mb)

    for w in result.warnings:
        logger.warning(w)

    if not result.mspm_pdf_path and not result.espm_pdf_path:
        logger.error("No content generated — check input data")
        sys.exit(1)

    logger.info("Done!")


async def _run_local_pipeline(args: argparse.Namespace) -> None:
    """Run with local drawings (DocumentMailer, folder, or none)."""
    from windchill_spm.documentmailer import find_latest_output, wait_for_output
    from windchill_spm.drawing_utils import convert_drawings, copy_to_clipboard
    from windchill_spm.enricher import (
        build_manual_content,
        explode_boms,
        generate_levels,
        load_drawings_from_folder,
    )
    from windchill_spm.pdf_generator import generate_pdf
    from windchill_spm.sap_reader import read_sap_export

    # ── Step 1: Parse SAP export ──
    logger.info("Step 1: Reading SAP export: %s", args.sap_export)
    sap_rows = read_sap_export(args.sap_export)
    logger.info("  %d rows parsed", len(sap_rows))

    # ── Step 2: Enrich ──
    service_boms: dict = {}
    if args.sboms and args.sboms.exists():
        from windchill_spm.pipeline import _load_service_boms_file
        service_boms = _load_service_boms_file(args.sboms)

    enriched = explode_boms(sap_rows, service_boms)

    if args.dwg_master and args.dwg_master.exists():
        from windchill_spm.enricher import match_assembly_drawings
        from windchill_spm.pipeline import _load_drawing_master_file
        enriched = match_assembly_drawings(enriched, _load_drawing_master_file(args.dwg_master))

    # ── Step 3: Generate Levels + Drawings list ──
    levels = generate_levels(enriched)
    logger.info("Step 2: %d level entries generated", len(levels))

    dwg_numbers = []
    for entry in levels:
        if entry.assembly_drawing_number and entry.assembly_drawing_number != "empty" and entry.explosion_level:
            if entry.assembly_drawing_number not in dwg_numbers:
                dwg_numbers.append(entry.assembly_drawing_number)

    args.output.mkdir(parents=True, exist_ok=True)
    drawings_list_path = args.output / "Drawings_list.txt"
    drawings_list_path.write_text("\n".join(dwg_numbers), encoding="utf-8")
    logger.info("Step 3: %d drawings needed → %s", len(dwg_numbers), drawings_list_path)

    copy_to_clipboard("\n".join(dwg_numbers))
    logger.info("  Drawings list copied to clipboard!")

    if args.drawings_list_only:
        logger.info("Done. Paste into DocumentMailer, then re-run without --drawings-list-only")
        return

    # ── Step 4: Get drawings ──
    drawings_folder = args.drawings

    if not drawings_folder:
        if args.wait:
            drawings_folder = wait_for_output()
        else:
            drawings_folder = find_latest_output()

    if not drawings_folder or not drawings_folder.exists():
        logger.warning("No drawings folder found. Generating PDFs without drawings.")
        logger.info("  Tip: use --windchill to download from Windchill SDK")
        logger.info("  Or use --drawings <folder> / --wait for DocumentMailer")
        drawings: dict = {}
    else:
        logger.info("Step 4: Loading drawings from: %s", drawings_folder)
        drawings = load_drawings_from_folder(drawings_folder)
        drawings = convert_drawings(drawings, args.output / "drawings_converted")
        logger.info("  %d drawings loaded (%d total pages)",
                     len(drawings), sum(len(v) for v in drawings.values()))

    # Report coverage
    found = set(drawings.keys())
    needed = set(dwg_numbers)
    missing = sorted(needed - found)
    if missing:
        logger.warning("  %d of %d drawings missing: %s%s",
                       len(missing), len(needed),
                       ", ".join(missing[:5]),
                       f" ... and {len(missing)-5} more" if len(missing) > 5 else "")

    # ── Step 5: Build manual content + generate PDFs ──
    logger.info("Step 5: Building manual content")
    mspm = build_manual_content("mechanical", levels, enriched, drawings)
    espm = build_manual_content("electrical", levels, enriched, drawings)

    prefix = f"{args.name} - " if args.name else ""

    has_mech = mspm.sections_with_drawing or mspm.general_parts or mspm.sections_without_drawing or mspm.main_overview_drawings
    has_elec = espm.sections_with_drawing or espm.general_parts or espm.sections_without_drawing

    if has_mech:
        mspm_path = generate_pdf(mspm, args.output / f"{prefix}MSPM.pdf")
        logger.info("  MSPM: %s (%.1f MB)", mspm_path, mspm_path.stat().st_size / 1024 / 1024)

    if has_elec:
        espm_path = generate_pdf(espm, args.output / f"{prefix}ESPM.pdf")
        logger.info("  ESPM: %s (%.1f MB)", espm_path, espm_path.stat().st_size / 1024 / 1024)

    if not has_mech and not has_elec:
        logger.error("No content generated — check input data")
        sys.exit(1)

    logger.info("Done!")


if __name__ == "__main__":
    main()
