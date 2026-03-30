# Domain JSON File


The <Domain JSON File> is a JSON file with the same name as the domain identifier, and has .json specified as extension in its file name. For example, for domain identifier ProdMgmt, the <Domain JSON File> file name is ProdMgmt.json. The file contains configuration metadata for the domain. The configuration metadata is specified in a JSON object with the following properties:

• name—Name of the domain. For example, Product Management.

• id—An unique identifier of the domain in camel case. For example, ProdMgmt for Product Management domain.

• description—Description of the domain.

• namespace—An OData identifier that appears in the domain EDM as a namespace qualifier for a domain. For example, PTC.ProdMgmt.

• containerName—An OData identifier that appears in the domain EDM as a container for the entity sets of the domain.

• conglomerate—Specifies if the domain is a conglomerate domain. When the property is set to true, the domain is treated as a conglomerate domain.

• defaultVersion—Default version of the domain API that is returned to the clients if they do not request a specific version of the domain API. The values for this property are specified as 1, 2, 3 and so on in the JSON file. The framework interprets the value of 1 as v1. It searches for the <Domain Folder>/v1 folder for entity configurations that must be used for processing requests. Similarly, a value of 2 is interpreted as v2, and so on.

For example, the ProdMgmt.json file from the Product Management domain is as shown below:

{

"name":"Product Management Domain",

"id":"ProdMgmt",

"description":"PTC Product Management Domain",

"namespace":"PTC.ProdMgmt",

"containerName":"Windchill",

"defaultVersion":"1"

}
