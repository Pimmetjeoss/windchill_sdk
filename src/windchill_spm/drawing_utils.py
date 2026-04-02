"""Drawing file conversion utilities — TIFF splitting, PDF conversion, clipboard."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from windchill_spm.models import DrawingFile

logger = logging.getLogger(__name__)


def convert_drawings(
    drawings: dict[str, list[DrawingFile]],
    convert_dir: Path,
) -> dict[str, list[DrawingFile]]:
    """Convert PDF and multi-page TIFF drawings to single-page images."""
    convert_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, list[DrawingFile]] = {}

    for wh_num, pages in drawings.items():
        converted: list[DrawingFile] = []

        for dwg in pages:
            suffix = dwg.file_path.suffix.lower()

            if suffix in (".tif", ".tiff"):
                converted.extend(_split_tiff(dwg, convert_dir))
            elif suffix == ".pdf":
                converted.extend(_convert_pdf(dwg, convert_dir))
            else:
                converted.append(dwg)

        if converted:
            converted.sort(key=lambda d: d.page_number)
            result[wh_num] = converted

    return result


def copy_to_clipboard(text: str) -> None:
    """Copy text to the Windows clipboard."""
    try:
        process = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
        process.communicate(text.encode("utf-8"))
    except Exception:
        logger.debug("Could not copy to clipboard")


def _split_tiff(dwg: DrawingFile, convert_dir: Path) -> list[DrawingFile]:
    """Split a multi-page TIFF into single-page files."""
    try:
        from PIL import Image

        img = Image.open(dwg.file_path)
        n_frames = getattr(img, "n_frames", 1)

        if n_frames <= 1:
            img.close()
            return [dwg]

        pages: list[DrawingFile] = []
        for i in range(n_frames):
            img.seek(i)
            out = convert_dir / f"{dwg.wh_number}_page{i + 1}.tif"
            img.save(out)
            pages.append(DrawingFile(wh_number=dwg.wh_number, file_path=out, page_number=i + 1))
        img.close()
        return pages
    except ImportError:
        return [dwg]
    except Exception:
        logger.debug("Failed to split TIFF %s", dwg.file_path, exc_info=True)
        return [dwg]


def _convert_pdf(dwg: DrawingFile, convert_dir: Path) -> list[DrawingFile]:
    """Convert PDF pages to PNG images using pymupdf."""
    try:
        import fitz  # pymupdf

        doc = fitz.open(str(dwg.file_path))
        pages: list[DrawingFile] = []
        for i in range(len(doc)):
            page = doc[i]
            # Render at 200 DPI (default is 72, so zoom = 200/72)
            zoom = 200 / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            out = convert_dir / f"{dwg.wh_number}_page{i + 1}.png"
            pix.save(str(out))
            pages.append(DrawingFile(wh_number=dwg.wh_number, file_path=out, page_number=i + 1))
        doc.close()
        return pages if pages else [dwg]
    except ImportError:
        return [dwg]
    except Exception:
        logger.debug("Failed to convert PDF %s", dwg.file_path, exc_info=True)
        return [dwg]
