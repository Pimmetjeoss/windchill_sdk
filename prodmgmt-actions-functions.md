# Actions and Functions Available in the PTC Product Management Domain

> Source: PTC Windchill REST Services 1.6 Documentation
> Pages: `wccg_restapisaccess_PTCProdMgmtDomainsfunctions.html`, `prodmgmtdomain_functions.html`

## Overview

The PTC Product Management domain (`ProdMgmt`) provides actions and functions for managing parts, BOMs, and related product data. Actions perform operations that modify data (POST), while functions retrieve data without side effects (GET).

**Base URL:** `/servlet/odata/ProdMgmt`

## Actions Available in the PTC Product Management Domain

Actions are invoked using the HTTP POST method and may require a CSRF nonce token.

### CheckOut

Checks out a part to create a working copy.

**Bound to:** `Part` entity

**URL:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.CheckOut
```

**Request Body:** `{}`

### CheckIn

Checks in a working copy of a part.

**Bound to:** `Part` entity

**URL:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.CheckIn
```

**Request Body:**
```json
{
  "Comment": "Check-in comment"
}
```

### UndoCheckOut

Reverts the check-out of a part and discards the working copy.

**Bound to:** `Part` entity

**URL:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.UndoCheckOut
```

**Request Body:** `{}`

### Revise

Creates a new revision of a part.

**Bound to:** `Part` entity

**URL:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.Revise
```

**Request Body:** `{}`

### SetLifeCycleState

Sets the life cycle state of a part.

**Bound to:** `Part` entity

**URL:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.SetLifeCycleState
```

**Request Body:**
```json
{
  "State": "INWORK"
}
```

### CheckOut (Multiple Objects)

Checks out multiple parts simultaneously.

**Unbound action**

**URL:**
```
POST /ProdMgmt/CheckOut
```

**Request Body:**
```json
{
  "Objects": [
    { "oid": "OR:wt.part.WTPart:108618" },
    { "oid": "OR:wt.part.WTPart:108620" }
  ]
}
```

### CheckIn (Multiple Objects)

Checks in multiple parts simultaneously.

**Unbound action**

**URL:**
```
POST /ProdMgmt/CheckIn
```

**Request Body:**
```json
{
  "Objects": [
    { "oid": "OR:wt.part.WTPart:108618", "Comment": "comment 1" },
    { "oid": "OR:wt.part.WTPart:108620", "Comment": "comment 2" }
  ]
}
```

### UndoCheckOut (Multiple Objects)

Reverts check-out for multiple parts.

**Unbound action**

**URL:**
```
POST /ProdMgmt/UndoCheckOut
```

### Revise (Multiple Objects)

Creates new revisions for multiple parts.

**Unbound action**

**URL:**
```
POST /ProdMgmt/Revise
```

### Delete (Multiple Objects)

Deletes multiple parts.

**Unbound action**

**URL:**
```
POST /ProdMgmt/Delete
```

### SaveAs

Creates a copy of a part with a new number.

**Bound to:** `Part` entity

**URL:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.SaveAs
```

**Request Body:**
```json
{
  "Number": "NEW_PART_NUMBER",
  "Name": "New Part Name"
}
```

## Functions Available in the PTC Product Management Domain

Functions are invoked using the HTTP GET method and do not modify data.

### GetPartsList

Retrieves the parts list for a given part. Returns the BOM structure.

**Bound to:** `Part` entity

**URL:**
```
GET /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.GetPartsList()
```

**Response:** Returns a collection of parts that constitute the BOM.

### GetPartStructure

Retrieves the part structure (BOM) for a part, expanded to multiple levels.

**URL:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=Uses($expand=Child($expand=Uses($expand=Child)))
```

This approach uses nested `$expand` to traverse the BOM hierarchy. Each level requires expanding `Uses` (PartUse links) and then `Child` (the child Part).

### GetWhereUsed

Retrieves information about where a part is used (reverse BOM lookup).

**Bound to:** `Part` entity

**URL:**
```
GET /ProdMgmt/Parts('<oid>')/PTC.ProdMgmt.GetWhereUsed()
```

## Entity Types in ProdMgmt Domain

| Entity | Windchill Class | Description |
|--------|----------------|-------------|
| `Part` | `wt.part.WTPart` | Represents a part version |
| `ElectricalPart` | Soft type of WTPart | Electrical part soft type |
| `BOM` | Part structure | Bill of materials |
| `PartUse` | `wt.part.WTPartUsageLink` | Association between parent and child parts |
| `UsageOccurrence` | Reference designator | Occurrence of a component in BOM |
| `PartContent` | Derived from FolderContent | Part residing in a folder |
| `SupplierPart` | Supplier part subtype | Read-only supplier part |
| `ManufacturerPart` | ManufacturerPart | Part produced by manufacturer |
| `VendorPart` | VendorPart | Part supplied by vendor |
| `AXLEntry` | AML/AVL association | Links SupplierPart to Part |

## Navigation Properties for Part Entity

| Navigation Property | Description |
|---------------------|-------------|
| `AssignedOptionSet` | Option set assigned to the part (requires Configurable Module Support) |
| `AXLEntries` | AML/AVL associations for manufacturer and vendor parts |
| `PartAssociations` | Association links between part and CAD document |
| `Effectivities` | Effectivities associated with the part |
| `Uses` | Child PartUse links (BOM children) |
| `UsedBy` | Parent PartUse links (where used) |
| `Attachments` | Attached files/documents |
| `ContainerReference` | Container (Product/Library) reference |
| `FolderReference` | Folder location |
| `LifeCycleState` | Current life cycle state |
| `SecurityLabels` | Applied security labels |

## Creating a Part

```
POST /ProdMgmt/Parts
Content-Type: application/json
CSRF_NONCE: <token>
```

```json
{
  "Number": "PART-001",
  "Name": "My Part",
  "ContainerReference": {
    "ID": "OR:wt.pdmlink.PDMLinkProduct:108601"
  },
  "FolderReference": {
    "ID": "OR:wt.folder.SubFolder:108605"
  },
  "Source": { "Value": "make" },
  "DefaultUnit": { "Value": "ea" }
}
```

## Creating a PartUse (BOM Link)

```
POST /ProdMgmt/Parts('<parent_oid>')/Uses
Content-Type: application/json
CSRF_NONCE: <token>
```

```json
{
  "Child@odata.bind": "Parts('OR:wt.part.WTPart:108620')",
  "Quantity": 2,
  "Unit": { "Value": "ea" },
  "LineNumber": 10
}
```

## AXL Entry Operations

### Creating an AXL Entry (AML/AVL)

```
POST /ProdMgmt/Parts('<OEM_PART_OID>')/AXLEntries
Content-Type: application/json
CSRF_NONCE: <token>
```

```json
{
  "SourcingContext@odata.bind": "SourcingContexts('OR:com.ptc.windchill.suma.axl.AXLContext:232901')",
  "VendorPartSourcingStatus": { "Value": "approved", "Display": "Approved" },
  "ManufacturerPartSourcingStatus": { "Value": "preferred", "Display": "Preferred" },
  "ManufacturerPartReference@odata.bind": "ManufacturerParts('OR:com.ptc.windchill.suma.part.ManufacturerPart:280604')",
  "VendorPartReference@odata.bind": "VendorParts('OR:com.ptc.windchill.suma.part.VendorPart:280463')"
}
```

**Required Parameters by AXL Type:**

| Type | Sourcing Context | Part Reference |
|------|-----------------|----------------|
| AML (Manufacturer) | Required | `ManufacturerPartReference` |
| AVL (Vendor) | Required | `VendorPartReference` |
| AXL (Both) | Required | `ManufacturerPartReference` + `VendorPartReference` |
