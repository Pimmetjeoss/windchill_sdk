# Latest Version Search

## Overview

Windchill REST Services provides a mechanism to retrieve only the latest version/iteration of versioned objects. By default, queries to entity sets like `Parts` or `Documents` may return all versions and iterations of each object. The latest version search feature allows clients to filter results to only the most recent version.

## How Versioning Works in Windchill

Windchill objects such as parts and documents use a two-level versioning scheme:

- **Version** (also called Revision): Major version identifier (e.g., A, B, C)
- **Iteration**: Minor version within a revision (e.g., 1, 2, 3)

For example, a part may have versions A.1, A.2, A.3, B.1, B.2 where the latest is B.2.

## Retrieving Latest Versions

### Using the $filter with LatestIteration

To retrieve only the latest iteration of each version, use the `LatestIteration` property:

```http
GET /ProdMgmt/Parts?$filter=LatestIteration eq true
```

### Using the LatestVersion Navigation/Property

To retrieve only the latest version (highest revision, latest iteration), use:

```http
GET /ProdMgmt/Parts?$filter=LatestIteration eq true and IsLatestVersion eq true
```

### Using Prefer Header

Some deployments support a `Prefer` header to request only latest versions:

```http
GET /ProdMgmt/Parts
Prefer: windchill.latestVersion=true
```

---

## Properties for Version Filtering

| Property | Type | Description |
|----------|------|-------------|
| `Version` | Edm.String | Version/revision label (e.g., A, B, C) |
| `Iteration` | Edm.String | Iteration number within the version |
| `LatestIteration` | Edm.Boolean | `true` if this is the latest iteration of its version |
| `IsLatestVersion` | Edm.Boolean | `true` if this is the latest version |
| `CheckoutState` | Edm.String | Checkout state (e.g., `Checked In`, `Checked Out`, `Working Copy`) |

---

## Working Copies

When an object is checked out, Windchill creates a working copy. By default, queries may return both the original and the working copy. To exclude working copies:

```http
GET /ProdMgmt/Parts?$filter=CheckoutState ne 'Working Copy' and LatestIteration eq true
```

To get only the working copies for the current user:

```http
GET /ProdMgmt/Parts?$filter=CheckoutState eq 'Working Copy'
```

---

## Common Patterns

### Get latest iteration of all parts

```http
GET /ProdMgmt/Parts?$filter=LatestIteration eq true
```

### Get latest version and latest iteration (most current)

```http
GET /ProdMgmt/Parts?$filter=LatestIteration eq true and IsLatestVersion eq true
```

### Get latest released parts only

```http
GET /ProdMgmt/Parts?$filter=LatestIteration eq true and State eq 'RELEASED'
```

### Get all versions of a specific part (by number)

```http
GET /ProdMgmt/Parts?$filter=Number eq '0000012345'
```

This returns all versions (A.1, A.2, B.1, etc.) of the part with that number.

### Get only the latest version of a specific part

```http
GET /ProdMgmt/Parts?$filter=Number eq '0000012345' and LatestIteration eq true and IsLatestVersion eq true
```

### Get latest documents

```http
GET /DocMgmt/Documents?$filter=LatestIteration eq true
```

---

## Version History Navigation

To retrieve the full version history of a specific object, use the `Iterations` or `Versions` navigation properties from the PTC common domain:

```http
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Iterations
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Versions
```

Or expand inline:

```http
GET /ProdMgmt/Parts('OR:wt.part.WTPart:12345')?$expand=Versions
```

---

## Notes

1. **Default behavior varies by domain and configuration.** Some Windchill deployments may default to returning only the latest iteration. Check your server configuration.

2. **Performance consideration:** Filtering for latest versions is more efficient than retrieving all versions and filtering client-side. Always use server-side filtering.

3. **Checkout awareness:** When working with checked-out objects, be aware that both the original and working copy may appear in results. Filter by `CheckoutState` as needed.

4. **Saved searches:** If using the SavedSearch domain, the saved search may already include version filtering criteria.
