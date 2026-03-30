# Common Domain (PTC)

## Overview

The PTC Common Domain provides access to common entities and navigations that are shared across multiple Windchill REST Services domains. It includes access to lifecycle, versioning, team membership, access control, and common navigational entities.

**Domain Name:** `PTC`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/PTC
```

**Metadata URL:**
```
GET /PTC/$metadata
```

## Entity Sets

### BusinessObjects

A generic entity set providing access to any Windchill business object by its object reference.

**Entity Set URL:**
```
GET /PTC/BusinessObjects
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Object name |
| `Number` | Edm.String | Object number |
| `Type` | Edm.String | Object type |
| `State` | Edm.String | Lifecycle state |
| `Version` | Edm.String | Version identifier |
| `Iteration` | Edm.String | Iteration identifier |
| `CheckoutState` | Edm.String | Checkout status |
| `ContainerName` | Edm.String | Name of the parent container |
| `ContainerID` | Edm.String | ID of the parent container |
| `CreatedOn` | Edm.DateTimeOffset | Creation timestamp |
| `LastModified` | Edm.DateTimeOffset | Last modification timestamp |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `LifeCycleHistory` | LifeCycleHistories | Lifecycle state change history |
| `Iterations` | Iterations | All iterations of this object |
| `TeamMembers` | TeamMembers | Team members associated with this object |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve business objects |

---

### LifeCycleTemplates

Lifecycle templates defined in the system.

**Entity Set URL:**
```
GET /PTC/LifeCycleTemplates
```

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Template name |
| `ContainerName` | Edm.String | Name of the container |

---

### TypeDefinitions

Type definitions available in Windchill.

**Entity Set URL:**
```
GET /PTC/TypeDefinitions
```

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `TypeName` | Edm.String | Internal type identifier |
| `DisplayName` | Edm.String | Localized display name |

---

## Common Navigation Properties

The PTC domain defines common navigations that are available across entities in all PTC domains:

| Navigation | Target Entity | Available On | Description |
|------------|---------------|-------------|-------------|
| `Attachments` | Attachments | Iterated objects | Content/file attachments |
| `LifeCycleHistory` | LifeCycleHistories | Lifecycle-managed objects | State change history |
| `Iterations` | Iterations | Iterated objects | All iterations of the object |
| `Versions` | Versions | Versioned objects | All versions of the object |
| `TeamMembers` | TeamMembers | Team-managed objects | Team membership |
| `AccessPermissions` | AccessPermissions | All objects | Access control information |
| `RelatedChangeObjects` | ChangeObjects | Change-managed objects | Associated change objects |

These navigations can be used from entities in other domains. For example:
```http
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Attachments
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/LifeCycleHistory
GET /DocMgmt/Documents('OR:wt.doc.WTDocument:67890')/Iterations
```

---

## Actions

### PTC.SetLifeCycleState

Sets the lifecycle state of a Windchill object.

**Bound to:** Entity instances (iterated objects with lifecycle)

**URL Pattern:**
```
POST /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.SetLifeCycleState
```

**Request Body:**
```json
{
  "State": "APPROVED"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `State` | Edm.String | Yes | Target lifecycle state internal name |

---

### PTC.CheckOut

Checks out a Windchill object.

**URL Pattern:**
```
POST /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.CheckOut
```

**Request Body:**
```json
{
  "Note": "Checking out for editing"
}
```

---

### PTC.CheckIn

Checks in a Windchill object.

**URL Pattern:**
```
POST /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.CheckIn
```

**Request Body:**
```json
{
  "Note": "Completed updates"
}
```

---

### PTC.UndoCheckOut

Undoes a checkout on a Windchill object.

**URL Pattern:**
```
POST /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.UndoCheckOut
```

---

### PTC.Revise

Creates a new revision (version) of a Windchill object.

**URL Pattern:**
```
POST /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.Revise
```

---

### PTC.Delete

Deletes a Windchill object.

**URL Pattern:**
```
POST /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.Delete
```

---

## Query Examples

**Get a business object by ID:**
```http
GET /PTC/BusinessObjects('OR:wt.part.WTPart:12345')
```

**Get lifecycle templates:**
```http
GET /PTC/LifeCycleTemplates?$filter=contains(Name,'Basic')
```

**Expand attachments on a product part (cross-domain navigation):**
```http
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')?$expand=Attachments
```
