# Revising Multiple Parts

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesRevisingMultipleParts.html`

## Overview

Revise multiple parts in a single operation using the `Revise` action in the PTC Product Management domain. Revising a part creates a new version (e.g., from version A to version B) while preserving the previous version in the system.

## Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Revise
```

- **Domain**: ProdMgmt (PTC Product Management)
- **Action**: `Revise` (unbound action)
- **HTTP Method**: POST

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
  "Objects": [
    {
      "ID": "OR:wt.part.WTPart:123456",
      "Number": "0000000123"
    },
    {
      "ID": "OR:wt.part.WTPart:123789",
      "Number": "0000000456"
    }
  ]
}
```

### Request Body Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `Objects` | Array | Yes | Array of part references to revise |
| `Objects[].ID` | String | Yes | Object reference of the part to revise (e.g., `OR:wt.part.WTPart:<dbid>`) |
| `Objects[].Number` | String | No | Part number (for reference) |

### Example Request

```http
POST /Windchill/servlet/odata/ProdMgmt/Revise HTTP/1.1
Host: windchill.ptc.com
Content-Type: application/json
Accept: application/json
CSRF_NONCE: <nonce_value>

{
  "Objects": [
    {
      "ID": "OR:wt.part.WTPart:123456"
    },
    {
      "ID": "OR:wt.part.WTPart:123789"
    }
  ]
}
```

## Response

### HTTP Status

- **200 OK** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/$metadata#Parts",
  "value": [
    {
      "ID": "OR:wt.part.WTPart:124000",
      "Number": "0000000123",
      "Name": "Test Part",
      "State": "In Work",
      "Version": "B",
      "Iteration": "1",
      "VersionID": "B.1",
      "LatestIteration": true,
      "CheckoutState": "Checked In"
    },
    {
      "ID": "OR:wt.part.WTPart:124001",
      "Number": "0000000456",
      "Name": "Another Part",
      "State": "In Work",
      "Version": "B",
      "Iteration": "1",
      "VersionID": "B.1",
      "LatestIteration": true,
      "CheckoutState": "Checked In"
    }
  ]
}
```

## Notes

- The response returns the newly created revised parts with new IDs and incremented version letters.
- The original versions remain in the system and are not modified.
- Revised parts start at iteration `1` of the new version (e.g., `B.1`).
- Revised parts inherit the BOM structure, attributes, and content from the source version.
- Parts must be in `Checked In` state to be revised.
- Parts typically need to be in a `Released` or equivalent life cycle state to be revised, depending on the configured revision rules.
- The revision scheme (A, B, C, ...) is determined by the Windchill server configuration.
- All parts in the request are revised within a single transaction. If any part fails, none are revised.
- The newly revised parts start in the `In Work` life cycle state.

## Revising a Single Part

For revising a single part, you can use the bound action on a specific part:

```
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123456')/PTC.ProdMgmt.Revise
```

## Common Errors

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | One or more parts cannot be revised (e.g., not in the correct state, already checked out) |
| `403 Forbidden` | The user does not have permission to revise one or more parts |
| `404 Not Found` | One or more specified part IDs do not exist |
