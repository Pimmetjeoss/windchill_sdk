# Domains Overview

> Source: PTC Windchill REST Services 1.6 Documentation
> Page: `WCCG_RESTAPIsAccessDomainsOverview.html`

## Overview

Windchill REST Services organizes its OData APIs into domains. Each domain corresponds to a specific functional area of Windchill and provides OData entity sets, actions, and functions relevant to that area. Domains are the top-level grouping mechanism for the REST API.

## PTC Domains

The following PTC-provided domains are available in Windchill REST Services 1.6:

| Domain | URL Segment | Description |
|--------|-------------|-------------|
| PTC Product Management | `ProdMgmt` | Parts, BOMs, part structures, supplier parts, and product data |
| PTC Document Management | `DocMgmt` | Documents, content, and document metadata |
| PTC Data Administration | `DataAdmin` | Containers, folders, folder contents, and organizational data |
| PTC Principal Management | `PrincipalMgmt` | Users, groups, organizations, and license groups |
| PTC Common | `PTC` | Common functions shared across domains (e.g., CSRF token, navigation criteria) |
| PTC Navigation Criteria | `NavCriteria` | Navigation criteria for controlling how structures are navigated |
| PTC Dynamic Document Management | `DynDocMgmt` | Dynamic documents and their structures |
| PTC Parts List Management | `PartsListMgmt` | Parts lists, parts list items, and illustrations |
| PTC Service Information Management | `ServiceInfoMgmt` | Information structures and publication structures |
| PTC Quality Management System (QMS) | `QMS` | Quality management system entities |
| PTC Nonconformance | `NC` | Nonconformance entities |
| PTC Customer Experience Management | `CEM` | Customer experience management entities |
| PTC Regulatory Master | `RegMstr` | Regulatory submissions and compliance data |
| PTC CAPA | `CAPA` | Corrective and preventive actions |
| PTC Audit | `Audit` | Audit management entities |
| PTC Info\*Engine System | `InfoEngine` | Info\*Engine task invocation |
| PTC Factory | `Factory` | Factory and manufacturing site data |
| PTC Manufacturing Process Management | `MfgProcessMgmt` | Process plans, operations, sequences, and manufacturing BOPs |
| PTC Change Management | `ChangeMgmt` | Problem reports, change requests, change notices, change tasks, variances |
| PTC Classification Structure | `ClfStructure` | Classification nodes, classified objects, and classification attributes |
| PTC Saved Search | `SavedSearch` | Saved searches and their execution |
| PTC Visualization | `Visualization` | Representations and fidelity information |
| PTC Product Platform Management | `ProdPlatformMgmt` | Options, option groups, option sets, and variant specifications |
| PTC CAD Document Management | `CADDocMgmt` | CAD documents, CAD structures, and related parts |
| PTC Effectivity Management | `EffectivityMgmt` | Effectivity contexts, date effectivities, unit effectivities, block effectivities |
| PTC Event Management | `EventMgmt` | Event subscriptions and webhook management |
| PTC Supplier Management | `SupplierMgmt` | Sourcing contexts and supplier data |
| PTC Workflow | `Workflow` | Work items, routing options, and workflow actions |
| PTC PDM | `PDM` | Product Data Management entities |

## Accessing Domain Service Documents

Each domain provides a service document listing all available entity sets:

```
GET /servlet/odata/<DomainName>
```

**Example:**
```
GET /servlet/odata/ProdMgmt
```

## Accessing Domain Metadata (EDM)

Each domain provides an Entity Data Model (EDM) metadata document that describes all entity types, properties, navigation properties, actions, and functions:

```
GET /servlet/odata/<DomainName>/$metadata
```

**Example:**
```
GET /servlet/odata/ProdMgmt/$metadata
```

The metadata document is in OData CSDL (Common Schema Definition Language) XML format.

## Cross-Domain References

Some domains reference entities from other domains. For example:

- **PTC Product Management** references the PTC Document Management domain to provide navigations to reference and describe documents associated with parts.
- **PTC Supplier Management** entities (SupplierPart, ManufacturerPart, VendorPart, AXLEntry) are also available in the PTC Product Management domain when the Supplier Management module is installed.
- **PTC Classification Structure** entities can be used with parts from the PTC Product Management domain when Windchill PartsLink is installed.

## Custom Domains

In addition to the PTC-provided domains, you can create custom domains. Custom domains allow you to:

- Expose custom Windchill types as OData entities
- Add custom properties and navigations
- Define custom actions and functions
- Extend existing PTC domains

Custom domains are configured using JSON configuration files placed in the Windchill domain configuration directory. See the Domain Configuration documentation for details.

## Domain Module Dependencies

Some domains require specific Windchill modules to be installed:

| Domain | Required Module |
|--------|----------------|
| PTC Supplier Management | Supplier Management module |
| PTC Classification Structure | Windchill PartsLink module |
| PTC Quality domains (QMS, NC, CEM, CAPA, Audit) | Windchill Quality Solutions |
| PTC Regulatory Master | Windchill Regulatory Master |
| PTC Manufacturing Process Management | Windchill MPMLink |
| PTC Service Information Management | Windchill Service Information Manager |
| PTC Product Platform Management | Windchill Options and Variants |

## URL Structure Summary

```
/servlet/odata                          -- Root service document
/servlet/odata/<Domain>                 -- Domain service document
/servlet/odata/<Domain>/$metadata       -- Domain EDM metadata
/servlet/odata/<Domain>/<EntitySet>     -- Entity collection
/servlet/odata/<Domain>/<EntitySet>('<oid>')  -- Single entity by OID
/servlet/odata/<Domain>/<EntitySet>('<oid>')/<NavigationProperty>  -- Navigate to related entities
/servlet/odata/<Domain>/<EntitySet>('<oid>')/<Namespace>.<Action>  -- Invoke bound action
/servlet/odata/<Domain>/<Function>()    -- Invoke unbound function
```
