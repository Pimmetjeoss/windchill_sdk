# Actions Available in the PTC Document Management Domain

> **Domain ID:** `DocMgmt`
> **Base URL:** `/Windchill/servlet/odata/DocMgmt`

## UpdateCommonProperties

The `UpdateCommonProperties` action edits the common properties of documents.

### Prerequisites

- The property `hasCommonProperties` must be set to `true` in the `Documents.json` file.
- The action must **not** be called on objects that are checked out.

### Editable Attributes

In the current release, you can only edit the following attributes:

| Attribute | Description |
|-----------|-------------|
| `Name` | Document name |
| `Number` | Document number |
| `Organization` | Organization associated with the document (via `PTC.UpdateableViaAction` annotation) |

### Usage

```http
POST /Windchill/servlet/odata/DocMgmt/Documents('<document_id>')/PTC.DocMgmt.UpdateCommonProperties HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Name": "UpdatedDocName",
  "Number": "DOC-001-Updated"
}
```

### Notes

- The `Organization` navigation property is annotated with `PTC.UpdateableViaAction` to indicate that this property can be updated using only an action (not via PATCH).

## Multi-Object Actions

The following actions are available for operating on multiple document objects. These actions follow the pattern `<Action><EntitySetName>`.

### CreateDocuments

Creates multiple documents in a single request.

```http
POST /Windchill/servlet/odata/DocMgmt/CreateDocuments HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Documents": [
    {
      "Name": "test doc1",
      "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:302725')"
    },
    {
      "Name": "test doc2",
      "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:302725')"
    }
  ]
}
```

### UpdateDocuments

Updates multiple documents in a single request.

```http
POST /Windchill/servlet/odata/DocMgmt/UpdateDocuments HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Documents": [
    {
      "ID": "OR:wt.doc.WTDocument:2276131",
      "Description": "Updated description1",
      "Title": "Updated title1"
    },
    {
      "ID": "OR:wt.doc.WTDocument:2276126",
      "Title": "Updated title2"
    }
  ]
}
```

### DeleteDocuments

Deletes multiple documents. Requires `"multiOperations": "DELETE"` in the Entity JSON file.

```http
POST /Windchill/servlet/odata/DocMgmt/DeleteDocuments HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

### CheckOutDocuments

Checks out multiple documents.

```http
POST /Windchill/servlet/odata/DocMgmt/CheckOutDocuments HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

### CheckInDocuments

Checks in multiple documents.

```http
POST /Windchill/servlet/odata/DocMgmt/CheckInDocuments HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

### UndoCheckOutDocuments

Undoes check-out for multiple documents.

```http
POST /Windchill/servlet/odata/DocMgmt/UndoCheckOutDocuments HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

### ReviseDocuments

Revises multiple documents (creates new versions).

```http
POST /Windchill/servlet/odata/DocMgmt/ReviseDocuments HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

## Content Upload Actions

### uploadStage1Action

Initiates the content upload process for a document. Returns cache descriptors needed for file upload.

**Bound to:** `Document` entity

```http
POST /Windchill/servlet/odata/DocMgmt/Documents('<document_id>')/PTC.DocMgmt.uploadStage1Action HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "noOfFiles": 3
}
```

Response:
```json
{
  "@odata.context": "$metadata#CacheDescriptor",
  "value": [
    {
      "ID": null,
      "ReplicaUrl": "https://windchill.ptc.com/Windchill/servlet/WindchillGW/...",
      "MasterUrl": "https://windchill.ptc.com/Windchill/servlet/WindchillGW",
      "VaultId": 150301,
      "FolderId": 150329,
      "StreamIds": [76030, 76032, 76031],
      "FileNames": [76030, 76032, 76031]
    }
  ]
}
```

The upload process follows three stages:
1. **Stage 1** -- Call `uploadStage1Action` to get cache descriptors (ReplicaUrl, StreamIds)
2. **Stage 2** -- Upload files to the ReplicaUrl or MasterUrl using multipart form data
3. **Stage 3** -- Commit the upload using ContentInfo entity with the StreamIds from Stage 1
