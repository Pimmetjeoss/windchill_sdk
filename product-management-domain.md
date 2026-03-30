# PTC Product Management Domain

> **Domain ID:** `ProdMgmt`
> **Base URL:** `/Windchill/servlet/odata/ProdMgmt`
> **Metadata URL:** `/Windchill/servlet/odata/ProdMgmt/$metadata`

The PTC Product Management domain provides access to parts, bills of materials (BOMs), supplier/manufacturer/vendor parts, and related product data in Windchill. It is one of the most commonly used domains for automation.

## Entities

| OData Entity | Description |
|---|---|
| `Part` | Core entity representing a Windchill part (WTPart). Supports versioned, workable, lifecycleManaged, contentHolder, foldered, contextManaged, viewManageable, representable, organizationOwned, subtypeable, softattributable, classifiable, securityLabeled, optionSetAssignable, expressionAssignable, effectivityManaged, partAssociations, variantSpecs capabilities. |
| `ElectricalPart` | Subtype of Part for electrical components. |
| `BOM` | Represents a bill of materials link between a parent part and a child part. |
| `PartUse` | Represents a part usage link in the BOM structure. |
| `UsageOccurrence` | Represents an occurrence of a part use within a product structure. |
| `PartContent` | Content (files) associated with a part. |
| `SupplierPart` | A supplier-provided part linked to a Windchill part. |
| `ManufacturerPart` | A manufacturer-provided part linked to a Windchill part. |
| `VendorPart` | A vendor-provided part linked to a Windchill part. |
| `AXLEntry` | An entry in the Approved Exchange List (AXL), covering AML (Approved Manufacturer List), AVL (Approved Vendor List), and AXL relationships. Supports full CRUD with SourcingContext. |

## Entity Sets

| Entity Set | URL |
|---|---|
| `Parts` | `/Windchill/servlet/odata/ProdMgmt/Parts` |
| `BOMs` | `/Windchill/servlet/odata/ProdMgmt/BOMs` |

## Navigation Properties on Part

### Core Navigation Properties

| Navigation Property | Type | Description |
|---|---|---|
| `Versions` | Collection | All versions of this part |
| `Revisions` | Collection | All revisions of this part |
| `PrimaryContent` | Single | The primary content (file) of this part |
| `Attachments` | Collection | Attached files/content |
| `Folder` | Single | The folder containing this part |
| `Context` | Single | The container context (product/library) |
| `Organization` | Single | The owning organization |
| `Representations` | Collection | 3D/2D representations |

### Product Structure Navigation

| Navigation Property | Type | Description |
|---|---|---|
| `Uses` | Collection(PartUse) | Parts used by this part (BOM children) |
| `UsedBy` | Collection(PartUse) | Parts that use this part (BOM parents) |

### v1.6 Navigation Properties

| Navigation Property | Type | Description |
|---|---|---|
| `AssignedOptionSet` | Single | The option set assigned to this part |
| `AXLEntries` | Collection(AXLEntry) | AML/AVL/AXL entries. Full CRUD supported. Filter by SourcingContext. |
| `PartAssociations` | Collection | Associated objects (CAD docs, etc.). Supports `$expand=RelatedCADDoc`. |
| `Effectivities` | Collection | Effectivity assignments. Links to EffectivityMgmt domain entities. |

## Key URLs and Examples

### Query Parts

```
GET /Windchill/servlet/odata/ProdMgmt/Parts
GET /Windchill/servlet/odata/ProdMgmt/Parts?$top=10&$skip=0&$orderby=Name asc
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=Number eq '0000001234'
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=contains(Name,'Bracket')&ptc.search.latestversion=true
```

### Get a Single Part

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')
```

### Get Part with Expanded Properties

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')?$expand=Context,Organization,Folder
```

### Create a Part

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts
Content-Type: application/json
CSRF_NONCE: <nonce_value>

{
  "Number": "0000001234",
  "Name": "Bracket Assembly",
  "Description": "Main bracket for housing",
  "Source": "MAKE",
  "DefaultUnit": "EA",
  "View": "Design",
  "Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:12345')",
  "Folder@odata.bind": "Folders('OR:wt.folder.SubFolder:67890')"
}
```

### Update a Part

```http
PATCH /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')
Content-Type: application/json
CSRF_NONCE: <nonce_value>

{
  "Name": "Updated Bracket Assembly",
  "Description": "Updated description"
}
```

### Delete a Part

```http
DELETE /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')
CSRF_NONCE: <nonce_value>
```

### Read BOM (Part Uses)

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Uses
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Uses?$expand=UsedBy
```

### Create a BOM Link (Part Usage)

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Uses
Content-Type: application/json
CSRF_NONCE: <nonce_value>

{
  "Quantity": 2,
  "Unit": "EA",
  "UsedBy@odata.bind": "Parts('OR:wt.part.WTPart:67890')",
  "LineNumber": 10,
  "FindNumber": "1"
}
```

### AXL Entries (AML/AVL)

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/AXLEntries
```

Create an AXL entry:

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/AXLEntries
Content-Type: application/json
CSRF_NONCE: <nonce_value>

{
  "ManufacturerName": "ACME Corp",
  "ManufacturerPartNumber": "ACM-12345",
  "SourcingContext@odata.bind": "SourcingContexts('OR:...')"
}
```

### Part Associations with CAD Documents

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PartAssociations?$expand=RelatedCADDoc
```

### Effectivities

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Effectivities
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Effectivities/PTC.EffectivityMgmt.DateEffectivity
```

### Variant Specifications

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.GetAllVariantSpecifications
```

## Actions on Part

| Action | HTTP Method | Description |
|---|---|---|
| `PTC.ProdMgmt.CheckOut` | POST | Check out a part for editing |
| `PTC.ProdMgmt.CheckIn` | POST | Check in a part after editing |
| `PTC.ProdMgmt.UndoCheckOut` | POST | Cancel a checkout |
| `PTC.ProdMgmt.Revise` | POST | Create a new revision of a part |
| `PTC.ProdMgmt.SetLifeCycleState` | POST | Change the lifecycle state |

### CheckOut Example

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.CheckOut
CSRF_NONCE: <nonce_value>
```

### CheckIn Example

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.CheckIn
Content-Type: application/json
CSRF_NONCE: <nonce_value>

{
  "Comment": "Updated BOM structure"
}
```

### Revise Example

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.Revise
CSRF_NONCE: <nonce_value>
```

## Classification (Requires PartsLink)

Part classification requires the PTC PartsLink module. When available, the `classifiable` capability provides:

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')?$select=ClassificationInfo
```

The `ClassificationInfo` complex type includes the classification node and attribute values.

## Common Part Properties

| Property | Type | Description |
|---|---|---|
| `ID` | String | OData entity ID (e.g., `OR:wt.part.WTPart:12345`) |
| `Number` | String | Part number |
| `Name` | String | Part name |
| `Description` | String | Part description |
| `State` | String | Lifecycle state (e.g., `INWORK`, `RELEASED`) |
| `Source` | String | Source type (`MAKE`, `BUY`, `MAKE_OR_BUY`) |
| `DefaultUnit` | String | Default unit of measure |
| `View` | String | View name (e.g., `Design`, `Manufacturing`) |
| `VersionID` | String | Version identifier (e.g., `A.1`) |
| `Revision` | String | Revision letter (e.g., `A`) |
| `Version` | String | Version number within revision (e.g., `1`) |
| `Latest` | Boolean | Whether this is the latest version |
| `LifeCycleTemplateName` | String | Name of the lifecycle template |
| `CheckOutStatus` | String | Current checkout status |
| `FolderName` | String | Name of the containing folder |
| `CabinetName` | String | Name of the containing cabinet |
| `FolderLocation` | String | Full folder path |

## Notes

- Always fetch a CSRF nonce before performing write operations (POST, PATCH, DELETE, actions).
- Use `ptc.search.latestversion=true` to get only the latest version when querying.
- BOM operations (create/update/delete part usage links) typically require checkout of the parent part first.
- The `$expand` query option works on navigation properties to inline related data.
- Part classification via `ClassificationInfo` requires PTC PartsLink license.
