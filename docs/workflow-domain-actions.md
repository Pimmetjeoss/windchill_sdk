# Actions Available in the PTC Workflow Domain

> **Domain ID:** `Workflow`
> **Base URL:** `/Windchill/servlet/odata/Workflow`

## CompleteWorkitem

The `CompleteWorkitem` action completes the specified task.

**Bound to:** `WorkItem` entity

### Request

```http
POST /Windchill/servlet/odata/Workflow/WorkItems('OR:wt.workflow.work.WorkItem:<workitem_id>')/PTC.Workflow.CompleteWorkitem HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `UserEventList` | `Array<String>` | Yes | Routing options (e.g., `["Reject"]`, `["Accept"]`). Empty array `[]` for default activity. |
| `WorkitemComment` | `String` | Yes | Comment for the work item |
| `VoteAction` | `String` | Yes | Vote option selected by the participant (e.g., `"Approve"`, `"Do not approve"`, `""` for none) |
| `AutomateFastTrack` | `Boolean` | Yes | Whether change notice should be explicitly created (`true` or `false`) |
| `Variables` | `Array<Object>` | Yes | Workflow activity variables. Each object has `Name` and `Value` properties. |

### Example: Default Activity (No Routing Options)

```json
{
  "UserEventList": [],
  "WorkitemComment": "Completing Workitem",
  "VoteAction": "",
  "AutomateFastTrack": false,
  "Variables": []
}
```

### Example: With Routing Option

```json
{
  "UserEventList": ["Reject"],
  "WorkitemComment": "Completing Workitem",
  "VoteAction": "",
  "AutomateFastTrack": false,
  "Variables": []
}
```

### Example: With Voting Option

```json
{
  "UserEventList": [],
  "WorkitemComment": "Completing Workitem",
  "VoteAction": "Approve",
  "AutomateFastTrack": false,
  "Variables": []
}
```

### Example: With Variables

```json
{
  "UserEventList": [],
  "WorkitemComment": "Completing Workitem",
  "VoteAction": "",
  "AutomateFastTrack": false,
  "Variables": [
    {
      "Name": "act3_string",
      "Value": "vxcvcvxcv"
    },
    {
      "Name": "act3_int",
      "Value": "1234"
    },
    {
      "Name": "act3_boolean",
      "Value": "false"
    },
    {
      "Name": "act3_date",
      "Value": "01/05/2019"
    }
  ]
}
```

---

## SaveWorkitem

The `SaveWorkitem` action saves the specified task without completing it.

**Bound to:** `WorkItem` entity

### Request

```http
POST /Windchill/servlet/odata/v1/Workflow/WorkItems('OR:wt.workflow.work.WorkItem:<workitem_id>')/PTC.Workflow.SaveWorkitem HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

### Request Body Parameters

Same parameters as `CompleteWorkitem`:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `UserEventList` | `Array<String>` | Yes | Routing options |
| `WorkitemComment` | `String` | Yes | Comment for the work item |
| `VoteAction` | `String` | Yes | Vote option |
| `AutomateFastTrack` | `Boolean` | Yes | Fast track option |
| `Variables` | `Array<Object>` | Yes | Workflow activity variables |

### Example: Save with Routing Option

```json
{
  "UserEventList": ["Accept"],
  "WorkitemComment": "Saving Workitem",
  "VoteAction": "",
  "AutomateFastTrack": false,
  "Variables": []
}
```

### Example: Save with Voting Option

```json
{
  "UserEventList": [],
  "WorkitemComment": "Saving Workitem",
  "VoteAction": "Do not approve",
  "AutomateFastTrack": false,
  "Variables": []
}
```

---

## ReassignWorkItems

The `ReassignWorkItems` action reassigns work items or tasks to a specified user.

**This is an unbound action** (not bound to a specific entity instance).

### Request

```http
POST /Windchill/servlet/odata/Workflow/ReassignWorkItems HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `WorkItems` | `Array<Object>` | Yes | List of work item entities. Only the `ID` attribute is considered; other attributes are ignored. |
| `User` | `Object` | Yes | User entity with `ID` property. |
| `Comment` | `String` | No | Optional reassignment comment. |

### Example

```json
{
  "WorkItems": [
    {"ID": "OR:wt.workflow.work.WorkItem:162155"}
  ],
  "User": {"ID": "OR:wt.org.WTUser:11"},
  "Comment": "Reassigning to backup reviewer"
}
```

### Notes

- While reassigning work items, if you pass all the attributes of a work item as input, the action only considers the work item `ID` attribute. Other work item attributes are ignored.
- You can pass either the entity objects or entity IDs as input parameters.
