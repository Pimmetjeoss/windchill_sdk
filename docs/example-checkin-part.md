# Checking In a Part

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesCheckinaPart.html`

## Overview

Check in a previously checked-out part (WTPart) to save your changes and release the lock. The checkin operation acts on the **working copy** (the checked-out copy) of the part.

## Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Parts('<working_copy_id>')/PTC.ProdMgmt.CheckIn
```

- **Domain**: ProdMgmt (PTC Product Management)
- **Entity Set**: `Parts`
- **Action**: `PTC.ProdMgmt.CheckIn` (bound action)
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
| `<working_copy_id>` | The ID of the **working copy** (checked-out copy) of the part, e.g., `OR:wt.part.WTPart:123457` |

### Example Request

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123457')/PTC.ProdMgmt.CheckIn HTTP/1.1
Host: windchill.ptc.com
Content-Type: application/json
Accept: application/json
CSRF_NONCE: <nonce_value>
```

The request body is empty for checkin operations.

## Response

### HTTP Status

- **200 OK** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/$metadata#Parts/$entity",
  "ID": "OR:wt.part.WTPart:123456",
  "Number": "0000000123",
  "Name": "Test Part",
  "Description": "A test part created via REST API",
  "State": "In Work",
  "Version": "A",
  "Iteration": "2",
  "VersionID": "A.2",
  "LatestIteration": true,
  "CheckoutState": "Checked In",
  "DefaultUnit": "ea",
  "Source": "Make",
  "View": "Design",
  "CreatedOn": "2024-01-15T10:30:00Z",
  "LastModified": "2024-01-15T11:30:00Z",
  "TypeID": "wt.part.WTPart"
}
```

### Key Response Properties

| Property | Type | Description |
|----------|------|-------------|
| `ID` | String | The object reference of the original (checked-in) part. Note: this reverts to the original part's ID. |
| `CheckoutState` | String | Will be `Checked In` after a successful checkin |
| `Iteration` | String | The iteration number is incremented after checkin |

## Typical Checkout-Edit-Checkin Flow

1. **Check out** the part to get a working copy:
   ```
   POST .../Parts('<original_id>')/PTC.ProdMgmt.CheckOut
   ```
2. **Update** the working copy with desired changes:
   ```
   PATCH .../Parts('<working_copy_id>')
   ```
3. **Check in** the working copy:
   ```
   POST .../Parts('<working_copy_id>')/PTC.ProdMgmt.CheckIn
   ```

## Notes

- You must use the **working copy ID** (returned by the checkout operation) for the checkin, not the original part ID.
- The response returns the checked-in part with its original ID.
- The iteration number is incremented after a successful checkin.
- Only the user who checked out the part can check it in.
- Any changes made to the working copy via PATCH are preserved after checkin.

## Undo Checkout

To cancel a checkout without saving changes, use the `UndoCheckOut` action instead:

```
POST https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Parts('<working_copy_id>')/PTC.ProdMgmt.UndoCheckOut
```

This discards the working copy and reverts to the previous iteration.

## Common Errors

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | The part is not checked out, or the ID is not a working copy |
| `403 Forbidden` | The user does not have permission to check in the part |
| `404 Not Found` | The specified part ID does not exist |
