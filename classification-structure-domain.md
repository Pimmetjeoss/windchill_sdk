# Classification Structure Domain (ClfStructure)

## Overview

The Classification Structure domain provides REST API access to classification hierarchies (nodes, attributes, and classified objects) in Windchill. This is used for managing parts classification taxonomies.

**Domain Name:** `ClfStructure`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/ClfStructure
```

**Metadata URL:**
```
GET /ClfStructure/$metadata
```

## Entity Sets

### ClassificationNodes

Represents nodes in a Windchill classification hierarchy.

**Entity Set URL:**
```
GET /ClfStructure/ClassificationNodes
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Node name |
| `Description` | Edm.String | Node description |
| `InternalName` | Edm.String | Internal identifier of the node |
| `NodeType` | Edm.String | Type of classification node |
| `HierarchyID` | Edm.String | ID of the parent hierarchy |
| `HierarchyName` | Edm.String | Name of the parent hierarchy |
| `ParentID` | Edm.String | ID of the parent node (empty for root nodes) |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Children` | ClassificationNodes | Child nodes in the hierarchy |
| `ClassificationAttributes` | ClassificationAttributes | Attributes defined on this node |
| `ClassifiedObjects` | ClassifiedObjects | Objects classified under this node |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve classification nodes |

**Example - Get root nodes:**
```http
GET /ClfStructure/ClassificationNodes?$filter=ParentID eq ''
```

**Example - Get children of a node:**
```http
GET /ClfStructure/ClassificationNodes('OR:com.ptc.core.lwc.server.LWCStructureNode:12345')/Children
```

---

### ClassificationAttributes

Represents classification attributes (properties) defined on classification nodes.

**Entity Set URL:**
```
GET /ClfStructure/ClassificationAttributes
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Attribute name |
| `InternalName` | Edm.String | Internal identifier |
| `Description` | Edm.String | Attribute description |
| `DataType` | Edm.String | Data type of the attribute (e.g., `STRING`, `REAL_NUMBER`, `INTEGER`, `BOOLEAN`, `TIMESTAMP`) |
| `DefaultValue` | Edm.String | Default value |
| `IsMandatory` | Edm.Boolean | Whether the attribute is required |
| `UnitOfMeasure` | Edm.String | Unit of measure (if applicable) |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve classification attributes |

---

### ClassifiedObjects

Represents objects that have been classified under a classification node.

**Entity Set URL (via navigation):**
```
GET /ClfStructure/ClassificationNodes('...')/ClassifiedObjects
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier of the classified object |
| `Name` | Edm.String | Object name |
| `Number` | Edm.String | Object number |
| `Type` | Edm.String | Object type |
| `NodeID` | Edm.String | Classification node ID |
| `NodeName` | Edm.String | Classification node name |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve classified objects |

---

## Functions

### GetChildNodes

Retrieves child nodes of a classification node.

**URL:**
```
GET /ClfStructure/GetChildNodes(NodeID='OR:com.ptc.core.lwc.server.LWCStructureNode:12345')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `NodeID` | Edm.String | Yes | Parent node object reference |

**Returns:** Collection of ClassificationNode entities

---

### GetClassificationAttributes

Retrieves the classification attributes for a node, including inherited attributes from parent nodes.

**URL:**
```
GET /ClfStructure/GetClassificationAttributes(NodeID='OR:com.ptc.core.lwc.server.LWCStructureNode:12345')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `NodeID` | Edm.String | Yes | Node object reference |

**Returns:** Collection of ClassificationAttribute entities

---

### GetRootNodes

Retrieves the root nodes of a classification hierarchy.

**URL:**
```
GET /ClfStructure/GetRootNodes(HierarchyName='Parts Classification')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `HierarchyName` | Edm.String | Yes | Name of the classification hierarchy |

**Returns:** Collection of ClassificationNode entities

---

## Query Examples

**Get all root classification nodes:**
```http
GET /ClfStructure/ClassificationNodes?$filter=ParentID eq ''
```

**Get classification attributes for a node (with expand):**
```http
GET /ClfStructure/ClassificationNodes('OR:com.ptc.core.lwc.server.LWCStructureNode:12345')?$expand=ClassificationAttributes
```

**Get classified objects under a node:**
```http
GET /ClfStructure/ClassificationNodes('OR:com.ptc.core.lwc.server.LWCStructureNode:12345')/ClassifiedObjects
```

**Filter classification nodes by name:**
```http
GET /ClfStructure/ClassificationNodes?$filter=contains(Name,'Fastener')
```
