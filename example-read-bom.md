# Reading a Bill of Materials (BOM)

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesReadBOM.html`

## Overview

Read the Bill of Materials (BOM) structure of a part by navigating from a parent part to its child components (UsesPartMaster). The BOM is represented through the `Uses` navigation property on the Part entity, which retrieves the part usage links (WTPartUsageLink) that connect a parent part to its child parts.

## Endpoint

```
GET https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Parts('<part_id>')/Uses
```

- **Domain**: ProdMgmt (PTC Product Management)
- **Entity Set**: `Parts`
- **Navigation Property**: `Uses`
- **HTTP Method**: GET
- **Returns**: Collection of `PartUseLink` entities

## Request

### Headers

| Header | Value |
|--------|-------|
| `Accept` | `application/json` |

### URL Parameters

| Parameter | Description |
|-----------|-------------|
| `<part_id>` | The ID (object reference) of the parent part, e.g., `OR:wt.part.WTPart:123456` |

### Example Request

```http
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123456')/Uses HTTP/1.1
Host: windchill.ptc.com
Accept: application/json
```

### With $expand to Get Child Part Details

To include the child part details in the same response, use `$expand`:

```http
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123456')/Uses?$expand=Uses HTTP/1.1
Host: windchill.ptc.com
Accept: application/json
```

## Response

### HTTP Status

- **200 OK** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/ProdMgmt/$metadata#PartUsageLinks",
  "value": [
    {
      "ID": "OR:wt.part.WTPartUsageLink:200001",
      "Quantity": 2.0,
      "Unit": "ea",
      "LineNumber": 10,
      "ReferenceDesignator": "",
      "TraceCode": "Untraced",
      "FindNumber": "1",
      "Uses@odata.navigationLink": "PartUsageLinks('OR:wt.part.WTPartUsageLink:200001')/Uses",
      "UsedBy@odata.navigationLink": "PartUsageLinks('OR:wt.part.WTPartUsageLink:200001')/UsedBy"
    },
    {
      "ID": "OR:wt.part.WTPartUsageLink:200002",
      "Quantity": 1.0,
      "Unit": "ea",
      "LineNumber": 20,
      "ReferenceDesignator": "R1",
      "TraceCode": "Untraced",
      "FindNumber": "2",
      "Uses@odata.navigationLink": "PartUsageLinks('OR:wt.part.WTPartUsageLink:200002')/Uses",
      "UsedBy@odata.navigationLink": "PartUsageLinks('OR:wt.part.WTPartUsageLink:200002')/UsedBy"
    }
  ]
}
```

### PartUsageLink Properties

| Property | Type | Description |
|----------|------|-------------|
| `ID` | String | Object reference of the usage link (`OR:wt.part.WTPartUsageLink:<dbid>`) |
| `Quantity` | Decimal | Quantity of the child part used |
| `Unit` | String | Unit of measure for the quantity |
| `LineNumber` | Int32 | Line number in the BOM |
| `ReferenceDesignator` | String | Reference designator for the component placement |
| `TraceCode` | String | Trace code: `Untraced`, `Lot Trace`, `Serial Trace` |
| `FindNumber` | String | Find number for the BOM line |

## Reading the Multi-Level BOM (Part Structure)

To read a multi-level BOM (part structure), use the `GetPartStructure` function:

```
GET https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/Parts('<part_id>')/PTC.ProdMgmt.GetPartStructure()
```

### Example Request

```http
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123456')/PTC.ProdMgmt.GetPartStructure() HTTP/1.1
Host: windchill.ptc.com
Accept: application/json
```

### GetPartStructure Response

The response returns a hierarchical collection containing the part structure with parent-child relationships at all levels.

## Navigating from Usage Link to Child Part

To get the child part details from a usage link, navigate using the `Uses` property:

```
GET https://<windchill_server>/Windchill/servlet/odata/ProdMgmt/PartUsageLinks('<link_id>')/Uses
```

## Using $expand for Inline BOM Data

Retrieve the BOM with child part details in a single request:

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123456')/Uses?$expand=Uses($select=ID,Number,Name,Version)
```

## Using $filter on BOM

Filter BOM entries:

```
GET /Windchill/servlet/odata/ProdMgmt/Parts('OR:wt.part.WTPart:123456')/Uses?$filter=Quantity gt 1
```

## Notes

- The `Uses` navigation returns the immediate (single-level) BOM.
- For multi-level BOM traversal, use `GetPartStructure()` or make recursive calls following `Uses` links.
- Navigation links in the response (`Uses@odata.navigationLink`, `UsedBy@odata.navigationLink`) can be followed to traverse the BOM tree.
- `Uses` navigates from the usage link to the child part.
- `UsedBy` navigates from the usage link back to the parent part.
- The BOM structure reflects the latest iteration of the parent part by default.
- Standard OData query options (`$filter`, `$select`, `$expand`, `$orderby`, `$top`, `$skip`) are supported on BOM navigations.
