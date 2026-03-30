# PTC CAD Document Management Domain

> **Domain ID:** `CADDocumentMgmt`
> **Base URL:** `/Windchill/servlet/odata/CADDocumentMgmt`
> **Metadata URL:** `/Windchill/servlet/odata/CADDocumentMgmt/$metadata`
> **Added in:** Windchill REST Services 1.4

The PTC CAD Document Management domain provides access to the CAD data management capabilities of Windchill. CAD data management uses business objects, referred to as CAD documents, to contain and manage CAD information in a Windchill database. A CAD document is a revision-controlled and lifecycle-managed object containing a CAD model or drawing file. The CAD model can be a file or a set of files containing information in a CAD application format.

## Entities

| Item | OData Entity | Windchill Class | Description |
|------|-------------|----------------|-------------|
| CAD document | `CADDocument` | `EPMDocument` / `EPMDocumentMaster` (internal names: `DefaultEPMDocument`, `DefaultEPMDocumentMaster`) | Represents a version of a CAD document. |
| CAD document usage link | `CADDocumentUse` | `EPMMemberLink` (internal: `DefaultEPMMemberLink`) | Represents the link between a parent assembly and its components. Contains attributes such as quantity, unit, location, etc. |
| CAD document reference | `CADDocumentReference` | `EPMReferenceLink` (internal: `DefaultEPMReferenceLink`) | Represents the link between a CAD document and its references. References are relationships between files without a hierarchical/structural relationship. |
| Derived source | `DerivedSource` | `EPMDerivedRepHistory` | Represents the link between an image CAD document and its source. An image is an object that has copied most of its content from a source object. |
| Part associations | `PartAssociation` | - | Represents association links between a CAD document and a `WTPart`. |
| Build rule association | `BuildRuleAssociation` | `EPMBuildRule` | Link between CAD document and WTPart for all associations except Content. |
| Build history association | `BuildHistoryAssociation` | `EPMBuildHistory` | Link between CAD document and WTPart (historical build info). |
| Content association | `ContentAssociation` | `EPMDescribeLink` | Link between CAD document and WTPart for content association type. |
| CAD document structure | `CADStructure` | - | Represents the CAD structure expanded to the required number of levels. Use the `GetStructure` action to retrieve it. |

## Entity Sets

| Entity Set | Description |
|-----------|-------------|
| `CADDocuments` | Collection of CAD document entities |

## Navigation Properties on CADDocument

| Navigation Property | Description |
|--------------------|-------------|
| `AllPrimaryContents` | Returns URLs to download primary content directly downloadable in Windchill. |
| `Uses` | Components of the CAD assembly (`CADDocumentUse` links) |
| `References` | Reference links to other CAD documents |
| `DerivedSources` | Links to source documents for image CAD documents |
| `PartAssociations` | Association links to WTPart entities |

### AllPrimaryContents Notes

- Supports all primary content that is directly downloadable in Windchill. Returns URLs to download the content.
- Primary content that is not directly downloadable (e.g., CAD assemblies that open in Creo Parametric) is **not** supported.
- When a CAD document has no primary content or only unsupported primary content, the response returns: `"AllPrimaryContents": []`
- The `PrimaryContent` navigation property is **not supported** for the `CADDocument` entity. Use `AllPrimaryContents` instead.

## Key URLs

### Retrieve a Specific CAD Document

```
GET /Windchill/servlet/odata/v1/CADDocumentMgmt/CADDocuments('OR%3Awt.epm.EPMDocument%3A167183')
```

### Retrieve CAD Document with Expanded Navigation

```
GET /Windchill/servlet/odata/v1/CADDocumentMgmt/CADDocuments('OR%3Awt.epm.EPMDocument%3A167183')?$expand=Uses
```

### Query CAD Documents Using a Filter

```
GET /Windchill/servlet/odata/v1/CADDocumentMgmt/CADDocuments?$filter=FileName eq 'ABC.prt'
```

### Retrieve Related Parts for a CAD Document

```
GET /Windchill/servlet/odata/v1/CADDocumentMgmt/CADDocuments('OR%3Awt.epm.EPMDocument%3A167183')?$expand=PartAssociations($expand=RelatedParts)
```

**Note:** Related parts information is NOT returned in the following cases:
- When a CAD document contains model items related to a Part
- When a CAD document has a custom association to a Part
- When a CAD document drawing has a calculated association to a Part

### Retrieve References for a CAD Document

```
GET /Windchill/servlet/odata/v1/CADDocumentMgmt/CADDocuments('OR%3Awt.epm.EPMDocument%3A167183')?$expand=References
```

### Retrieve Source for an Image CAD Document

```
GET /Windchill/servlet/odata/v1/CADDocumentMgmt/CADDocuments('OR%3Awt.epm.EPMDocument%3A167183')?$expand=DerivedSources($expand=SourceCADDocuments)
```

## GetStructure Action

The `GetStructure` action returns a CAD structure. The action is bound to the `CADDocument` entity.

### Request

```http
POST /Windchill/servlet/odata/v1/CADDocumentMgmt/CADDocuments('OR%3Awt.epm.EPMDocument%3A167183')/PTC.CADDocumentMgmt.GetStructure?$expand=Components($levels=max) HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

### Request Body Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `NavigationCriteria` (ID) | `String` | default filter | ID of the saved filter to use as filter criteria. If not specified, the default filter is used. |
| `NavigationCriteria` (inline) | `Object` | - | Alternatively, specify the full navigation criteria in the request payload. |
| `BOMMembersOnly` | `Boolean` | `false` | If `true`, only CAD documents that participate in the BOM structure are returned. |

### Example: Retrieve Structure with BOMMembersOnly

```json
{
  "BOMMembersOnly": true
}
```

### Response Attributes

The action returns additional attributes in the response:

| Attribute | Description |
|-----------|-------------|
| `Resolved` | Boolean indicating if the link to the document is resolved in the configuration specification. |
| `PVTreeId` | Occurrence path of the CAD assembly to its member subcomponents in the viewable file. Full path from root. Used to work with Visualization tree. |
| `PVParentTreeId` | Occurrence path to the parent of the component part in the viewable file. Full path from root. |

### BOMMembersOnly Behavior

- If `BOMMembersOnly` is `true`, CAD documents not participating in the BOM structure are excluded.
- The preferences set for the **Auto Associate** action in Windchill are honored by `GetStructure` while returning the structure.
- Document types/subtypes added in `Utilities > Preference Management > Operation > Auto Associate > Disallow Structure CAD Document Types` do not participate in the BOM structure.
- CAD documents with a reusable attribute set in `Utilities > Preference Management > Operation > Auto Associate > Part Structure Override Attribute Name` are also excluded.
- If the BOM structure contains documents the user does not have access to, unresolved dependents may still be returned even when `BOMMembersOnly` is `true`.

## Inherited Capabilities (added in v1.4)

| Capability | Entities |
|-----------|----------|
| `subtypeable` | `CADDocument` |
| `softattributable` | `CADDocument`, `CADDocumentUse`, `CADDocumentReference` |
