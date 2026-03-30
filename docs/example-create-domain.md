# Creating a New Domain


This example shows you how to create a new domain.

Consider an example, where a new domain with the name NewDomain should be created. The Windchill types, WTChangeIssue and Changeable2 must be exposed as ProblemReport and ChangeableItem entities respectively. Further, the ReportedAgainst relationship between ProblemReport and ChangeItem entities must also be exposed. The version v1 should also be set up for NewDomain. Information can only be read from Windchill using the domain. The following properties of the two entities of the domain are exposed:

• ProblemReport

◦ Number

◦ Name

◦ Occurrence date

◦ Need date

◦ Priority

◦ Category

◦ State

• ChangeableItem

◦ Number

◦ Name

◦ Revision

◦ State

To configure a domain for all the criteria mentioned in the example, perform the following steps:

1\. Create the folder <Windchill>/codebase/rest/custom/domain/NewDomain.

2\. Create the file <Windchill>/codebase/rest/custom/domain/NewDomain.json with the following content:

{

"name": "NewDomain",

"id": "NewDomain",

"description": "NewDomain Domain",

"nameSpace": "Custom.NewDomain",

"containerName": "Windchill",

"defaultVersion": "1"

}

3\. Create the folder <Windchill>/codebase/rest/custom/domain/NewDomain/v1.

4\. Create the file <Windchill>/codebase/rest/custom/domain/NewDomain/v1/import.json with the following content:

{

"imports": \[\
\
{"name": "PTC", "version": "1"}\
\
\]

}

5\. Create the folder <Windchill>/codebase/rest/custom/domain/NewDomain/v1/entity.

6\. Create the file <Windchill>/codebase/rest/custom/domain/NewDomain/v1/entity/ChangeableItems.json with the following content:

{

"name": "ChangeableItem",

"collectionName": "ChangeableItems",

"type": "wcType",

"wcType": "wt.change2.Changeable2",

"description": "Changeable Item",

"operations": "READ",

"attributes": \[\
\
{"name": "Name", "internalName": "name", "type": "String"},\
\
{"name": "Number", "internalName": "number", "type": "String"}\
\
\],

"inherits": \[\
\
{"name": "lifecycleManaged"},\
\
{"name": "versioned"}\
\
\]

}

7\. Create the file <Windchill>/codebase/rest/custom/domain/NewDomain/v1/entity/ProblemReports.json with the following content:

{

"name": "ProblemReport",

"collectionName": "ProblemReports",

"type": "wcType",

"wcType": "wt.change2.WTChangeIssue",

"description": "Problem Report",

"operations": "READ",

"attributes": \[\
\
{"name": "Name", "internalName": "name", "type": "String"},\
\
{"name": "Number", "internalName": "number", "type": "String"},\
\
{"name": "Priority", "internalName": "theIssuePriority", "type": "String"},\
\
{"name": "Category", "internalName": "theCategory", "type": "String"},\
\
{"name": "OccurrenceDate", "internalName": "occurrenceDate", "type": "DateTimeOffset"},\
\
{"name": "NeedDate", "internalName": "needDate", "type": "DateTimeOffset"}\
\
\],

"navigations": \[\
\
{"name": "ReportedAgainst", "target": "ChangeableItems", "type": "ChangeableItem", "containsTarget": true, "isCollection": true}\
\
\],

"inherits": \[\
\
{"name": "lifecycleManaged"}\
\
\]

}

8\. Create the file <Windchill>/codebase/rest/custom/domain/NewDomain/v1/entity/ProblemReports.js with the following content:

function getRelatedEntityCollection(navProcessorData) {

var HashMap = Java.type('java.util.HashMap');

var ArrayList = Java.type('java.util.ArrayList');

var WTArrayList = Java.type('wt.fc.collections.WTArrayList');

var ChangeHelper2 = Java.type('wt.change2.ChangeHelper2');

var targetName = navProcessorData.getTargetSetName();

var map = new HashMap();

var sourcePRs = new WTArrayList(navProcessorData.getSourceObjects());

if("ReportedAgainst".equals(targetName)) {

for(var i = 0; i < sourcePRs.size(); i++) {

var sourcePR = sourcePRs.getPersistable(i);

var reportedAgainstItems = ChangeHelper2.service.getChangeables(sourcePR, true);

var list = new ArrayList();

while(reportedAgainstItems.hasMoreElements()) {

list.add(reportedAgainstItems.nextElement());

}

map.put(sourcePR, list);

}

}

return map;

}

This creates a new domain called NewDomain with all the entities and relationships described in the example. To test the domain, use the following URLs:

• To see the EDM for NewDomain, use the URL:

https://<Windchill server>/Windchill/servlet/odata/NewDomain/$metadata

• To see the list of ProblemReports, use the URL:

https://<Windchill server>/Windchill/servlet/odata/NewDomain/ProblemReports

• To see the list of ProblemReport with ChangeableItems, use the URL:

https://<Windchill server>/Windchill/servlet/odata/NewDomain/ProblemReports?$expand=ReportedAgainst
