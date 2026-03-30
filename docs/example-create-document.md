# Creating a Document

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesCreateaDocument.html`

## Overview

Create a new document (WTDocument) in Windchill using the PTC Document Management domain. This operation uses an HTTP POST request to the Documents entity set.

## Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/DocMgmt/Documents
```

- **Domain**: DocMgmt (PTC Document Management)
- **Entity Set**: `Documents`
- **HTTP Method**: POST
- **Mapped Windchill Type**: `wt.doc.WTDocument`

## Request

### Headers

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `Accept` | `application/json` |
| `CSRF_NONCE` | `<nonce_value>` |

### Request Body

```json
{
  "Number": "DOC-000001",
  "Name": "Design Specification",
  "Description": "Main design specification for the project",
  "TypeID": "wt.doc.WTDocument",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:12345",
  "FolderPath": "/Default/Documents",
  "Department": "Engineering",
  "DocType": "Document"
}
```

### Request Body Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `Number` | String | No | Document number. If omitted, Windchill auto-generates one. |
| `Name` | String | Yes | Display name of the document |
| `Description` | String | No | Description of the document |
| `TypeID` | String | No | Windchill type identifier. Defaults to `wt.doc.WTDocument`. Use soft type internal names for subtypes. |
| `ContainerID` | String | No | Object reference of the target product/library container. If omitted, uses the user's default container. |
| `FolderPath` | String | No | Folder path within the container. Must start with `/Default`. |
| `Department` | String | No | Department that owns the document |
| `DocType` | String | No | Document type classification |

### Example Request

```http
POST /Windchill/servlet/odata/DocMgmt/Documents HTTP/1.1
Host: windchill.ptc.com
Content-Type: application/json
Accept: application/json
CSRF_NONCE: <nonce_value>

{
  "Number": "DOC-000001",
  "Name": "Design Specification",
  "Description": "Main design specification for the project",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:12345",
  "FolderPath": "/Default/Documents"
}
```

## Response

### HTTP Status

- **201 Created** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/DocMgmt/$metadata#Documents/$entity",
  "ID": "OR:wt.doc.WTDocument:234567",
  "Number": "DOC-000001",
  "Name": "Design Specification",
  "Description": "Main design specification for the project",
  "State": "In Work",
  "Version": "A",
  "Iteration": "1",
  "VersionID": "A.1",
  "LatestIteration": true,
  "CheckoutState": "Checked In",
  "HasContents": false,
  "Department": "Engineering",
  "DocType": "Document",
  "TypeID": "wt.doc.WTDocument",
  "CreatedOn": "2024-01-15T10:30:00Z",
  "LastModified": "2024-01-15T10:30:00Z"
}
```

### Key Response Properties

| Property | Type | Description |
|----------|------|-------------|
| `ID` | String | Object reference identifier (`OR:wt.doc.WTDocument:<dbid>`) |
| `Number` | String | Document number |
| `Name` | String | Display name |
| `State` | String | Life cycle state (e.g., `In Work`, `Released`) |
| `Version` | String | Version letter (e.g., `A`, `B`) |
| `Iteration` | String | Iteration number within the version |
| `VersionID` | String | Combined version and iteration (e.g., `A.1`) |
| `LatestIteration` | Boolean | Whether this is the latest iteration |
| `CheckoutState` | String | Checkout status |
| `HasContents` | Boolean | Whether the document has file content attached |
| `CreatedOn` | DateTimeOffset | Creation timestamp |
| `LastModified` | DateTimeOffset | Last modification timestamp |

## Complete Workflow: Create Document with Content

1. **Fetch NONCE**:
   ```
   GET /Windchill/servlet/odata/PTC/GetCSRFToken()
   ```

2. **Create document**:
   ```
   POST /Windchill/servlet/odata/DocMgmt/Documents
   ```

3. **Check out document**:
   ```
   POST /Windchill/servlet/odata/DocMgmt/Documents('<doc_id>')/PTC.DocMgmt.CheckOut
   ```

4. **Upload content** to the working copy:
   ```
   POST /Windchill/servlet/odata/DocMgmt/Documents('<working_copy_id>')/PTC.DocMgmt.UploadContent
   ```
   See [example-upload-content.md](example-upload-content.md) for upload details.

5. **Check in document**:
   ```
   POST /Windchill/servlet/odata/DocMgmt/Documents('<working_copy_id>')/PTC.DocMgmt.CheckIn
   ```

## Creating a Document in a Different Organization

To create a document in a different organization, include the `OrganizationID` property:

```json
{
  "Name": "Cross-Org Document",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:99999",
  "OrganizationID": "OR:wt.org.WTOrganization:54321"
}
```

## Notes

- The newly created document starts in the `In Work` life cycle state.
- The document is created at version `A`, iteration `1`.
- Documents are created without file content. Use the upload workflow to attach files.
- The `ContainerID` must reference a container that the user has access to.
- If `FolderPath` is specified, the folder must already exist within the container.
- Auto-numbering is applied if `Number` is not provided.

## Common Errors

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | Missing required fields or invalid property values |
| `403 Forbidden` | User does not have permission to create documents in the specified container |
| `404 Not Found` | The specified container or folder does not exist |
| `409 Conflict` | A document with the specified number already exists |
