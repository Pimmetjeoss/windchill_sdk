# Windchill REST Services v1.6 - SDK Reference

> Complete API reference for PTC Windchill REST Services v1.6 (OData-based).
> Base URL: `https://<server>/Windchill/servlet/odata/`
> Authentication: HTTP Basic Auth or session cookie. CSRF_NONCE required for write operations.

## Quick Start

1. [Accessing Domains](accessing-domains.md) - URL structure and authentication
2. [Domains Overview](domains-overview.md) - All available domains with IDs
3. [Fetch NONCE Token](example-fetch-nonce.md) - Required before any write operation
4. [OData Query Parameters](odata-query-parameters.md) - $filter, $select, $expand, $orderby, $top, $skip

---

## Framework & Architecture

| File | Description |
|------|-------------|
| [Framework Overview](framework-overview.md) | Architecture, configuration-driven design, JavaScript hooks |
| [OData as Service](odata-as-service.md) | Domains as OData services, URL patterns |
| [Entity Data Model](entity-data-model.md) | EDM, $metadata endpoint, CSDL format |
| [OData Primitives](odata-primitives.md) | Supported types: String, Int, Boolean, DateTimeOffset, etc. |
| [Process HTTP Requests](process-http-requests.md) | Request pipeline, Nashorn JS hooks, Windchill Java API access |
| [PTC Annotations](ptc-annotations.md) | PTC.ReadOnly, PTC.Operations, PTC.SecurityLabel, etc. |
| [Inheriting Capabilities](inheriting-capabilities.md) | 20+ capabilities: versioned, workable, lifecycleManaged, contentHolder, etc. |
| [API Catalog](api-catalog.md) | Swagger/API catalog in Windchill UI |

## OData Query & Filtering

| File | Description |
|------|-------------|
| [OData Query Parameters](odata-query-parameters.md) | $filter, $select, $expand, $orderby, $top, $skip, $count |
| [Filter on Navigation Properties](filter-navigation-properties.md) | Lambda expressions, Context/Organization/Folder/Attachments filtering |
| [OrderBy Sorting Options](orderby-sorting-options.md) | Sorting on primitives, complex types, navigation properties |
| [DateTime Offset](datetime-offset.md) | Date filtering syntax and examples |
| [OData Prefer Headers](odata-prefer-headers.md) | odata.maxpagesize, return=representation/minimal |
| [Latest Version Search](latest-version-search.md) | ptc.search.latestversion query option |

## Common Operations

| File | Description |
|------|-------------|
| [CheckIn/CheckOut/Delete](actions-checkin-checkout-delete.md) | Single and bulk operations, atomic behavior |
| [Common Navigation Properties](common-navigation-properties.md) | Creator, Modifier - available in all domains |
| [Lifecycle States](lifecycle-states.md) | GetValidStateTransitions function |
| [Set Lifecycle State](set-lifecycle-state.md) | SetState action |
| [NONCE Token Function](nonce-token-function.md) | CSRF protection for write operations |
| [Error Codes](error-codes.md) | HTTP status codes returned by Windchill REST Services |
| [Batch Support](batch-support-theory.md) | Batch request protocol and theory |
| [Batch Request Examples](batch-request-examples.md) | Simple + advanced batch with Content-ID cross-references |

---

## Domain References

### Core Domains

| File | Domain ID | Description |
|------|-----------|-------------|
| [Product Management](product-management-domain.md) | `ProdMgmt` | Parts, BOM, PartUse, AXL entries |
| [Product Management Actions](prodmgmt-actions-functions.md) | `ProdMgmt` | GetBOM, GetPartStructure, GetPartsList, UpdateCommonProperties |
| [Document Management](document-management-domain.md) | `DocMgmt` | Documents, content upload/download |
| [Document Management Actions](document-management-actions.md) | `DocMgmt` | UpdateCommonProperties for documents |
| [Change Management](change-management-domain.md) | `ChangeMgmt` | ProblemReport, ChangeRequest, ChangeNotice, ChangeTask, Variance |
| [Workflow](workflow-domain.md) | `Workflow` | WorkItems, Activities, completion, reassignment |
| [Workflow Actions](workflow-domain-actions.md) | `Workflow` | CompleteWorkitem, SaveWorkitem, ReassignWorkItems |
| [Workflow Functions](workflow-domain-functions.md) | `Workflow` | GetWorkItemReassignUserList |

### Data & Administration

| File | Domain ID | Description |
|------|-----------|-------------|
| [Data Administration](data-administration-domain.md) | `DataAdmin` | Containers, Folders (CRUD), Products, Libraries, Projects |
| [Principal Management](principal-management-domain.md) | `PrincipalMgmt` | Users, Groups, Organizations, License Groups |
| [Common Domain](common-domain.md) | `PTC` | ContentItem, ApplicationData, URLData, WindchillEntity |
| [Common Domain Functions](common-domain-functions.md) | `PTC` | GetEnumTypeConstraint, GetAllStates, GetWindchillMetaInfo |

### Engineering

| File | Domain ID | Description |
|------|-----------|-------------|
| [CAD Document Management](cad-document-management-domain.md) | `CADDocumentMgmt` | CADDocument, PartAssociation, CADStructure |
| [Manufacturing Process Mgmt](manufacturing-process-management-domain.md) | `MfgProcMgmt` | ProcessPlans, Operations, Sequences, BOP |
| [Classification Structure](classification-structure-domain.md) | `ClfStructure` | ClfNode, ClassifiedObject, classification search |
| [Effectivity Management](effectivity-management-domain.md) | `EffectivityMgmt` | Date/Unit/Block/Serial effectivities |
| [Product Platform Mgmt](product-platform-management-domain.md) | `ProdPlatformMgmt` | Options, Choices, OptionSets, VariantSpecifications |
| [Visualization](visualization-domain.md) | `Visualization` | Representations, Creo View URLs, thumbnails |

### Supply Chain

| File | Domain ID | Description |
|------|-----------|-------------|
| [Supplier Management](supplier-management-domain.md) | `SupplierMgmt` | SourcingContext, AML/AVL entries |

### Quality (requires Quality product)

| File | Domain ID | Description |
|------|-----------|-------------|
| [Quality Management System](quality-management-system-domain.md) | `QMS` | People, Places, Addresses, Subjects |
| [Nonconformance](nonconformance-domain.md) | `NC` | Nonconformance processes |
| [CAPA](capa-domain.md) | `CAPA` | Corrective & Preventive Actions |
| [Customer Experience Mgmt](customer-experience-management-domain.md) | `CEM` | Customer complaints/feedback |

### Other Domains

| File | Domain ID | Description |
|------|-----------|-------------|
| [Saved Search](saved-search-domain.md) | `SavedSearch` | Execute saved searches via API |
| [Event Management](event-management-domain.md) | `EventMgmt` | Webhook subscriptions |
| [PDM (Conglomerate)](pdm-domain.md) | `PDM` | Read-only combined domain for PowerBI/Excel |

---

## Code Examples

### Parts & BOM
| File | Operation |
|------|-----------|
| [Create Part](example-create-part.md) | POST to ProdMgmt/Parts |
| [Checkout Part](example-checkout-part.md) | PTC.ProdMgmt.CheckOut action |
| [Checkin Part](example-checkin-part.md) | PTC.ProdMgmt.CheckIn action |
| [Read BOM](example-read-bom.md) | GetBOM / GetPartStructure with $expand |
| [Create Part Usage Link](example-create-part-usage-link.md) | BOM entry with occurrences |
| [Revise Multiple Parts](example-revise-multiple-parts.md) | Bulk revision |
| [Query with Filter](example-query-filter.md) | $filter examples |

### Documents
| File | Operation |
|------|-----------|
| [Create Document](example-create-document.md) | POST to DocMgmt/Documents |
| [Upload Content](example-upload-content.md) | 3-stage file upload process |

### Workflow
| File | Operation |
|------|-----------|
| [Complete Work Item](example-complete-workitem.md) | CompleteWorkitem with routing/voting |
| [Reassign Work Items](example-reassign-workitems.md) | ReassignWorkItems action |

### Authentication
| File | Operation |
|------|-----------|
| [Fetch NONCE](example-fetch-nonce.md) | GetCSRFToken() function |

### Batch Operations
| File | Operation |
|------|-----------|
| [Batch Requests](batch-request-examples.md) | Multipart batch with cross-references |

---

## Domain Customization

| File | Description |
|------|-------------|
| [Config Paths](config-paths.md) | Configuration file locations |
| [Domain JSON File](domain-json-file.md) | Domain JSON structure |
| [Create New Domain](create-new-domain.md) | Creating custom domains |
| [Extending Domains](extending-domains.md) | Adding to existing PTC domains |
| [Add Custom Properties](add-custom-properties.md) | Custom properties on entities |
| [Add New Actions](add-new-actions.md) | Custom actions |
| [Add New Functions](add-new-functions.md) | Custom functions |
| [Example: Create Domain](example-create-domain.md) | Full domain creation example |
| [Example: Soft Type](example-soft-type.md) | Extending ProdMgmt with soft type |

---

## Changelogs

| File | Version |
|------|---------|
| [v1.6](changelog-v1.6.md) | Effectivity, PDM domain, ChangeTask, webhooks, pagination |
| [v1.5](changelog-v1.5.md) | API Catalog, Workflow domain, Regulatory Master, security labels |
| [v1.4](changelog-v1.4.md) | Multi-object CRUD, Options & Variants, CAD/Event/Supplier domains |
| [v1.3](changelog-v1.3.md) | Batch refs, classification, Parts List/Visualization/Audit domains |
| [v1.2](changelog-v1.2.md) | MPM, Change Mgmt, Classification, Saved Search domains |
| [v1.1](changelog-v1.1.md) | Dynamic Doc, Quality, Info*Engine, Factory domains |

---

*Source: PTC Windchill REST Services v1.6 Documentation*
*Generated: 2026-03-30*
