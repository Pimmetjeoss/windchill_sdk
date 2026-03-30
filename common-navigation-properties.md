# Common Navigation Properties Available in All Domains

> Source: PTC Windchill REST Services 1.6 Documentation
> Page: `common_navigations_all_domains.html`

## Overview

Windchill REST Services provides common navigation properties that are available across all domains. These navigation properties allow you to traverse relationships between entities and retrieve related data using the `$expand` query option.

## Common Navigation Properties

The following navigation properties are available for entities across all domains that support them.

### Attachments

Retrieves the attachments associated with an object.

**Navigation Property:** `Attachments`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')/Attachments
GET /ProdMgmt/Parts('<oid>')?$expand=Attachments
```

**Supported Operations:** Read (GET)

### ContainerReference

Retrieves the container (Product, Library, Project, etc.) in which the object resides.

**Navigation Property:** `ContainerReference`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')/ContainerReference
GET /ProdMgmt/Parts('<oid>')?$expand=ContainerReference
```

### Contributors

Retrieves the team members who are contributors to the object.

**Navigation Property:** `Contributors`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=Contributors
```

### LifeCycleState

Retrieves the life cycle state information of the object.

**Navigation Property:** `LifeCycleState`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=LifeCycleState
```

### OrganizationReference

Retrieves the organization associated with the object.

**Navigation Property:** `OrganizationReference`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')/OrganizationReference
GET /ProdMgmt/Parts('<oid>')?$expand=OrganizationReference
```

### FolderReference

Retrieves the folder location of the object.

**Navigation Property:** `FolderReference`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')/FolderReference
GET /ProdMgmt/Parts('<oid>')?$expand=FolderReference
```

### VersionedBy

Retrieves the version information of the object.

**Navigation Property:** `VersionedBy`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=VersionedBy
```

### CheckedOutBy

Retrieves information about who has the object checked out.

**Navigation Property:** `CheckedOutBy`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=CheckedOutBy
```

### CreatedBy

Retrieves information about the user who created the object.

**Navigation Property:** `CreatedBy`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=CreatedBy
```

### LastModifiedBy

Retrieves information about the user who last modified the object.

**Navigation Property:** `LastModifiedBy`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=LastModifiedBy
```

### SecurityLabels

Retrieves the security labels applied to the object.

**Navigation Property:** `SecurityLabels`

**URL Example:**
```
GET /ProdMgmt/Parts('<oid>')?$expand=SecurityLabels
```

## Using $expand with Multiple Navigation Properties

You can expand multiple navigation properties in a single request by separating them with commas:

```
GET /ProdMgmt/Parts('<oid>')?$expand=ContainerReference,FolderReference,LifeCycleState
```

## Using $expand with Nested Expansion

You can perform nested expansions to traverse multiple levels of relationships:

```
GET /ProdMgmt/Parts('<oid>')?$expand=Attachments($expand=ContentItem)
```

## Combining $expand with Other Query Options

You can combine `$expand` with `$select`, `$filter`, `$top`, `$skip`, and `$orderby`:

```
GET /ProdMgmt/Parts?$expand=ContainerReference&$select=Name,Number&$top=10
```

## Applicability

Not all navigation properties are available on every entity. The available navigation properties depend on the Windchill type that the entity represents. Refer to the Entity Data Model (EDM) metadata for each domain to see the exact navigation properties available:

```
GET /servlet/odata/ProdMgmt/$metadata
GET /servlet/odata/DocMgmt/$metadata
GET /servlet/odata/ChangeMgmt/$metadata
```

## Common Structural Properties

In addition to navigation properties, the following structural properties are commonly available across entities in all domains:

| Property | Type | Description |
|----------|------|-------------|
| `ID` | `Edm.String` | The unique OID of the object |
| `Name` | `Edm.String` | Display name of the object |
| `Number` | `Edm.String` | The number/identifier of the object |
| `State` | Complex Type | The current life cycle state |
| `Version` | `Edm.String` | The version identifier (e.g., "A") |
| `Iteration` | `Edm.String` | The iteration identifier (e.g., "1") |
| `CheckOutStatus` | `Edm.String` | Current checkout status |
| `CreatedOn` | `Edm.DateTimeOffset` | Date and time the object was created |
| `LastModified` | `Edm.DateTimeOffset` | Date and time the object was last modified |
| `Description` | `Edm.String` | Description of the object |
