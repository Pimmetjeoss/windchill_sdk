# Checking Out a Part

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesCheckoutaPart.html`

## Overview

Check out a part (WTPart) from Windchill to lock it for editing. Checking out an object creates a working copy that only the checkout user can modify. Other users can still view the original checked-in version.

## Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Parts('<part_id>')/PTC.ProdMgmt.CheckOut
```

- **Domain**: ProdMgmt (PTC Product Management)
- **Entity Set**: `Parts`
- **Action**: `PTC.ProdMgmt.CheckOut` (bound action)
- **HTTP Method**: POST

## Request

### Headers

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `Accept` | `application/json` |
| `CSRF_NONCE` | `<nonce_value>` |

### URL Parameters

| Parameter | Description |
|-----------|-------------|
| `<part_id>` | The ID (object reference) of the part to check out, e.g., `OR:wt.part.WTPart:123456` |

### Example Request

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123456')/PTC.ProdMgmt.CheckOut HTTP/1.1
Host: windchill.ptc.com
Content-Type: application/json
Accept: application/json
CSRF_NONCE: <nonce_value>
```

The request body is empty for checkout operations.

## Response

### HTTP Status

- **200 OK** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/$metadata#Parts/$entity",
  "ID": "OR:wt.part.WTPart:123457",
  "Number": "0000000123",
  "Name": "Test Part",
  "Description": "A test part created via REST API",
  "State": "In Work",
  "Version": "A",
  "Iteration": "2",
  "VersionID": "A.2",
  "LatestIteration": true,
  "CheckoutState": "Checked Out",
  "DefaultUnit": "ea",
  "Source": "Make",
  "View": "Design",
  "CreatedOn": "2024-01-15T10:30:00Z",
  "LastModified": "2024-01-15T11:00:00Z",
  "TypeID": "wt.part.WTPart"
}
```

### Key Response Properties

| Property | Type | Description |
|----------|------|-------------|
| `ID` | String | The object reference of the **working copy** (checked-out copy). Note: this ID differs from the original. |
| `CheckoutState` | String | Will be `Checked Out` after a successful checkout |
| `Iteration` | String | The working copy may have a new iteration number |

## Notes

- The response returns the **working copy** of the part. The working copy has a different `ID` than the original part.
- The working copy is the editable version. Use its `ID` for subsequent update (PATCH) operations.
- Only one user can check out a part at a time.
- A part must be in `Checked In` state to be checked out.
- After checkout, modify the working copy using PATCH, then check it in to save changes.
- If the part is already checked out by another user, the server returns an error.

## Common Errors

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | The part is already checked out |
| `403 Forbidden` | The user does not have permission to check out the part |
| `404 Not Found` | The specified part ID does not exist |
