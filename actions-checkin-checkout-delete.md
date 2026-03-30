# Actions Available for Single and Multiple Objects

> Source: PTC Windchill REST Services 1.6 Documentation
> Page: `wccg_restapisaccess_checkin_checkout_undocheckout_delete_operations.html`

## Overview

Windchill REST Services provides actions that can be performed on single or multiple objects. These actions include Check-In, Check-Out, Undo Check-Out, Revise, and Delete operations. These actions are available across multiple domains including PTC Product Management and PTC Document Management.

## Actions on Single Objects

### Check-Out (Single Object)

Checks out a single object. The check-out action creates a working copy of the object.

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.CheckOut
POST /DocMgmt/Documents('<oid>')/PTC.DocMgmt.CheckOut
```

**Request Headers:**
| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `CSRF_NONCE` | `<nonce_token>` |

**Request Body:** Empty JSON object `{}`

**Response:** Returns the checked-out working copy of the object.

### Check-In (Single Object)

Checks in a single object. The check-in action creates a new iteration of the object.

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.CheckIn
POST /DocMgmt/Documents('<oid>')/PTC.DocMgmt.CheckIn
```

**Request Headers:**
| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `CSRF_NONCE` | `<nonce_token>` |

**Request Body (optional):**
```json
{
  "Comment": "Check-in comment"
}
```

### Undo Check-Out (Single Object)

Reverts the check-out operation and discards any changes made to the working copy.

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.UndoCheckOut
POST /DocMgmt/Documents('<oid>')/PTC.DocMgmt.UndoCheckOut
```

**Request Body:** Empty JSON object `{}`

### Revise (Single Object)

Creates a new version (revision) of the object.

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.Revise
POST /DocMgmt/Documents('<oid>')/PTC.DocMgmt.Revise
```

**Request Body:** Empty JSON object `{}`

**Response:** Returns the new revision of the object.

### Delete (Single Object)

Deletes a single object.

**HTTP Method:** `DELETE`

**URL Pattern:**
```
DELETE /ProdMgmt/Parts('<oid>')
DELETE /DocMgmt/Documents('<oid>')
```

**Request Headers:**
| Header | Value |
|--------|-------|
| `CSRF_NONCE` | `<nonce_token>` |

## Actions on Multiple Objects

These actions allow performing operations on multiple objects in a single request.

### Check-Out (Multiple Objects)

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/CheckOut
POST /DocMgmt/CheckOut
```

**Request Body:**
```json
{
  "Objects": [
    {
      "oid": "OR:wt.part.WTPart:108618"
    },
    {
      "oid": "OR:wt.part.WTPart:108620"
    }
  ]
}
```

### Check-In (Multiple Objects)

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/CheckIn
POST /DocMgmt/CheckIn
```

**Request Body:**
```json
{
  "Objects": [
    {
      "oid": "OR:wt.part.WTPart:108618",
      "Comment": "Check-in comment for part 1"
    },
    {
      "oid": "OR:wt.part.WTPart:108620",
      "Comment": "Check-in comment for part 2"
    }
  ]
}
```

### Undo Check-Out (Multiple Objects)

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/UndoCheckOut
POST /DocMgmt/UndoCheckOut
```

**Request Body:**
```json
{
  "Objects": [
    {
      "oid": "OR:wt.part.WTPart:108618"
    },
    {
      "oid": "OR:wt.part.WTPart:108620"
    }
  ]
}
```

### Revise (Multiple Objects)

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/Revise
POST /DocMgmt/Revise
```

**Request Body:**
```json
{
  "Objects": [
    {
      "oid": "OR:wt.part.WTPart:108618"
    },
    {
      "oid": "OR:wt.part.WTPart:108620"
    }
  ]
}
```

### Delete (Multiple Objects)

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/Delete
POST /DocMgmt/Delete
```

**Request Body:**
```json
{
  "Objects": [
    {
      "oid": "OR:wt.part.WTPart:108618"
    },
    {
      "oid": "OR:wt.part.WTPart:108620"
    }
  ]
}
```

## CSRF Nonce Requirement

All write operations (POST, PATCH, DELETE) require a CSRF nonce token. Obtain the nonce token first using:

```
GET /servlet/odata/PTC/GetCSRFToken()
```

Include the token in the request header:
```
CSRF_NONCE: <token_value>
```

## Important Notes

- Check-Out creates a working copy. The OID of the working copy is different from the original object.
- Check-In must be performed on the working copy (checked-out object), not the original.
- Undo Check-Out discards the working copy and reverts to the original iteration.
- Revise creates a new version (e.g., A.1 -> B.1). The new revision has a new OID.
- Delete operations are permanent and cannot be undone.
- For multiple object operations, the response includes the status for each object individually.
- If any object in a multiple-object action fails, the other objects may still succeed (non-atomic by default).
