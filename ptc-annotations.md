# PTC Annotations

## Overview

PTC Annotations are custom OData annotations defined by PTC for Windchill REST Services. They extend the standard OData metadata to provide Windchill-specific information about entities, properties, and capabilities. Annotations appear in the `$metadata` document of each domain.

**Namespace:** `PTC` (used as prefix in annotation terms)

## Annotation Terms

### PTC.ReadOnly

Indicates that a property is read-only and cannot be set in POST or PATCH requests.

**Applies to:** Property

**Type:** Edm.Boolean

**Example in $metadata:**
```xml
<Property Name="ID" Type="Edm.String">
  <Annotation Term="PTC.ReadOnly" Bool="true"/>
</Property>
```

**Usage note:** Properties marked as `PTC.ReadOnly` will be ignored if included in POST or PATCH payloads.

---

### PTC.Filterable

Indicates whether a property supports the `$filter` query parameter.

**Applies to:** Property

**Type:** Edm.Boolean

**Example in $metadata:**
```xml
<Property Name="Name" Type="Edm.String">
  <Annotation Term="PTC.Filterable" Bool="true"/>
</Property>
```

**Usage note:** Only properties with `PTC.Filterable=true` can be used in `$filter` expressions. Attempting to filter on a non-filterable property returns an error.

---

### PTC.Sortable

Indicates whether a property supports the `$orderby` query parameter.

**Applies to:** Property

**Type:** Edm.Boolean

**Example in $metadata:**
```xml
<Property Name="Name" Type="Edm.String">
  <Annotation Term="PTC.Sortable" Bool="true"/>
</Property>
```

---

### PTC.Searchable

Indicates whether a property supports the `$search` query parameter.

**Applies to:** Property

**Type:** Edm.Boolean

---

### PTC.Required

Indicates that a property is required when creating an entity (POST).

**Applies to:** Property

**Type:** Edm.Boolean

**Example in $metadata:**
```xml
<Property Name="Number" Type="Edm.String">
  <Annotation Term="PTC.Required" Bool="true"/>
</Property>
```

---

### PTC.Updatable

Indicates whether a property can be updated via PATCH.

**Applies to:** Property

**Type:** Edm.Boolean

---

### PTC.Insertable

Indicates whether a property can be set during creation (POST).

**Applies to:** Property

**Type:** Edm.Boolean

---

### PTC.MaxLength

Specifies the maximum length of a string property value.

**Applies to:** Property (Edm.String)

**Type:** Edm.Int32

**Example in $metadata:**
```xml
<Property Name="Name" Type="Edm.String">
  <Annotation Term="PTC.MaxLength" Int="200"/>
</Property>
```

---

### PTC.DefaultValue

Specifies the default value for a property.

**Applies to:** Property

**Type:** Varies

**Example in $metadata:**
```xml
<Property Name="Source" Type="Edm.String">
  <Annotation Term="PTC.DefaultValue" String="Buy"/>
</Property>
```

---

### PTC.EnumValues

Specifies the list of valid values for a property (enumeration constraint).

**Applies to:** Property

**Type:** Collection(Edm.String)

**Example in $metadata:**
```xml
<Property Name="Source" Type="Edm.String">
  <Annotation Term="PTC.EnumValues">
    <Collection>
      <String>Buy</String>
      <String>Make</String>
      <String>Make or Buy</String>
    </Collection>
  </Annotation>
</Property>
```

---

### PTC.DisplayName

Specifies the localized display name for a property or entity type.

**Applies to:** Property, EntityType

**Type:** Edm.String

**Example in $metadata:**
```xml
<Property Name="CreatedOn" Type="Edm.DateTimeOffset">
  <Annotation Term="PTC.DisplayName" String="Created On"/>
</Property>
```

---

### PTC.WindchillType

Maps an OData entity type to the underlying Windchill Java type.

**Applies to:** EntityType

**Type:** Edm.String

**Example in $metadata:**
```xml
<EntityType Name="Part">
  <Annotation Term="PTC.WindchillType" String="wt.part.WTPart"/>
</EntityType>
```

**Usage note:** This annotation is useful for understanding which Windchill persistable class backs the OData entity.

---

### PTC.Expandable

Indicates whether a navigation property supports `$expand`.

**Applies to:** NavigationProperty

**Type:** Edm.Boolean

---

### PTC.NavigationFilterable

Indicates whether a navigation property supports `$filter` with lambda operators (`any`, `all`).

**Applies to:** NavigationProperty

**Type:** Edm.Boolean

---

### PTC.SupportedOperations

Lists the HTTP operations supported for an entity set.

**Applies to:** EntitySet

**Type:** Collection(Edm.String)

**Example in $metadata:**
```xml
<EntitySet Name="Parts" EntityType="ProdMgmt.Part">
  <Annotation Term="PTC.SupportedOperations">
    <Collection>
      <String>GET</String>
      <String>POST</String>
      <String>PATCH</String>
      <String>DELETE</String>
    </Collection>
  </Annotation>
</EntitySet>
```

---

## Reading Annotations from $metadata

To retrieve the full metadata with annotations for a domain:

```http
GET /Windchill/servlet/odata/ProdMgmt/$metadata
Accept: application/xml
```

The response is an EDMX (Entity Data Model XML) document containing entity types, properties, and their annotations.

---

## Using Annotations for SDK Logic

When building SDK clients, annotations can be used to:

1. **Validate payloads before sending:** Check `PTC.Required` and `PTC.ReadOnly` to build valid POST/PATCH payloads.
2. **Build query UIs:** Use `PTC.Filterable` and `PTC.Sortable` to determine which properties can be used in filters and sorting.
3. **Show valid values:** Use `PTC.EnumValues` to populate dropdown menus.
4. **Enforce constraints:** Use `PTC.MaxLength` for input validation.
5. **Map to Windchill types:** Use `PTC.WindchillType` for type-aware logic.

---

## Example: Parsing Annotations Programmatically

```javascript
// Fetch metadata
const response = await fetch('/Windchill/servlet/odata/ProdMgmt/$metadata');
const xml = await response.text();
const parser = new DOMParser();
const doc = parser.parseFromString(xml, 'application/xml');

// Find all filterable properties
const properties = doc.querySelectorAll('Property');
properties.forEach(prop => {
  const filterAnnotation = prop.querySelector('Annotation[Term="PTC.Filterable"]');
  if (filterAnnotation && filterAnnotation.getAttribute('Bool') === 'true') {
    console.log(`Filterable: ${prop.getAttribute('Name')}`);
  }
});
```
