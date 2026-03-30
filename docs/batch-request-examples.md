# Windchill REST Services - Batch Request Examples

## Overview

Windchill REST Services supports OData batch requests via the `$batch` endpoint. Batch requests allow multiple operations to be sent in a single HTTP request using `multipart/mixed` content type. Batch requests support:

- **Simple batch**: Multiple independent operations grouped together
- **Changesets**: Atomic groups of operations that succeed or fail together
- **Cross-references**: Operations within a changeset can reference results of earlier operations using `Content-ID`

## Batch Endpoint

```
POST /Windchill/servlet/odata/ProdMgmt/$batch
Content-Type: multipart/mixed; boundary=batch_boundary
CSRF_NONCE: <nonce_value>
```

## Simple Batch: Creating Multiple Parts with Changesets

This example creates two parts within a single atomic changeset. If either creation fails, both are rolled back.

```http
POST /Windchill/servlet/odata/ProdMgmt/$batch HTTP/1.1
Host: windchill.example.com
Content-Type: multipart/mixed; boundary=batch_36522ad7
CSRF_NONCE: abc123

--batch_36522ad7
Content-Type: multipart/mixed; boundary=changeset_77162fcd

--changeset_77162fcd
Content-Type: application/http
Content-Transfer-Encoding: binary

POST Parts HTTP/1.1
Content-Type: application/json
Content-ID: 1

{
  "Number": "BRK-001",
  "Name": "Bracket A",
  "Source": "MAKE",
  "DefaultUnit": "EA",
  "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:12345')",
  "Folder@odata.bind": "Folders('OR:wt.folder.SubFolder:67890')"
}

--changeset_77162fcd
Content-Type: application/http
Content-Transfer-Encoding: binary

POST Parts HTTP/1.1
Content-Type: application/json
Content-ID: 2

{
  "Number": "BRK-002",
  "Name": "Bracket B",
  "Source": "MAKE",
  "DefaultUnit": "EA",
  "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:12345')",
  "Folder@odata.bind": "Folders('OR:wt.folder.SubFolder:67890')"
}

--changeset_77162fcd--
--batch_36522ad7--
```

### Response

```http
HTTP/1.1 200 OK
Content-Type: multipart/mixed; boundary=batchresponse_abc123

--batchresponse_abc123
Content-Type: multipart/mixed; boundary=changesetresponse_def456

--changesetresponse_def456
Content-Type: application/http
Content-Transfer-Encoding: binary

HTTP/1.1 201 Created
Content-Type: application/json
Content-ID: 1

{
  "@odata.context": "$metadata#Parts/$entity",
  "ID": "OR:wt.part.WTPart:111111",
  "Number": "BRK-001",
  "Name": "Bracket A"
}

--changesetresponse_def456
Content-Type: application/http
Content-Transfer-Encoding: binary

HTTP/1.1 201 Created
Content-Type: application/json
Content-ID: 2

{
  "@odata.context": "$metadata#Parts/$entity",
  "ID": "OR:wt.part.WTPart:222222",
  "Number": "BRK-002",
  "Name": "Bracket B"
}

--changesetresponse_def456--
--batchresponse_abc123--
```

## Advanced Batch: Cross-References with Content-ID

This example demonstrates a complex workflow where operations reference results of previous operations using `$<Content-ID>` syntax. The workflow:

1. Create a PARENT part (`Content-ID: 1_1`)
2. Create a CHILD part (`Content-ID: 2_1`)
3. Check out the PARENT part (`Content-ID: 3_1`, referencing `$1_1`)
4. Create a BOM link from the checked-out PARENT to the CHILD (`Content-ID: 4_1`, referencing `$3_1` and binding `$2_1`)
5. Check in the PARENT part (referencing `$3_1`)

```http
POST /Windchill/servlet/odata/ProdMgmt/$batch HTTP/1.1
Host: windchill.example.com
Content-Type: multipart/mixed; boundary=batch_abc123
CSRF_NONCE: xyz789

--batch_abc123
Content-Type: multipart/mixed; boundary=changeset_def456

--changeset_def456
Content-Type: application/http
Content-Transfer-Encoding: binary

POST Parts HTTP/1.1
Content-Type: application/json
Content-ID: 1_1

{
  "Number": "PARENT-001",
  "Name": "Parent Assembly",
  "Source": "MAKE",
  "DefaultUnit": "EA",
  "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:12345')",
  "Folder@odata.bind": "Folders('OR:wt.folder.SubFolder:67890')"
}

--changeset_def456
Content-Type: application/http
Content-Transfer-Encoding: binary

POST Parts HTTP/1.1
Content-Type: application/json
Content-ID: 2_1

{
  "Number": "CHILD-001",
  "Name": "Child Component",
  "Source": "BUY",
  "DefaultUnit": "EA",
  "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:12345')",
  "Folder@odata.bind": "Folders('OR:wt.folder.SubFolder:67890')"
}

--changeset_def456
Content-Type: application/http
Content-Transfer-Encoding: binary

POST $1_1/PTC.ProdMgmt.CheckOut HTTP/1.1
Content-Type: application/json
Content-ID: 3_1

{}

--changeset_def456
Content-Type: application/http
Content-Transfer-Encoding: binary

POST $3_1/Uses HTTP/1.1
Content-Type: application/json
Content-ID: 4_1

{
  "Quantity": 2,
  "Unit": "EA",
  "LineNumber": 10,
  "FindNumber": "1",
  "UsedBy@odata.bind": "$2_1"
}

--changeset_def456
Content-Type: application/http
Content-Transfer-Encoding: binary

POST $3_1/PTC.ProdMgmt.CheckIn HTTP/1.1
Content-Type: application/json
Content-ID: 5_1

{
  "Comment": "Created BOM structure with child component"
}

--changeset_def456--
--batch_abc123--
```

### How Content-ID Cross-References Work

| Reference | Resolves To |
|---|---|
| `$1_1` | The URI of the entity created by the operation with `Content-ID: 1_1` (the PARENT part) |
| `$2_1` | The URI of the entity created by the operation with `Content-ID: 2_1` (the CHILD part) |
| `$3_1` | The URI of the entity returned by the operation with `Content-ID: 3_1` (the checked-out working copy of PARENT) |

Cross-references can be used in:
- **URL path**: `POST $1_1/PTC.ProdMgmt.CheckOut` -- invoke action on previously created entity
- **URL path for navigation**: `POST $3_1/Uses` -- create a child entity on a previously returned entity
- **Binding references**: `"UsedBy@odata.bind": "$2_1"` -- bind to a previously created entity

### Important Rules

1. **Content-ID scope**: Content-IDs are scoped to a changeset. They cannot be referenced across changesets.
2. **Order matters**: Operations within a changeset are processed in order. A reference can only point to a Content-ID from a preceding operation.
3. **Atomicity**: All operations in a changeset succeed or fail together. If the BOM creation fails, the part creations and checkout are also rolled back.
4. **Content-ID format**: Use alphanumeric identifiers. The `N_M` naming convention (e.g., `1_1`, `2_1`) is recommended but not required.

## Batch with GET Requests Outside Changesets

GET requests cannot be inside changesets (they are not state-changing). Place them outside:

```http
POST /Windchill/servlet/odata/ProdMgmt/$batch HTTP/1.1
Content-Type: multipart/mixed; boundary=batch_getexample
CSRF_NONCE: abc123

--batch_getexample
Content-Type: application/http
Content-Transfer-Encoding: binary

GET Parts?$filter=Number eq 'BRK-001'&$select=ID,Name,Number HTTP/1.1
Accept: application/json

--batch_getexample
Content-Type: application/http
Content-Transfer-Encoding: binary

GET Parts?$filter=Number eq 'BRK-002'&$select=ID,Name,Number HTTP/1.1
Accept: application/json

--batch_getexample--
```

## Notes

- Always include the `CSRF_NONCE` header for batch requests containing write operations.
- The batch endpoint path is `{domain_base_url}/$batch`.
- Maximum batch size may be limited by server configuration.
- Use changesets for atomic operations; use bare batch (without changeset) for independent read queries.
- Failed changesets return error details in the batch response for the failing operation.
