# Support for $filter on Navigation Properties

> Source: PTC Windchill REST Services 1.6 Documentation
> Page: `filteringoptions.html`

## Overview

Windchill REST Services supports the OData `$filter` system query option on navigation properties. This enables filtering of entities based on the properties of their related entities using lambda expressions (`any` and `all` operators).

## Lambda Expressions

Lambda expressions allow you to filter a collection of entities based on properties of related entities accessed through navigation properties.

### The `any` Operator

The `any` operator returns entities where **at least one** related entity matches the filter condition.

**Syntax:**
```
$filter=<NavigationProperty>/any(x:x/<Property> <operator> <value>)
```

### The `all` Operator

The `all` operator returns entities where **all** related entities match the filter condition.

**Syntax:**
```
$filter=<NavigationProperty>/all(x:x/<Property> <operator> <value>)
```

## Examples

### Filter Parts by Container Name

Retrieve parts that belong to a container with a specific name:

```
GET /ProdMgmt/Parts?$filter=ContainerReference/any(c:c/Name eq 'MyProduct')
```

### Filter Parts by Folder Path

Retrieve parts in a specific folder:

```
GET /ProdMgmt/Parts?$filter=FolderReference/any(f:f/Name eq 'Design')
```

### Filter Parts by AXL Entries (Supplier)

Retrieve parts that have a specific sourcing status in their AXL entries:

```
GET /ProdMgmt/Parts?$filter=AXLEntries/any(a:a/VendorPartSourcingStatus/Value eq 'approved')
```

### Filter Parts by Sourcing Context and Sourcing Status

```
GET /ProdMgmt/Parts?$filter=AXLEntries/any(a:a/SourcingContext/Name eq 'Global' and a/VendorPartSourcingStatus/Value eq 'approved')
```

### Filter Change Notices by Affected Objects

Retrieve change notices that affect a specific part:

```
GET /ChangeMgmt/ChangeNotices?$filter=AffectedObjects/any(a:a/Number eq 'PART-001')
```

### Filter Documents by Container

```
GET /DocMgmt/Documents?$filter=ContainerReference/any(c:c/Name eq 'MyProduct')
```

## Supported Filter Operators

The following comparison operators are supported within lambda expressions:

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equal | `x/Name eq 'value'` |
| `ne` | Not equal | `x/Name ne 'value'` |
| `gt` | Greater than | `x/CreatedOn gt 2024-01-01T00:00:00Z` |
| `ge` | Greater than or equal | `x/Quantity ge 10` |
| `lt` | Less than | `x/Quantity lt 100` |
| `le` | Less than or equal | `x/Quantity le 50` |

## Supported Filter Functions

The following string functions can be used within lambda expressions:

| Function | Description | Example |
|----------|-------------|---------|
| `contains` | String contains | `$filter=NavigationProp/any(x:contains(x/Name,'search'))` |
| `startswith` | String starts with | `$filter=NavigationProp/any(x:startswith(x/Name,'prefix'))` |
| `endswith` | String ends with | `$filter=NavigationProp/any(x:endswith(x/Name,'suffix'))` |

## Combining Lambda Expressions with Direct Filters

You can combine lambda expressions on navigation properties with direct property filters using logical operators (`and`, `or`):

```
GET /ProdMgmt/Parts?$filter=State/Value eq 'INWORK' and AXLEntries/any(a:a/VendorPartSourcingStatus/Value eq 'approved')
```

## Combining with Other Query Options

Lambda expressions can be combined with `$select`, `$expand`, `$orderby`, `$top`, and `$skip`:

```
GET /ProdMgmt/Parts?$filter=AXLEntries/any(a:a/VendorPartSourcingStatus/Value eq 'approved')&$expand=AXLEntries&$select=Name,Number&$top=20
```

## Limitations

- Not all navigation properties support `$filter` with lambda expressions. Refer to the domain EDM metadata for supported navigation properties.
- The `all` operator may not be supported on all navigation properties.
- Nested lambda expressions (lambda within lambda) are not supported.
- Deep filtering on more than one level of navigation (e.g., filtering on a property of a property of a navigation property) may not be supported for all entity types.
- Performance may be affected when filtering on large collections of related entities.
