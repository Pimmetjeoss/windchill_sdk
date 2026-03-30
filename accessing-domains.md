# Accessing Domains

> Source: PTC Windchill REST Services 1.6 Documentation
> Page: `WCCG_RESTAPIsAccess.html`

## Overview

Windchill REST Services organizes its OData services into domains. Each domain represents a functional area of Windchill and provides access to related entities, actions, and functions. All domains are accessed through the base OData servlet URL.

## Base URL

All Windchill REST Services endpoints start with the base URL:

```
https://<windchill_host>/Windchill/servlet/odata
```

For example:
```
https://windchill.example.com/Windchill/servlet/odata
```

## Accessing a Domain

Each domain is accessed by appending its name to the base URL:

```
GET /servlet/odata/<DomainName>
```

This returns the service document for the domain, which lists all available entity sets.

### Examples

```
GET /servlet/odata/ProdMgmt          -- Product Management
GET /servlet/odata/DocMgmt           -- Document Management
GET /servlet/odata/ChangeMgmt        -- Change Management
GET /servlet/odata/DataAdmin         -- Data Administration
GET /servlet/odata/PrincipalMgmt     -- Principal Management
GET /servlet/odata/PTC               -- Common Domain
GET /servlet/odata/NavCriteria       -- Navigation Criteria
GET /servlet/odata/DynDocMgmt        -- Dynamic Document Management
GET /servlet/odata/PartsListMgmt     -- Parts List Management
GET /servlet/odata/ServiceInfoMgmt   -- Service Information Management
GET /servlet/odata/InfoEngine        -- Info*Engine
GET /servlet/odata/Factory           -- Factory
GET /servlet/odata/MfgProcessMgmt    -- Manufacturing Process Management
GET /servlet/odata/ChangeMgmt        -- Change Management
GET /servlet/odata/ClfStructure      -- Classification Structure
GET /servlet/odata/SavedSearch       -- Saved Search
GET /servlet/odata/Visualization     -- Visualization
GET /servlet/odata/ProdPlatformMgmt  -- Product Platform Management
GET /servlet/odata/CADDocMgmt        -- CAD Document Management
GET /servlet/odata/EffectivityMgmt   -- Effectivity Management
GET /servlet/odata/EventMgmt         -- Event Management
GET /servlet/odata/SupplierMgmt      -- Supplier Management
GET /servlet/odata/Workflow           -- Workflow
GET /servlet/odata/PDM               -- PDM
```

## Service Document

The service document returns the available entity sets within a domain:

```
GET /servlet/odata/ProdMgmt
```

**Response:**
```json
{
  "@odata.context": "/servlet/odata/ProdMgmt/$metadata",
  "value": [
    {
      "name": "Parts",
      "kind": "EntitySet",
      "url": "Parts"
    },
    {
      "name": "ManufacturerParts",
      "kind": "EntitySet",
      "url": "ManufacturerParts"
    },
    {
      "name": "VendorParts",
      "kind": "EntitySet",
      "url": "VendorParts"
    }
  ]
}
```

## Entity Data Model (EDM) Metadata

Retrieve the full metadata (EDM) for a domain to see all entities, properties, navigation properties, actions, and functions:

```
GET /servlet/odata/ProdMgmt/$metadata
```

The metadata response is in XML format (CSDL) and describes:
- Entity types and their properties
- Complex types
- Navigation properties
- Entity sets
- Bound and unbound actions
- Bound and unbound functions
- Annotations

## Accessing Entity Sets

Once you know the domain and entity set name, access entities using:

```
GET /servlet/odata/<DomainName>/<EntitySet>
GET /servlet/odata/<DomainName>/<EntitySet>('<oid>')
```

### Examples

```
GET /servlet/odata/ProdMgmt/Parts
GET /servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:108618')
GET /servlet/odata/DocMgmt/Documents
GET /servlet/odata/ChangeMgmt/ChangeNotices
```

## Authentication

Windchill REST Services uses the same authentication as the Windchill server. Requests must include valid authentication credentials. Common methods include:

- **Basic Authentication:** Include `Authorization: Basic <base64(username:password)>` header
- **SSO / Windchill session:** Use an existing authenticated session

## Common Request Headers

| Header | Description | Required |
|--------|-------------|----------|
| `Accept` | Response format: `application/json` | Recommended |
| `Content-Type` | Request body format: `application/json` | For POST/PATCH |
| `CSRF_NONCE` | CSRF token for write operations | For POST/PATCH/DELETE |
| `Prefer` | OData preference headers (e.g., `odata.maxpagesize=50`) | Optional |

## OData Query Options

All standard OData query options are supported:

| Query Option | Description | Example |
|-------------|-------------|---------|
| `$select` | Select specific properties | `?$select=Name,Number` |
| `$filter` | Filter results | `?$filter=Name eq 'Test'` |
| `$expand` | Expand navigation properties | `?$expand=ContainerReference` |
| `$orderby` | Sort results | `?$orderby=Name asc` |
| `$top` | Limit number of results | `?$top=10` |
| `$skip` | Skip results (pagination) | `?$skip=20` |
| `$count` | Include count of results | `?$count=true` |
| `$search` | Full-text search | `?$search=keyword` |

## Pagination

By default, Windchill REST Services returns a limited number of results per page. Use the `Prefer` header or `$top`/`$skip` for pagination:

```
GET /ProdMgmt/Parts?$top=50&$skip=0
```

Or use the `Prefer` header:
```
Prefer: odata.maxpagesize=100
```

When more results are available, the response includes an `@odata.nextLink` property with the URL to the next page of results.
