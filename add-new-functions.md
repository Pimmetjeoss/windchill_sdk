# Adding New Functions to PTC Domains


A PTC domain can be extended to add both bound and unbound OData functions. OData functionsare available in the EDM of a domain. They are invoked with a GET request to the Odata URL of the function. For example, consider a case where you want to add a bound function to the Product Management domain that identifies costly parts in an entity set Parts. Perform the following steps to add a bound function:

1\. In the custom configuration path, create the following folder structure for the PTC Product Management domain at <Windchill>/codebase/rest/custom/domain/:

◦ ProdMgmt

▪ <version>

▪ entity

2\. Create the PartsExt.json file at <Windchill>/codebase/rest/custom/domain/ProdMgmt/<version>/entity and add the following content in the file:

{

"extends": "Part",

"functions": \[\
\
{\
\
"name": "GetCostlyParts",\
\
"description": "Return expensive parts",\
\
"isComposable": false,\
\
"parameters": \[\
\
{\
\
"name": "PartSet",\
\
"type": "Part",\
\
"isCollection": true,\
\
"isNullable": false\
\
}\
\
\],\
\
"returnType": {\
\
"type": "Part",\
\
"isCollection": true\
\
}\
\
}\
\
\]

}

Create the PartsExt.js file at <Windchill>/codebase/rest/custom/domain/ProdMgmt/<version>/entity and implement the function. Ensure that the Part entity has a numeric property DevelopmentCost.

function function\_GetCostlyParts(data, params) {

var EntityCollection = Java.type('org.apache.olingo.commons.api.data.EntityCollection');

var entityCollection = new EntityCollection();

var partEntities = params.get("PartSet").getValue().getEntities();

for (var i = 0; i < partEntities.size(); i++) {

var partEntity = partEntities.get(i);

var partCostProperty = partEntity.getProperty('DevelopmentCost');

if (partCostProperty) {

var partCost = partCostProperty.getValue();

if (partCost && partCost > 0.10) {

entityCollection.getEntities().add(partEntity);

}

}

}

return entityCollection;

}

After the configuration, the GetCostlyParts function is available for the Part entity in the metadata URL of the PTC Product Management domain. You can call the function on the Parts entity set and get a list of the costly parts for the specified set. For example, to get a list of costly parts associated with a specific part in the entity set, use the following URL:

/Parts(<oid>)/UsedBy/PTC.ProdMgmt.GetCostlyParts()

Use unbound functions to work with operations that access or process large entity sets. If you perform operations on bound entity sets, all the entities in the entity set may be passed as input to the function. If an operation accesses a bound entity set, which contains more than 2000 entities, the BoundParameterLimitExceededException is thrown. You can catch the exception by having an alternate implementation in the event if the entity limit is exceeded.

function function\_GetCostlyParts(data, params) {

try {

var partEntities = params.get("PartSet").getValue().getEntities();

// Continue on normally...

}

catch (ex) {

var BoundParameterLimitExceededException = Java.type('com.ptc.odata.core.entity.operation.BoundParameterLimitExceededException');

if (ex instanceof BoundParameterLimitExceededException) {

// Entity limit exceeded...

}

}

}
