# $orderby Sorting Options and Navigation Property Filtering

## Overview

Windchill REST Services supports `$orderby` for sorting results and provides special support for `$filter` and `$orderby` on navigation properties. This page covers the advanced sorting and filtering capabilities.

## $orderby on Structural Properties

### Basic Sorting

Sort by a single property:
```http
GET /ProdMgmt/Parts?$orderby=Name asc
GET /ProdMgmt/Parts?$orderby=CreatedOn desc
```

### Multi-Property Sorting

Sort by multiple properties (comma-separated):
```http
GET /ProdMgmt/Parts?$orderby=State asc,Name asc
GET /ProdMgmt/Parts?$orderby=Version desc,Iteration desc
```

### Sort Direction

| Direction | Keyword | Description |
|-----------|---------|-------------|
| Ascending | `asc` | Default. Smallest to largest (A-Z, oldest to newest) |
| Descending | `desc` | Largest to smallest (Z-A, newest to oldest) |

If no direction is specified, `asc` is the default.

---

## $orderby on Navigation Properties

Windchill REST Services supports sorting entity sets based on properties of related (navigated) entities. This is useful when you want to sort a collection based on a property of a related entity.

### Syntax

```
$orderby=NavigationProperty/Property direction
```

### Example

Sort parts by their associated document name:
```http
GET /ProdMgmt/Parts?$orderby=UsesPartDocuments/Name asc
```

### Limitations

- Only single-level navigation is supported for `$orderby`.
- The navigation property must be a single-valued navigation (not a collection).
- Not all navigation properties support `$orderby`. Check the domain metadata for supported navigations.

---

## $filter on Navigation Properties

Windchill REST Services supports filtering entity sets based on properties of related entities using the `any` and `all` lambda operators.

### any Operator

The `any` operator returns entities where at least one related entity matches the condition.

**Syntax:**
```
$filter=NavigationProperty/any(alias:alias/Property operator value)
```

**Examples:**

Filter parts that have at least one document with state RELEASED:
```http
GET /ProdMgmt/Parts?$filter=UsesPartDocuments/any(d:d/State eq 'RELEASED')
```

Filter parts that have at least one attachment with a specific name:
```http
GET /ProdMgmt/Parts?$filter=Attachments/any(a:contains(a/FileName,'spec'))
```

### all Operator

The `all` operator returns entities where every related entity matches the condition.

**Syntax:**
```
$filter=NavigationProperty/all(alias:alias/Property operator value)
```

**Example:**

Filter parts where all documents are in RELEASED state:
```http
GET /ProdMgmt/Parts?$filter=UsesPartDocuments/all(d:d/State eq 'RELEASED')
```

### Single-Valued Navigation

For single-valued navigation properties, you can reference the property directly:

```http
GET /ProdMgmt/Parts?$filter=Container/Name eq 'Engine Product'
```

### Nested Conditions

Combine navigation property filters with structural property filters:
```http
GET /ProdMgmt/Parts?$filter=State eq 'RELEASED' and UsesPartDocuments/any(d:d/State eq 'RELEASED')
```

---

## Sortable Properties by Domain

Not all properties support sorting. The following general rules apply:

| Property Type | Sortable | Notes |
|--------------|----------|-------|
| Edm.String | Yes | Case-sensitive sorting |
| Edm.Int32 / Edm.Int64 | Yes | Numeric sorting |
| Edm.Decimal | Yes | Numeric sorting |
| Edm.DateTimeOffset | Yes | Chronological sorting |
| Edm.Boolean | Yes | false before true |
| Complex properties | No | Not directly sortable |
| Collection properties | No | Not sortable |

---

## Common Sorting Patterns

**Most recently modified first:**
```http
GET /ProdMgmt/Parts?$orderby=LastModified desc
```

**Alphabetical by name:**
```http
GET /ProdMgmt/Parts?$orderby=Name asc
```

**By version and iteration (latest first):**
```http
GET /ProdMgmt/Parts?$orderby=Version desc,Iteration desc
```

**By state then by name:**
```http
GET /ProdMgmt/Parts?$orderby=State asc,Name asc
```

**Combined with filtering and paging:**
```http
GET /ProdMgmt/Parts?$filter=State eq 'RELEASED'&$orderby=LastModified desc&$top=25&$skip=0
```
