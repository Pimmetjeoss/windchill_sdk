# Extending Product Management Domain to Add A Soft Type


This example shows you how to extend the Product Management domain to add a soft type of an existing part. Consider a case where you want to create WTPart of soft type Capacitor which has its parent soft type as Electrical Part.

To extend the domain to add the soft type, create a custom configuration file Capacitors.json at:

<Windchill>/codebase/rest/custom/domain/ProdMgmt/<version>/entity

wcType property must have the same Internal Name as defined for the soft type in Type Management.

![](https://support.ptc.com/help/windchill_rest_services/r1.6/en/windchill_rest_services/images/wrs_helpcenter.1.233.1.jpg)

{

"name": "Capacitor",

"collectionName": "Capacitors",

"wcType": "com.ptc.ptcnet.Capacitor",

"description": "This part extends ElectricalParts entity.",

"parent": {

"name": "ElectricalParts"

},

"attributes": \[\
\
{\
\
"name":"Capacitance",\
\
"internalName":"Capacitance",\
\
"type":"String"\
\
}\
\
\]

}

Sample request to create WTPart with soft type ‘Capacitor’:

{

"@odata.type": "PTC.ProdMgmt.Capacitor",

"Name":"TestWTPart\_002",

"Number":"TestWTPart\_002",

"AssemblyMode": {

"Value": "component",

"Display": "Component"

},

"Context@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:48788507')"

}
