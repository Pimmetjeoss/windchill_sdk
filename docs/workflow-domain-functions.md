# Functions Available in the PTC Workflow Domain

> **Domain ID:** `Workflow`
> **Base URL:** `/Windchill/servlet/odata/Workflow`

## GetWorkItemReassignUserList

The `GetWorkItemReassignUserList` function returns a list of valid users to whom the specified work items can be reassigned.

**Type:** Unbound function

### Request

```
GET /Windchill/servlet/odata/v1/Workflow/GetWorkItemReassignUserList(WorkItems=@wi)?@wi=["<workitem_id_1>","<workitem_id_2>","<workitem_id_3>"]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `WorkItems` | `Array<String>` | Yes | Array of work item IDs. Passed as a URL parameter using an alias (e.g., `@wi`). |

### Example

```
GET /Windchill/servlet/odata/v1/Workflow/GetWorkItemReassignUserList(WorkItems=@wi)?@wi=["OR:wt.workflow.work.WorkItem:232279","OR:wt.workflow.work.WorkItem:232290","OR:wt.workflow.work.WorkItem:232297"]
```

### Notes

- `@wi` represents an alias, which can be replaced with any other name (e.g., `@items`, `@workitems`).
- The function returns `User` entities representing valid reassignment targets.
- The returned list is filtered to users who are permitted to receive the specified work items based on Windchill access controls and workflow configuration.

### Response

The response contains a collection of user entities with properties such as:

| Property | Type | Description |
|----------|------|-------------|
| `ID` | `Edm.String` | User identifier (e.g., `OR:wt.org.WTUser:11`) |
| `Name` | `Edm.String` | Display name of the user |

## Related Functions from Imported Domains

The Workflow domain imports the PTC Common domain, making these additional functions available:

### GetEnumTypeConstraint

Returns valid values for properties represented as `EnumType`. Useful for getting valid `Status` values for work items.

```
GET /Windchill/servlet/odata/Workflow/GetEnumTypeConstraint(entityName='PTC.Workflow.WorkItem',propertyName='Status')
```

### GetAllStates

Returns a list of life cycle states available in Windchill.

```
GET /Windchill/servlet/odata/Workflow/GetAllStates()
```

### GetWindchillMetaInfo

Returns Windchill metadata for OData entity types and properties available in the Workflow domain.

```
GET /Windchill/servlet/odata/Workflow/GetWindchillMetaInfo()
```

To get metadata for a specific entity:

```
GET /Windchill/servlet/odata/Workflow/GetWindchillMetaInfo(EntityName='PTC.Workflow.WorkItem')
```
