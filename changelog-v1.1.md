# Summary of Changes for Windchill REST Services 1.1

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_REST_atechsum_1_1.html`

## Overview

Changes and new features introduced in Windchill REST Services 1.1. This was the first major update to the Windchill REST Services framework following the initial release.

## New Domains

### PTC Product Management Domain (ProdMgmt)
- Initial domain for product data management.
- **Entity Sets**: `Parts`
- **Base URL**: `/Windchill/servlet/odata/ProdMgmt`
- Supports reading Part entities with basic properties.
- Mapped Windchill type: `wt.part.WTPart`

### PTC Document Management Domain (DocMgmt)
- Initial domain for document data management.
- **Entity Sets**: `Documents`
- **Base URL**: `/Windchill/servlet/odata/DocMgmt`
- Supports reading Document entities with basic properties.
- Mapped Windchill type: `wt.doc.WTDocument`

### PTC Common Domain (PTC)
- Shared domain for common functions and entities.
- **Base URL**: `/Windchill/servlet/odata/PTC`
- Functions: `GetCSRFToken()` for NONCE token retrieval.

## Core Features

### OData v4 Foundation
- Windchill REST Services is built on OData v4 protocol.
- JSON format for request and response payloads.
- Standard OData URL conventions for entity access.

### Entity Access via OData URLs
- Read entity sets: `GET /Windchill/servlet/odata/<Domain>/<EntitySet>`
- Read single entity: `GET /Windchill/servlet/odata/<Domain>/<EntitySet>('<id>')`
- Entity Data Model: `GET /Windchill/servlet/odata/<Domain>/$metadata`
- Service Document: `GET /Windchill/servlet/odata/<Domain>`

### Authentication
- HTTP Basic Authentication support.
- Session-based authentication after initial login.
- Integration with Windchill's security model.

### Domain Configuration Framework
- JSON-based configuration for defining OData domains.
- Entity configuration with structural properties.
- Mapping between OData entities and Windchill persistable types.
- JavaScript hooks for customizing entity processing.

### OData Primitives Support
- Support for OData primitive types:
  - `Edm.String` - String values
  - `Edm.Int32` - 32-bit integers
  - `Edm.Int64` - 64-bit integers
  - `Edm.Decimal` - Decimal numbers
  - `Edm.Boolean` - Boolean values
  - `Edm.DateTimeOffset` - Date and time with timezone
  - `Edm.Double` - Double-precision floating point

### HTTP Methods
- **GET**: Read entities and entity sets.
- **POST**: Create new entities (introduced in initial release with limited support).
- Response format: JSON (OData v4 compliant).

### Entity Properties
- Read-only system properties (ID, CreatedOn, LastModified).
- Writable business properties (Name, Number, Description).
- Computed properties derived from Windchill object attributes.

## API Framework

### OData Services as Domains
- Each Windchill REST Services domain is an OData service.
- Domains are independently versioned and configured.
- Each domain has its own `$metadata` and service document.

### Configuration Structure
- Domain configuration stored in JSON files.
- Configuration paths follow standard Windchill directory structure.
- Entity-level JavaScript files for custom processing hooks.

### Entity Processor Classes
- `BasicEntityProcessor` for non-persistable entities.
- `PersistableEntityProcessor` for Windchill persistable entities.
- Default processing for CRUD operations on persistable entities.

## Notes

- Windchill REST Services 1.1 is the foundational release that established the OData-based REST API framework for Windchill.
- Subsequent releases (1.2 through 1.6) built upon this foundation by adding new domains, query capabilities, write operations, and customization features.
- The core URL pattern `/Windchill/servlet/odata/<Domain>/<EntitySet>` established in 1.1 remains consistent across all versions.

## Breaking Changes

- None (initial major release).

## Deprecated Features

- None (initial major release).
