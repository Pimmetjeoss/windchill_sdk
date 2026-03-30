# Common Domain Functions (PTC)

## Overview

The PTC Common Domain exposes several unbound and bound functions that provide common utility capabilities across all domains in Windchill REST Services.

**Domain Name:** `PTC`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/PTC
```

## Unbound Functions

### GetNonceToken

Retrieves a CSRF nonce token required for write operations (POST, PATCH, DELETE). The nonce token must be included in the `CSRF_NONCE` header of subsequent write requests.

**URL:**
```
GET /PTC/GetNonceToken()
```

**Parameters:** None

**Returns:** `Edm.String` - The nonce token value

**Example Request:**
```http
GET /Windchill/servlet/odata/PTC/GetNonceToken()
Accept: application/json
```

**Example Response:**
```json
{
  "@odata.context": "$metadata#Edm.String",
  "value": "A1B2C3D4E5F6"
}
```

**Usage:** Include the returned token in subsequent write requests:
```http
POST /Windchill/servlet/odata/ProdMgmt/Parts
CSRF_NONCE: A1B2C3D4E5F6
Content-Type: application/json

{ ... }
```

---

### GetTypeDefinitions

Retrieves type definitions available in Windchill.

**URL:**
```
GET /PTC/GetTypeDefinitions()
```

**Parameters:** None

**Returns:** Collection of type definition objects

---

### GetObjectByID

Retrieves a Windchill object by its object reference ID.

**URL:**
```
GET /PTC/GetObjectByID(ID='OR:wt.part.WTPart:12345')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ID` | Edm.String | Yes | The object reference identifier |

**Returns:** Business object entity

**Example Request:**
```http
GET /Windchill/servlet/odata/PTC/GetObjectByID(ID='OR:wt.part.WTPart:12345')
Accept: application/json
```

---

### GetLifeCycleStates

Retrieves the available lifecycle states for a given lifecycle template.

**URL:**
```
GET /PTC/GetLifeCycleStates(TemplateName='Basic')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `TemplateName` | Edm.String | Yes | Name of the lifecycle template |

**Returns:** Collection of lifecycle state definitions

---

### GetContainers

Retrieves Windchill containers accessible to the current user.

**URL:**
```
GET /PTC/GetContainers()
```

**Parameters:** None

**Returns:** Collection of container entities

---

### SearchByKeyword

Performs a keyword search across Windchill objects.

**URL:**
```
GET /PTC/SearchByKeyword(Keyword='valve')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `Keyword` | Edm.String | Yes | The search keyword |

**Returns:** Collection of matching business objects

---

## Bound Functions

### PTC.GetVersions

Retrieves all versions of a specific object.

**Bound to:** Entity instances

**URL Pattern:**
```
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.GetVersions()
```

**Returns:** Collection of version entities

---

### PTC.GetIterations

Retrieves all iterations of a specific versioned object.

**Bound to:** Entity instances

**URL Pattern:**
```
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.GetIterations()
```

**Returns:** Collection of iteration entities

---

### PTC.GetLifeCycleHistory

Retrieves the lifecycle state change history for an object.

**Bound to:** Lifecycle-managed entity instances

**URL Pattern:**
```
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.GetLifeCycleHistory()
```

**Returns:** Collection of lifecycle history entries

---

### PTC.GetAccessPermissions

Retrieves the access permissions for an object.

**Bound to:** Entity instances

**URL Pattern:**
```
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.GetAccessPermissions()
```

**Returns:** Collection of access permission entries

---

## Notes for SDK Usage

1. **Nonce Token is Required:** All write operations (POST, PATCH, DELETE) require a valid CSRF nonce token. Always call `GetNonceToken()` first and include the value in the `CSRF_NONCE` header.

2. **Cross-Domain Usage:** PTC common functions and actions can be used with entities from any domain (ProdMgmt, DocMgmt, etc.).

3. **Object Reference Format:** IDs follow the format `OR:<java-class>:<database-id>`, for example `OR:wt.part.WTPart:12345`.
