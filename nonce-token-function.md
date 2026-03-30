# Function to Get the Value of Nonce Token


Nonce is server generated token which helps in preventing cross-site request forgery (CSRF) attacks. REST clients must provide the token while creating, updating, or deleting the entities in the system.

In the framework, use the function GetCSRFToken() to get the value of the nonce token. The function is available in the PTC Common domain. To get the nonce value, use the URL:

https://<Windchill server>/Windchill/servlet/odata/PTC/GetCSRFToken()

The token is returned in the JSON response. For example the response is as shown below:

{

"@odata.context": "https://windchill.ptc.com/Windchill/servlet/odata/v1/PTC/$metadata#CSRFToken",

"NonceKey": "CSRF\_NONCE",

"NonceValue": "8q87WtSxvWkSH9FMtsQUboOI5TtCS7gWh8RUb4OG ="

}
