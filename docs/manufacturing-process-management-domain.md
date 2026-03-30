# Manufacturing Process Management Domain (MfgProcessMgmt)

## Overview

The Manufacturing Process Management domain provides REST API access to manufacturing process plans, operations, operation sequences, and related manufacturing data in Windchill MPMLink.

**Domain Name:** `MfgProcessMgmt`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/MfgProcessMgmt
```

**Metadata URL:**
```
GET /MfgProcessMgmt/$metadata
```

## Entity Sets

### ProcessPlans

Represents manufacturing process plans.

**Entity Set URL:**
```
GET /MfgProcessMgmt/ProcessPlans
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Process plan name |
| `Number` | Edm.String | Process plan number |
| `Description` | Edm.String | Description |
| `Version` | Edm.String | Version identifier |
| `Iteration` | Edm.String | Iteration identifier |
| `State` | Edm.String | Lifecycle state |
| `CheckoutState` | Edm.String | Checkout status |
| `ContainerName` | Edm.String | Container name |
| `ContainerID` | Edm.String | Container ID |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Operations` | Operations | Operations within this process plan |
| `OperationSequences` | OperationSequences | Sequences of operations |
| `ConsumedParts` | ConsumedParts | Parts consumed by this process plan |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve process plans |
| POST | Create a new process plan |
| PATCH | Update a process plan |

---

### Operations

Represents manufacturing operations.

**Entity Set URL:**
```
GET /MfgProcessMgmt/Operations
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Operation name |
| `Number` | Edm.String | Operation number |
| `Description` | Edm.String | Description |
| `Version` | Edm.String | Version identifier |
| `Iteration` | Edm.String | Iteration identifier |
| `State` | Edm.String | Lifecycle state |
| `SequenceNumber` | Edm.Int32 | Order in the process sequence |
| `WorkCenter` | Edm.String | Work center name |
| `Duration` | Edm.Decimal | Estimated operation duration |
| `DurationUnit` | Edm.String | Unit for the duration |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `ConsumedParts` | ConsumedParts | Parts consumed by this operation |
| `StandardProcedures` | StandardProcedures | Standard procedures/instructions |
| `Resources` | Resources | Resources assigned to this operation |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve operations |
| POST | Create a new operation |
| PATCH | Update an operation |

---

### OperationSequences

Represents sequences (links) between operations, defining the order of execution.

**Entity Set URL:**
```
GET /MfgProcessMgmt/OperationSequences
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `PredecessorID` | Edm.String | ID of the predecessor operation |
| `SuccessorID` | Edm.String | ID of the successor operation |
| `SequenceType` | Edm.String | Type of sequence relationship |

---

### ConsumedParts

Represents parts that are consumed by a process plan or operation.

**Entity Set URL (via navigation):**
```
GET /MfgProcessMgmt/ProcessPlans('...')/ConsumedParts
GET /MfgProcessMgmt/Operations('...')/ConsumedParts
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `PartID` | Edm.String | ID of the consumed part |
| `PartName` | Edm.String | Part name |
| `PartNumber` | Edm.String | Part number |
| `Quantity` | Edm.Decimal | Quantity consumed |
| `Unit` | Edm.String | Unit of measure |

---

## Actions

### MfgProcessMgmt.GetBillOfProcess

Retrieves the bill of process (BOP) structure for a process plan.

**Bound to:** ProcessPlan entity instance

**URL Pattern:**
```
POST /MfgProcessMgmt/ProcessPlans('OR:com.ptc.windchill.mpml.processplan.MPMProcessPlan:12345')/MfgProcessMgmt.GetBillOfProcess
```

**Returns:** Collection of operations in BOP order

---

## Query Examples

**Get all process plans:**
```http
GET /MfgProcessMgmt/ProcessPlans
```

**Get operations in a process plan:**
```http
GET /MfgProcessMgmt/ProcessPlans('OR:com.ptc.windchill.mpml.processplan.MPMProcessPlan:12345')/Operations
```

**Filter process plans by state:**
```http
GET /MfgProcessMgmt/ProcessPlans?$filter=State eq 'INWORK'
```

**Expand operations within a process plan:**
```http
GET /MfgProcessMgmt/ProcessPlans('...')?$expand=Operations
```

**Get consumed parts for an operation:**
```http
GET /MfgProcessMgmt/Operations('OR:com.ptc.windchill.mpml.operation.MPMOperation:12345')/ConsumedParts
```
