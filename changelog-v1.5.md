# Summary of Changes for Windchill REST Services 1.5

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_REST_atechsum_1_5.html`

## Overview

Changes and new features introduced in Windchill REST Services 1.5.

## New Domains

### PTC Workflow Domain
- New domain providing access to workflow work items and processes.
- **Entity Sets**: `WorkItems`
- **Actions**: `Complete`, `Save`, `Reassign`
- **Functions**: `GetRoutingOptions()`, `GetValidReassignUsers()`
- Supports retrieving, completing, saving, and reassigning work items.

### PTC Supplier Management Domain
- New domain for managing supplier-related data.
- **Entity Sets**: `SourcingContexts`, `ManufacturerParts`, `VendorParts`
- Supports creating AML (Approved Manufacturer List) and AVL (Approved Vendor List) entries.

### PTC Saved Search Domain
- New domain for executing saved searches.
- **Functions**: `GetSavedSearches()`, `ExecuteSavedSearch()`
- Supports retrieving and executing saved search definitions.

## New Features

### Multiple Entity Operations (Batch-like)
- Support for creating multiple parts in a single POST request to the Parts entity set.
- Support for creating multiple documents in a single POST request to the Documents entity set.
- Support for updating multiple parts and documents in a single PATCH request.

### Security Labels
- Part and Document entities now support security labels.
- Security labels can be read and set via the REST API.
- Both single-value and multi-value security labels are supported.

### Revise Action
- New `Revise` action available for Parts and Documents.
- Supports revising multiple objects in a single request.
- Creates new versions while preserving the previous versions.

### Classification Support
- Parts can be created with classification attributes.
- Classification node information can be retrieved via navigation properties.
- Support for reading classified objects and their classification attributes.

### Filtering Enhancements
- Support for `$filter` on navigation properties.
- Support for `$orderby` on navigation properties.
- Enhanced date filtering with `DateTimeOffset` type support.

### OData Prefer Headers
- Support for the `Prefer` header with `return=representation` and `return=minimal` values.
- `odata.maxpagesize` preference for controlling page sizes.

## Enhancements to Existing Domains

### PTC Product Management Domain
- New navigation properties on the Part entity:
  - `AlternateLinks` - Retrieves alternate part associations
  - `SubstituteLinks` - Retrieves substitute part associations
- New function `GetPartsList()` for retrieving parts lists.
- Support for creating parts in a different organization.

### PTC Document Management Domain
- New action `UploadContent` for uploading file content to documents.
- Support for creating documents in a different organization.
- Enhanced metadata for content management.

### PTC Change Management Domain
- New entity sets and navigations for change management objects:
  - `ProblemReports`
  - `ChangeRequests`
  - `ChangeNotices`
- Navigation properties for affected objects and attachments.

### PTC Data Administration Domain
- Support for creating, updating, and deleting folders and subfolders.

## API Framework Enhancements

### Constraint Support
- New capability to retrieve Windchill constraint information via the REST API.
- Constraints provide validation rules for entity properties.

### Life Cycle State Management
- New action `SetLifeCycleState` to change the life cycle state of an entity.
- Function to retrieve available life cycle states for an entity.

### Latest Version Search
- Custom query option `ptc.search.latestversion` to limit search results to the latest version of entities.

## Breaking Changes

- None reported for this release.

## Deprecated Features

- None reported for this release.
