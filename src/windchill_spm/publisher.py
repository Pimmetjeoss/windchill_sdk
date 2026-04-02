"""Publish generated SPM PDFs to Windchill.

Creates a WTDocument with a WH-number and uploads the PDF file.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


async def publish_to_windchill(
    client: Any,
    pdf_path: str | Path,
    document_name: str,
    *,
    document_number: str | None = None,
    context_id: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Create a WTDocument in Windchill and upload the PDF.

    Workflow:
    1. Create document (gets a WH-number)
    2. Checkout (get working copy)
    3. Upload PDF as primary content
    4. Checkin

    Args:
        client: WindchillClient instance.
        pdf_path: Path to the generated PDF file.
        document_name: Name for the document (e.g. "SPM Machine X - Mechanical").
        document_number: Optional WH-number. If None, auto-generated.
        context_id: Container to create the document in.
        description: Optional document description.

    Returns:
        Dict with document info including the assigned WH-number.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Step 1: Create document
    logger.info("Creating document: %s", document_name)
    doc = await client.doc_mgmt.create_document(
        document_name,
        number=document_number,
        context_id=context_id,
        description=description or f"Spare Parts Manual - {document_name}",
    )

    doc_id = doc.get("ID", "")
    doc_number = doc.get("Number", "")
    logger.info("Created document %s (ID: %s)", doc_number, doc_id)

    # Step 2: Checkout
    logger.info("Checking out document %s", doc_number)
    working_copy = await client.doc_mgmt.checkout_document(doc_id)
    wc_id = working_copy.get("ID", "")

    try:
        # Step 3: Upload PDF
        logger.info("Uploading %s (%.1f MB)", pdf_path.name, pdf_path.stat().st_size / (1024 * 1024))
        await client.doc_mgmt.upload_content(wc_id, pdf_path, role="PRIMARY")

        # Step 4: Checkin
        logger.info("Checking in document %s", doc_number)
        await client.doc_mgmt.checkin_document(
            wc_id, comment="SPM generated automatically"
        )

        logger.info("Published %s as %s", pdf_path.name, doc_number)
        return {
            "document_id": doc_id,
            "document_number": doc_number,
            "document_name": document_name,
            "file_name": pdf_path.name,
            "file_size": pdf_path.stat().st_size,
            "status": "published",
        }

    except Exception:
        # Attempt to undo checkout on failure
        logger.error("Upload failed, attempting to undo checkout")
        try:
            await client.doc_mgmt.undo_checkout_document(wc_id)
        except Exception as undo_exc:
            logger.error("Undo checkout also failed: %s", undo_exc)
        raise


async def update_existing_document(
    client: Any,
    pdf_path: str | Path,
    document_number: str,
) -> dict[str, Any]:
    """Update an existing WTDocument with a new PDF revision.

    For when the document already exists (e.g. WH806126) and you want
    to upload a new version.

    Args:
        client: WindchillClient instance.
        pdf_path: Path to the new PDF file.
        document_number: Existing WH-number (e.g. "WH806126").

    Returns:
        Dict with updated document info.
    """
    from windchill.odata.filter import F
    from windchill.odata.query import Query

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Find existing document
    query = Query().filter(F.eq("Number", document_number)).top(1)
    response = await client.doc_mgmt.list_documents(query)

    if not response.items:
        raise ValueError(f"Document {document_number} not found in Windchill")

    doc = response.items[0]
    doc_id = doc.get("ID", "")

    # Revise → Checkout → Upload → Checkin
    logger.info("Revising document %s", document_number)
    revised = await client.doc_mgmt.revise_document(doc_id)
    revised_id = revised.get("ID", "")

    logger.info("Checking out revision")
    working_copy = await client.doc_mgmt.checkout_document(revised_id)
    wc_id = working_copy.get("ID", "")

    try:
        logger.info("Uploading new PDF")
        await client.doc_mgmt.upload_content(wc_id, pdf_path, role="PRIMARY")

        logger.info("Checking in revision")
        await client.doc_mgmt.checkin_document(
            wc_id, comment="SPM updated automatically"
        )

        return {
            "document_id": revised_id,
            "document_number": document_number,
            "file_name": pdf_path.name,
            "file_size": pdf_path.stat().st_size,
            "status": "updated",
        }

    except Exception:
        logger.error("Update failed, attempting to undo checkout")
        try:
            await client.doc_mgmt.undo_checkout_document(wc_id)
        except Exception as undo_exc:
            logger.error("Undo checkout also failed: %s", undo_exc)
        raise
