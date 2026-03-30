# Windchill REST Services v1.6 - Changelog

## Overview

Version 1.6 of PTC Windchill REST Services introduces new capabilities, domains, navigation properties, and webhook support. This document summarizes all changes from v1.5 to v1.6.

## New Capabilities

Three new inheriting capabilities were added:

| Capability | Description |
|---|---|
| `effectivityManaged` | Allows entities to have effectivities (date, serial number, lot, unit, etc.) navigated via `Effectivities` property |
| `partAssociations` | Enables navigation from Part to associated CAD documents and other related objects via `PartAssociations` |
| `variantSpecs` | Adds `GetAllVariantSpecifications` function and variant specification navigations |

## Domain JSON: conglomerate Property

A new boolean property `conglomerate` can be set in Domain JSON configuration to define read-only conglomerate domains that combine multiple source domains into one. Example:

```json
{
  "name": "PDM",
  "conglomerate": true,
  "description": "Product Data Management conglomerate domain",
  "sourceDomains": ["ProdMgmt", "DocMgmt", "ChangeMgmt", "PrincipalMgmt", "CADDocMgmt"]
}
```

## Developer Documentation

- **Javadoc** for Java server-side API is now published
- **JSDoc** for JavaScript hook API is now published
- Both available under `{windchill-base}/codebase/rest/docs/`

## Enhanced Actions and Functions on Navigated Entities

Actions and functions (bound operations) can now be invoked on entities reached via navigation properties. For example, you can check out a Part that was navigated to from a BOM:

```
POST /PTC/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Uses('OR:...')/UsedBy/PTC.ProdMgmt.CheckOut
```

## Pagination on Function Responses

Functions that return collections now support server-driven pagination via `@odata.nextLink`. Example:

```
GET /PTC/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.GetAllVariantSpecifications?$top=10

Response:
{
  "value": [...],
  "@odata.nextLink": "/PTC/ProdMgmt/Parts('OR:...')/PTC.ProdMgmt.GetAllVariantSpecifications?$top=10&$skip=10"
}
```

## Change Management Enhancements

| Feature | Details |
|---|---|
| `ChangeTask` entity type | New entity for individual change tasks within a change process |
| `ImplementationPlan` navigation | Navigate from ChangeNotice to its implementation plan |
| `$filter` on process objects | Filter change process and reference objects |
| `$orderby` on process objects | Sort change process and reference objects |
| `$count` on process objects | Count change process and reference objects |

### Example: Filter change tasks

```
GET /PTC/ChangeMgmt/ChangeNotices('OR:...')/ImplementationPlan/ChangeTask?$filter=State eq 'OPEN'&$orderby=Priority desc&$count=true
```

## Part Navigation Enhancements

New navigation properties on Part entity:

| Navigation | Description |
|---|---|
| `AXLEntries` | Navigate to AML/AVL/AXL entries (Approved Manufacturer/Vendor/Exchange Lists) with full CRUD support |
| `PartAssociations` | Navigate to associated objects (CAD documents, etc.) with `$expand=RelatedCADDoc` |
| `Effectivities` | Navigate to effectivity assignments on a Part |

### Example: Get part associations with expanded CAD docs

```
GET /PTC/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PartAssociations?$expand=RelatedCADDoc
```

## VariantSpecification Navigations

New navigation properties on VariantSpecification:

| Navigation | Description |
|---|---|
| `NavigationCriteria` | Get the navigation criteria used by a variant specification |
| `ConfigurableModule` | Get the configurable module associated with a variant specification |
| `OptionSet` | Get the option set linked to a variant specification |

## New Domains

### Effectivity Management Domain (`EffectivityMgmt`)

A new domain for managing product effectivities. Includes entity types:
- `Effectivity` (base type)
- `SerialNumberEffectivity`
- `LotEffectivity`
- `UnitEffectivity`
- `MSNEffectivity`
- `BlockEffectivity`
- `DateEffectivity`
- `PartEffectivityContext`

### PDM Conglomerate Domain

A read-only conglomerate domain combining `ProdMgmt`, `DocMgmt`, `ChangeMgmt`, `PrincipalMgmt`, and `CADDocMgmt`. Designed for BI tools like PowerBI and Excel. No write operations supported.

## New Query Options

### ptc.search.latestversion

A new custom query option that restricts search results to only the latest version of each object:

```
GET /PTC/ProdMgmt/Parts?ptc.search.latestversion=true&$filter=contains(Name,'Bracket')
```

## CADDocument Security Labels

CADDocument entities now support the `securityLabeled` capability, allowing security label read and write operations:

```
GET /PTC/CADDocMgmt/CADDocuments('OR:...')?$select=SecurityLabels

PATCH /PTC/CADDocMgmt/CADDocuments('OR:...')
{
  "SecurityLabels": {
    "ITAR": "UNRESTRICTED"
  }
}
```

## Webhook / Event Subscriptions

Webhook (event) subscriptions are now supported for the following additional domains:

| Domain | Service Name |
|---|---|
| CAD Document Management | `CADDocMgmt` |
| Service Information Management | `ServiceInfoMgmt` |
| Parts List Management | `PartsListMgmt` |
| Dynamic Document Management | `DynamicDocMgmt` |

These join the previously supported domains: `ProdMgmt`, `DocMgmt`, `DataAdmin`, `ChangeMgmt`.

### Example: Create webhook subscription for CAD documents

```http
POST /PTC/EventMgmt/EntityTypeInContainerEventSubscriptions
Content-Type: application/json

{
  "DomainName": "CADDocMgmt",
  "TypeId": "CADDocument",
  "ContainerId": "OR:wt.inf.library.WTLibrary:12345",
  "CallbackURL": "https://myapp.example.com/webhooks/cad",
  "EventType": "CREATE"
}
```
