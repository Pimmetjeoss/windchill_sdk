# Entity Data Model (EDM)

## Overview

Each Windchill REST Services domain exposes an **Entity Data Model (EDM)** that describes the structure of its OData service. The EDM defines entity types, entity sets, properties, navigation properties, actions, functions, and complex types. It is the schema contract between the server and OData clients.

## Metadata URL

The EDM is available at the `$metadata` endpoint of each domain:

```
GET /Windchill/servlet/odata/{DomainID}/$metadata
```

### Examples

```
GET /Windchill/servlet/odata/ProdMgmt/$metadata
GET /Windchill/servlet/odata/DocMgmt/$metadata
GET /Windchill/servlet/odata/ChangeMgmt/$metadata
GET /Windchill/servlet/odata/PDM/$metadata
```

## CSDL Format

The metadata document is returned in **CSDL (Common Schema Definition Language)** format, which is an XML-based schema language defined by the OData specification.

### Example CSDL Response

```xml
<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:Reference Uri="/Windchill/servlet/odata/PTC/$metadata">
    <edmx:Include Namespace="PTC" Alias="PTC" />
  </edmx:Reference>
  <edmx:DataServices>
    <Schema Namespace="PTC.ProdMgmt" xmlns="http://docs.oasis-open.org/odata/ns/edm">

      <!-- Entity Type Definition -->
      <EntityType Name="Part">
        <Key>
          <PropertyRef Name="ID" />
        </Key>
        <Property Name="ID" Type="Edm.String" Nullable="false" />
        <Property Name="Number" Type="Edm.String" />
        <Property Name="Name" Type="Edm.String" />
        <Property Name="Description" Type="Edm.String" />
        <Property Name="State" Type="Edm.String" />
        <Property Name="Source" Type="Edm.String" />
        <Property Name="DefaultUnit" Type="Edm.String" />
        <Property Name="View" Type="Edm.String" />
        <Property Name="VersionID" Type="Edm.String" />
        <Property Name="Revision" Type="Edm.String" />
        <Property Name="Version" Type="Edm.String" />
        <Property Name="Latest" Type="Edm.Boolean" />
        <Property Name="LifeCycleTemplateName" Type="Edm.String" />
        <Property Name="FolderName" Type="Edm.String" />
        <Property Name="CabinetName" Type="Edm.String" />
        <Property Name="FolderLocation" Type="Edm.String" />
        <NavigationProperty Name="Uses" Type="Collection(PTC.ProdMgmt.PartUse)" />
        <NavigationProperty Name="Versions" Type="Collection(PTC.ProdMgmt.Part)" />
        <NavigationProperty Name="Revisions" Type="Collection(PTC.ProdMgmt.Part)" />
        <NavigationProperty Name="Context" Type="PTC.DataAdmin.Container" />
        <NavigationProperty Name="Organization" Type="PTC.PrincipalMgmt.Organization" />
        <NavigationProperty Name="Folder" Type="PTC.DataAdmin.Folder" />
        <NavigationProperty Name="PrimaryContent" Type="PTC.ProdMgmt.PartContent" />
        <NavigationProperty Name="Attachments" Type="Collection(PTC.ProdMgmt.PartContent)" />
        <NavigationProperty Name="Representations" Type="Collection(PTC.Visualization.Representation)" />
        <NavigationProperty Name="AXLEntries" Type="Collection(PTC.ProdMgmt.AXLEntry)" />
        <NavigationProperty Name="PartAssociations" Type="Collection(PTC.ProdMgmt.PartAssociation)" />
        <NavigationProperty Name="Effectivities" Type="Collection(PTC.EffectivityMgmt.Effectivity)" />
      </EntityType>

      <!-- Entity Set (Collection) -->
      <EntityContainer Name="ProdMgmtContainer">
        <EntitySet Name="Parts" EntityType="PTC.ProdMgmt.Part">
          <NavigationPropertyBinding Path="Context" Target="PTC.DataAdmin.DataAdminContainer/Containers" />
          <NavigationPropertyBinding Path="Organization" Target="PTC.PrincipalMgmt.PrincipalMgmtContainer/Organizations" />
        </EntitySet>
        <EntitySet Name="BOMs" EntityType="PTC.ProdMgmt.BOM" />
      </EntityContainer>

      <!-- Bound Action -->
      <Action Name="CheckOut" IsBound="true">
        <Parameter Name="bindingParameter" Type="PTC.ProdMgmt.Part" />
        <ReturnType Type="PTC.ProdMgmt.Part" />
      </Action>

      <Action Name="CheckIn" IsBound="true">
        <Parameter Name="bindingParameter" Type="PTC.ProdMgmt.Part" />
        <Parameter Name="Comment" Type="Edm.String" />
        <ReturnType Type="PTC.ProdMgmt.Part" />
      </Action>

      <!-- Bound Function -->
      <Function Name="GetAllVariantSpecifications" IsBound="true">
        <Parameter Name="bindingParameter" Type="PTC.ProdMgmt.Part" />
        <ReturnType Type="Collection(PTC.ProdMgmt.VariantSpecification)" />
      </Function>

      <!-- Complex Type -->
      <ComplexType Name="QuantityOfMeasureType">
        <Property Name="Value" Type="Edm.Double" />
        <Property Name="Unit" Type="Edm.String" />
      </ComplexType>

    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
```

## Service Document

The **service document** is generated dynamically when a client accesses the domain root URL (without `$metadata`). It lists all entity sets available in the domain.

```
GET /Windchill/servlet/odata/ProdMgmt
```

Response:

```json
{
  "@odata.context": "$metadata",
  "value": [
    {
      "name": "Parts",
      "url": "Parts",
      "kind": "EntitySet"
    },
    {
      "name": "BOMs",
      "url": "BOMs",
      "kind": "EntitySet"
    }
  ]
}
```

## EDM Generation

The EDM is **generated per domain** based on:

1. **Domain JSON configuration** -- Defines entity types, properties, navigation properties, and capabilities
2. **Inheriting capabilities** -- Capabilities like `versioned`, `workable`, etc. contribute additional properties and operations to the EDM
3. **Windchill type system** -- Soft types and soft attributes are dynamically included

The EDM is regenerated when:
- The domain configuration changes
- New soft types or soft attributes are added in Windchill
- The server is restarted

## Cross-Domain References

Domains can reference entity types from other domains using `edmx:Reference`:

```xml
<edmx:Reference Uri="/Windchill/servlet/odata/PTC/$metadata">
  <edmx:Include Namespace="PTC" Alias="PTC" />
</edmx:Reference>
<edmx:Reference Uri="/Windchill/servlet/odata/DataAdmin/$metadata">
  <edmx:Include Namespace="PTC.DataAdmin" />
</edmx:Reference>
```

The PDM conglomerate domain does not use external references -- it includes all schemas inline, which is required for BI tools like PowerBI and Excel that do not resolve external `edmx:Reference` elements.

## Key EDM Concepts for Automation

| Concept | OData Term | Description |
|---|---|---|
| Windchill type | EntityType | Defines the shape (properties + navigations) of an entity |
| Collection | EntitySet | A queryable set of entities of a given type |
| Property | Property | A scalar value on an entity (String, Int32, Boolean, etc.) |
| Relationship | NavigationProperty | A link to one or more related entities |
| Write operation | Action | A POST-based operation that may have side effects |
| Read operation | Function | A GET-based operation that returns data without side effects |
| Structured value | ComplexType | A group of properties (not independently addressable) |
| Key | Key/PropertyRef | The property or properties that uniquely identify an entity |

## Notes

- The EDM is the source of truth for what properties and operations are available on each entity type.
- OData clients (including code generators) use `$metadata` to discover the API surface.
- The `ID` property (Windchill Object Reference) is always the entity key.
- Navigation properties that cross domain boundaries use `edmx:Reference` to declare the external schema dependency.
