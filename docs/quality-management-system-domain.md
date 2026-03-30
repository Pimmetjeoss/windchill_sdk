# Quality Management System Domain (QMS)

## Overview

The Quality Management System (QMS) domain provides REST API access to quality-related objects in Windchill Quality Solutions, including audits, audit findings, and quality actions.

**Domain Name:** `QMS`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/QMS
```

**Metadata URL:**
```
GET /QMS/$metadata
```

## Entity Sets

### Audits

Represents quality audits.

**Entity Set URL:**
```
GET /QMS/Audits
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Audit name |
| `Number` | Edm.String | Audit number |
| `Description` | Edm.String | Audit description |
| `AuditType` | Edm.String | Type of audit |
| `State` | Edm.String | Lifecycle state |
| `Version` | Edm.String | Version identifier |
| `Iteration` | Edm.String | Iteration identifier |
| `Priority` | Edm.String | Audit priority |
| `PlannedStartDate` | Edm.DateTimeOffset | Planned start date |
| `PlannedEndDate` | Edm.DateTimeOffset | Planned end date |
| `ActualStartDate` | Edm.DateTimeOffset | Actual start date |
| `ActualEndDate` | Edm.DateTimeOffset | Actual end date |
| `ContainerName` | Edm.String | Container name |
| `ContainerID` | Edm.String | Container ID |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `AuditFindings` | AuditFindings | Findings from this audit |
| `AuditActions` | QualityActions | Actions resulting from this audit |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve audits |
| POST | Create a new audit |
| PATCH | Update an audit |

---

### AuditFindings

Represents findings from quality audits.

**Entity Set URL:**
```
GET /QMS/AuditFindings
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Finding name |
| `Number` | Edm.String | Finding number |
| `Description` | Edm.String | Finding description |
| `FindingType` | Edm.String | Type of finding (e.g., Major, Minor, Observation) |
| `State` | Edm.String | Lifecycle state |
| `Severity` | Edm.String | Severity level |
| `AuditID` | Edm.String | Reference to parent audit |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve audit findings |
| POST | Create a new finding |
| PATCH | Update a finding |

---

### QualityActions

Represents quality actions (corrective/preventive measures).

**Entity Set URL:**
```
GET /QMS/QualityActions
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Action name |
| `Number` | Edm.String | Action number |
| `Description` | Edm.String | Action description |
| `ActionType` | Edm.String | Type of quality action |
| `State` | Edm.String | Lifecycle state |
| `DueDate` | Edm.DateTimeOffset | Due date |
| `AssignedTo` | Edm.String | User assigned to the action |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve quality actions |
| POST | Create a new quality action |
| PATCH | Update a quality action |

---

## Query Examples

**Get all audits:**
```http
GET /QMS/Audits
```

**Filter audits by state:**
```http
GET /QMS/Audits?$filter=State eq 'OPEN'
```

**Get findings for a specific audit:**
```http
GET /QMS/Audits('OR:com.ptc.qualitymanagement.audit.Audit:12345')/AuditFindings
```

**Expand findings with audit:**
```http
GET /QMS/Audits('...')?$expand=AuditFindings
```
