"""DocumentMailer integration — detect and wait for output folders."""

from __future__ import annotations

import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_DIR = Path("X:/DocumentMailer.Output")


def find_latest_output(base_dir: Path = DEFAULT_OUTPUT_DIR) -> Path | None:
    """Find the most recent DocumentMailer output folder containing drawings."""
    if not base_dir.exists():
        return None

    folders = sorted(
        base_dir.iterdir(),
        key=lambda p: p.stat().st_mtime if p.is_dir() else 0,
        reverse=True,
    )

    for folder in folders:
        if not folder.is_dir():
            continue
        if not any(folder.iterdir()):
            continue
        has_drawings = any(
            f.suffix.lower() in (".tif", ".tiff", ".pdf")
            for f in folder.iterdir()
            if f.is_file()
        )
        if has_drawings:
            logger.info("Found DocumentMailer output: %s", folder)
            return folder

    return None


def wait_for_output(
    base_dir: Path = DEFAULT_OUTPUT_DIR,
    timeout_minutes: int = 10,
) -> Path | None:
    """Wait for new DocumentMailer output to appear on X-drive."""
    logger.info("Waiting for DocumentMailer output on %s ...", base_dir)
    logger.info("(Paste the drawings list into DocumentMailer and click Send)")

    if not base_dir.exists():
        logger.error("X-drive not available: %s", base_dir)
        return None

    existing = {p.name for p in base_dir.iterdir() if p.is_dir()}

    deadline = time.time() + timeout_minutes * 60
    while time.time() < deadline:
        current = {p.name for p in base_dir.iterdir() if p.is_dir()}
        new_folders = current - existing

        for name in new_folders:
            folder = base_dir / name
            files = list(folder.iterdir())
            if len(files) > 0:
                logger.info("New folder detected: %s (%d files)", name, len(files))
                time.sleep(5)
                files = list(folder.iterdir())
                logger.info("Folder ready: %d files", len(files))
                return folder

        time.sleep(3)

    logger.warning("Timeout: no new DocumentMailer output after %d minutes", timeout_minutes)
    return None
