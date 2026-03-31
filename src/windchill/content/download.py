"""File download utilities for Windchill REST API."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from windchill.http import HttpTransport

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ContentInfo:
    """Metadata about a downloadable file in Windchill."""

    id: str
    file_name: str
    file_size: int
    mime_type: str
    format: str
    download_url: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ContentInfo:
        content = data.get("Content", {})
        return cls(
            id=data.get("ID", ""),
            file_name=data.get("FileName", ""),
            file_size=data.get("FileSize", 0),
            mime_type=data.get("MimeType", ""),
            format=data.get("Format", ""),
            download_url=content.get("URL", ""),
        )


async def download_file(
    http: HttpTransport,
    download_url: str,
    output_path: Path,
) -> Path:
    """Download a file from a Windchill signed download URL.

    Uses session-based download to handle signed URLs correctly.
    """
    file_bytes, _ = await http.download_content_url(download_url)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(file_bytes)

    return output_path


async def get_primary_content_info(
    http: HttpTransport,
    doc_url: str,
) -> ContentInfo | None:
    """Get primary content metadata from a Document entity URL.

    Args:
        http: HTTP transport instance.
        doc_url: Full URL to the document entity (e.g., .../DocMgmt/Documents('{id}')).

    Returns:
        ContentInfo with download URL, or None if no content.
    """
    nav_url = f"{doc_url}/PrimaryContent"
    data = await http.get_json(nav_url)

    # PrimaryContent can return a single entity or a collection
    if "value" in data:
        items = data["value"]
        if not items:
            return None
        content_data = items[0]
    elif "ID" in data:
        content_data = data
    else:
        return None

    return ContentInfo.from_dict(content_data)


async def get_part_document_content(
    http: HttpTransport,
    base_url: str,
    part_id: str,
) -> ContentInfo | None:
    """Get content info for a Part by following the DescribedBy chain.

    Path: Part -> DescribedBy (links) -> DescribedBy (document) -> PrimaryContent

    This works on Windchill servers where Parts don't have direct content
    navigation, but have linked Documents via PartDescribeLink.

    Args:
        http: HTTP transport instance.
        base_url: OData base URL with version (e.g., .../odata/v3).
        part_id: Part Object Reference ID.

    Returns:
        ContentInfo with download URL, or None if no content found.
    """
    # Step 1: Get DescribedBy links from the Part
    links_url = f"{base_url}/ProdMgmt/Parts('{part_id}')/DescribedBy"
    logger.debug("Getting DescribedBy links from %s", links_url)

    links_data = await http.get_json(links_url)
    links = links_data.get("value", [])

    if not links:
        logger.debug("No DescribedBy links found for part %s", part_id)
        return None

    # Step 2: Follow each link's DescribedBy navigation to get the Document
    for link in links:
        link_id = link.get("ID", "")
        if not link_id:
            continue

        doc_url = f"{links_url}('{link_id}')/DescribedBy"
        logger.debug("Following link %s to document", link_id)

        try:
            doc_data = await http.get_json(doc_url)
        except Exception:
            logger.debug("Failed to follow link %s", link_id)
            continue

        doc_id = doc_data.get("ID", "")
        if not doc_id:
            continue

        # Step 3: Get PrimaryContent from the Document
        content_url = f"{base_url}/DocMgmt/Documents('{doc_id}')/PrimaryContent"
        logger.debug("Getting PrimaryContent from document %s", doc_id)

        try:
            content_info = await get_primary_content_info(http, f"{base_url}/DocMgmt/Documents('{doc_id}')")
            if content_info and content_info.download_url:
                return content_info
        except Exception:
            logger.debug("No primary content on document %s", doc_id)
            continue

    return None


async def download_part_content(
    http: HttpTransport,
    base_url: str,
    part_id: str,
    output_path: Path | None = None,
) -> Path:
    """Download the primary content file associated with a Part.

    Follows the full chain: Part -> DescribedBy -> Document -> PrimaryContent -> Download.

    Args:
        http: HTTP transport instance.
        base_url: OData base URL with version.
        part_id: Part Object Reference ID.
        output_path: Where to save. If None, uses the original filename.

    Returns:
        Path to the downloaded file.

    Raises:
        ValueError: If no content is found for the part.
    """
    content_info = await get_part_document_content(http, base_url, part_id)

    if not content_info or not content_info.download_url:
        raise ValueError(f"No downloadable content found for part {part_id}")

    if output_path is None:
        output_path = Path(content_info.file_name or "download.bin")

    logger.info(
        "Downloading %s (%s, %d bytes)",
        content_info.file_name,
        content_info.format,
        content_info.file_size,
    )

    return await download_file(http, content_info.download_url, output_path)


async def download_primary_content(
    http: HttpTransport,
    entity_url: str,
    output_path: Path,
) -> Path:
    """Download the primary content of a Document entity.

    Args:
        http: HTTP transport instance.
        entity_url: URL to the entity (e.g., .../DocMgmt/Documents('id')).
        output_path: Where to save the file.
    """
    content_info = await get_primary_content_info(http, entity_url)

    if not content_info or not content_info.download_url:
        raise ValueError("No primary content found")

    return await download_file(http, content_info.download_url, output_path)


async def download_attachments(
    http: HttpTransport,
    entity_url: str,
    output_dir: Path,
) -> list[Path]:
    """Download all attachments of an entity.

    Args:
        http: HTTP transport instance.
        entity_url: URL to the entity.
        output_dir: Directory to save files into.

    Returns:
        List of paths to downloaded files.
    """
    nav_url = f"{entity_url}/Attachments"
    data = await http.get_json(nav_url)

    attachments = data.get("value", [])
    downloaded: list[Path] = []

    for attachment in attachments:
        content_info = ContentInfo.from_dict(attachment)
        if content_info.download_url:
            file_path = output_dir / content_info.file_name
            await download_file(http, content_info.download_url, file_path)
            downloaded.append(file_path)

    return downloaded
