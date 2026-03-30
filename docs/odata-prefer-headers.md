# OData Prefer Headers

## Overview

Windchill REST Services supports the OData `Prefer` HTTP header, which allows clients to request specific server behaviors. The `Prefer` header is included in the request, and the server acknowledges applied preferences via the `Preference-Applied` response header.

## Supported Prefer Headers

### return=representation

Requests that the server return the full entity representation in the response body after a create (POST) or update (PATCH) operation. This is the default behavior.

**Request:**
```http
PATCH /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')
Content-Type: application/json
Prefer: return=representation
CSRF_NONCE: <token>

{
  "Name": "Updated Part Name"
}
```

**Response:** Returns the full updated entity in the response body with status `200 OK`.

---

### return=minimal

Requests that the server return a minimal response (no body) after a create or update operation. This reduces bandwidth and improves performance when the client does not need the response entity.

**Request:**
```http
PATCH /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')
Content-Type: application/json
Prefer: return=minimal
CSRF_NONCE: <token>

{
  "Name": "Updated Part Name"
}
```

**Response:** Returns status `204 No Content` with an `OData-EntityId` header containing the entity URL.

**Response Headers:**
```
HTTP/1.1 204 No Content
Preference-Applied: return=minimal
OData-EntityId: https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')
```

---

### odata.maxpagesize

Requests that the server limit the number of items per page in the response. This controls server-side paging.

**Request:**
```http
GET /Windchill/servlet/odata/ProdMgmt/Parts
Prefer: odata.maxpagesize=50
```

**Response:** Returns at most 50 items. If more items are available, the response includes an `@odata.nextLink` for the next page.

**Response Headers:**
```
Preference-Applied: odata.maxpagesize=50
```

**Example Response:**
```json
{
  "@odata.context": "$metadata#Parts",
  "value": [ ... ],
  "@odata.nextLink": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/Parts?$skiptoken=50"
}
```

**Notes:**
- The server may return fewer items than requested if the actual page size limit is smaller.
- The server acknowledges the applied page size in the `Preference-Applied` header.
- The `@odata.nextLink` URL should be followed to get subsequent pages.

---

### odata.track-changes

Requests delta tracking for change tracking scenarios.

**Request:**
```http
GET /Windchill/servlet/odata/ProdMgmt/Parts
Prefer: odata.track-changes
```

> Note: Support for delta tracking may be limited. Check domain-specific documentation.

---

## Combining Prefer Headers

Multiple preferences can be combined in a single `Prefer` header, separated by commas:

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts
Content-Type: application/json
Prefer: return=representation,odata.maxpagesize=25
CSRF_NONCE: <token>

{ ... }
```

---

## Preference-Applied Response Header

The server indicates which preferences were applied via the `Preference-Applied` response header:

```
Preference-Applied: return=representation
```

If a requested preference is not supported or cannot be honored, it will not appear in the `Preference-Applied` header. The client should check this header to confirm which preferences were applied.

---

## Usage Summary

| Prefer Value | Use Case | Applicable Methods |
|-------------|----------|-------------------|
| `return=representation` | Get full entity back after write | POST, PATCH |
| `return=minimal` | Minimize response payload on writes | POST, PATCH |
| `odata.maxpagesize=N` | Control server paging size | GET |
| `odata.track-changes` | Delta tracking | GET |

---

## Best Practices

1. **Use `return=minimal` for bulk operations** to reduce response sizes and improve throughput.
2. **Use `odata.maxpagesize`** to control page sizes when dealing with large entity sets.
3. **Always check `Preference-Applied`** to confirm the server honored your preference.
4. **Default behavior:** If no `Prefer` header is specified, the server uses `return=representation` for POST/PATCH and its default page size for GET.
