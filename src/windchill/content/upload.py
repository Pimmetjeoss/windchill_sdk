"""File upload utilities for Windchill REST API.

Supports both direct multipart upload and 3-stage upload for large files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from windchill.http import HttpTransport


@dataclass(frozen=True)
class UploadResult:
    """Result of a file upload operation."""

    success: bool
    content_id: str | None = None
    stream_id: str | None = None
    message: str = ""


async def direct_upload(
    http: HttpTransport,
    upload_url: str,
    file_path: Path,
    *,
    role: str = "PRIMARY",
    description: str | None = None,
) -> UploadResult:
    """Upload a file using direct multipart/form-data.

    Args:
        http: HTTP transport instance.
        upload_url: The bound action URL for UploadContent.
        file_path: Path to the file to upload.
        role: Content role ("PRIMARY" or "SECONDARY").
        description: Optional content description.
    """
    metadata: dict[str, Any] = {
        "ContentRole": role,
        "FileName": file_path.name,
    }
    if description:
        metadata["ContentDescription"] = description

    boundary = "windchill_sdk_upload"
    body = _build_multipart_body(boundary, metadata, file_path)

    response = await http.request(
        "POST",
        upload_url,
        data=body,
        content_type=f"multipart/form-data; boundary={boundary}",
    )

    if response.status_code in (200, 201, 204):
        resp_data = response.json() if response.content else {}
        return UploadResult(
            success=True,
            content_id=resp_data.get("ID"),
            message="Upload successful",
        )

    from windchill.errors import raise_for_status

    resp_body = response.json() if response.content else {}
    raise_for_status(response.status_code, resp_body)
    return UploadResult(success=False, message="Upload failed")


@dataclass(frozen=True)
class Stage1Result:
    """Result from Stage 1 of the 3-stage upload."""

    replica_url: str
    master_url: str
    stream_id: str
    cache_descriptors: dict[str, Any]


async def staged_upload_stage1(
    http: HttpTransport,
    stage1_url: str,
    file_name: str,
    *,
    role: str = "PRIMARY",
    description: str | None = None,
) -> Stage1Result:
    """Stage 1: Initiate upload and get cache descriptors."""
    body: dict[str, Any] = {
        "ContentRole": role,
        "FileName": file_name,
    }
    if description:
        body["ContentDescription"] = description

    data = await http.post_json(stage1_url, body)

    return Stage1Result(
        replica_url=data.get("ReplicaUrl", ""),
        master_url=data.get("MasterUrl", ""),
        stream_id=data.get("StreamId", ""),
        cache_descriptors=data,
    )


async def staged_upload_stage2(
    http: HttpTransport,
    upload_url: str,
    file_path: Path,
    stream_id: str,
) -> bool:
    """Stage 2: Upload file data to the replica/master URL."""
    boundary = "windchill_sdk_stage2"
    metadata = {"StreamId": stream_id}
    body = _build_multipart_body(boundary, metadata, file_path)

    response = await http.request(
        "POST",
        upload_url,
        data=body,
        content_type=f"multipart/form-data; boundary={boundary}",
    )

    return response.status_code in (200, 201, 204)


async def staged_upload_stage3(
    http: HttpTransport,
    content_info_url: str,
    stream_id: str,
) -> dict[str, Any]:
    """Stage 3: Commit the upload by updating ContentInfo with StreamId."""
    return await http.patch_json(content_info_url, {"StreamId": stream_id})


def _build_multipart_body(
    boundary: str,
    metadata: dict[str, Any],
    file_path: Path,
) -> bytes:
    """Build a multipart/form-data body with JSON metadata and file content."""
    parts = []

    # Part 1: JSON metadata
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="metadata"')
    parts.append("Content-Type: application/json")
    parts.append("")
    parts.append(json.dumps(metadata))

    # Part 2: File binary
    parts.append(f"--{boundary}")
    parts.append(
        f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"'
    )
    parts.append("Content-Type: application/octet-stream")
    parts.append("")

    preamble = "\r\n".join(parts) + "\r\n"
    epilogue = f"\r\n--{boundary}--\r\n"

    return preamble.encode("utf-8") + file_path.read_bytes() + epilogue.encode("utf-8")
