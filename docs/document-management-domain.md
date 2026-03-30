# PTC Document Management Domain

> **Domain ID:** `DocMgmt`
> **Base URL:** `/Windchill/servlet/odata/DocMgmt`
> **Metadata URL:** `/Windchill/servlet/odata/DocMgmt/$metadata`

The Document Management domain provides access to the document management capabilities of Windchill. It enables you to create documents. You can also upload and download content from documents.

## Entities

The following table lists the significant OData entities available in the Document Management domain. To see all the OData entities available, refer to the EDM of the domain at the metadata URL.

| Item | OData Entity | Windchill Class | Description |
|------|-------------|----------------|-------------|
| Business document | `Document` | `WTDocument` / `WTDocumentMaster` | Represents a document version. Use the `WTDocument` and `WTDocumentMaster` classes to work with document versions. |
| Content information | `ContentInfo` | - | Contains content information used in Stage 3 for uploading content to the document. |

## Entity Sets

| Entity Set | Description |
|-----------|-------------|
| `Documents` | Collection of `Document` entities |

## Key URLs

### Read Documents

```
GET /Windchill/servlet/odata/DocMgmt/Documents
```

### Read a Specific Document by ID

```
GET /Windchill/servlet/odata/DocMgmt/Documents('<document_id>')
```

Example:
```
GET /Windchill/servlet/odata/DocMgmt/Documents('VR:wt.doc.WTDocument:48796553')
```

### Create a Document

```http
POST /Windchill/servlet/odata/DocMgmt/Documents HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Name": "TestDoc1",
  "Description": "TestDoc1_Description",
  "Title": "TestDoc1_Title",
  "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:48788507')"
}
```

### Create a Document in a Different Organization

Set the preference **Expose Organization** in Preference Management utility to **Yes**.

```http
POST /Windchill/servlet/odata/DocMgmt/Documents HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Name": "TestDoc1",
  "Description": "TestDoc1_Description",
  "Title": "TestDoc1_Title",
  "Organization@odata.bind": "Organizations('OR:wt.inf.container.OrgContainer:373739')",
  "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:48788507')"
}
```

### Create Multiple Documents

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

### Update a Document

```http
PATCH /Windchill/servlet/odata/DocMgmt/Documents('VR:wt.doc.WTDocument:48796553') HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Description": "TestDoc1_Description_Update",
  "CustomAttribute": "This is Test Attribute"
}
```

### Update Multiple Documents

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

### Check Out a Document

```http
POST /Windchill/servlet/odata/DocMgmt/Documents HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "CheckOutNote": "This is checkout note."
}
```

## Uploading Content for a Document

Content upload is a multi-stage process:

### Stage 1 -- Initiate Upload

```http
POST /Windchill/servlet/odata/DocMgmt/Documents('OR:wt.doc.WTDocument:48796581')/PTC.DocMgmt.uploadStage1Action HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "noOfFiles": 3
}
```

Stage 1 Response (sample):
```json
{
  "@odata.context": "$metadata#CacheDescriptor",
  "value": [
    {
      "ID": null,
      "ReplicaUrl": "https://windchill.ptc.com/Windchill/servlet/WindchillGW/wt.fv.uploadtocache.DoUploadToCache_Server/doUploadToChache_Master?...",
      "MasterUrl": "https://windchill.ptc.com/Windchill/servlet/WindchillGW",
      "VaultId": 150301,
      "FolderId": 150329,
      "StreamIds": [76030, 76032, 76031],
      "FileNames": [76030, 76032, 76031]
    }
  ]
}
```

### Stage 2 -- Upload Files

Upload files to the `ReplicaUrl` or `MasterUrl` returned in Stage 1 using multipart form data.

### Stage 3 -- Commit Upload

Use the `ContentInfo` entity with the stream IDs from Stage 1 to finalize the content association.

## Multi-Object Actions

The following actions are available for operating on multiple documents (added in v1.3/v1.4):

| Action | HTTP Method | Description |
|--------|------------|-------------|
| `CreateDocuments` | POST | Create multiple documents |
| `UpdateDocuments` | POST | Update multiple documents |
| `DeleteDocuments` | POST | Delete multiple documents |
| `CheckInDocuments` | POST | Check in multiple documents |
| `CheckOutDocuments` | POST | Check out multiple documents |
| `UndoCheckOutDocuments` | POST | Undo check out for multiple documents |
| `ReviseDocuments` | POST | Revise multiple documents |

## Inherited Capabilities

The Document entity inherits common Windchill capabilities:

- **workable** -- Supports check-in, check-out, undo check-out operations
- **versioned** -- Supports revise operations
- **lifecycleManaged** -- Supports lifecycle state management
- **subtypeable** -- Supports soft type extensions
- **softattributable** -- Supports soft attributes
- **classifiable** -- Supports classification

## Navigation Properties

Common navigation properties available on the `Document` entity:

| Navigation Property | Description |
|--------------------|-------------|
| `Context` | The container context of the document |
| `Organization` | The organization of the document |
| `Folder` | The folder containing the document |
| `Creator` | User who created the document |
| `Modifier` | User who last modified the document |
| `PrimaryContent` | Primary content associated with the document |
| `Attachments` | Attachments associated with the document |
| `Contents` | All content items associated with the document |

## Extending the Domain

To extend the Document Management domain (e.g., to add a soft attribute), create a custom configuration file at:

```
<Windchill>/codebase/rest/custom/domain/DocMgmt/<version>/entity/DocumentsExt.json
```
