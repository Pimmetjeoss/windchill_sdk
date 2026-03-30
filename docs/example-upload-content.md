# Uploading Content to a Document

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesUploadContent.html`

## Overview

Upload file content (primary or secondary) to a Windchill document (WTDocument). This is a multi-step process: the document must first be checked out, then content is uploaded to the working copy, and finally the document is checked back in.

Content upload uses a multipart/form-data POST request to attach files to the document's ContentHolder.

## Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/DocMgmt/Documents('<working_copy_id>')/PTC.DocMgmt.UploadContent
```

- **Domain**: DocMgmt (PTC Document Management)
- **Entity Set**: `Documents`
- **Action**: `PTC.DocMgmt.UploadContent` (bound action)
- **HTTP Method**: POST

## Prerequisites

1. The document must be **checked out** before uploading content.
2. A valid NONCE token is required.
3. Use the **working copy ID** (returned from the checkout operation).

## Request

### Headers

| Header | Value |
|--------|-------|
| `Content-Type` | `multipart/form-data; boundary=<boundary>` |
| `Accept` | `application/json` |
| `CSRF_NONCE` | `<nonce_value>` |

### Multipart Request Body

The request body uses `multipart/form-data` encoding with the following parts:

#### Part 1: Content Metadata (JSON)

```
--boundary
Content-Disposition: form-data; name="ContentMetaData"
Content-Type: application/json

{
  "ContentRole": "PRIMARY",
  "ContentDescription": "Main design document",
  "FileName": "design-spec.pdf"
}
```

#### Part 2: File Content (Binary)

```
--boundary
Content-Disposition: form-data; name="FileContent"; filename="design-spec.pdf"
Content-Type: application/pdf

<binary file content>
--boundary--
```

### Content Metadata Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `ContentRole` | String | Yes | Role of the content: `PRIMARY` or `SECONDARY` |
| `ContentDescription` | String | No | Description of the content being uploaded |
| `FileName` | String | Yes | Name of the file being uploaded |

### Example Full Request

```http
POST /Windchill/servlet/odata/DocMgmt/Documents('OR:wt.doc.WTDocument:234568')/PTC.DocMgmt.UploadContent HTTP/1.1
Host: windchill.ptc.com
Accept: application/json
CSRF_NONCE: <nonce_value>
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="ContentMetaData"
Content-Type: application/json

{
  "ContentRole": "PRIMARY",
  "FileName": "design-spec.pdf"
}
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="FileContent"; filename="design-spec.pdf"
Content-Type: application/pdf

<binary file content>
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

## Response

### HTTP Status

- **200 OK** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/DocMgmt/$metadata#Documents/$entity",
  "ID": "OR:wt.doc.WTDocument:234568",
  "Number": "DOC-000001",
  "Name": "Design Specification",
  "State": "In Work",
  "CheckoutState": "Checked Out",
  "HasContents": true
}
```

## Complete Upload Workflow

1. **Check out** the document:
   ```
   POST .../DocMgmt/Documents('<doc_id>')/PTC.DocMgmt.CheckOut
   ```

2. **Upload content** to the working copy:
   ```
   POST .../DocMgmt/Documents('<working_copy_id>')/PTC.DocMgmt.UploadContent
   ```

3. **Check in** the document:
   ```
   POST .../DocMgmt/Documents('<working_copy_id>')/PTC.DocMgmt.CheckIn
   ```

## Notes

- The document must be checked out before uploading content.
- Use the working copy ID, not the original document ID.
- Each document can have one PRIMARY content and multiple SECONDARY contents.
- Uploading PRIMARY content replaces any existing primary content.
- The maximum file size is governed by the Windchill server configuration.
- After uploading, you must check in the document for the content to be visible to other users.
- Supported content types depend on the Windchill server configuration.
- For large files, ensure appropriate timeout settings on both the client and server.

## Common Errors

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | Missing required fields or the document is not checked out |
| `403 Forbidden` | The user does not have permission to modify the document |
| `404 Not Found` | The specified document ID does not exist |
| `413 Payload Too Large` | The uploaded file exceeds the maximum allowed size |
