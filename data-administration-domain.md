# Data Administration Domain (DataAdmin)

## Overview

The Data Administration domain provides REST API access to administrative objects in Windchill, such as containers, folders, cabinets, lifecycle templates, teams, and access control.

**Domain Name:** `DataAdmin`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/DataAdmin
```

**Metadata URL:**
```
GET /DataAdmin/$metadata
```

## Entity Sets

### Containers

Represents Windchill containers (Products, Libraries, Projects, etc.).

**Entity Set URL:**
```
GET /DataAdmin/Containers
```

**Key Property:** `ID` (Edm.String) - Object reference identifier (e.g., `OR:wt.inf.container.WTContainer:12345`)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Container name |
| `Description` | Edm.String | Container description |
| `ContainerType` | Edm.String | Type of container (e.g., `Product`, `Library`, `Project`) |
| `CreatedOn` | Edm.DateTimeOffset | Date the container was created |
| `LastModified` | Edm.DateTimeOffset | Date the container was last modified |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Folders` | Folders | Folders within the container |
| `SubFolders` | SubFolders | Sub-folders within the container |
| `Cabinets` | Cabinets | Cabinets within the container |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve containers or a specific container |

**Example - Get all containers:**
```http
GET /DataAdmin/Containers
```

**Example - Get a specific container:**
```http
GET /DataAdmin/Containers('OR:wt.inf.container.WTContainer:12345')
```

---

### Folders

Represents Windchill folders.

**Entity Set URL:**
```
GET /DataAdmin/Folders
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Folder name |
| `Description` | Edm.String | Folder description |
| `FolderPath` | Edm.String | Full path of the folder |
| `ContainerID` | Edm.String | ID of the parent container |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `SubFolders` | SubFolders | Child folders |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve folders |
| POST | Create a new folder |
| PATCH | Update a folder |
| DELETE | Delete a folder |

**Example - Create a folder:**
```http
POST /DataAdmin/Folders
Content-Type: application/json

{
  "Name": "NewFolder",
  "Description": "A new folder",
  "ContainerID": "OR:wt.inf.container.WTContainer:12345",
  "FolderPath": "/Default/NewFolder"
}
```

---

### SubFolders

Represents sub-folders within a parent folder.

**Entity Set URL (via navigation):**
```
GET /DataAdmin/Folders('OR:wt.folder.SubFolder:12345')/SubFolders
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Sub-folder name |
| `Description` | Edm.String | Sub-folder description |
| `FolderPath` | Edm.String | Full path |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve sub-folders |
| POST | Create a new sub-folder |
| PATCH | Update a sub-folder |
| DELETE | Delete a sub-folder |

---

### Cabinets

Represents Windchill cabinets (root-level folder objects within containers).

**Entity Set URL:**
```
GET /DataAdmin/Cabinets
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Cabinet name |
| `ContainerID` | Edm.String | ID of the parent container |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Folders` | Folders | Folders within the cabinet |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve cabinets |

---

### LifeCycleTemplates

Represents lifecycle templates defined in the system.

**Entity Set URL:**
```
GET /DataAdmin/LifeCycleTemplates
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Lifecycle template name |
| `ContainerName` | Edm.String | Container where the template is defined |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve lifecycle templates |

---

### Teams

Represents Windchill teams associated with containers.

**Entity Set URL:**
```
GET /DataAdmin/Teams
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Team name |
| `Description` | Edm.String | Team description |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve teams |

---

## Query Examples

**Filter containers by type:**
```http
GET /DataAdmin/Containers?$filter=ContainerType eq 'Product'
```

**Get folders within a specific container:**
```http
GET /DataAdmin/Containers('OR:wt.inf.container.WTContainer:12345')/Folders
```

**Get sub-folders of a folder:**
```http
GET /DataAdmin/Folders('OR:wt.folder.SubFolder:67890')/SubFolders
```

**Select specific properties:**
```http
GET /DataAdmin/Containers?$select=Name,ContainerType
```
