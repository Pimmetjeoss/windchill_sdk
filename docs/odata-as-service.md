# OData Services as Domains

## Overview

In PTC Windchill REST Services, **OData services are implemented as domains**. Each domain is an independent OData service that exposes a subset of Windchill functionality through a standardized OData v4 interface.

## Concept

A **domain** maps Windchill types (Java classes) to **OData entity types**, and Windchill collections to **OData entity sets**. The domain's URL serves as the OData service root, providing a uniform interface for all CRUD operations, queries, actions, and functions.

```
OData Service  =  Domain
Entity Types   =  Windchill object types (mapped)
Entity Sets    =  Collections of Windchill objects
Service Root   =  Domain base URL
```

## URL Structure

All domain URLs follow this pattern:

```
https://{server}/Windchill/servlet/odata/{DomainID}
```

### Standard OData URLs

| URL Pattern | Description |
|---|---|
| `/{DomainID}` | Service document -- lists all entity sets |
| `/{DomainID}/$metadata` | EDM metadata document (CSDL XML) |
| `/{DomainID}/{EntitySet}` | Query an entity set (collection) |
| `/{DomainID}/{EntitySet}('{key}')` | Get a single entity by key |
| `/{DomainID}/{EntitySet}('{key}')/{NavProperty}` | Navigate to related entities |
| `/{DomainID}/{EntitySet}('{key}')/{Action}` | Invoke a bound action |
| `/{DomainID}/{EntitySet}('{key}')/{Function}()` | Invoke a bound function |
| `/{DomainID}/{Function}()` | Invoke an unbound function |

### Examples

```
GET /Windchill/servlet/odata/ProdMgmt                          -- Service document
GET /Windchill/servlet/odata/ProdMgmt/$metadata                -- Metadata
GET /Windchill/servlet/odata/ProdMgmt/Parts                    -- All parts
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')  -- Single part
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Uses  -- BOM children
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:...')/PTC.ProdMgmt.CheckOut -- Action
```

## Available Domains

| Domain ID | Description |
|---|---|
| `ProdMgmt` | Product Management -- Parts, BOMs, sourcing |
| `DocMgmt` | Document Management -- Documents, content |
| `ChangeMgmt` | Change Management -- Change requests, notices, tasks |
| `CADDocMgmt` | CAD Document Management -- CAD documents |
| `DataAdmin` | Data Administration -- Containers, folders |
| `PrincipalMgmt` | Principal Management -- Users, groups |
| `Workflow` | Workflow -- Work items, process definitions |
| `EffectivityMgmt` | Effectivity Management -- Date/unit/lot effectivities |
| `EventMgmt` | Event Management -- Webhook subscriptions |
| `ClfStructure` | Classification Structure -- Classification nodes |
| `SupplierMgmt` | Supplier Management -- Sourcing contexts |
| `NavCriteria` | Navigation Criteria -- Filters and navigation |
| `Visualization` | Visualization -- Representations |
| `SavedSearch` | Saved Search -- Stored queries |
| `MfgProcessMgmt` | Manufacturing Process Management -- Process plans |
| `PDM` | PDM conglomerate -- Read-only, combines multiple domains for BI tools |
| `PTC` | Common -- Shared entity types, complex types, functions |

## Uniform Interface

Because all domains implement the OData v4 protocol, clients interact with every domain the same way:

- **GET** for reading and querying
- **POST** for creating entities and invoking actions
- **PATCH** for partial updates
- **PUT** for full replacement updates
- **DELETE** for removing entities

Standard OData query options work across all domains:

| Query Option | Example |
|---|---|
| `$filter` | `$filter=Name eq 'Bracket'` |
| `$select` | `$select=Name,Number,State` |
| `$expand` | `$expand=Context,Organization` |
| `$orderby` | `$orderby=Name asc` |
| `$top` | `$top=10` |
| `$skip` | `$skip=20` |
| `$count` | `$count=true` |

## Cross-Domain References

Entities in one domain can reference entities in another domain via navigation properties. For example, a Part in `ProdMgmt` may navigate to effectivities in `EffectivityMgmt`:

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:...')?$expand=Effectivities
```

The EDM metadata uses `edmx:Reference` to declare dependencies on other domain schemas.

## Notes

- Each domain has its own `$metadata` endpoint describing its entity data model.
- The service document at the domain root lists all available entity sets.
- Custom domains can be created by adding Domain JSON configuration files.
- Conglomerate domains (like PDM) combine multiple domain schemas into one for BI tool compatibility.
