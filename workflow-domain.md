# PTC Workflow Domain

> **Domain ID:** `Workflow`
> **Base URL:** `/Windchill/servlet/odata/Workflow`
> **Metadata URL:** `/Windchill/servlet/odata/Workflow/$metadata`
> **Added in:** Windchill REST Services 1.5

The PTC Workflow domain provides access to the workflow capabilities of Windchill. A workflow enables you to automate procedures in which information, tasks, and documents are passed to several participants, possibly across multiple companies.

## Domain Capabilities

Use this domain to perform the following operations:

- Get the list of states of the work items
- Get the work items assigned to you
- Save tasks
- Complete tasks
- Get the list of users to whom a specified task can be reassigned
- Reassign your tasks to other users

## Entities

The following table lists the significant OData entities available in the PTC Workflow domain. To see all entities, refer to the EDM of the domain at the metadata URL.

| Item | OData Entity | Windchill Class | Description |
|------|-------------|----------------|-------------|
| Work item | `WorkItem` | `wt.workflow.work.WorkItem` | Represents tasks in Windchill. A work item is a task assigned to a user. |
| Subject of a workflow | `Subject` | (lifecycle-managed object) | Represents a business object associated with the `WorkItem` entity. Can be any lifecycle-managed object (parts, CAD documents, change requests, etc.). |
| Activity in workflow | `Activity` | - | Represents an action in a process assigned as tasks/work items to users. Every `WorkItem` entity is associated with an `Activity`. |
| Workflow template | `WorkItemProcessTemplate` | `WfProcessTemplate` | Represents a workflow template. The `WorkItem` entity is associated with a workflow template. |
| User information | `Owner` | `WTUser` | Owner information is available for every `WorkItem`. |
| User information | `CompletedBy` | `WTUser` | Populated using the complete, reassign, or delegate action. |
| User information | `OriginalOwner` | `WTUser` | Populated using the complete, reassign, or delegate action. |
| Audit details | `VotingEventAudit` | - | Contains audit information for a specific task. Associated with work items that are complete. |
| Audit details | `WfEventAudit` | - | Contains audit information for a specific task. Associated with work items that are complete. |

## Entity Sets

| Entity Set | Description |
|-----------|-------------|
| `WorkItems` | Collection of work items assigned to the authenticated user |

## Key URLs

### Retrieve All Work Items

```
GET /Windchill/servlet/odata/Workflow/WorkItems
```

### Retrieve Work Items with Activity Details

```
GET /Windchill/servlet/odata/Workflow/WorkItems?$expand=Activity
```

### Filter Work Items by Activity and Status

```
GET /Windchill/servlet/odata/Workflow/WorkItems?$expand=Activity&$filter=Activity/Name eq 'Analyze Change Request' and Status/Display eq 'Potential'
```

### Get Enum Type Constraints for WorkItem Status

```
GET /Windchill/Workflow/GetEnumTypeConstraint(entityName='PTC.Workflow.WorkItem',propertyName='Status')
```

### Retrieve Routing Options for a Work Item

```
GET /Windchill/servlet/odata/Workflow/WorkItems('OR:wt.workflow.work.WorkItem:178380')/Activity/UserEventList
```

### Retrieve Subjects for Work Items

```
GET /Windchill/servlet/odata/Workflow/WorkItems?$expand=Subject
```

## Navigation Properties

| Navigation Property | Target Entity | Description |
|--------------------|---------------|-------------|
| `Activity` | `Activity` | The workflow activity associated with the work item |
| `Subject` | `Subject` | The business object associated with the work item |
| `Owner` | `Owner` | The user to whom the work item is assigned |
| `CompletedBy` | `CompletedBy` | The user who completed the work item |
| `OriginalOwner` | `OriginalOwner` | The original owner before reassignment |
| `WorkItemProcessTemplate` | `WorkItemProcessTemplate` | The workflow template |
| `VotingEventAudit` | `VotingEventAudit` | Voting audit trail for completed items |
| `WfEventAudit` | `WfEventAudit` | Event audit trail for completed items |

## Activity Entity Properties

The `Activity` entity contains:

| Property | Description |
|----------|-------------|
| `Name` | Name of the activity |
| `UserEventList` | Available routing options for the activity |

## WorkItem Properties

Key properties on the `WorkItem` entity:

| Property | Type | Description |
|----------|------|-------------|
| `ID` | `Edm.String` | Unique identifier (e.g., `OR:wt.workflow.work.WorkItem:178380`) |
| `Status` | `EnumType` | Current status of the work item (e.g., `Potential`, `Complete`) |
| `WorkitemComment` | `Edm.String` | Comment associated with the work item |
