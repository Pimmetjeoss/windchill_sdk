# HTTP Status Codes Returned by Windchill REST Services Responses


Windchill REST Services returns appropriate HTTP status code along with its responses. If an error occurs, Windchill REST Services returns an HTTP status code along with an appropriate error message.

The table shows you the HTTP status codes that are returned along with Windchill REST Services responses.

| HTTP Status Code | HTTP Status Code Definition | Windchill REST Services Description |
| --- | --- | --- |
| 200 | HTTP request is successful | Windchill REST Services returns this code when an end point successfully returns entities or entity collections. |
| 201 | HTTP request successfully created a resource | Windchill REST Services returns this code when a POST request to a resource or an action successfully creates an entity. The response returns the newly created entity. |
| 204 | HTTP request is successful, but the service does not return any response. | Windchill REST Services returns this code when an entity instance is successfully updated or deleted with:<br>• PUT, PATCH, and DELETE requests<br>• POST request to action<br>Windchill REST Services returns 204 HTTP code with no response. |
| 400 | Bad HTTP request | Windchill REST Services returns this code when the client request is malformed or cannot be processed by the server. |
| 403 | HTTP request is formed correctly, but is denied by the service | Windchill REST Services returns this code when the user of the request does not have necessary permissions to process the request. |
| 404 | Requested resource is not found | Windchill REST Services returns this code when the domain versions, navigations, or entity instances being requested are not available. |
| 500 | Internal server error | Windchill REST Services returns this code when the processing of the request fails due to unexpected runtime conditions. |
| 501 | Functionality has not been implemented on the server | Windchill REST Services returns this code when URLs are valid OData URLs, but the functionality has not been implemented. For example, in Windchill REST Services some operations in $filter parameter are not implemented. If the client requests for such operations in the URL, Windchill REST Services returns the 501 HTTP code. |
