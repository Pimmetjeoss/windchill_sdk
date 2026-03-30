# Principal Management Domain (PrincipalMgmt)

## Overview

The Principal Management domain provides REST API access to users and groups in Windchill.

**Domain Name:** `PrincipalMgmt`

**Base URL Pattern:**
```
https://<windchill-host>/Windchill/servlet/odata/PrincipalMgmt
```

**Metadata URL:**
```
GET /PrincipalMgmt/$metadata
```

## Entity Sets

### Users

Represents Windchill users (WTPrincipal / WTUser).

**Entity Set URL:**
```
GET /PrincipalMgmt/Users
```

**Key Property:** `ID` (Edm.String) - Object reference identifier (e.g., `OR:wt.org.WTUser:12345`)

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | User login name |
| `FullName` | Edm.String | Full display name |
| `EMail` | Edm.String | Email address |
| `Description` | Edm.String | User description |
| `Disabled` | Edm.Boolean | Whether the user account is disabled |
| `DN` | Edm.String | Distinguished name (LDAP DN) |
| `CreatedOn` | Edm.DateTimeOffset | Date the user was created |
| `LastModified` | Edm.DateTimeOffset | Date the user was last modified |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Groups` | Groups | Groups the user belongs to |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve users or a specific user |

**Example - Get all users:**
```http
GET /PrincipalMgmt/Users
```

**Example - Get a specific user by ID:**
```http
GET /PrincipalMgmt/Users('OR:wt.org.WTUser:12345')
```

---

### Groups

Represents Windchill groups (WTGroup).

**Entity Set URL:**
```
GET /PrincipalMgmt/Groups
```

**Key Property:** `ID` (Edm.String) - Object reference identifier

**Structural Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ID` | Edm.String | Object reference identifier |
| `Name` | Edm.String | Group name |
| `Description` | Edm.String | Group description |
| `DN` | Edm.String | Distinguished name (LDAP DN) |
| `CreatedOn` | Edm.DateTimeOffset | Date the group was created |
| `LastModified` | Edm.DateTimeOffset | Date the group was last modified |

**Navigation Properties:**

| Navigation | Target Entity | Description |
|------------|---------------|-------------|
| `Members` | Users | Members of the group |

**Supported Operations:**

| HTTP Method | Description |
|-------------|-------------|
| GET | Retrieve groups or a specific group |

**Example - Get all groups:**
```http
GET /PrincipalMgmt/Groups
```

**Example - Get members of a group:**
```http
GET /PrincipalMgmt/Groups('OR:wt.org.WTGroup:12345')/Members
```

---

## Query Examples

**Filter users by name:**
```http
GET /PrincipalMgmt/Users?$filter=contains(Name,'admin')
```

**Filter users by email:**
```http
GET /PrincipalMgmt/Users?$filter=contains(EMail,'@ptc.com')
```

**Get user with expanded group memberships:**
```http
GET /PrincipalMgmt/Users('OR:wt.org.WTUser:12345')?$expand=Groups
```

**Select specific user properties:**
```http
GET /PrincipalMgmt/Users?$select=Name,FullName,EMail
```

**Search groups by name:**
```http
GET /PrincipalMgmt/Groups?$filter=contains(Name,'Engineering')
```

**Top N users with paging:**
```http
GET /PrincipalMgmt/Users?$top=10&$skip=20
```
