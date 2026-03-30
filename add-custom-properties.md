# Adding Custom Properties to Entities in PTC Domains


A PTC domain can be extended to have custom properties which have been added to Windchill types by customizers. Customizers add new properties for Windchill types such as, WTParts, WTDocuments, and so on. WTParts and WTDocuments are available as Part and Document entities in the Product Management and Document Management domains respectively. You can add new attributes as properties for these entities. To add OwningBusinessUnit and DesignCost attributes to the Part entity from the Product Management domain, the customizers mirror the ProdMgmt domain folder structure in the custom configuration path. Then, create the PartsExt.json file to add custom configuration. In the JSON file, under extends property, add the PTC domain entity which you want to extend. In the attributes property, add the new attributes. Perform the following steps to add custom properties to entities:

1\. In the custom configuration path, create the following folder structure for the Product Management domain at <Windchill>/codebase/rest/custom/domain/:

◦ ProdMgmt

▪ <version>

▪ entity

2\. Create the PartsExt.json file at <Windchill>/codebase/rest/custom/domain/ProdMgmt/<version>/entity and add the following content in the file:

{

"extends": "Part",

"attributes": \[\
\
{\
\
"name": "OwningBusinessUnit",\
\
"internalName": "OwningBusinessUnit",\
\
"type": "String"\
\
},\
\
{\
\
"name": "DesignCost",\
\
"internalName": "DesignCost",\
\
"type": "Double"\
\
}\
\
\]

}

After the configuration, when you visit the metadata URL for Product Management domain, it shows the new properties OwningBusinessUnit and DesignCost on the Part entity for ProdMgmt domain. Since the Part entity has additional attributes, they can be used in standard OData URLs.
