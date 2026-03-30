# Creating a Part

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesCreatePart.html`

## Overview

Create a new part (WTPart) in Windchill using the PTC Product Management domain. This operation uses an HTTP POST request to the Parts entity set.

## Endpoint

```
POST https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Parts
```

- **Domain**: ProdMgmt (PTC Product Management)
- **Entity Set**: `Parts`
- **HTTP Method**: POST
- **Mapped Windchill Type**: `wt.part.WTPart`

## Request

### Headers

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `Accept` | `application/json` |
| `CSRF_NONCE` | `<nonce_value>` |

> **Prerequisite**: Fetch the NONCE token first using `GET /Windchill/servlet/odata/PTC/GetCSRFToken()`. See [example-fetch-nonce.md](example-fetch-nonce.md).

### Request Body

```json
{
  "Number": "0000000123",
  "Name": "Test Part",
  "Description": "A test part created via REST API",
  "DefaultUnit": "ea",
  "Source": "Make",
  "TypeID": "wt.part.WTPart",
  "ContainerID": "OR:wt.pdmlink.PDMLinkProduct:12345",
  "FolderPath": "/Default/Design"
}
```

### Request Body Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `Number` | String | No | Part number. If omitted, Windchill auto-generates one based on configured numbering scheme. |
| `Name` | String | Yes | Display name of the part |
| `Description` | String | No | Description of the part |
| `DefaultUnit` | String | No | Default unit of measure (e.g., `ea`, `kg`, `m`) |
| `Source` | String | No | Source type: `Make`, `Buy`, or `Make or Buy` |
| `TypeID` | String | No | The Windchill type identifier. Defaults to `wt.part.WTPart`. Use soft type internal names for subtypes (e.g., `com.ptc.MyCustomPart`). |
| `ContainerID` | String | No | Object reference of the target product/library container (e.g., `OR:wt.pdmlink.PDMLinkProduct:12345`). If omitted, uses the user's default container. |
| `FolderPath` | String | No | Folder path within the container where the part will be created. Must start with `/Default`. |
| `View` | String | No | View of the part (e.g., `Design`, `Manufacturing`) |
| `PartType` | String | No | Part type classification: `Separable`, `Inseparable`, or `Component` |
| `GatheringPart` | Boolean | No | Whether this is a gathering part |

## Response

### HTTP Status

- **201 Created** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/$metadata#Parts/$entity",
  "ID": "OR:wt.part.WTPart:123456",
  "Number": "0000000123",
  "Name": "Test Part",
  "Description": "A test part created via REST API",
  "State": "In Work",
  "Version": "A",
  "Iteration": "1",
  "VersionID": "A.1",
  "LatestIteration": true,
  "CheckoutState": "Checked In",
  "DefaultUnit": "ea",
  "Source": "Make",
  "PartType": "Separable",
  "GatheringPart": false,
  "View": "Design",
  "CreatedOn": "2024-01-15T10:30:00Z",
  "LastModified": "2024-01-15T10:30:00Z",
  "TypeID": "wt.part.WTPart"
}
```

### Key Response Properties

| Property | Type | Description |
|----------|------|-------------|
| `ID` | String | Object reference identifier in the format `OR:wt.part.WTPart:<dbid>` |
| `Number` | String | Part number |
| `Name` | String | Display name |
| `State` | String | Life cycle state (e.g., `In Work`, `Released`) |
| `Version` | String | Version letter (e.g., `A`, `B`) |
| `Iteration` | String | Iteration number within the version |
| `VersionID` | String | Combined version and iteration (e.g., `A.1`) |
| `LatestIteration` | Boolean | Whether this is the latest iteration |
| `CheckoutState` | String | Checkout status: `Checked In`, `Checked Out`, `Checked Out by Another User` |
| `CreatedOn` | DateTimeOffset | Creation timestamp |
| `LastModified` | DateTimeOffset | Last modification timestamp |

## Notes

- The `ContainerID` must reference an existing Product or Library that the user has access to.
- If `FolderPath` is specified, the folder must already exist within the container.
- The newly created part starts in the `In Work` life cycle state.
- The part is created at version `A`, iteration `1`.
- Auto-numbering: if `Number` is not provided, Windchill generates a number based on the object type's numbering scheme.
- To create parts of a specific soft type, set `TypeID` to the internal name of the soft type.
