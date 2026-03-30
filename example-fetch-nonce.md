# Fetching a NONCE Token from a Service

> **Source**: Windchill REST Services 1.6 Documentation
> **Page**: `WCCG_RESTAccessExamplesFetchNONCE.html`

## Overview

A NONCE token (also called a CSRF token) is a server-generated token that prevents cross-site request forgery (CSRF) attacks. REST clients **must** provide this token when creating, updating, or deleting entities in the system.

The NONCE token must be fetched before any write operation (POST, PATCH, DELETE) and included as a header in those requests.

## Endpoint

```
GET https://<windchill_server>/Windchill/servlet/odata/PTC/GetCSRFToken()
```

- **Domain**: PTC (Common Domain)
- **Function**: `GetCSRFToken()`
- **HTTP Method**: GET
- **Authentication**: Basic Auth or pre-established session

## Request

### Headers

| Header | Value |
|--------|-------|
| `Accept` | `application/json` |

### Example Request

```http
GET /Windchill/servlet/odata/PTC/GetCSRFToken() HTTP/1.1
Host: windchill.ptc.com
Accept: application/json
Authorization: Basic <credentials>
```

## Response

### HTTP Status

- **200 OK** on success

### Example Response

```json
{
  "@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/v1/PTC/$metadata#CSRFToken",
  "NonceKey": "CSRF_NONCE",
  "NonceValue": "8q87WtSxvWkSH9FMtsQUboOI5TtCS7gWh8RUb4OG ="
}
```

### Response Properties

| Property | Type | Description |
|----------|------|-------------|
| `@odata.context` | String | Metadata context URL for the CSRFToken type |
| `NonceKey` | String | The header name to use when sending the NONCE. Always `CSRF_NONCE` |
| `NonceValue` | String | The actual token value to send in subsequent write requests |

## Usage in Subsequent Requests

After fetching the NONCE, include it as a header in all POST, PATCH, and DELETE requests:

```http
POST /Windchill/servlet/odata/ProdMgmt/Parts HTTP/1.1
Host: windchill.ptc.com
Content-Type: application/json
Accept: application/json
CSRF_NONCE: 8q87WtSxvWkSH9FMtsQUboOI5TtCS7gWh8RUb4OG =
```

## Notes

- The NONCE token is tied to the user session. If the session expires, a new token must be fetched.
- The NONCE token is required for all write operations (POST, PATCH, DELETE) across all domains.
- The `NonceKey` value (`CSRF_NONCE`) is used as the HTTP header name in subsequent requests.
- GET requests do not require a NONCE token.
- The NONCE is typically fetched once per session and reused for multiple write operations within that session.
