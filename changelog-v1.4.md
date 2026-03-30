# Summary of Changes for Windchill REST Services 1.4

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_REST_atechsum_1_4.html`

## Overview

Changes and new features introduced in Windchill REST Services 1.4.

## New Domains

### PTC Change Management Domain
- New domain for accessing change management objects.
- **Entity Sets**: `ProblemReports`, `ChangeRequests`, `ChangeNotices`
- Navigation properties for affected objects, affected links, and attachments.
- Supports read operations on change management objects.

### PTC Classification Structure Domain
- New domain for accessing classification hierarchies.
- **Entity Sets**: `ClassificationNodes`
- **Functions**: `GetChildNodes()`, `GetClassifiedObjects()`
- Supports navigating classification trees and retrieving classified objects.

### PTC Navigation Criteria Domain
- New domain for working with navigation criteria (used with configurable products and variant specifications).

### PTC Event Management Domain
- New domain for webhook subscriptions.
- Supports subscribing to events on Windchill objects.
- Supports create, read, update, and delete of event subscriptions.

## New Features

### Batch Request Support
- Support for OData batch requests using `$batch` endpoint.
- Multiple operations can be grouped in a single HTTP request.
- Both individual requests and change sets (transactional groups) are supported.
- Content-Type: `multipart/mixed` with boundary delimiter.

### Checkout, Checkin, and Undo Checkout
- New bound actions for Part and Document entities:
  - `CheckOut` - Checks out the object and returns the working copy.
  - `CheckIn` - Checks in the working copy.
  - `UndoCheckOut` - Cancels the checkout and discards the working copy.
  - `Delete` - Deletes an object.

### Update Operations (PATCH)
- Support for updating part and document common attributes.
- Support for updating multiple parts and documents in a single request.
- PATCH method for modifying entity properties.

### $expand Support
- Support for `$expand` query option on navigation properties.
- Inline expansion of related entities in a single response.
- Nested `$expand` for multi-level navigation.

### Soft Type Support
- Support for Windchill soft types (subtypes) in the REST API.
- Soft type entities inherit properties from their parent types.
- Custom properties (soft attributes) on soft types are accessible.

## Enhancements to Existing Domains

### PTC Product Management Domain
- New entity `PartUsageLink` representing BOM relationships.
- Navigation properties: `Uses` (child components), `UsedBy` (parent assemblies).
- Support for creating, reading, and deleting part usage links.
- New bound function `GetPartStructure()` for multi-level BOM traversal.
- Support for reading parts by ID.

### PTC Document Management Domain
- New navigation properties for document content management.
- Support for checkout, checkin, and undo checkout operations.

### PTC Data Administration Domain
- New entity sets for folder management.
- Support for folder hierarchy navigation.

### PTC Common Domain
- `GetCSRFToken()` function for fetching NONCE tokens (previously available, now documented).

## API Framework Enhancements

### Versioning of Domain API
- Support for API versioning through URL path segments.
- Version number in the URL: `/Windchill/servlet/odata/v<version>/ProdMgmt/Parts`
- Default version used when version is omitted from the URL.

### Configuring Unbound Functions and Actions
- Support for configuring unbound functions and actions in domain JSON files.
- Unbound operations are not tied to a specific entity.

### Entity Configuration Enhancements
- Support for configuring bound functions and actions on entities.
- Enhanced structural and navigational property configuration.
- `inherits` property for inheriting Windchill capabilities (e.g., `checkinout`, `revisionControlled`).

## Breaking Changes

- None reported for this release.

## Deprecated Features

- None reported for this release.
