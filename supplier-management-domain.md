# PTC Supplier Management Domain

> **Domain ID:** `SupplierMgmt`
> **Base URL:** `/Windchill/servlet/odata/SupplierMgmt`
> **Metadata URL:** `/Windchill/servlet/odata/SupplierMgmt/$metadata`
> **Added in:** Windchill REST Services 1.4
> **Prerequisite:** Supplier Management module must be installed in Windchill

The PTC Supplier Management domain provides access to the supplier management capabilities of Windchill. Supplier management enables companies to integrate and manage supply chain data in Windchill.

You can create supplier organizations in Windchill PDMLink and populate the database with manufacturer and vendor parts. You can also create and update Approved Manufacturer Part Lists (AMLs) and Approved Vendor Part Lists (AVLs). The AMLs and AVLs are created using the sourcing contexts.

## Cross-Domain Note

The PTC Supplier Management domain enables you to read **sourcing contexts**. Other supplier management objects such as supplier part, manufacturer part, vendor part, and AXLEntry are available in the **PTC Product Management domain** (`ProdMgmt`).

## Entities

| Item | OData Entity | Description |
|------|-------------|-------------|
| Sourcing context (sourcing relationship) | `SourcingContext` | Represents the relationship between sourcing contexts in Windchill. A sourcing context is created in an organization and is used to create an AML or AVL in a specific context. |

## Entity Sets

| Entity Set | Domain | Description |
|-----------|--------|-------------|
| `SourcingContexts` | `SupplierMgmt` | Collection of sourcing context entities |
| `SupplierParts` | `ProdMgmt` | Collection of supplier parts (in Product Management domain) |
| `ManufacturerParts` | `ProdMgmt` | Collection of manufacturer parts (in Product Management domain) |
| `VendorParts` | `ProdMgmt` | Collection of vendor parts (in Product Management domain) |

## Complex Types

| Complex Type | Description |
|-------------|-------------|
| `SourcingStatus` | Represents the sourcing status of a part. Supports filtering with `$filter` and lambda operator `ANY`. |

## Key URLs

### Retrieve All Sourcing Contexts

```
GET /Windchill/servlet/odata/SupplierMgmt/SourcingContexts
```

### Retrieve Supplier, Manufacturer, and Vendor Parts

These entities are in the **PTC Product Management domain**:

```
GET /Windchill/servlet/odata/ProdMgmt/SupplierParts
```

```
GET /Windchill/servlet/odata/ProdMgmt/ManufacturerParts
```

```
GET /Windchill/servlet/odata/ProdMgmt/VendorParts
```

### Retrieve AXLEntry for Parts

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$expand=AXLEntries
```

### Retrieve AXLEntry for a Specific Part

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('<Part_ID>')/AXLEntries
```

### Retrieve Sourcing Context for a Specific AXLEntry

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('<Part_ID>')/AXLEntries('<AXLEntry_ID>')/SourcingContext
```

## Filtering with Lambda Expressions

The `SourcingContext` entity and `SourcingStatus` complex type support filtering using `$filter` parameter along with the lambda operator `ANY` in the URL.

### Filter Parts by Sourcing Context ID and Sourcing Status Value

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=(OEMPartSourcingStatus/any(d:d/SourcingStatus/Value eq 'preferred' and d/SourcingContext/SourcingContextId eq 'com.ptc.windchill.suma.axl.AXLContext:204742'))
```

### Filter Parts with Combinations of Sourcing Status and Contexts

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=startswith(Name,'OEM') and (OEMPartSourcingStatus/any(d:d/SourcingStatus/Value eq 'preferred' and d/SourcingContext/SourcingContextId eq 'com.ptc.windchill.suma.axl.AXLContext:204742') or OEMPartSourcingStatus/any(d:d/SourcingStatus/Value eq 'do_not_use' and d/SourcingContext/SourcingContextId eq 'com.ptc.windchill.suma.axl.AXLContext:204742'))
```

## Navigation Properties on Part Entity (ProdMgmt domain)

| Navigation Property | Description |
|--------------------|-------------|
| `AXLEntries` | AML/AVL entries associated with the part |
| `OEMPartSourcingStatus` | Sourcing status information for the part |

### AXLEntry Navigation Properties

| Navigation Property | Description |
|--------------------|-------------|
| `SourcingContext` | The sourcing context for the AXL entry |
