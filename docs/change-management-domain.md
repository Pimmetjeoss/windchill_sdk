# PTC Change Management Domain

> Source: PTC Windchill REST Services 1.6 Documentation
> Page: `changemgmtdomain.html`

## Overview

The PTC Change Management domain (`ChangeMgmt`) provides access to the change management capabilities of Windchill. It exposes OData entities that represent change management business objects such as Problem Reports, Change Requests, Change Notices, Change Tasks, and Variances.

**Base URL:** `/servlet/odata/ChangeMgmt`

**Metadata URL:**
```
GET /servlet/odata/ChangeMgmt/$metadata
```

**Service Document:**
```
GET /servlet/odata/ChangeMgmt
```

## Entity Types

The following table lists the significant OData entities available in the Change Management domain.

| Items | OData Entity | Windchill Class | Description |
|-------|-------------|-----------------|-------------|
| Problem Report | `ProblemReport` | `wt.change2.WTChangeIssue` | Represents a problem report that identifies a quality or design issue |
| Change Request | `ChangeRequest` | `wt.change2.WTChangeRequest2` | Represents a formal request for a change |
| Change Notice | `ChangeNotice` | `wt.change2.WTChangeOrder2` | Represents an approved change notice |
| Change Task | `ChangeTask` | `wt.change2.WTChangeActivity2` | Represents a task within a change notice |
| Variance | `Variance` | `wt.change2.WTVariance` | Represents a variance (deviation or waiver) |

## Entity Sets

| Entity Set | Description |
|-----------|-------------|
| `ProblemReports` | Collection of all Problem Reports |
| `ChangeRequests` | Collection of all Change Requests |
| `ChangeNotices` | Collection of all Change Notices |
| `ChangeTasks` | Collection of all Change Tasks |
| `Variances` | Collection of all Variances |

## Retrieving Change Objects

### Get All Problem Reports
```
GET /ChangeMgmt/ProblemReports
```

### Get a Specific Problem Report
```
GET /ChangeMgmt/ProblemReports('<oid>')
```

### Get All Change Requests
```
GET /ChangeMgmt/ChangeRequests
```

### Get a Specific Change Request
```
GET /ChangeMgmt/ChangeRequests('<oid>')
```

### Get All Change Notices
```
GET /ChangeMgmt/ChangeNotices
```

### Get a Specific Change Notice
```
GET /ChangeMgmt/ChangeNotices('<oid>')
```

### Get All Change Tasks
```
GET /ChangeMgmt/ChangeTasks
```

### Get a Specific Change Task
```
GET /ChangeMgmt/ChangeTasks('<oid>')
```

### Get All Variances
```
GET /ChangeMgmt/Variances
```

## Navigation Properties

### Navigation Properties for Change Objects

The following navigation properties are available on change management entities:

| Navigation Property | Available On | Description |
|--------------------|-------------|-------------|
| `AffectedLinks` | ChangeNotice, ChangeTask | Links to the affected objects (before change) |
| `AffectedObjects` | ChangeNotice, ChangeTask | The actual affected objects |
| `AffectedByLinks` | Various | Reverse links showing which change objects affect an item |
| `AffectedByObjects` | Various | The change objects that affect an item |
| `ResultingLinks` | ChangeNotice, ChangeTask | Links to the resulting objects (after change) |
| `ResultingObjects` | ChangeNotice, ChangeTask | The resulting objects after change implementation |
| `UnincorporatedLinks` | ChangeNotice | Links to objects not yet incorporated |
| `ProcessLinks` | All change objects | Links in the change process flow |
| `ProcessObjects` | All change objects | Objects in the change process flow |
| `ReferenceLinks` | All change objects | Reference links to supporting documents |
| `ReferenceObjects` | All change objects | Referenced supporting objects |
| `Attachments` | All change objects | File attachments |
| `ContainerReference` | All change objects | Container reference |
| `LifeCycleState` | All change objects | Current life cycle state |
| `VarianceOwners` | Variance | Owners of the variance |

### Examples

#### Retrieve Affected Links for a Change Notice
```
GET /ChangeMgmt/ChangeNotices('<oid>')/AffectedLinks
```

#### Retrieve Affected Objects for a Change Notice
```
GET /ChangeMgmt/ChangeNotices('<oid>')/AffectedObjects
```

#### Retrieve Affected Links with Expanded Affected Objects
```
GET /ChangeMgmt/ChangeNotices('<oid>')?$expand=AffectedLinks($expand=AffectedObject)
```

#### Retrieve Attachments for a Change Object
```
GET /ChangeMgmt/ChangeNotices('<oid>')/Attachments
```

#### Retrieve Process Links for Change Objects
```
GET /ChangeMgmt/ChangeNotices('<oid>')/ProcessLinks
```

#### Retrieve Process Objects for a Specific Change Object
```
GET /ChangeMgmt/ChangeRequests('<oid>')/ProcessObjects
```

#### Retrieve Reference Links and Reference Objects
```
GET /ChangeMgmt/ChangeNotices('<oid>')/ReferenceLinks
GET /ChangeMgmt/ChangeNotices('<oid>')/ReferenceObjects
```

#### Retrieve Resulting Links and Resulting Objects
```
GET /ChangeMgmt/ChangeNotices('<oid>')/ResultingLinks
GET /ChangeMgmt/ChangeNotices('<oid>')/ResultingObjects
```

#### Retrieve Unincorporated Links
```
GET /ChangeMgmt/ChangeNotices('<oid>')/UnincorporatedLinks
```

#### Retrieve Variances with Variance Owners
```
GET /ChangeMgmt/Variances?$expand=VarianceOwners
```

## Change Process Flow

The change management process in Windchill follows this typical flow:

```
Problem Report --> Change Request --> Change Notice --> Change Task(s)
```

The `ProcessLinks` and `ProcessObjects` navigation properties allow traversing this flow:

- From a **Problem Report**, `ProcessObjects` returns related Change Requests
- From a **Change Request**, `ProcessObjects` returns related Change Notices
- From a **Change Notice**, `ProcessObjects` returns related Change Tasks

## Filtering Change Objects

### Filter by Name
```
GET /ChangeMgmt/ChangeNotices?$filter=Name eq 'ECN-0001'
```

### Filter by Number
```
GET /ChangeMgmt/ProblemReports?$filter=Number eq 'PR-0001'
```

### Filter by State
```
GET /ChangeMgmt/ChangeNotices?$filter=State/Value eq 'OPEN'
```

### Filter by Created Date
```
GET /ChangeMgmt/ChangeRequests?$filter=CreatedOn gt 2024-01-01T00:00:00Z
```

## Structural Properties

Common structural properties available on change management entities:

| Property | Type | Description |
|----------|------|-------------|
| `ID` | `Edm.String` | Unique object identifier (OID) |
| `Name` | `Edm.String` | Display name |
| `Number` | `Edm.String` | Change object number |
| `State` | Complex Type | Current life cycle state (Value/Display) |
| `Description` | `Edm.String` | Description text |
| `CreatedOn` | `Edm.DateTimeOffset` | Creation date |
| `LastModified` | `Edm.DateTimeOffset` | Last modification date |
| `NeedDate` | `Edm.DateTimeOffset` | Target completion date |
| `Category` | `Edm.String` | Change category |
| `Complexity` | `Edm.String` | Complexity level |
| `Priority` | Complex Type | Priority level |
| `Resolution` | `Edm.String` | Resolution description (Problem Reports) |
