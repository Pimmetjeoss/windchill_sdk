# Customer Experience Management Domain (CEM)

## Overview

The Customer Experience Management (CEM) domain provides REST API access to customer complaints, feedback records, and regulatory master data in Windchill Quality Solutions.

**Domain Name:** `CEM`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/CEM
```

**Metadata URL:**
```
GET /CEM/$metadata
```

## Entity Sets

### CustomerComplaints

Represents customer complaint records.

**Entity Set URL:**
```
GET /CEM/CustomerComplaints
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Complaint name |
| `Number` | Edm.String | Complaint number |
| `Description` | Edm.String | Description of the complaint |
| `ComplaintType` | Edm.String | Type of complaint |
| `State` | Edm.String | Lifecycle state |
| `Version` | Edm.String | Version identifier |
| `Iteration` | Edm.String | Iteration identifier |
| `Priority` | Edm.String | Priority level |
| `Severity` | Edm.String | Severity level |
| `Source` | Edm.String | Complaint source |
| `CustomerName` | Edm.String | Customer who filed the complaint |
| `ReceivedDate` | Edm.DateTimeOffset | Date the complaint was received |
| `ContainerName` | Edm.String | Container name |
| `ContainerID` | Edm.String | Container ID |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `AffectedItems` | AffectedItems | Items referenced by the complaint |
| `RelatedNonconformances` | Nonconformances | Related NC records |
| `RelatedCAPAs` | CAPAs | Related CAPA records |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve customer complaints |
| POST | Create a new complaint |
| PATCH | Update a complaint |

---

### CustomerFeedbacks

Represents customer feedback records (non-complaint feedback).

**Entity Set URL:**
```
GET /CEM/CustomerFeedbacks
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Feedback name |
| `Number` | Edm.String | Feedback number |
| `Description` | Edm.String | Description |
| `FeedbackType` | Edm.String | Type of feedback |
| `State` | Edm.String | Lifecycle state |
| `Source` | Edm.String | Feedback source |
| `ReceivedDate` | Edm.DateTimeOffset | Date the feedback was received |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve customer feedback |
| POST | Create new feedback |
| PATCH | Update feedback |

---

### AffectedItems

Represents items referenced in a customer complaint.

**Entity Set URL (via navigation):**
```
GET /CEM/CustomerComplaints('...')/AffectedItems
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

**Get all customer complaints:**
```http
GET /CEM/CustomerComplaints
```

**Filter complaints by priority:**
```http
GET /CEM/CustomerComplaints?$filter=Priority eq 'High'
```

**Filter complaints by state:**
```http
GET /CEM/CustomerComplaints?$filter=State eq 'OPEN'
```

**Get complaints received within a date range:**
```http
GET /CEM/CustomerComplaints?$filter=ReceivedDate ge 2024-01-01T00:00:00Z and ReceivedDate le 2024-12-31T23:59:59Z
```

**Get affected items for a complaint:**
```http
GET /CEM/CustomerComplaints('OR:com.ptc.qualitymanagement.cem.CustomerComplaint:12345')/AffectedItems
```

**Expand affected items:**
```http
GET /CEM/CustomerComplaints?$expand=AffectedItems
```
