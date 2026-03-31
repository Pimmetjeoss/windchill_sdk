"""Document Management domain - Documents, content upload/download."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from windchill.domains.base import BaseDomain
from windchill.odata.query import Query
from windchill.types import ODataResponse


class DocMgmt(BaseDomain):
    """Document Management domain (DocMgmt).

    Manages documents, file content upload/download, and document-specific
    actions like checkout, checkin, and property updates.
    """

    domain = "DocMgmt"
    namespace = "PTC.DocMgmt"

    # ── Documents CRUD ──

    async def list_documents(self, query: Query | None = None) -> ODataResponse:
        """List documents with optional OData query."""
        return await self.list("Documents", query)

    async def get_document(self, doc_id: str) -> dict[str, Any]:
        """Get a single document by Object Reference ID."""
        return await self.get("Documents", doc_id)

    async def create_document(
        self,
        name: str,
        *,
        number: str | None = None,
        context_id: str | None = None,
        description: str | None = None,
        odata_type: str | None = None,
        **attributes: Any,
    ) -> dict[str, Any]:
        """Create a new document.

        Args:
            name: Document name.
            number: Document number (auto-generated if omitted).
            context_id: Container Object Reference ID.
            description: Document description.
            odata_type: OData type for soft types.
            **attributes: Additional properties.
        """
        data: dict[str, Any] = {"Name": name, **attributes}
        if number:
            data["Number"] = number
        if context_id:
            data["Context@odata.bind"] = f"Containers('{context_id}')"
        if description:
            data["Description"] = description
        if odata_type:
            data["@odata.type"] = odata_type
        return await self.create("Documents", data)

    async def update_document(
        self, doc_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update properties on an existing document."""
        return await self.update("Documents", doc_id, data)

    async def delete_document(self, doc_id: str) -> None:
        """Delete a document."""
        await self.delete("Documents", doc_id)

    # ── Document Actions (bound, single object) ──

    async def checkout_document(self, doc_id: str) -> dict[str, Any]:
        """Check out a document. Returns the working copy entity."""
        return await self.action("Documents", doc_id, "CheckOut", {})

    async def checkin_document(
        self, working_copy_id: str, comment: str | None = None
    ) -> dict[str, Any]:
        """Check in a document working copy."""
        body: dict[str, Any] = {}
        if comment:
            body["Comment"] = comment
        return await self.action("Documents", working_copy_id, "CheckIn", body)

    async def undo_checkout_document(self, working_copy_id: str) -> dict[str, Any]:
        """Undo checkout of a document working copy."""
        return await self.action("Documents", working_copy_id, "UndoCheckOut", {})

    async def revise_document(self, doc_id: str) -> dict[str, Any]:
        """Create a new revision of a document."""
        return await self.action("Documents", doc_id, "Revise", {})

    async def set_document_state(self, doc_id: str, state: str) -> dict[str, Any]:
        """Set the lifecycle state of a document."""
        return await self.action(
            "Documents", doc_id, "SetLifeCycleState", {"State": state}
        )

    async def update_common_properties(
        self,
        doc_id: str,
        *,
        name: str | None = None,
        number: str | None = None,
        organization: str | None = None,
    ) -> dict[str, Any]:
        """Update common properties on a checked-in document.

        Only works when hasCommonProperties is true and the document is not checked out.
        """
        body: dict[str, Any] = {}
        if name:
            body["Name"] = name
        if number:
            body["Number"] = number
        if organization:
            body["Organization"] = organization
        return await self.action("Documents", doc_id, "UpdateCommonProperties", body)

    # ── Content Upload ──

    async def upload_content(
        self,
        working_copy_id: str,
        file_path: str | Path,
        *,
        role: str = "PRIMARY",
        description: str | None = None,
    ) -> dict[str, Any]:
        """Upload file content to a document working copy using multipart/form-data.

        Args:
            working_copy_id: The working copy's Object Reference ID.
            file_path: Path to the file to upload.
            role: Content role - "PRIMARY" or "SECONDARY".
            description: Optional content description.
        """
        file_path = Path(file_path)
        url = self._bound_action_url("Documents", working_copy_id, "UploadContent")

        import json

        metadata: dict[str, Any] = {
            "ContentRole": role,
            "FileName": file_path.name,
        }
        if description:
            metadata["ContentDescription"] = description

        # Build multipart/form-data manually
        boundary = "windchill_sdk_upload_boundary"
        parts = []

        # Part 1: JSON metadata
        parts.append(f"--{boundary}")
        parts.append('Content-Disposition: form-data; name="metadata"')
        parts.append("Content-Type: application/json")
        parts.append("")
        parts.append(json.dumps(metadata))

        # Part 2: File content
        parts.append(f"--{boundary}")
        parts.append(
            f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"'
        )
        parts.append("Content-Type: application/octet-stream")
        parts.append("")

        preamble = "\r\n".join(parts) + "\r\n"
        epilogue = f"\r\n--{boundary}--\r\n"

        file_bytes = file_path.read_bytes()
        body = preamble.encode("utf-8") + file_bytes + epilogue.encode("utf-8")

        response = await self._http.request(
            "POST",
            url,
            data=body,
            content_type=f"multipart/form-data; boundary={boundary}",
        )

        if response.status_code == 204:
            return {}
        from windchill.errors import raise_for_status

        resp_body = response.json() if response.content else {}
        raise_for_status(response.status_code, resp_body)
        return resp_body

    async def upload_stage1(
        self,
        working_copy_id: str,
        file_name: str,
        *,
        role: str = "PRIMARY",
        description: str | None = None,
    ) -> dict[str, Any]:
        """Stage 1 of the 3-stage upload process: initiate upload.

        Returns cache descriptors with ReplicaUrl/MasterUrl and StreamIds.
        """
        body: dict[str, Any] = {
            "ContentRole": role,
            "FileName": file_name,
        }
        if description:
            body["ContentDescription"] = description
        return await self.action(
            "Documents", working_copy_id, "uploadStage1Action", body
        )

    # ── Content Download ──

    async def get_primary_content(self, doc_id: str) -> ODataResponse:
        """Get primary content metadata for a document."""
        return await self.navigate("Documents", doc_id, "PrimaryContent")

    async def get_attachments(
        self, doc_id: str, query: Query | None = None
    ) -> ODataResponse:
        """Get attachments (secondary content) for a document."""
        return await self.navigate("Documents", doc_id, "Attachments", query)

    async def download_primary(
        self, doc_id: str, output_path: str | Path
    ) -> Path:
        """Download the primary content file of a document.

        Args:
            doc_id: Document Object Reference ID.
            output_path: Path where the file should be saved.

        Returns:
            Path to the downloaded file.
        """
        output_path = Path(output_path)
        content_response = await self.get_primary_content(doc_id)
        content = content_response.first

        if not content:
            raise ValueError(f"Document {doc_id} has no primary content")

        download_url = content.get("DownloadURL") or content.get("downloadUrl", "")
        if not download_url:
            raise ValueError(f"No download URL found for document {doc_id}")

        file_bytes, headers = await self._http.get_bytes(download_url)
        output_path.write_bytes(file_bytes)
        return output_path

    # ── Multi-Object Actions (unbound) ──

    async def checkout_documents(self, doc_ids: list[str]) -> dict[str, Any]:
        """Check out multiple documents."""
        objects = [{"ID": did} for did in doc_ids]
        return await self.unbound_action("CheckOutDocuments", {"Objects": objects})

    async def checkin_documents(
        self, working_copy_ids: list[str]
    ) -> dict[str, Any]:
        """Check in multiple document working copies."""
        objects = [{"ID": wid} for wid in working_copy_ids]
        return await self.unbound_action("CheckInDocuments", {"Objects": objects})

    async def get_all_documents(
        self, query: Query | None = None, max_items: int | None = None
    ) -> list[dict[str, Any]]:
        """Collect all documents across all pages."""
        return await self.list_all("Documents", query, max_items)
