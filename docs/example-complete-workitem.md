# Completing a Work Item

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `workflow_domain_completing_workitems.html`

## Overview

Complete a workflow work item (task) in Windchill by specifying the routing option (approval decision) and optional comments. Work items represent tasks assigned to users within a Windchill workflow process.

## Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.Complete
```

- **Domain**: Workflow (PTC Workflow)
- **Entity Set**: `WorkItems`
- **Action**: `PTC.Workflow.Complete` (bound action)
- **HTTP Method**: POST

## Prerequisites

1. The work item must be assigned to the current user.
2. The work item must be in an active state (not already completed or suspended).
3. A valid NONCE token is required.
4. You should first retrieve available routing options for the work item.

## Retrieving Routing Options

Before completing a work item, retrieve the available routing options:

```
GET https://<windchill_server>/Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.GetRoutingOptions()
```

### Example Routing Options Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/Workflow/$metadata#Collection(PTC.Workflow.RoutingOption)",
  "value": [
    {
      "Name": "Approve",
      "Description": "Approve the work item"
    },
    {
      "Name": "Reject",
      "Description": "Reject the work item"
    }
  ]
}
```

## Request

### Headers

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `Accept` | `application/json` |
| `CSRF_NONCE` | `<nonce_value>` |

### Request Body

```json
{
  "RoutingOption": "Approve",
  "Comments": "Reviewed and approved. All specifications meet requirements."
}
```

### Request Body Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `RoutingOption` | String | Yes | The routing option to select. Must match one of the options returned by `GetRoutingOptions()`. Common values: `Approve`, `Reject`, `Rework`. |
| `Comments` | String | No | Comments or notes to attach to the completed work item |

### Example Request

```http
POST /Windchill/servlet/odata/Workflow/WorkItems('OR:wt.workflow.work.WorkItem:345678')/PTC.Workflow.Complete HTTP/1.1
Host: windchill.ptc.com
Content-Type: application/json
Accept: application/json
CSRF_NONCE: <nonce_value>

{
  "RoutingOption": "Approve",
  "Comments": "Reviewed and approved."
}
```

## Response

### HTTP Status

- **200 OK** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/Workflow/$metadata#WorkItems/$entity",
  "ID": "OR:wt.workflow.work.WorkItem:345678",
  "Name": "Review Design Specification",
  "Status": "Completed",
  "AssignedTo": "jsmith",
  "CompletedOn": "2024-01-16T14:30:00Z",
  "RoutingOption": "Approve",
  "Comments": "Reviewed and approved."
}
```

## Complete Workflow: Get and Complete Work Items

1. **Get work items** assigned to the current user:
   ```
   GET /Windchill/servlet/odata/Workflow/WorkItems
   ```

2. **Get routing options** for the work item:
   ```
   GET /Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.GetRoutingOptions()
   ```

3. **Get subjects** (associated objects) of the work item:
   ```
   GET /Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/Subjects
   ```

4. **Complete** the work item:
   ```
   POST /Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.Complete
   ```

## Saving a Work Item (Without Completing)

To save progress on a work item without completing it:

```
POST /Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.Save
```

```json
{
  "Comments": "Work in progress, will complete later."
}
```

## Filtering Work Items

### By Activity Status

```
GET /Windchill/servlet/odata/Workflow/WorkItems?$filter=Status eq 'Active'
```

### By Assigned User

```
GET /Windchill/servlet/odata/Workflow/WorkItems?$filter=AssignedTo eq 'jsmith'
```

## Notes

- The `RoutingOption` must exactly match one of the values returned by `GetRoutingOptions()`.
- Completing a work item is irreversible. Once completed, the workflow progresses to the next step.
- If the work item is the last in the workflow, completing it may trigger state changes on the associated objects (e.g., promoting a part from `In Work` to `Released`).
- Comments are stored in the workflow history and are visible to other workflow participants.
- Work items can only be completed by the user they are assigned to (or an administrator).

## Common Errors

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | Invalid routing option or work item is not in a completable state |
| `403 Forbidden` | The work item is not assigned to the current user |
| `404 Not Found` | The specified work item ID does not exist |
