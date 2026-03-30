# Summary of Changes for Windchill REST Services 1.3

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_REST_atechsum_1_3.html`

## Overview

Changes and new features introduced in Windchill REST Services 1.3.

## New Domains

### PTC Product Platform Management Domain
- New domain for managing product platforms and variant specifications.
- **Entity Sets**: `VariantSpecifications`, `ConfigurableModules`, `OptionSets`
- Supports reading product platform configuration data.

### PTC Manufacturing Process Management Domain
- New domain for manufacturing process planning.
- **Entity Sets**: `Operations`, `ProcessPlans`
- Actions for managing manufacturing process data.
- Supports reading bill of process structures.

### PTC CAD Document Management Domain
- New domain for CAD document management.
- **Entity Sets**: `CADDocuments`
- Actions for CAD document operations.
- Supports reading CAD-specific metadata and associations.

### PTC Service Information Management Domain
- New domain for service information.
- Supports service-specific entities and operations.

### PTC Parts List Management Domain
- New domain for parts list management.
- Supports reading and managing parts lists.

### PTC Dynamic Document Management Domain
- New domain for dynamic documents.
- Supports dynamic document-specific operations.

## New Features

### Customizing Domains
- **Extending Domains**: Add custom properties, navigation properties, functions, and actions to existing PTC domains.
- **Creating New Domains**: Build entirely new REST API domains with custom entities and operations.
- **Type Extensions**: Add soft type extensions of Windchill types to PTC domains.

### Custom Properties
- Support for adding custom properties (soft attributes) to entities in PTC domains.
- Custom properties are configured in the domain's JSON extension files.
- Both typed attributes and IBA (Instance-Based Attributes) are supported.

### Custom Navigation Properties
- Support for adding custom navigation paths between entities.
- Custom navigations are implemented via JavaScript hooks.

### Custom Functions and Actions
- Support for adding new bound and unbound functions to existing domains.
- Support for adding new bound and unbound actions to existing domains.
- Functions and actions are configured in JSON and implemented in JavaScript.

### Info*Engine Integration
- New domain for invoking Info*Engine tasks via the REST API.
- Supports executing Info*Engine webjects and tasks.

## Enhancements to Existing Domains

### PTC Product Management Domain
- Enhanced part entity with additional properties.
- Improved BOM (Bill of Materials) navigation and traversal.

### PTC Document Management Domain
- Enhanced document entity with additional metadata properties.

### PTC Common Domain
- Enhanced common functions available across domains.

## API Framework Enhancements

### Import Domain JSON File
- Support for importing domain configuration from JSON files.
- Enables programmatic domain setup and deployment.

### Disabling Entity Sets
- Ability to disable entity sets for specific entities in the service document.
- Useful for hiding entities that should not be directly accessible.

### Excluding Subtypes
- Support for excluding specific subtypes from entity sets.
- Prevents certain Windchill subtypes from appearing in query results.

### Naming Convention for Subtypes
- Standardized naming convention for representing Windchill subtypes in OData.
- Ensures consistent type naming across the API.

## Breaking Changes

- None reported for this release.

## Deprecated Features

- None reported for this release.
