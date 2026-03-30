# Summary of Changes for Windchill REST Services 1.2

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_REST_atechsum_1_2.html`

## Overview

Changes and new features introduced in Windchill REST Services 1.2.

## New Domains

### PTC Data Administration Domain
- New domain for data administration tasks.
- **Entity Sets**: `Folders`, `SubFolders`, `Containers`
- Supports folder and container management operations.

### PTC Principal Management Domain
- New domain for user and group management.
- **Entity Sets**: `Users`, `Groups`
- Supports reading user and group information.

### PTC Quality Domains
- Introduction of quality management domains:
  - **QMS Domain**: Quality Management System objects
  - **NC Domain**: Nonconformance management
  - **CEM Domain**: Customer Experience Management
  - **CAPA Domain**: Corrective and Preventive Actions
  - **Audit Domain**: Audit management
  - **Regulatory Master Domain**: Regulatory compliance objects

## New Features

### $filter Support
- Full support for the OData `$filter` query option.
- Supported operators: `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `and`, `or`, `not`.
- Supported functions: `contains()`, `startswith()`, `endswith()`.
- Filter by structural properties of entities.

### $orderby Support
- Support for the OData `$orderby` query option.
- Ascending and descending sort order.
- Multi-property sorting.

### $select Support
- Support for the OData `$select` query option.
- Select specific properties to reduce response payload size.

### $top and $skip Support
- Support for OData pagination query options.
- `$top` limits the number of results returned.
- `$skip` skips a specified number of results.

### $count Support
- Support for the OData `$count` query option.
- Returns the total count of matching entities alongside results.
- Also available as a path segment: `.../Parts/$count` returns just the count.

### Server-Side Paging
- Automatic server-side paging for large result sets.
- `@odata.nextLink` in response for navigating to the next page.
- Configurable default page size on the server.

### Create Operations (POST)
- Support for creating new entities via POST requests.
- Part creation in the PTC Product Management domain.
- Document creation in the PTC Document Management domain.
- Auto-numbering support when entity number is not specified.

### Navigation Properties
- Support for navigating between related entities.
- Relationship traversal via URL paths (e.g., `Parts('<id>')/Uses`).
- Navigation links included in entity responses.

## Enhancements to Existing Domains

### PTC Product Management Domain
- Enhanced Part entity with full CRUD support.
- Entity Set: `Parts` with support for create, read, update, and delete.
- Navigation properties for BOM relationships.

### PTC Document Management Domain
- Enhanced Document entity with full CRUD support.
- Entity Set: `Documents` with support for create, read, update, and delete.

### PTC Common Domain
- NONCE token function `GetCSRFToken()` for CSRF protection.
- Common navigations available across all domains.

## API Framework Enhancements

### Domain Configuration
- JSON-based domain configuration files.
- Support for configuring entities, properties, and navigations.
- Configuration paths and file structure standardized.

### Entity Data Model (EDM)
- OData Entity Data Model support.
- `$metadata` endpoint for each domain.
- Structural and navigational property definitions.

### PTC Annotations
- Custom PTC annotations on entity properties.
- Annotations provide additional metadata about properties (e.g., read-only, required).

### Processing HTTP Requests
- Framework support for processing GET, POST, PATCH, DELETE requests.
- JavaScript hooks for customizing request processing.
- Entity processor classes for persistable and basic entities.

## Breaking Changes

- None reported for this release.

## Deprecated Features

- None reported for this release.
