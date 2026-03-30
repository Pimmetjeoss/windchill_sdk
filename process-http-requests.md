# Windchill REST Services - How the Framework Processes HTTP Requests

## Overview

The Windchill REST Services framework processes incoming OData HTTP requests through a pipeline that translates OData operations into Windchill API calls and transforms the results back into OData responses. The framework also supports JavaScript hooks (via Nashorn engine in Java 8) that can customize request processing at various stages.

## Request Processing Pipeline

### GET Request Processing

1. **Type Check** -- The framework validates the requested entity type exists in the domain's Entity Data Model (EDM). Returns `404 Not Found` if the entity type or entity set is not recognized.

2. **Query Windchill** -- The framework translates OData query options (`$filter`, `$orderby`, `$top`, `$skip`, `$select`, `$expand`, `$count`) into Windchill QuerySpec API calls and executes them against the Windchill database.

3. **Convert to OData** -- Query results (Windchill persistable objects) are converted into OData entity representations using the domain's property mappings. Navigation properties are resolved if `$expand` was specified.

4. **Response** -- The OData JSON payload is serialized and returned with appropriate HTTP status code (`200 OK` for collections, `200 OK` for single entities, `404 Not Found` if entity not found).

```
Client                  Framework                    Windchill
  |                         |                            |
  |-- GET /Parts?$filter -->|                            |
  |                         |-- Validate entity type ---->|
  |                         |-- Build QuerySpec --------->|
  |                         |-- Execute query ----------->|
  |                         |<-- Persistable objects -----|
  |                         |-- Convert to OData -------->|
  |<-- 200 OK + JSON ------|                            |
```

### POST Request Processing (Create)

1. **Type Check** -- Validates the target entity set and the `@odata.type` if present.

2. **Deserialize** -- Parses the JSON request body into property values and binding references.

3. **Pre-create Hook** -- If a JavaScript hook is registered for `beforeCreate`, it executes. The hook can modify property values or cancel the operation.

4. **Create in Windchill** -- The framework calls the appropriate Windchill API to create the object (e.g., `PersistenceHelper.manager.store()`).

5. **Post-create Hook** -- If a JavaScript hook is registered for `afterCreate`, it executes. The hook receives the created object.

6. **Convert to OData** -- The created Windchill object is converted to an OData entity.

7. **Response** -- Returns `201 Created` with the created entity in the response body and a `Location` header pointing to the new entity.

### PATCH Request Processing (Update)

1. **Type Check** -- Validates the entity type and entity key.

2. **Resolve Entity** -- Retrieves the existing Windchill object by its OData key (Object Reference ID).

3. **Deserialize** -- Parses the JSON request body for updated property values.

4. **Pre-update Hook** -- If registered, the `beforeUpdate` hook executes.

5. **Update in Windchill** -- Applies property changes and persists via Windchill API.

6. **Post-update Hook** -- If registered, the `afterUpdate` hook executes.

7. **Convert to OData** -- Returns the updated entity.

8. **Response** -- Returns `200 OK` with the updated entity.

### PUT Request Processing (Replace)

Same as PATCH but replaces all properties (properties not in the request body are reset to defaults). In practice, PATCH is preferred over PUT.

### DELETE Request Processing

1. **Type Check** -- Validates the entity type and key.

2. **Resolve Entity** -- Retrieves the existing Windchill object.

3. **Pre-delete Hook** -- If registered, the `beforeDelete` hook executes.

4. **Delete in Windchill** -- Calls Windchill API to delete the object.

5. **Post-delete Hook** -- If registered, the `afterDelete` hook executes.

6. **Response** -- Returns `204 No Content`.

## JavaScript Hooks (Nashorn Engine)

The framework supports server-side JavaScript hooks executed via the **Nashorn JavaScript engine** (bundled with Java 8). Hooks allow customization of request processing without modifying Java code.

### Hook Types

| Hook | Trigger | Use Case |
|---|---|---|
| `beforeRead` | Before a GET query executes | Modify query parameters, add filters |
| `afterRead` | After query results are retrieved | Transform results, add computed properties |
| `beforeCreate` | Before a POST creates an object | Validate input, set default values |
| `afterCreate` | After an object is created | Trigger workflows, send notifications |
| `beforeUpdate` | Before a PATCH/PUT updates an object | Validate changes, enforce business rules |
| `afterUpdate` | After an object is updated | Audit logging, cascade updates |
| `beforeDelete` | Before a DELETE removes an object | Authorization checks, prevent deletion |
| `afterDelete` | After an object is deleted | Cleanup, cascade deletes |

### Hook Registration

Hooks are defined in JavaScript files placed in the domain's configuration directory:

```
{windchill-base}/codebase/rest/domains/{DomainName}/hooks/
```

Example hook file (`beforeCreate.js`):

```javascript
// beforeCreate.js - Validate part number format before creation
function beforeCreate(context) {
    var entity = context.getEntity();
    var number = entity.getProperty("Number");

    if (number && !number.match(/^[A-Z]{3}-\d{6}$/)) {
        throw new Error("Part number must match format XXX-000000");
    }

    // Set default values
    if (!entity.getProperty("Source")) {
        entity.setProperty("Source", "MAKE");
    }
}
```

### Calling Windchill Java APIs from Hooks

Since Nashorn runs on the JVM, hooks can directly call Windchill Java APIs:

```javascript
// afterCreate.js - Call Windchill Java API after part creation
function afterCreate(context) {
    var entity = context.getEntity();
    var windchillObject = context.getWindchillObject();

    // Import Java classes
    var WTPartHelper = Java.type('wt.part.WTPartHelper');
    var SessionHelper = Java.type('wt.session.SessionHelper');

    // Access Windchill services
    var currentUser = SessionHelper.manager.getPrincipal();

    // Example: Log the creation
    var logger = Java.type('wt.log4j.LogR').getLogger('com.custom.rest');
    logger.info('Part ' + entity.getProperty('Number') + ' created by ' + currentUser.getName());
}
```

### Hook Context Object

The `context` parameter passed to hooks provides:

| Method | Description |
|---|---|
| `context.getEntity()` | The OData entity being processed |
| `context.getWindchillObject()` | The underlying Windchill persistable object |
| `context.getRequest()` | The HTTP request object |
| `context.getQueryOptions()` | OData query options ($filter, $select, etc.) |
| `context.setProperty(name, value)` | Set a property value on the entity |
| `context.getProperty(name)` | Get a property value from the entity |

### Hook Configuration in Domain JSON

```json
{
  "entityTypes": [
    {
      "name": "Part",
      "hooks": {
        "beforeCreate": "hooks/part-beforeCreate.js",
        "afterCreate": "hooks/part-afterCreate.js",
        "beforeUpdate": "hooks/part-beforeUpdate.js",
        "beforeDelete": "hooks/part-beforeDelete.js"
      }
    }
  ]
}
```

## Notes

- JavaScript hooks run in the same JVM as Windchill, so they have full access to Windchill Java APIs.
- Nashorn engine is available in Java 8. For Java 11+, GraalVM JavaScript engine may be used instead.
- Hooks execute synchronously within the request pipeline. Long-running hook logic increases response time.
- Exceptions thrown in `before*` hooks cancel the operation and return an error response.
- Exceptions thrown in `after*` hooks do not roll back the operation but are reported in the response.
