# Reassigning Work Items to Another User

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `workflow_domain_reassigning_workitems.html`

## Overview

Reassign one or more workflow work items from the current assignee to another user. Before reassigning, you should retrieve the list of valid users who can receive the work item.

## Step 1: Retrieve Valid Users for Reassignment

### Endpoint

```
GET https://<windchill_server>/Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.GetValidReassignUsers()
```

- **Domain**: Workflow (PTC Workflow)
- **Entity Set**: `WorkItems`
- **Function**: `PTC.Workflow.GetValidReassignUsers()` (bound function)
- **HTTP Method**: GET

### Example Request

```http
GET /Windchill/servlet/odata/Workflow/WorkItems('OR:wt.workflow.work.WorkItem:345678')/PTC.Workflow.GetValidReassignUsers() HTTP/1.1
Host: windchill.ptc.com
Accept: application/json
```

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/Workflow/$metadata#Collection(PTC.Workflow.User)",
  "value": [
    {
      "ID": "OR:wt.org.WTPrincipalReference:100001",
      "Name": "jdoe",
      "FullName": "Jane Doe",
      "Email": "jdoe@example.com"
    },
    {
      "ID": "OR:wt.org.WTPrincipalReference:100002",
      "Name": "bsmith",
      "FullName": "Bob Smith",
      "Email": "bsmith@example.com"
    }
  ]
}
```

### User Properties

| Property | Type | Description |
|----------|------|-------------|
| `ID` | String | Object reference of the user principal |
| `Name` | String | Username / login name |
| `FullName` | String | Full display name of the user |
| `Email` | String | Email address of the user |

## Step 2: Reassign the Work Item

### Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.Reassign
```

- **Domain**: Workflow (PTC Workflow)
- **Entity Set**: `WorkItems`
- **Action**: `PTC.Workflow.Reassign` (bound action)
- **HTTP Method**: POST

### Headers

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `Accept` | `application/json` |
| `CSRF_NONCE` | `<nonce_value>` |

### Request Body

```json
{
  "ReassignTo": "jdoe",
  "Comments": "Reassigning to Jane Doe for review as I am out of office."
}
```

### Request Body Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `ReassignTo` | String | Yes | The username (login name) of the user to reassign the work item to. Must be one of the valid reassign users. |
| `Comments` | String | No | Reason or notes for the reassignment |

### Example Request

```http
POST /Windchill/servlet/odata/Workflow/WorkItems('OR:wt.workflow.work.WorkItem:345678')/PTC.Workflow.Reassign HTTP/1.1
Host: windchill.ptc.com
Content-Type: application/json
Accept: application/json
CSRF_NONCE: <nonce_value>

{
  "ReassignTo": "jdoe",
  "Comments": "Reassigning to Jane Doe for review."
}
```

### Response

#### HTTP Status

- **200 OK** on success

#### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/Workflow/$metadata#WorkItems/$entity",
  "ID": "OR:wt.workflow.work.WorkItem:345678",
  "Name": "Review Design Specification",
  "Status": "Active",
  "AssignedTo": "jdoe",
  "Comments": "Reassigning to Jane Doe for review."
}
```

## Complete Workflow: Reassign a Work Item

1. **Get work items** assigned to the current user:
   ```
   GET /Windchill/servlet/odata/Workflow/WorkItems
   ```

2. **Get valid reassign users** for the work item:
   ```
   GET /Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.GetValidReassignUsers()
   ```

3. **Fetch NONCE**:
   ```
   GET /Windchill/servlet/odata/PTC/GetCSRFToken()
   ```

4. **Reassign** the work item:
   ```
   POST /Windchill/servlet/odata/Workflow/WorkItems('<workitem_id>')/PTC.Workflow.Reassign
   ```

## Notes

- The `ReassignTo` value must be a valid username from the list returned by `GetValidReassignUsers()`.
- The valid user list is determined by the workflow template configuration (e.g., role-based or team-based assignments).
- Reassignment is logged in the workflow history with the provided comments.
- The original assignee loses access to the work item after reassignment.
- Only the current assignee (or an administrator) can reassign a work item.
- The work item remains in `Active` status after reassignment.

## Common Errors

| HTTP Status | Description |
|-------------|-------------|
| `400 Bad Request` | The specified user is not a valid reassignment target |
| `403 Forbidden` | The current user does not have permission to reassign this work item |
| `404 Not Found` | The specified work item ID does not exist |
