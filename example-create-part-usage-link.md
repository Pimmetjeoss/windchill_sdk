# Creating a Part Usage Link (BOM Entry)

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesCreatePartUse.html`

## Overview

Create a part usage link (WTPartUsageLink) to add a child part to a parent part's Bill of Materials (BOM). This establishes a "uses" relationship between a parent assembly and a child component.

The parent part must be checked out before adding usage links to its BOM.

## Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Parts('<parent_part_working_copy_id>')/Uses
```

- **Domain**: ProdMgmt (PTC Product Management)
- **Entity Set**: `Parts`
- **Navigation Property**: `Uses`
- **HTTP Method**: POST
- **Mapped Windchill Type**: `wt.part.WTPartUsageLink`

## Prerequisites

1. The **parent part** must be checked out. Use the working copy ID.
2. The **child part** must already exist in Windchill.
3. A valid NONCE token is required.

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
  "Uses": {
    "ID": "OR:wt.part.WTPartMaster:567890"
  },
  "Quantity": 2.0,
  "Unit": "ea",
  "LineNumber": 10,
  "TraceCode": "Untraced",
  "FindNumber": "1"
}
```

### Request Body Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `Uses.ID` | String | Yes | Object reference of the **child part master** (WTPartMaster, not WTPart). Format: `OR:wt.part.WTPartMaster:<dbid>` |
| `Quantity` | Decimal | No | Quantity of the child part. Defaults to `1.0` |
| `Unit` | String | No | Unit of measure for the quantity (e.g., `ea`, `kg`) |
| `LineNumber` | Int32 | No | Line number in the BOM. Auto-assigned if omitted. |
| `TraceCode` | String | No | Traceability code: `Untraced`, `Lot Trace`, or `Serial Trace`. Defaults to `Untraced`. |
| `FindNumber` | String | No | Find number for the BOM line |
| `ReferenceDesignator` | String | No | Reference designator string |

### Example Request

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123457')/Uses HTTP/1.1
Host: windchill.ptc.com
Content-Type: application/json
Accept: application/json
CSRF_NONCE: <nonce_value>

{
  "Uses": {
    "ID": "OR:wt.part.WTPartMaster:567890"
  },
  "Quantity": 2.0,
  "Unit": "ea",
  "LineNumber": 10,
  "TraceCode": "Untraced"
}
```

## Response

### HTTP Status

- **201 Created** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/$metadata#PartUsageLinks/$entity",
  "ID": "OR:wt.part.WTPartUsageLink:200003",
  "Quantity": 2.0,
  "Unit": "ea",
  "LineNumber": 10,
  "ReferenceDesignator": "",
  "TraceCode": "Untraced",
  "FindNumber": "1",
  "Uses@odata.navigationLink": "PartUsageLinks('OR:wt.part.WTPartUsageLink:200003')/Uses",
  "UsedBy@odata.navigationLink": "PartUsageLinks('OR:wt.part.WTPartUsageLink:200003')/UsedBy"
}
```

## Complete Workflow: Add Component to BOM

1. **Fetch NONCE**:
   ```
   GET /Windchill/servlet/odata/PTC/GetCSRFToken()
   ```

2. **Check out parent part**:
   ```
   POST /Windchill/servlet/odata/ProdMgmt/Parts('<parent_id>')/PTC.ProdMgmt.CheckOut
   ```

3. **Create usage link** on the working copy:
   ```
   POST /Windchill/servlet/odata/ProdMgmt/Parts('<working_copy_id>')/Uses
   ```

4. **Check in parent part**:
   ```
   POST /Windchill/servlet/odata/ProdMgmt/Parts('<working_copy_id>')/PTC.ProdMgmt.CheckIn
   ```

## Deleting a Part Usage Link

To remove a component from the BOM, use DELETE on the usage link:

```
DELETE /Windchill/servlet/odata/ProdMgmt/PartUsageLinks('OR:wt.part.WTPartUsageLink:200003')
```

The parent part must be checked out before deleting usage links.

## Notes

- The `Uses.ID` must reference a **WTPartMaster** (not WTPart). The part master is the version-independent identity of the part.
- The parent part must be checked out, and you must use the **working copy ID** in the URL.
- You can add multiple usage links (components) to the same parent part while it is checked out.
- After adding all desired components, check in the parent part to finalize the BOM changes.
- Duplicate components (same child part master) are allowed with different line numbers.
- Line numbers are typically assigned in increments of 10 (10, 20, 30, etc.).

## Common Errors

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | Parent part is not checked out, or the child part master does not exist |
| `403 Forbidden` | The user does not have permission to modify the BOM |
| `404 Not Found` | The parent part ID or child part master ID does not exist |
