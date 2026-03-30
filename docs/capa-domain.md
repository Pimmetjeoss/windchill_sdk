# CAPA Domain (CAPA)

## Overview

The CAPA (Corrective and Preventive Action) domain provides REST API access to CAPA records in Windchill Quality Solutions. CAPAs track corrective and preventive actions taken to address quality issues.

**Domain Name:** `CAPA`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/CAPA
```

**Metadata URL:**
```
GET /CAPA/$metadata
```

## Entity Sets

### CAPAs

Represents Corrective and Preventive Action records.

**Entity Set URL:**
```
GET /CAPA/CAPAs
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | CAPA name |
| `Number` | Edm.String | CAPA number |
| `Description` | Edm.String | CAPA description |
| `CAPAType` | Edm.String | Type of CAPA (Corrective, Preventive) |
| `State` | Edm.String | Lifecycle state |
| `Version` | Edm.String | Version identifier |
| `Iteration` | Edm.String | Iteration identifier |
| `Priority` | Edm.String | Priority level |
| `Severity` | Edm.String | Severity level |
| `RootCause` | Edm.String | Root cause description |
| `DueDate` | Edm.DateTimeOffset | Due date for completion |
| `AssignedTo` | Edm.String | User assigned to the CAPA |
| `ContainerName` | Edm.String | Container name |
| `ContainerID` | Edm.String | Container ID |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `CAPAActions` | CAPAActions | Individual actions within this CAPA |
| `AffectedItems` | AffectedItems | Items affected by this CAPA |
| `RelatedNonconformances` | Nonconformances | Related NC records (cross-domain) |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve CAPAs |
| POST | Create a new CAPA |
| PATCH | Update a CAPA |

---

### CAPAActions

Represents individual corrective or preventive actions within a CAPA.

**Entity Set URL:**
```
GET /CAPA/CAPAActions
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Action name |
| `Number` | Edm.String | Action number |
| `Description` | Edm.String | Action description |
| `ActionType` | Edm.String | Type of action |
| `State` | Edm.String | Lifecycle state |
| `DueDate` | Edm.DateTimeOffset | Due date |
| `CompletedDate` | Edm.DateTimeOffset | Completion date |
| `AssignedTo` | Edm.String | User assigned to the action |
| `CAPAID` | Edm.String | Reference to parent CAPA |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve CAPA actions |
| POST | Create a new CAPA action |
| PATCH | Update a CAPA action |

---

### AffectedItems

Represents items affected by a CAPA.

**Entity Set URL (via navigation):**
```
GET /CAPA/CAPAs('...')/AffectedItems
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `ItemID` | Edm.String | ID of the affected item |
| `ItemName` | Edm.String | Name of the affected item |
| `ItemNumber` | Edm.String | Number of the affected item |
| `ItemType` | Edm.String | Type of the affected item |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve affected items |

---

## Query Examples

**Get all CAPAs:**
```http
GET /CAPA/CAPAs
```

**Filter CAPAs by type:**
```http
GET /CAPA/CAPAs?$filter=CAPAType eq 'Corrective'
```

**Filter CAPAs by state:**
```http
GET /CAPA/CAPAs?$filter=State eq 'OPEN'
```

**Get actions for a specific CAPA:**
```http
GET /CAPA/CAPAs('OR:com.ptc.qualitymanagement.capa.CAPA:12345')/CAPAActions
```

**Get CAPAs with expanded actions:**
```http
GET /CAPA/CAPAs?$expand=CAPAActions
```

**Get CAPAs due soon:**
```http
GET /CAPA/CAPAs?$filter=DueDate le 2024-06-30T23:59:59Z and State ne 'CLOSED'
```
