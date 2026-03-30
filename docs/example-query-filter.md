# Querying and Filtering Parts

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesQueryFilter.html`

## Overview

Use OData query options to search, filter, sort, and paginate entity sets in Windchill REST Services. This example demonstrates querying the Parts entity set in the PTC Product Management domain.

## Base Endpoint

```
GET https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Parts
```

- **Domain**: ProdMgmt (PTC Product Management)
- **Entity Set**: `Parts`
- **HTTP Method**: GET

## Supported OData Query Options

| Option | Description |
|--------|-------------|
| `$filter` | Filter results based on criteria |
| `$select` | Select specific properties to return |
| `$expand` | Expand navigation properties inline |
| `$orderby` | Sort results by property |
| `$top` | Limit the number of results |
| `$skip` | Skip a number of results (for pagination) |
| `$count` | Include total count of matching entities |
| `$search` | Full-text keyword search |

## Filter Examples

### Filter by Part Number

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=Number eq '0000000123'
```

### Filter by Name (Contains)

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=contains(Name,'Bracket')
```

### Filter by Name (Starts With)

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=startswith(Name,'Test')
```

### Filter by Life Cycle State

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=State eq 'In Work'
```

### Filter by Checkout State

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=CheckoutState eq 'Checked Out'
```

### Filter by Created Date (DateTimeOffset)

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=CreatedOn gt 2024-01-01T00:00:00Z
```

### Filter with Multiple Conditions (AND)

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=State eq 'In Work' and Source eq 'Make'
```

### Filter with OR Condition

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=Source eq 'Make' or Source eq 'Buy'
```

### Filter by Latest Iteration Only

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=LatestIteration eq true
```

### Custom Query: Latest Version Search

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?ptc.search.latestversion=true
```

## Supported Filter Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equal | `Number eq '0000000123'` |
| `ne` | Not equal | `State ne 'Released'` |
| `gt` | Greater than | `CreatedOn gt 2024-01-01T00:00:00Z` |
| `ge` | Greater than or equal | `Quantity ge 10` |
| `lt` | Less than | `Quantity lt 100` |
| `le` | Less than or equal | `LastModified le 2024-12-31T23:59:59Z` |
| `and` | Logical AND | `State eq 'In Work' and Source eq 'Make'` |
| `or` | Logical OR | `Source eq 'Make' or Source eq 'Buy'` |
| `not` | Logical NOT | `not contains(Name,'Test')` |

## Supported Filter Functions

| Function | Description | Example |
|----------|-------------|---------|
| `contains(property, value)` | Substring match | `contains(Name,'Bracket')` |
| `startswith(property, value)` | Prefix match | `startswith(Number,'000')` |
| `endswith(property, value)` | Suffix match | `endswith(Name,'Assembly')` |

## Selecting Specific Properties

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$select=ID,Number,Name,State,Version
```

## Sorting Results

### Sort Ascending

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$orderby=Number asc
```

### Sort Descending

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$orderby=LastModified desc
```

### Multi-column Sort

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$orderby=State asc,Number desc
```

## Pagination

### Limit Results

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$top=10
```

### Skip and Top (Page 2)

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$skip=10&$top=10
```

### Include Count

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$count=true&$top=10
```

### Server-Side Paging

If the result set exceeds the server's page size, the response includes an `@odata.nextLink` property:

```json
{
  "@odata.context": "...",
  "@odata.nextLink": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/Parts?$skiptoken=10",
  "value": [...]
}
```

Follow the `@odata.nextLink` URL to get the next page of results.

## Combined Query Example

Get the first 10 in-work parts containing "Bracket" in the name, sorted by creation date, with only key properties:

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=State eq 'In Work' and contains(Name,'Bracket')&$select=ID,Number,Name,State,CreatedOn&$orderby=CreatedOn desc&$top=10&$count=true
```

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/$metadata#Parts(ID,Number,Name,State,CreatedOn)",
  "@odata.count": 42,
  "value": [
    {
      "ID": "OR:wt.part.WTPart:123456",
      "Number": "0000000456",
      "Name": "Mounting Bracket",
      "State": "In Work",
      "CreatedOn": "2024-01-20T14:30:00Z"
    },
    {
      "ID": "OR:wt.part.WTPart:123457",
      "Number": "0000000789",
      "Name": "Support Bracket Assembly",
      "State": "In Work",
      "CreatedOn": "2024-01-19T09:15:00Z"
    }
  ]
}
```

## Notes

- All query options can be combined in a single request.
- URL encoding may be necessary for special characters in filter values.
- The server applies a default page size. Use `$top` to control page size or follow `@odata.nextLink` for additional pages.
- String comparisons in `$filter` are case-sensitive by default.
- The `$search` option performs a keyword search across searchable properties.
- The `ptc.search.latestversion=true` custom query option limits results to the latest version of each entity.
- Filter on navigation properties is supported using `$filter` on `$expand` (e.g., `$expand=Uses($filter=Quantity gt 1)`).
