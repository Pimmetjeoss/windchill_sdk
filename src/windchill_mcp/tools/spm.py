"""Spare Parts Manual generation tool for Windchill MCP Server."""

from __future__ import annotations

import json
import logging

from windchill_mcp.server import get_client, mcp

logger = logging.getLogger(__name__)


@mcp.tool()
async def windchill_generate_spm(
    sap_export_path: str,
    output_dir: str = "",
    drawings_folder: str = "",
    machine_name: str = "",
    publish_to_windchill: bool = False,
    context_id: str = "",
    service_boms_file: str = "",
    drawing_master_file: str = "",
) -> str:
    """Generate Spare Parts Manuals (MSPM + ESPM) from a SAP BOM export.

    Creates both a Mechanical (MSPM) and Electrical (ESPM) spare parts
    manual as PDF files. Optionally uploads them to Windchill as WTDocuments.

    Data sources:
    - SAP BOM export (required): Excel file with 14-column BOM structure
    - Windchill (optional): Service BOMs for BOM explosion, drawings download
    - Local drawings folder (optional): TIFF/PDF files for assembly drawings
    - Legacy files (optional): Service BOMs text file, Drawing master data

    Args:
        sap_export_path: Path to the SAP BOM export Excel file (.xls/.xlsx).
        output_dir: Directory to save generated PDFs. Defaults to temp dir.
        drawings_folder: Path to folder with TIFF/PDF drawing files.
        machine_name: Machine name for document titles (e.g. "CW850").
        publish_to_windchill: If true, upload PDFs as new WTDocuments.
        context_id: Windchill container ID for new documents (required if publishing).
        service_boms_file: Path to legacy Service BOMs text file (tab-delimited).
        drawing_master_file: Path to legacy Assembly Drawing master data file.

    Returns:
        JSON string with generation results including file paths and WH-numbers.
    """
    from windchill_spm.pipeline import generate_spm

    client = None
    try:
        client = await get_client()
    except Exception:
        logger.info("No Windchill client available — running without Windchill enrichment")

    result = await generate_spm(
        sap_export_path,
        client=client,
        drawings_folder=drawings_folder or None,
        output_dir=output_dir or None,
        publish=publish_to_windchill,
        context_id=context_id or None,
        machine_name=machine_name,
        service_boms_file=service_boms_file or None,
        drawing_master_file=drawing_master_file or None,
    )

    return json.dumps(
        {
            "mspm_pdf": str(result.mspm_pdf_path) if result.mspm_pdf_path else None,
            "espm_pdf": str(result.espm_pdf_path) if result.espm_pdf_path else None,
            "mspm_wh_number": result.mspm_wh_number,
            "espm_wh_number": result.espm_wh_number,
            "warnings": list(result.warnings),
        },
        indent=2,
    )
