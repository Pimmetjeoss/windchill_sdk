# Saved Search Domain (SavedSearch)

## Overview

The Saved Search domain provides REST API access to saved search definitions in Windchill and the ability to execute them. Saved searches are pre-configured queries that users have stored in the Windchill interface.

**Domain Name:** `SavedSearch`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/SavedSearch
```

**Metadata URL:**
```
GET /SavedSearch/$metadata
```

## Entity Sets

### SavedSearches

Represents saved search definitions.

**Entity Set URL:**
```
GET /SavedSearch/SavedSearches
```

**Key Property:** `ID` (Edm.String)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Saved search name |
| `Description` | Edm.String | Description of the saved search |
| `SearchType` | Edm.String | Type of object being searched |
| `IsShared` | Edm.Boolean | Whether the search is shared with other users |
| `Owner` | Edm.String | Owner of the saved search |
| `ContainerName` | Edm.String | Container context |
| `CreatedOn` | Edm.DateTimeOffset | Creation date |
| `LastModified` | Edm.DateTimeOffset | Last modification date |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve saved searches |

---

## Functions

### ExecuteSavedSearch

Executes a saved search and returns results.

**URL:**
```
GET /SavedSearch/ExecuteSavedSearch(SavedSearchID='OR:wt.query.savedSearch.SavedSearch:12345')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `SavedSearchID` | Edm.String | Yes | Object reference ID of the saved search |

**Returns:** Collection of search result entities

**Example Request:**
```http
GET /Windchill/servlet/odata/SavedSearch/ExecuteSavedSearch(SavedSearchID='OR:wt.query.savedSearch.SavedSearch:12345')
Accept: application/json
```

**Example Response:**
```json
{
  "@odata.context": "$metadata#Collection(PTC.SearchResult)",
  "value": [
    {
      "ID": "OR:wt.part.WTPart:67890",
      "Name": "Bolt Assembly",
      "Number": "0000012345",
      "Type": "wt.part.WTPart",
      "State": "INWORK",
      "Version": "A",
      "Iteration": "1"
    }
  ]
}
```

---

### GetSavedSearches

Retrieves all saved searches accessible to the current user.

**URL:**
```
GET /SavedSearch/GetSavedSearches()
```

**Parameters:** None

**Returns:** Collection of SavedSearch entities

---

### GetSavedSearchesByType

Retrieves saved searches filtered by the type of object they search for.

**URL:**
```
GET /SavedSearch/GetSavedSearchesByType(SearchType='wt.part.WTPart')
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `SearchType` | Edm.String | Yes | The Windchill type to filter by |

**Returns:** Collection of SavedSearch entities

---

## Query Examples

**Get all saved searches:**
```http
GET /SavedSearch/SavedSearches
```

**Filter saved searches by name:**
```http
GET /SavedSearch/SavedSearches?$filter=contains(Name,'Parts')
```

**Get only shared saved searches:**
```http
GET /SavedSearch/SavedSearches?$filter=IsShared eq true
```

**Execute a saved search:**
```http
GET /SavedSearch/ExecuteSavedSearch(SavedSearchID='OR:wt.query.savedSearch.SavedSearch:12345')
```

**Execute with OData query options on results:**
```http
GET /SavedSearch/ExecuteSavedSearch(SavedSearchID='OR:wt.query.savedSearch.SavedSearch:12345')?$top=10&$skip=0
```

## Notes

- Saved search execution respects the access control of the current user - only objects the user has permission to see will be returned.
- The search criteria are defined in the saved search itself; you cannot modify the criteria via the API.
- Use `$top` and `$skip` on the results to implement paging.
