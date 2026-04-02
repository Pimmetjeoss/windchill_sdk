"""PDF generator for Spare Parts Manuals.

Replaces both MSPM and ESPM Word macros. Generates a professional PDF
with drawings, BOM tables, and proper heading hierarchy.
Uses reportlab for PDF creation.
"""

from __future__ import annotations

import logging
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from windchill_spm.models import BomLine, DrawingFile, ManualContent

logger = logging.getLogger(__name__)

# ── Page Setup ──

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 2 * cm
MARGIN_RIGHT = 2 * cm
MARGIN_TOP = 2 * cm
MARGIN_BOTTOM = 2 * cm
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
CONTENT_HEIGHT = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

# Drawing heights matching VBA (17cm first, 17.5cm subsequent)
DRAWING_HEIGHT_FIRST = 17 * cm
DRAWING_HEIGHT_SUBSEQUENT = 17.5 * cm

# BOM column spacing
COL_SPACING = 5  # Characters of space between columns (matches VBA ColumnSpace = 5)

# Monospace font for BOMs
BOM_FONT = "Courier"
BOM_FONT_SIZE = 7
BOM_LINE_HEIGHT = 9


def _build_styles() -> dict[str, ParagraphStyle]:
    """Create paragraph styles matching the VBA manual formatting."""
    base = getSampleStyleSheet()

    return {
        "heading1": ParagraphStyle(
            "SPMHeading1",
            parent=base["Heading1"],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=6,
            textColor=colors.black,
            fontName="Helvetica-Bold",
        ),
        "heading2": ParagraphStyle(
            "SPMHeading2",
            parent=base["Heading2"],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=6,
            textColor=colors.black,
            fontName="Helvetica-Bold",
        ),
        "heading3": ParagraphStyle(
            "SPMHeading3",
            parent=base["Heading3"],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=4,
            textColor=colors.black,
            fontName="Helvetica-Bold",
        ),
        "normal": ParagraphStyle(
            "SPMNormal",
            parent=base["Normal"],
            fontSize=10,
            fontName="Helvetica",
        ),
        "bom": ParagraphStyle(
            "SPMBom",
            fontSize=BOM_FONT_SIZE,
            fontName=BOM_FONT,
            leading=BOM_LINE_HEIGHT,
            alignment=TA_LEFT,
        ),
        "bom_bold": ParagraphStyle(
            "SPMBomBold",
            fontSize=BOM_FONT_SIZE,
            fontName="Courier-Bold",
            leading=BOM_LINE_HEIGHT,
            alignment=TA_LEFT,
        ),
    }


# ── PDF Builder ──


def generate_pdf(content: ManualContent, output_path: str | Path) -> Path:
    """Generate a complete Spare Parts Manual PDF.

    Args:
        content: ManualContent with all sections, drawings, and BOMs.
        output_path: Where to save the PDF.

    Returns:
        Path to the generated PDF file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = _build_styles()
    story: list = []

    # ── Main Overview Drawing(s) ──
    if content.main_overview_drawings:
        story.append(Paragraph("Main Overview Drawing(s)", styles["heading1"]))
        _add_drawings(story, content.main_overview_drawings, styles)

    # ── General Overview Drawings ──
    if content.general_overview_drawings:
        story.append(Paragraph("Overview Drawings", styles["heading1"]))
        _add_drawings(story, content.general_overview_drawings, styles)

    # ── Sections with Drawing (Mechanical or Electrical parts) ──
    if content.sections_with_drawing:
        section_title = _main_chapter_title(content.title)
        story.append(Paragraph(section_title, styles["heading1"]))

        # Group sections by drawing number to avoid duplicates
        done_drawings: set[str] = set()

        for section in content.sections_with_drawing:
            # Write drawing (if not already written)
            if section.assembly_drawing_number not in done_drawings and section.drawings:
                story.append(
                    Paragraph(
                        f"Drawing {section.assembly_drawing_number} "
                        f"{_escape(section.name)} ({section.sort_key})",
                        styles["heading2"],
                    )
                )
                _add_drawings(story, section.drawings, styles)
                done_drawings.add(section.assembly_drawing_number)

            # Write BOM
            if section.bom_lines:
                story.append(
                    Paragraph(f"BOM {section.legend_number}", styles["heading3"])
                )
                _add_bom_table(story, section.bom_lines, styles)

            story.append(PageBreak())

    # ── General Parts (standalone, no children) ──
    if content.general_parts:
        general_title = (
            "General mechanical parts"
            if "Mechanical" in content.title
            else "General electrical parts"
        )
        story.append(Paragraph(general_title, styles["heading1"]))
        _add_bom_table(story, content.general_parts, styles)
        story.append(PageBreak())

    # ── Sections without Drawing ──
    if content.sections_without_drawing:
        no_dwg_title = (
            "Mechanical Boms without drawing"
            if "Mechanical" in content.title
            else "Electrical Boms without drawing"
        )
        story.append(Paragraph(no_dwg_title, styles["heading1"]))

        for section in content.sections_without_drawing:
            if section.bom_lines:
                story.append(
                    Paragraph(f"BOM {section.legend_number}", styles["heading3"])
                )
                _add_bom_table(story, section.bom_lines, styles)
                story.append(Spacer(1, 12))

    # ── Build PDF ──
    if not story:
        story.append(Paragraph("No content available.", styles["normal"]))

    doc = BaseDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title=content.title,
        author="Contiweb SPM Generator",
    )

    frame = Frame(
        MARGIN_LEFT,
        MARGIN_BOTTOM,
        CONTENT_WIDTH,
        CONTENT_HEIGHT,
        id="main",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])

    doc.build(story)

    file_size = output_path.stat().st_size
    logger.info(
        "Generated PDF: %s (%.1f MB, %s)",
        output_path.name,
        file_size / (1024 * 1024),
        content.title,
    )
    return output_path


# ── Drawing Insertion ──


def _add_drawings(
    story: list,
    drawings: tuple[DrawingFile, ...] | list[DrawingFile],
    styles: dict[str, ParagraphStyle],
) -> None:
    """Add drawing images to the story."""
    for idx, dwg in enumerate(drawings):
        if not dwg.file_path.exists():
            story.append(
                Paragraph(
                    f"[Drawing not found: {dwg.wh_number}]", styles["normal"]
                )
            )
            continue

        try:
            height = DRAWING_HEIGHT_FIRST if idx == 0 else DRAWING_HEIGHT_SUBSEQUENT

            img = Image(str(dwg.file_path))

            # Scale to fit width while maintaining aspect ratio
            aspect = img.imageWidth / img.imageHeight if img.imageHeight > 0 else 1
            target_width = height * aspect

            # Constrain to content width
            if target_width > CONTENT_WIDTH:
                target_width = CONTENT_WIDTH
                height = target_width / aspect

            img.drawWidth = target_width
            img.drawHeight = height

            story.append(img)
            story.append(PageBreak())

        except Exception as exc:
            logger.warning("Failed to insert drawing %s: %s", dwg.wh_number, exc)
            story.append(
                Paragraph(
                    f"[Error loading drawing: {dwg.wh_number} - {exc}]",
                    styles["normal"],
                )
            )


# ── BOM Table ──


def _add_bom_table(
    story: list,
    bom_lines: tuple[BomLine, ...] | list[BomLine],
    styles: dict[str, ParagraphStyle],
) -> None:
    """Add a BOM table to the story.

    Uses a reportlab Table with monospace font, matching the VBA
    Lucida Sans Typewriter formatting.
    """
    if not bom_lines:
        return

    # Table headers
    headers = ["Pos no", "Function no", "Part no", "Part name", "Device tag"]

    # Build table data
    data = [headers]
    for line in bom_lines:
        data.append([
            line.pos_number,
            line.function_number,
            line.part_number,
            line.part_name,
            line.device_tag,
        ])

    # Calculate column widths based on content
    col_widths = _calculate_col_widths(data)

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle([
            # Header row
            ("FONTNAME", (0, 0), (-1, 0), "Courier-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), BOM_FONT_SIZE),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
            ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
            # Data rows
            ("FONTNAME", (0, 1), (-1, -1), BOM_FONT),
            ("FONTSIZE", (0, 1), (-1, -1), BOM_FONT_SIZE),
            ("TOPPADDING", (0, 1), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 1),
            # Alignment
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            # Alternating row colors for readability
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ])
    )

    story.append(table)
    story.append(Spacer(1, 6))


def _calculate_col_widths(data: list[list[str]]) -> list[float]:
    """Calculate column widths based on content length.

    Uses character count with monospace font metrics.
    """
    num_cols = len(data[0])
    max_lengths = [0] * num_cols

    for row in data:
        for i, cell in enumerate(row):
            max_lengths[i] = max(max_lengths[i], len(str(cell)))

    # Character width in Courier at BOM_FONT_SIZE
    char_width = BOM_FONT_SIZE * 0.6  # Approximate Courier character width

    # Add padding (matches VBA ColumnSpace = 5)
    widths = [(length + COL_SPACING) * char_width for length in max_lengths]

    # Ensure total doesn't exceed content width
    total = sum(widths)
    if total > CONTENT_WIDTH:
        scale = CONTENT_WIDTH / total
        widths = [w * scale for w in widths]

    return widths


# ── Helpers ──


def _main_chapter_title(manual_title: str) -> str:
    """Get the main chapter title based on manual type."""
    if "Mechanical" in manual_title:
        return "Mechanical parts"
    return "Electrical drawings"


def _escape(text: str) -> str:
    """Escape special characters for reportlab Paragraph."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
