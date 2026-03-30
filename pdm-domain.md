# PDM Domain

> **Domain ID:** `PDM`
> **Base URL:** `/Windchill/servlet/odata/PDM`
> **Metadata URL:** `/Windchill/servlet/odata/PDM/$metadata`
> **Added in:** Windchill REST Services 1.6

The PDM domain is a **read-only** conglomerate domain that combines all core Windchill domains into a single domain. It is designed for OData clients, such as **Microsoft Power BI** and **Microsoft Excel**, that cannot get data directly from core domains.

If you want to build Windchill reports or dashboards using Microsoft Power BI and Excel, you should use the PDM domain instead of using the core domains directly.

## Key Characteristics

| Property | Value |
|----------|-------|
| Read-only | Yes |
| Supports CREATE | No |
| Supports UPDATE | No |
| Supports DELETE | No |
| Supports Actions | No |
| Supports Functions | Yes (read-only functions from imported domains) |

## Operations

You can perform only **READ** operations on entities and execution of **functions** for the imported domains. CREATE, UPDATE, and DELETE operations, and actions are **not supported**.

## Imported Domains

The PDM domain combines the following core Windchill domains along with their dependent domains:

### Core Domains

| Domain | Domain ID | Description |
|--------|-----------|-------------|
| PTC Product Management | `ProdMgmt` | Parts, BOM, product structures |
| PTC Document Management | `DocMgmt` | Documents, content management |
| PTC Data Administration | `DataAdmin` | Containers, folders, organizations |
| PTC Principal Management | `PrincipalMgmt` | Users, groups, organizations |
| PTC Common | `PTC` | Common entities, complex types, functions |
| PTC Navigation Criteria | `NavCriteria` | Filters and navigation criteria |
| PTC Change Management | `ChangeMgmt` | Change requests, notices, tasks |
| PTC Classification Structure | `ClfStructure` | Classification nodes and objects |
| PTC CAD Document Management | `CADDocumentMgmt` | CAD documents and structures |
| PTC Supplier Management | `SupplierMgmt` | Sourcing contexts |
| PTC Effectivity Management | `EffectivityMgmt` | Effectivity information |
| PTC Workflow | `Workflow` | Work items and workflow tasks |
| PTC Saved Search | `SavedSearch` | Saved searches |
| PTC Visualization | `Visualization` | Representations and fidelity |
| PTC Manufacturing Process Management | `MfgProcessMgmt` | Process plans, operations |
| PTC Event Management | `EventMgmt` | Event subscriptions |

### Dependent Domains

The PDM domain also includes the dependent domains of the core Windchill domains, such as PTC Data Administration and PTC Navigation Criteria.

## EDM Characteristics

The EDM (Entity Data Model) of the PDM conglomerate domain includes EDMs of all the core and dependent domains. As a conglomerate domain, it **does not reference any external schema**. This enables clients that do not understand `edmx:Reference` to access and work with the PTC domains.

## Key URLs

### Access the PDM Domain Root

```
GET /Windchill/servlet/odata/PDM
```

### Read Parts via PDM Domain

```
GET /Windchill/servlet/odata/PDM/Parts
```

### Read Documents via PDM Domain

```
GET /Windchill/servlet/odata/PDM/Documents
```

### Read Containers via PDM Domain

```
GET /Windchill/servlet/odata/PDM/Containers
```

### Read with OData Query Parameters

Standard OData query parameters work with the PDM domain:

```
GET /Windchill/servlet/odata/PDM/Parts?$filter=Name eq 'MyPart'&$expand=Context&$select=Name,Number,State
```

### Access Metadata

```
GET /Windchill/servlet/odata/PDM/$metadata
```

## Usage with Power BI

When connecting Power BI to Windchill:

1. Use the PDM domain base URL: `https://<windchill_server>/Windchill/servlet/odata/PDM`
2. Power BI will discover all available entity sets from the service document
3. Select the entity sets you want to import into your report/dashboard
4. The PDM domain's self-contained EDM (no external references) ensures compatibility with Power BI's OData connector

## Usage with Excel

When connecting Excel to Windchill:

1. Use **Data > Get Data > From Other Sources > From OData Feed**
2. Enter the PDM domain URL: `https://<windchill_server>/Windchill/servlet/odata/PDM`
3. Authenticate with your Windchill credentials
4. Select the tables (entity sets) to import

## Notes

- Since all core domain entities are accessible through a single endpoint, Power BI and Excel can join data across domains (e.g., Parts with Change Notices) in a single data model.
- Functions from imported domains remain available for execution.
- The PDM domain simplifies client configuration by eliminating the need to connect to multiple domain endpoints.
