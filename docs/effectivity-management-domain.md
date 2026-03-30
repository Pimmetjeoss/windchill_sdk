# PTC Effectivity Management Domain

> **Domain ID:** `EffectivityMgmt`
> **Base URL:** `/Windchill/servlet/odata/EffectivityMgmt`
> **Metadata URL:** `/Windchill/servlet/odata/EffectivityMgmt/$metadata`
> **Added in:** Windchill REST Services 1.6

The PTC Effectivity Management domain enables you to access effectivity information of Windchill objects. Effectivity is the planned date, lot, or serial number at which old versions of the object are replaced with new versions in production.

## Effectivity-Managed Objects

Objects that can be effectivity-managed include:

- **Parts** and **documents**
- **Manufacturing process objects** such as process plans, sequences, and operations
- **Manufacturing resources** such as plants, resource groups, skills, process materials, tooling, and work centers

## Entities

The following table lists the significant OData entities available in the PTC Effectivity Management domain. To see all entities, refer to the EDM of the domain at the metadata URL.

| OData Entity | Description |
|-------------|-------------|
| `PartEffectivityContext` | Represents the effectivity context for a part. Accessed via the `PartEffectivityContexts` entity set. |
| `Effectivity` | Base entity type for all effectivity types. |
| `DateEffectivity` | Represents date-based effectivity. Objects become effective at a specific date or date range. |
| `SerialNumberEffectivity` | Represents serial-number-based effectivity. Objects become effective at specific serial numbers. |
| `LotEffectivity` | Represents lot-based effectivity. Objects become effective for a specific lot. |
| `UnitEffectivity` | Represents unit-based effectivity. Objects become effective at a specific unit range. |
| `MSNEffectivity` | Represents MSN (Manufacturing Serial Number) effectivity. |
| `BlockEffectivity` | Represents block-based effectivity. |

## Entity Sets

| Entity Set | Description |
|-----------|-------------|
| `PartEffectivityContexts` | Collection of effectivity contexts for parts |

## Key URLs

### Retrieve Effectivity Contexts

```
GET /Windchill/servlet/odata/EffectivityMgmt/PartEffectivityContexts
```

### Retrieve a Specific Effectivity Context

```
GET /Windchill/servlet/odata/EffectivityMgmt/PartEffectivityContexts('OR:wt.part.WTPartMaster:156014')
```

### Retrieve Effectivity Context with Organization

```
GET /Windchill/servlet/odata/EffectivityMgmt/PartEffectivityContexts('OR:wt.part.WTPartMaster:156014')?$expand=Organization
```

### Retrieve Effectivities of a Part (via Product Management Domain)

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:156011')?$expand=Effectivities
```

### Retrieve Effectivities with Effectivity Context Expanded

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:156011')?$expand=Effectivities($expand=EffectivityContext)
```

### Retrieve Date Effectivities

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:156011')?$expand=Effectivities/PTC.EffectivityMgmt.DateEffectivity
```

### Retrieve Unit Effectivities

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:156011')?$expand=Effectivities/PTC.EffectivityMgmt.UnitEffectivity
```

### Retrieve Block Effectivities

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:156011')?$expand=Effectivities/PTC.EffectivityMgmt.BlockEffectivity
```

### Retrieve Effectivities on an Independent Assigned Expression

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('<part_id>')?$expand=Effectivities($expand=AssignedExpression)
```

## Cross-Domain Usage

The Effectivity Management domain works together with other domains:

### Product Management Domain Integration

Parts in the Product Management domain have an `Effectivities` navigation property (enabled by the `effectivityManaged` capability) that links to entities in the Effectivity Management domain.

```
GET /Windchill/servlet/odata/ProdMgmt/Parts?$expand=Effectivities
```

### GetAssignedExpression Function

To retrieve assigned expressions for effectivity-managed objects, use the `GetAssignedExpression()` function defined in the PTC Product Management domain.

## Navigation Properties

### On PartEffectivityContext

| Navigation Property | Description |
|--------------------|-------------|
| `Organization` | The organization associated with the effectivity context |

### On Effectivity Entities

| Navigation Property | Description |
|--------------------|-------------|
| `EffectivityContext` | The effectivity context for this effectivity |
| `AssignedExpression` | Expression assigned to the effectivity |

## Effectivity Types

### DateEffectivity

Effectivity based on date ranges. Key properties include:

| Property | Type | Description |
|----------|------|-------------|
| `StartDate` | `DateTimeOffset` | Start date of the effectivity |
| `EndDate` | `DateTimeOffset` | End date of the effectivity |

### UnitEffectivity

Effectivity based on unit/serial/lot numbers. Subtypes include:

- **Serial number effectivity** -- Based on specific serial numbers
- **Lot number effectivity** -- Based on lot numbers
- **Block effectivity** -- Based on block ranges (MSN, etc.)

### BlockEffectivity

Effectivity based on named blocks of units.

## Notes

- The `effectivityManaged` capability in an entity's `inherits` property enables the `Effectivities` navigation property.
- Only **product effectivity** is supported (not manufacturing effectivity).
- Both dependent and independent expression modes are supported for assigned expressions.
- Basic and advanced types of expressions are supported.
- Use the `Effectivities` navigation property on Part (ProdMgmt domain) and `IndependentAssignedExpression` to access effectivity data.
