# OData Primitive and Complex Types in Windchill REST Services

## Overview

Windchill REST Services uses a subset of OData v4 primitive types for entity properties, along with several Windchill-specific complex types. This reference documents all supported types for use in queries, POST/PATCH payloads, and response parsing.

## Supported Primitive Types

| OData Type | Description | Example Value | JSON Representation |
|---|---|---|---|
| `Edm.String` | Unicode text string | `"Bracket Assembly"` | `"Bracket Assembly"` |
| `Edm.Int16` | 16-bit signed integer | `42` | `42` |
| `Edm.Int32` | 32-bit signed integer | `100000` | `100000` |
| `Edm.Int64` | 64-bit signed integer | `9999999999` | `9999999999` |
| `Edm.Boolean` | True/false value | `true` | `true` |
| `Edm.DateTimeOffset` | Date and time with timezone offset (ISO 8601) | `2026-03-15T10:30:00Z` | `"2026-03-15T10:30:00Z"` |
| `Edm.Single` | 32-bit IEEE 754 floating point | `3.14` | `3.14` |
| `Edm.Double` | 64-bit IEEE 754 floating point | `3.141592653589793` | `3.141592653589793` |

### String Usage

Strings are the most common type. Most Windchill properties (Number, Name, Description, State, etc.) are strings.

```
$filter=Name eq 'Bracket'
$filter=contains(Name,'Bracket')
$filter=startswith(Number,'BRK-')
```

### Numeric Usage

Numeric types are used for quantities, line numbers, and similar values.

```
$filter=LineNumber gt 10
$filter=Quantity ge 5
```

### Boolean Usage

Boolean properties use `true` or `false` (lowercase in JSON, no quotes).

```
$filter=Latest eq true
```

### DateTimeOffset Usage

All date/time values use ISO 8601 format with timezone offset. Windchill typically stores times in UTC.

```
$filter=CreatedOn gt 2026-01-01T00:00:00Z
$filter=ModifiedOn ge 2026-03-01T00:00:00Z and ModifiedOn lt 2026-04-01T00:00:00Z
$orderby=CreatedOn desc
```

In JSON request/response bodies:

```json
{
  "CreatedOn": "2026-03-15T10:30:00Z",
  "ModifiedOn": "2026-03-15T14:45:30Z",
  "ExpirationDate": "2027-12-31T23:59:59Z"
}
```

## Complex Types

Complex types are structured values composed of multiple properties. They are not independently addressable entities -- they exist only as property values on entities.

### QuantityOfMeasureType

Represents a numeric value with a unit of measure. Used for part quantities, weights, dimensions, etc.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `Value` | `Edm.Double` | The numeric value |
| `Unit` | `Edm.String` | The unit of measure code (e.g., `EA`, `kg`, `mm`) |

**JSON Example:**

```json
{
  "Quantity": {
    "Value": 2.5,
    "Unit": "kg"
  }
}
```

**In $filter:**

```
$filter=Quantity/Value gt 1.0
```

### Hyperlink

Represents a URL hyperlink with display text.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `URL` | `Edm.String` | The URL |
| `Description` | `Edm.String` | Display text for the link |

**JSON Example:**

```json
{
  "Reference": {
    "URL": "https://example.com/spec.pdf",
    "Description": "Product Specification Document"
  }
}
```

### Icon

Represents an icon image reference.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `URL` | `Edm.String` | URL of the icon image |

**JSON Example:**

```json
{
  "TypeIcon": {
    "URL": "/Windchill/servlet/rest/icons/part.png"
  }
}
```

### EnumType

OData enumeration types represent a fixed set of named values. Windchill uses these for properties with a defined list of valid values.

**Common EnumType Properties:**

| Property | Enum Values | Description |
|---|---|---|
| `Source` | `MAKE`, `BUY`, `MAKE_OR_BUY` | Part source type |
| `State` (lifecycle) | `INWORK`, `UNDERREVIEW`, `RELEASED`, `CANCELLED`, etc. | Lifecycle state |

**JSON Example:**

```json
{
  "Source": "MAKE",
  "State": "INWORK"
}
```

**In $filter:**

```
$filter=Source eq 'MAKE'
$filter=State eq 'RELEASED'
```

Note: Although these are semantically enumerations, they are often represented as `Edm.String` in the EDM with validation enforced server-side.

### ClassificationInfo

Represents classification metadata for classifiable entities. Available when the `classifiable` capability is inherited.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `ClassificationNodeId` | `Edm.String` | ID of the classification node |
| `ClassificationNodeName` | `Edm.String` | Display name of the classification node |
| `Attributes` | Complex | Classification attribute name-value pairs |

**JSON Example:**

```json
{
  "ClassificationInfo": {
    "ClassificationNodeId": "node_12345",
    "ClassificationNodeName": "Fasteners > Bolts > Hex Bolts",
    "Attributes": {
      "ThreadSize": "M10",
      "Length": "50",
      "Material": "Stainless Steel 304",
      "HeadType": "Hex"
    }
  }
}
```

## Type Mapping: Windchill to OData

| Windchill Java Type | OData Type |
|---|---|
| `java.lang.String` | `Edm.String` |
| `java.lang.Boolean` / `boolean` | `Edm.Boolean` |
| `java.lang.Integer` / `int` | `Edm.Int32` |
| `java.lang.Long` / `long` | `Edm.Int64` |
| `java.lang.Short` / `short` | `Edm.Int16` |
| `java.lang.Float` / `float` | `Edm.Single` |
| `java.lang.Double` / `double` | `Edm.Double` |
| `java.sql.Timestamp` | `Edm.DateTimeOffset` |
| `wt.units.QuantityOfMeasure` | `QuantityOfMeasureType` |

## Null Handling

- Properties can be null unless declared `Nullable="false"` in the EDM.
- In JSON, null values are represented as `null`:

```json
{
  "Description": null,
  "ExpirationDate": null
}
```

- To filter for null: `$filter=Description eq null`
- To filter for non-null: `$filter=Description ne null`

## Notes

- Always check the domain `$metadata` to confirm the exact type of a property.
- `Edm.DateTimeOffset` values must include timezone information. UTC (`Z` suffix) is recommended.
- Complex type properties can be accessed with path syntax in `$filter` and `$select` (e.g., `Quantity/Value`).
- Numeric overflow (e.g., sending a value too large for `Int16`) returns a `400 Bad Request` error.
