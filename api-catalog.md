# API Catalog for Windchill REST Services Endpoints


The Windchill REST Services release includes an API catalog, which is a developer document. The catalog is a web page that is accessible from the Windchill user interface. It lists all the endpoints along with the supported operations. The catalog is the Swagger specification of the endpoints that are available in Windchill REST Services. You can interactively execute the HTTP operations on the endpoint URLs.

You can access the catalog from a running instance of Windchill. To access the catalog in Windchill perform the following steps:

1\. To display the Customization icon on the Browse tab, in the Preference Management utility, set Client Customization to Yes.

2\. In the Browse tab, click the Customization icon. The Customization page opens.

3\. Click Documentation.

4\. Under the API menu, click OData REST APIs. The Windchill REST Services catalog opens.

The catalog lists all the domains that are supported by your current installation of Windchill. The list of domains that appear in the catalog are generated based on a set of catalog configuration files. The configuration files are available in the PTC and custom configuration paths. There is one catalog configuration file for every domain. The name of the catalog configuration file is specified in the following format:

config.<domain\_name>.json

where, <domain\_name> is the name of the domain. For example, ProdMgmt, DocMgmt, PrincipalMgmt, and so on.

The JSON object in the configuration file contains key-value pairs that correspond to the following configurable options:

• includeInDocumentation—Includes the domain in the catalog. Specify as true to include the domain. It takes a Boolean value as input.

If the configuration file is not defined for a domain, it does not appear in the catalog.

• blackListedEndpoints—Excludes endpoints from the catalog. It is a JSON array. Its value is set as an array of objects that contain path and ops keys.

◦ path key is a regular expression of the endpoints that should be excluded.

◦ ops key is an array of strings, which specifies the operations that should be excluded for the endpoints specified in path.

|     |     |
| --- | --- |
| ![*](https://support.ptc.com/help/windchill_rest_services/r1.6/en/windchill_rest_services/note_16x16.png) | The strings in the ops array are case-sensitive. For example, specify the operations as \[“GET”, “POST”, “PATCH”\]. Do not specify the operations as \[“get”, “Post”, “patch”\]. |

• navigationLevel—Specifies the levels of navigation the catalog generator should follow to find endpoints for a given domain. It is an integer and is configurable up to 3 levels.

• htmlInfoFileName—Specifies the name of the static HTML file that is set as the summary page for the domain. The file opens when you click the name of the domain in the sidebar of the catalog and have not selected a version. The value that is set for this option corresponds to an HTML file that is available at:

<Windchill>/codebase/netmarkets/html/wrs/catalog

where, <Windchill> is the Windchill installation directory.

If this option is not specified or the HTML file specified in the option does not exist, the content area remains blank until a version is selected from the sidebar.

For example, a catalog configuration file for PTC Product Management domain can be defined as:

{

"includeInDocumentation" : true,

"blackListedEndpoints" :\[\
\
{\
\
"path":"\\\/.\*/SmallThumbnails.\*",\
\
"ops":\["GET", "DELETE", "PATCH", "POST"\]\
\
},{\
\
"path":"\\\/.\*/Thumbnails.\*",\
\
"ops":\["GET", "DELETE", "PATCH", "POST"\]\
\
}\
\
\],

"navigationLevel" : 1,

"htmlInfoFileName" : "prodmgmtdomain.html"

}

The domains listed in catalog are extensible. You can include any custom domains configured in your installation in this list. To include a custom domain in the catalog, create a domain configuration file and add it at the following location:

<Windchill>/codebase/rest/custom/doc

The domain configuration files defined by PTC for the catalog are available at the following location:

<Windchill>/codebase/rest/ptc/doc

In addition to the endpoints that are automatically generated, you can extend the catalog with manually authored Swagger specification. This enables you to add additional endpoints to your custom domains. You can also override the existing endpoints in the PTC provided domains.

Every version of each domain can have its own file for additional endpoints. You should define these endpoints in a separate JSON file. The naming convention for these JSON files is:

doc.<Version>.<domain\_name>.json

For example, if you added or updated endpoints in the PTC Product Management domain for v1 version, the name of the file should be doc.v1.ProdMgmt.json.

|     |     |
| --- | --- |
| ![*](https://support.ptc.com/help/windchill_rest_services/r1.6/en/windchill_rest_services/note_16x16.png) | Save the Swagger specification file in JSON format. |

All user-specified Swagger specification files that extend PTC or custom domains, should be at:

<Windchill>/codebase/rest/custom/doc

See the Swagger documentation for more information about Swagger Specification and Swagger Editor.

In the catalog, the PTC provided endpoints that are automatically generated or manually authored by PTC in the Swagger specification files, are listed under Service Endpoints. The endpoints that are created by users at <Windchill>/codebase/rest/custom/doc are listed under Custom Endpoints in the catalog.

|     |     |
| --- | --- |
| ![*](https://support.ptc.com/help/windchill_rest_services/r1.6/en/windchill_rest_services/note_16x16.png) | All possible combinations of OData URLs are not available. Only a subset of URLs is available in the catalog. |
