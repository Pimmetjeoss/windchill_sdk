# Product Platform Management Domain (ProdPlatformMgmt)

## Overview

The Product Platform Management domain provides REST API access to product platforms, options, choices, and expressions used for configurable product structures in Windchill.

**Domain Name:** `ProdPlatformMgmt`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/ProdPlatformMgmt
```

**Metadata URL:**
```
GET /ProdPlatformMgmt/$metadata
```

## Entity Sets

### Platforms

Represents product platforms.

**Entity Set URL:**
```
GET /ProdPlatformMgmt/Platforms
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Platform name |
| `Number` | Edm.String | Platform number |
| `Description` | Edm.String | Platform description |
| `State` | Edm.String | Lifecycle state |
| `Version` | Edm.String | Version identifier |
| `Iteration` | Edm.String | Iteration identifier |
| `ContainerName` | Edm.String | Container name |
| `ContainerID` | Edm.String | Container ID |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `OptionSets` | OptionSets | Option sets defined in this platform |
| `Options` | Options | Options within this platform |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve platforms |
| POST | Create a new platform |
| PATCH | Update a platform |

---

### OptionSets

Represents option sets (groups of related options).

**Entity Set URL:**
```
GET /ProdPlatformMgmt/OptionSets
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Option set name |
| `Description` | Edm.String | Option set description |
| `PlatformID` | Edm.String | Reference to parent platform |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Choices` | Choices | Choices within this option set |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve option sets |
| POST | Create a new option set |
| PATCH | Update an option set |

---

### Options

Represents configurable options.

**Entity Set URL:**
```
GET /ProdPlatformMgmt/Options
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Option name |
| `Description` | Edm.String | Option description |
| `OptionSetID` | Edm.String | Reference to parent option set |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Choices` | Choices | Choices for this option |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve options |
| POST | Create a new option |
| PATCH | Update an option |

---

### Choices

Represents individual choices (values) for an option.

**Entity Set URL:**
```
GET /ProdPlatformMgmt/Choices
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Choice name |
| `Description` | Edm.String | Choice description |
| `OptionID` | Edm.String | Reference to parent option |
| `OptionSetID` | Edm.String | Reference to option set |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve choices |
| POST | Create a new choice |
| PATCH | Update a choice |

---

### Expressions

Represents configuration expressions (rules) that define valid combinations of options.

**Entity Set URL:**
```
GET /ProdPlatformMgmt/Expressions
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Expression name |
| `Expression` | Edm.String | Expression string |
| `ExpressionType` | Edm.String | Type of expression |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve expressions |

---

## Actions

### ProdPlatformMgmt.AssignOptionSet

Assigns an option set to a product platform.

**Bound to:** Platform entity instance

**URL Pattern:**
```
POST /ProdPlatformMgmt/Platforms('...')/ProdPlatformMgmt.AssignOptionSet
```

**Request Body:**
```json
{
  "OptionSetID": "OR:com.ptc.windchill.option.model.OptionSet:12345"
}
```

---

## Query Examples

**Get all platforms:**
```http
GET /ProdPlatformMgmt/Platforms
```

**Get option sets for a platform:**
```http
GET /ProdPlatformMgmt/Platforms('OR:com.ptc.windchill.option.model.OptionPool:12345')/OptionSets
```

**Get choices for an option:**
```http
GET /ProdPlatformMgmt/Options('OR:com.ptc.windchill.option.model.Option:12345')/Choices
```

**Expand options on a platform:**
```http
GET /ProdPlatformMgmt/Platforms('...')?$expand=Options
```

**Filter platforms by state:**
```http
GET /ProdPlatformMgmt/Platforms?$filter=State eq 'RELEASED'
```
