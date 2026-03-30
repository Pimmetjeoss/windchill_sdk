# Visualization Domain (Visualization)

## Overview

The Visualization domain provides REST API access to visualization-related objects in Windchill, including thumbnail images, representation data, and 3D viewable structures.

**Domain Name:** `Visualization`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/Visualization
```

**Metadata URL:**
```
GET /Visualization/$metadata
```

## Entity Sets

### Representations

Represents visualization representations (viewable files) associated with Windchill objects.

**Entity Set URL:**
```
GET /Visualization/Representations
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Representation name |
| `Description` | Edm.String | Representation description |
| `RepresentationType` | Edm.String | Type of representation (e.g., `Default`, `Design`, `Lightweight`) |
| `Format` | Edm.String | File format (e.g., `PVS`, `OL`, `ED`) |
| `IsOutOfDate` | Edm.Boolean | Whether the representation is out of date |
| `SourceObjectID` | Edm.String | ID of the source object |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `RepresentationFiles` | RepresentationFiles | Files within this representation |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve representations |

---

### RepresentationFiles

Represents individual files within a representation.

**Entity Set URL (via navigation):**
```
GET /Visualization/Representations('...')/RepresentationFiles
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `FileName` | Edm.String | File name |
| `FileSize` | Edm.Int64 | File size in bytes |
| `ContentType` | Edm.String | MIME content type |
| `DownloadURL` | Edm.String | URL to download the file |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve representation files |

---

### Thumbnails

Represents thumbnail images for Windchill objects.

**Entity Set URL:**
```
GET /Visualization/Thumbnails
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `SourceObjectID` | Edm.String | ID of the source object |
| `ImageURL` | Edm.String | URL of the thumbnail image |
| `SmallImageURL` | Edm.String | URL of the small thumbnail image |
| `ContentType` | Edm.String | MIME type of the image |
| `Width` | Edm.Int32 | Image width in pixels |
| `Height` | Edm.Int32 | Image height in pixels |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve thumbnails |

---

## Functions

### GetThumbnail

Retrieves the thumbnail image for a specific Windchill object.

**URL:**
```
GET /Visualization/GetThumbnail(ObjectID='OR:wt.part.WTPart:12345')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ObjectID` | Edm.String | Yes | Object reference ID |

**Returns:** Thumbnail entity with image URL

---

### GetRepresentations

Retrieves all representations for a specific Windchill object.

**URL:**
```
GET /Visualization/GetRepresentations(ObjectID='OR:wt.part.WTPart:12345')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ObjectID` | Edm.String | Yes | Object reference ID |

**Returns:** Collection of Representation entities

---

### GetStructure

Retrieves the 3D structure (product structure with visualization data) for a part.

**URL:**
```
GET /Visualization/GetStructure(ObjectID='OR:wt.part.WTPart:12345')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ObjectID` | Edm.String | Yes | Object reference ID of the root part |

**Returns:** Hierarchical structure with representation data

---

## Query Examples

**Get all representations:**
```http
GET /Visualization/Representations
```

**Get representations for a specific object:**
```http
GET /Visualization/GetRepresentations(ObjectID='OR:wt.part.WTPart:12345')
```

**Get thumbnail for a part:**
```http
GET /Visualization/GetThumbnail(ObjectID='OR:wt.part.WTPart:12345')
```

**Get representation files:**
```http
GET /Visualization/Representations('OR:wt.representation.Representation:12345')/RepresentationFiles
```

**Filter representations by type:**
```http
GET /Visualization/Representations?$filter=RepresentationType eq 'Default'
```

**Filter out-of-date representations:**
```http
GET /Visualization/Representations?$filter=IsOutOfDate eq true
```
