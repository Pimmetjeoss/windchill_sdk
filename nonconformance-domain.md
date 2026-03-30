# Nonconformance Domain (NC)

## Overview

The Nonconformance (NC) domain provides REST API access to nonconformance objects in Windchill Quality Solutions, including nonconformances, dispositions, and affected items.

**Domain Name:** `NC`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/NC
```

**Metadata URL:**
```
GET /NC/$metadata
```

## Entity Sets

### Nonconformances

Represents nonconformance records (quality deviations).

**Entity Set URL:**
```
GET /NC/Nonconformances
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Nonconformance name |
| `Number` | Edm.String | Nonconformance number |
| `Description` | Edm.String | Description of the nonconformance |
| `NCType` | Edm.String | Nonconformance type |
| `State` | Edm.String | Lifecycle state |
| `Version` | Edm.String | Version identifier |
| `Iteration` | Edm.String | Iteration identifier |
| `Severity` | Edm.String | Severity level |
| `Priority` | Edm.String | Priority |
| `Category` | Edm.String | Category classification |
| `Source` | Edm.String | Source of the nonconformance |
| `DetectedDate` | Edm.DateTimeOffset | Date the NC was detected |
| `ContainerName` | Edm.String | Container name |
| `ContainerID` | Edm.String | Container ID |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Dispositions` | Dispositions | Dispositions for this NC |
| `AffectedItems` | AffectedItems | Items affected by this NC |
| `RelatedCAPAs` | CAPAs | Related CAPA records (cross-domain) |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve nonconformances |
| POST | Create a new nonconformance |
| PATCH | Update a nonconformance |

---

### Dispositions

Represents dispositions applied to nonconformances.

**Entity Set URL:**
```
GET /NC/Dispositions
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Disposition name |
| `Number` | Edm.String | Disposition number |
| `Description` | Edm.String | Disposition description |
| `DispositionType` | Edm.String | Type of disposition (e.g., Rework, Scrap, Use As Is, Return to Supplier) |
| `State` | Edm.String | Lifecycle state |
| `Quantity` | Edm.Decimal | Quantity affected |
| `NonconformanceID` | Edm.String | Reference to parent NC |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve dispositions |
| POST | Create a new disposition |
| PATCH | Update a disposition |

---

### AffectedItems

Represents items (parts, documents, etc.) affected by a nonconformance.

**Entity Set URL (via navigation):**
```
GET /NC/Nonconformances('...')/AffectedItems
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
| `Quantity` | Edm.Decimal | Quantity affected |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve affected items |

---

## Query Examples

**Get all nonconformances:**
```http
GET /NC/Nonconformances
```

**Filter NCs by severity:**
```http
GET /NC/Nonconformances?$filter=Severity eq 'Critical'
```

**Filter NCs by state:**
```http
GET /NC/Nonconformances?$filter=State eq 'OPEN'
```

**Get dispositions for a specific NC:**
```http
GET /NC/Nonconformances('OR:com.ptc.qualitymanagement.nc.Nonconformance:12345')/Dispositions
```

**Expand affected items:**
```http
GET /NC/Nonconformances('...')?$expand=AffectedItems
```

**Get NCs detected within a date range:**
```http
GET /NC/Nonconformances?$filter=DetectedDate ge 2024-01-01T00:00:00Z and DetectedDate le 2024-12-31T23:59:59Z
```
