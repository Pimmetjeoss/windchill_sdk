# OData Query Parameters

## Overview

Windchill REST Services supports a subset of OData v4 query parameters for filtering, selecting, ordering, paging, and expanding entity data. These query parameters can be appended to entity set URLs.

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/<Domain>/<EntitySet>?<query-parameters>
```

## Supported Query Parameters

### $select

Specifies a subset of properties to return. Reduces response payload size.

**Syntax:**
```
$select=Property1,Property2,Property3
```

**Examples:**
```http
GET /ProdMgmt/Parts?$select=Name,Number,State
GET /DocMgmt/Documents?$select=Name,Number,Version,Iteration
```

---

### $filter

Filters the entity set based on conditions.

**Syntax:**
```
$filter=<expression>
```

**Supported Filter Operators:**

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equal | `$filter=State eq 'INWORK'` |
| `ne` | Not equal | `$filter=State ne 'CANCELLED'` |
| `gt` | Greater than | `$filter=CreatedOn gt 2024-01-01T00:00:00Z` |
| `ge` | Greater than or equal | `$filter=CreatedOn ge 2024-01-01T00:00:00Z` |
| `lt` | Less than | `$filter=CreatedOn lt 2024-12-31T23:59:59Z` |
| `le` | Less than or equal | `$filter=CreatedOn le 2024-12-31T23:59:59Z` |
| `and` | Logical AND | `$filter=State eq 'INWORK' and Version eq 'A'` |
| `or` | Logical OR | `$filter=State eq 'INWORK' or State eq 'RELEASED'` |
| `not` | Logical NOT | `$filter=not contains(Name,'test')` |

**Supported Filter Functions:**

| Function | Description | Example |
|----------|-------------|---------|
| `contains(property,value)` | String contains | `$filter=contains(Name,'bolt')` |
| `startswith(property,value)` | String starts with | `$filter=startswith(Number,'000')` |
| `endswith(property,value)` | String ends with | `$filter=endswith(Name,'Assembly')` |
| `length(property)` | String length | `$filter=length(Name) gt 10` |
| `tolower(property)` | Lowercase comparison | `$filter=tolower(Name) eq 'bolt'` |
| `toupper(property)` | Uppercase comparison | `$filter=toupper(Name) eq 'BOLT'` |

**Examples:**
```http
GET /ProdMgmt/Parts?$filter=State eq 'RELEASED'
GET /ProdMgmt/Parts?$filter=contains(Name,'valve') and State eq 'INWORK'
GET /ProdMgmt/Parts?$filter=CreatedOn ge 2024-01-01T00:00:00Z
GET /ProdMgmt/Parts?$filter=startswith(Number,'0000') and Version eq 'A'
```

**Filtering on Navigation Properties:**

You can filter on navigation properties using the `any` lambda operator:

```http
GET /ProdMgmt/Parts?$filter=UsesPartDocuments/any(d:d/Name eq 'Spec Sheet')
```

See the [orderby-sorting-options.md](orderby-sorting-options.md) for details on `$filter` with navigation properties.

---

### $orderby

Sorts the result set by one or more properties.

**Syntax:**
```
$orderby=Property1 asc,Property2 desc
```

If no direction is specified, ascending (`asc`) is the default.

**Examples:**
```http
GET /ProdMgmt/Parts?$orderby=Name asc
GET /ProdMgmt/Parts?$orderby=CreatedOn desc
GET /ProdMgmt/Parts?$orderby=State asc,Name asc
```

---

### $top

Limits the number of results returned.

**Syntax:**
```
$top=<integer>
```

**Examples:**
```http
GET /ProdMgmt/Parts?$top=10
GET /ProdMgmt/Parts?$top=50&$orderby=CreatedOn desc
```

---

### $skip

Skips the specified number of results. Used with `$top` for paging.

**Syntax:**
```
$skip=<integer>
```

**Examples:**
```http
GET /ProdMgmt/Parts?$top=10&$skip=0    (page 1)
GET /ProdMgmt/Parts?$top=10&$skip=10   (page 2)
GET /ProdMgmt/Parts?$top=10&$skip=20   (page 3)
```

---

### $expand

Expands navigation properties inline, fetching related entities in the same request.

**Syntax:**
```
$expand=NavigationProperty
$expand=NavigationProperty1,NavigationProperty2
$expand=NavigationProperty($select=Prop1,Prop2)
$expand=NavigationProperty($filter=<expression>)
$expand=NavigationProperty($top=5)
```

**Examples:**
```http
GET /ProdMgmt/Parts('...')?$expand=UsesPartDocuments
GET /ProdMgmt/Parts('...')?$expand=UsesPartDocuments($select=Name,Number)
GET /ProdMgmt/Parts?$expand=Attachments
GET /ProdMgmt/Parts('...')?$expand=UsesPartDocuments($filter=State eq 'RELEASED')
```

**Nested expand:**
```http
GET /ProdMgmt/Parts('...')?$expand=UsesPartDocuments($expand=Attachments)
```

---

### $count

Returns the count of entities in the result set.

**Syntax:**
```
$count=true
```

When set to `true`, the response includes an `@odata.count` property with the total count.

**Example:**
```http
GET /ProdMgmt/Parts?$count=true&$top=10
```

**Response:**
```json
{
  "@odata.context": "...",
  "@odata.count": 1523,
  "value": [ ... ]
}
```

---

### $search

Performs a free-text search on the entity set.

**Syntax:**
```
$search="keyword"
```

**Example:**
```http
GET /ProdMgmt/Parts?$search="valve assembly"
```

> Note: `$search` support may vary by entity set and domain.

---

## Server-Side Paging

Windchill REST Services implements server-side paging. When a result set exceeds the server page size, the response includes an `@odata.nextLink` property containing the URL to fetch the next page of results.

**Example Response with Next Link:**
```json
{
  "@odata.context": "...",
  "value": [ ... ],
  "@odata.nextLink": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/Parts?$skiptoken=100"
}
```

To get the next page, issue a GET request to the `@odata.nextLink` URL.

---

## Combining Query Parameters

Multiple query parameters can be combined with `&`:

```http
GET /ProdMgmt/Parts?$filter=State eq 'RELEASED'&$select=Name,Number,Version&$orderby=Name asc&$top=25&$skip=0&$count=true&$expand=Attachments
```

## Notes

- Not all query parameters are supported on all entity sets. Check the domain metadata for supported capabilities.
- The `$filter` function support may be limited for certain property types (e.g., complex properties).
- Server-side paging limits are configured on the Windchill server. The default page size varies by deployment.
- `$skip` values must be non-negative integers.
- `$top` values must be positive integers.
