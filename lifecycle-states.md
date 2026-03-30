# Getting Information About Windchill Life Cycle States

> Source: PTC Windchill REST Services 1.6 Documentation
> Page: `wccg_restapi_lifecycle_state.html`

## Overview

Windchill REST Services provides the ability to retrieve life cycle state information for entities and to set the life cycle state of an entity. Life cycle states represent the stages of an object's life (e.g., In Work, Under Review, Released, Cancelled).

## Retrieving Life Cycle State Information

### Using the LifeCycleState Navigation Property

The `LifeCycleState` navigation property is available on entities that support life cycle management. Use `$expand` to include life cycle state information in the response.

**URL:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=LifeCycleState
```

**Response includes:**
```json
{
  "ID": "OR:wt.part.WTPart:108618",
  "Name": "My Part",
  "Number": "PART-001",
  "State": {
    "Value": "INWORK",
    "Display": "In Work"
  },
  "LifeCycleState": {
    "LifeCycleTemplateName": "Basic",
    "CurrentState": {
      "Value": "INWORK",
      "Display": "In Work"
    },
    "PossibleStates": [
      {
        "Value": "UNDERREVIEW",
        "Display": "Under Review"
      },
      {
        "Value": "CANCELLED",
        "Display": "Cancelled"
      }
    ]
  }
}
```

### Key Fields in LifeCycleState

| Field | Type | Description |
|-------|------|-------------|
| `LifeCycleTemplateName` | `Edm.String` | Name of the life cycle template applied to the object |
| `CurrentState` | Complex Type | The current state with `Value` (internal) and `Display` (localized) |
| `PossibleStates` | Collection | Collection of valid states the object can transition to from its current state |

### Using the State Property

The `State` structural property provides the current state directly on the entity:

```
GET /ProdMgmt/Parts('<oid>')?$select=Name,Number,State
```

**Response:**
```json
{
  "Name": "My Part",
  "Number": "PART-001",
  "State": {
    "Value": "INWORK",
    "Display": "In Work"
  }
}
```

## Filtering by Life Cycle State

Filter entities by their current state:

```
GET /ProdMgmt/Parts?$filter=State/Value eq 'INWORK'
GET /ProdMgmt/Parts?$filter=State/Value eq 'RELEASED'
GET /DocMgmt/Documents?$filter=State/Value eq 'UNDERREVIEW'
```

## Setting the Life Cycle State

### SetLifeCycleState Action

Use the `SetLifeCycleState` action to transition an object to a new life cycle state.

**HTTP Method:** `POST`

**URL Pattern:**
```
POST /ProdMgmt/Parts('<oid>')/PTC.SetLifeCycleState
POST /DocMgmt/Documents('<oid>')/PTC.SetLifeCycleState
POST /ChangeMgmt/ChangeNotices('<oid>')/PTC.SetLifeCycleState
```

**Request Headers:**
| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `CSRF_NONCE` | `<nonce_token>` |

**Request Body:**
```json
{
  "State": "RELEASED"
}
```

The `State` value must be one of the valid states for the object's current life cycle template, and it must be a valid transition from the object's current state. The value is the internal name (e.g., `INWORK`, `UNDERREVIEW`, `RELEASED`, `CANCELLED`).

### Common Life Cycle State Values

The following are common life cycle state values used in Windchill. The exact states available depend on the life cycle template configured for the object.

| Internal Value | Display Name | Description |
|---------------|-------------|-------------|
| `INWORK` | In Work | Object is being created or modified |
| `UNDERREVIEW` | Under Review | Object is under review |
| `RELEASED` | Released | Object is released for production/use |
| `CANCELLED` | Cancelled | Object has been cancelled |
| `OPEN` | Open | Change object is open (Change Management) |
| `RESOLVED` | Resolved | Issue has been resolved (Change Management) |
| `CLOSED` | Closed | Change object is closed (Change Management) |
| `APPROVED` | Approved | Object has been approved |
| `REWORK` | Rework | Object needs rework |
| `IMPLEMENTATION` | Implementation | Change is being implemented |

## Important Notes

- The available states depend on the life cycle template assigned to the object type.
- State transitions must follow the valid transitions defined in the life cycle template. Attempting an invalid transition returns an error.
- Setting the life cycle state may trigger Windchill workflows or other automation.
- Use the `PossibleStates` field from the `LifeCycleState` navigation property to determine valid transitions before attempting to set a new state.
- The CSRF nonce token is required for the `SetLifeCycleState` action.
