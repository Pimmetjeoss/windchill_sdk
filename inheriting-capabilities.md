# Windchill REST Services - Inheriting Capabilities

## Overview

Inheriting capabilities are reusable behavior modules that entity types can inherit to gain standardized properties, navigation properties, actions, and functions. When an entity type inherits a capability, it automatically receives all the properties and operations defined by that capability.

Capabilities are declared in the Domain JSON entity configuration using the `inherits` array:

```json
{
  "entityType": "Part",
  "inherits": [
    { "name": "versioned" },
    { "name": "workable" },
    { "name": "lifecycleManaged" },
    { "name": "contentHolder" },
    { "name": "foldered" },
    { "name": "contextManaged" },
    { "name": "viewManageable" },
    { "name": "representable" },
    { "name": "organizationOwned" },
    { "name": "subtypeable" },
    { "name": "softattributable" },
    { "name": "classifiable" },
    { "name": "securityLabeled" },
    { "name": "optionSetAssignable" },
    { "name": "expressionAssignable" },
    { "name": "effectivityManaged" },
    { "name": "sourcingRelationship" },
    { "name": "eventSubscribable" },
    { "name": "partAssociations" },
    { "name": "variantSpecs" },
    { "name": "serviceStructure" }
  ]
}
```

## Complete Capability Reference

### versioned

Enables version and revision tracking on an entity.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `VersionID` | String | Combined version identifier (e.g., `A.1`) |
| `Revision` | String | Revision letter (e.g., `A`, `B`) |
| `Version` | String | Version (iteration) number within a revision (e.g., `1`, `2`) |
| `Latest` | Boolean | Whether this is the latest version |

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `Versions` | Collection | All versions (iterations) of this object |
| `Revisions` | Collection | All revisions of this object |

**Actions:**

| Action | Description |
|---|---|
| `Revise` | Creates a new revision of the object. Returns the new revision. |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Versions
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Revisions
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.Revise
```

---

### workable

Enables check-out/check-in workflow for concurrent editing control.

**Actions:**

| Action | Description |
|---|---|
| `CheckOut` | Checks out the object for exclusive editing. Returns the working copy. |
| `CheckIn` | Checks in the working copy. Accepts optional `Comment` parameter. |
| `UndoCheckOut` | Cancels the checkout and discards working copy changes. |

**Functions:**

| Function | Return Type | Description |
|---|---|---|
| `IsCheckoutAllowed` | Boolean | Returns whether checkout is allowed for the current user |

**Example:**

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.CheckOut
CSRF_NONCE: <nonce_value>
```

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.CheckIn
Content-Type: application/json
CSRF_NONCE: <nonce_value>

{
  "Comment": "Updated geometry"
}
```

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.UndoCheckOut
CSRF_NONCE: <nonce_value>
```

---

### lifecycleManaged

Enables lifecycle state management on an entity.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `LifeCycleTemplateName` | String | Name of the lifecycle template assigned to this object |
| `State` | String | Current lifecycle state (e.g., `INWORK`, `UNDERREVIEW`, `RELEASED`, `CANCELLED`) |

**Actions:**

| Action | Description |
|---|---|
| `SetLifeCycleState` | Sets the lifecycle state. Requires `State` parameter. |

**Example:**

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.SetLifeCycleState
Content-Type: application/json
CSRF_NONCE: <nonce_value>

{
  "State": "RELEASED"
}
```

---

### contentHolder

Enables content (file) management on an entity.

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `PrimaryContent` | Single | The primary content file |
| `Attachments` | Collection | Secondary/attached content files |
| `Thumbnails` | Collection | Thumbnail images |
| `SmallThumbnails` | Collection | Small thumbnail images |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PrimaryContent
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Attachments
GET /Windchill/servlet/odata/DocMgmt/Documents('OR:wt.doc.WTDocument:12345')/PrimaryContent/$value
```

To upload content, use multipart POST with the content stream.

---

### foldered

Enables folder location tracking on an entity.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `FolderName` | String | Name of the folder containing this object |
| `CabinetName` | String | Name of the cabinet |
| `FolderLocation` | String | Full path of the folder (e.g., `/Default/Design/Brackets`) |

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `Folder` | Single | The folder entity containing this object |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')?$select=FolderName,CabinetName,FolderLocation
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Folder
```

---

### contextManaged

Associates the entity with a Windchill container context (product, library, project, etc.).

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `Context` | Single | The container context (product/library/project) |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Context
GET /Windchill/servlet/odata/ProdMgmt/Parts?$expand=Context&$filter=Context/Name eq 'MyProduct'
```

---

### viewManageable

Enables view assignment on an entity (e.g., Design view, Manufacturing view).

**Properties:**

| Property | Type | Description |
|---|---|---|
| `View` | String | The view name (e.g., `Design`, `Manufacturing`) |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$filter=View eq 'Design'
```

---

### representable

Enables 3D/2D representation access on an entity.

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `Representations` | Collection | Available representations (3D models, 2D drawings, etc.) |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Representations
```

---

### organizationOwned

Associates the entity with an organization.

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `Organization` | Single | The owning organization |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Organization
```

---

### subtypeable

Allows the entity to be a Windchill soft type. Soft types are user-defined subtypes of base types.

Soft types are identified by their `TypeID` property. When creating an entity of a soft type, specify the `@odata.type` annotation:

```json
{
  "@odata.type": "PTC.ProdMgmt.Part",
  "TypeID": "com.mycompany.MechanicalPart",
  "Number": "MP-0001",
  "Name": "Custom Bracket"
}
```

---

### softattributable

Allows the entity to have soft attributes (custom attributes defined on soft types). Soft attributes appear as dynamic properties on the entity.

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:...')?$select=Name,Number,CustomWeight,CustomMaterial
```

---

### classifiable

Enables classification of the entity using classification structures. Requires PTC PartsLink for Part classification.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `ClassificationInfo` | ComplexType | Contains classification node ID and classified attribute values |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')?$select=ClassificationInfo
```

Response:

```json
{
  "ClassificationInfo": {
    "ClassificationNodeId": "node_12345",
    "ClassificationNodeName": "Fasteners > Bolts",
    "Attributes": {
      "ThreadSize": "M10",
      "Length": "50mm"
    }
  }
}
```

---

### securityLabeled

Enables security label assignment on an entity.

**Properties:**

| Property | Type | Description |
|---|---|---|
| `SecurityLabels` | ComplexType | Map of security label names to values |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:...')?$select=SecurityLabels
```

```http
PATCH /Windchill/servlet/odata/ProdMgmt/Parts('OR:...')
Content-Type: application/json
CSRF_NONCE: <nonce_value>

{
  "SecurityLabels": {
    "ITAR": "UNRESTRICTED",
    "Export_Classification": "EAR99"
  }
}
```

---

### optionSetAssignable

Enables option set assignment for configurable products.

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `AssignedOptionSet` | Single | The option set assigned to this object |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/AssignedOptionSet
```

---

### expressionAssignable

Enables assignment of variant expressions for configurable products.

Entities with this capability can have variant expressions assigned that control product configuration.

---

### effectivityManaged

Added in v1.6. Enables effectivity information on an entity.

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `Effectivities` | Collection | Effectivity assignments (date, serial number, lot, unit, MSN, block) |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Effectivities
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Effectivities/PTC.EffectivityMgmt.DateEffectivity
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/Effectivities/PTC.EffectivityMgmt.UnitEffectivity
```

---

### sourcingRelationship

Enables AXL (Approved Exchange List) entries linking parts to manufacturer/vendor parts.

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `AXLEntries` | Collection(AXLEntry) | AML/AVL/AXL entries with full CRUD support |

**Example:**

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
  "ManufacturerPartNumber": "ACM-12345"
}
```

---

### eventSubscribable

Enables webhook/event subscription support on this entity type. Entities with this capability can be subscribed to via the EventMgmt domain.

See the [Event Management Domain](event-management-domain.md) for subscription examples.

---

### partAssociations

Added in v1.6. Enables navigation to associated objects (particularly CAD documents) from a Part.

**Navigation Properties:**

| Navigation | Type | Description |
|---|---|---|
| `PartAssociations` | Collection | Associated objects. Supports `$expand=RelatedCADDoc`. |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PartAssociations
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PartAssociations?$expand=RelatedCADDoc
```

---

### variantSpecs

Added in v1.6. Enables variant specification access and navigation.

**Functions:**

| Function | Return Type | Description |
|---|---|---|
| `GetAllVariantSpecifications` | Collection | Returns all variant specifications for the entity |

**Navigation Properties on VariantSpecification:**

| Navigation | Type | Description |
|---|---|---|
| `NavigationCriteria` | Single | Navigation criteria used by this variant spec |
| `ConfigurableModule` | Single | The configurable module associated with this variant spec |
| `OptionSet` | Single | The option set linked to this variant spec |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.GetAllVariantSpecifications
```

---

### serviceStructure

Enables service structure navigation and the GetStructure function.

**Functions:**

| Function | Return Type | Description |
|---|---|---|
| `GetStructure` | Collection | Returns the service structure hierarchy |

**Example:**

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:12345')/PTC.ProdMgmt.GetStructure
```

---

## Capability Combinations by Entity Type

Common entity types and their typical capabilities:

| Entity Type | Key Capabilities |
|---|---|
| Part | versioned, workable, lifecycleManaged, contentHolder, foldered, contextManaged, viewManageable, representable, organizationOwned, subtypeable, softattributable, classifiable, securityLabeled, effectivityManaged, sourcingRelationship, partAssociations, variantSpecs |
| Document | versioned, workable, lifecycleManaged, contentHolder, foldered, contextManaged, organizationOwned, subtypeable, softattributable |
| CADDocument | versioned, workable, lifecycleManaged, contentHolder, foldered, contextManaged, organizationOwned, subtypeable, securityLabeled |
| ChangeRequest | versioned, lifecycleManaged, foldered, contextManaged, organizationOwned, subtypeable |
| ChangeNotice | versioned, lifecycleManaged, foldered, contextManaged, organizationOwned, subtypeable |

## JSON Configuration Reference

Full example of an entity type with capabilities in Domain JSON:

```json
{
  "entityTypes": [
    {
      "name": "Part",
      "windchillType": "wt.part.WTPart",
      "inherits": [
        { "name": "versioned" },
        { "name": "workable" },
        { "name": "lifecycleManaged" },
        { "name": "contentHolder" },
        { "name": "foldered" },
        { "name": "contextManaged" },
        { "name": "viewManageable" },
        { "name": "representable" },
        { "name": "organizationOwned" },
        { "name": "subtypeable" },
        { "name": "softattributable" },
        { "name": "classifiable" },
        { "name": "securityLabeled" },
        { "name": "optionSetAssignable" },
        { "name": "expressionAssignable" },
        { "name": "effectivityManaged" },
        { "name": "sourcingRelationship" },
        { "name": "eventSubscribable" },
        { "name": "partAssociations" },
        { "name": "variantSpecs" },
        { "name": "serviceStructure" }
      ],
      "properties": [
        { "name": "Source", "windchillAttribute": "source" },
        { "name": "DefaultUnit", "windchillAttribute": "defaultUnit" }
      ]
    }
  ]
}
```
