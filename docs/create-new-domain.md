# Creating New Domains


Windchill REST Services enables you to create new domains. The new domains are created in the custom configuration path.

To create a new domain, perform the following steps:

1\. Decide a domain identifier and the domain version. Create the domain folder <Windchill>/codebase/rest/custom/domain/<Domain\_Identifier>/<Domain\_Version>

2\. Create the <Windchill>/codebase/rest/custom/domain/<Domain\_Identifier>.json file and provide values for domain metadata attributes.

3\. Decide which other domains to import and set up the <Windchill>/codebase/rest/custom/domain/<Domain\_Identifier>/<Domain\_Version>/import.json file.

4\. Decide if the domain must have unbound actions or functions and set up the <Windchill>/codebase/rest/custom/domain/<Domain\_Identifier>/<Domain\_Version>/import.json and <Windchill>/codebase/rest/custom/domain/<Domain\_Identifier>/<Domain\_Version>/import.js files.

5\. If complexTypes are required then set up the complex type JSON files at <Windchill>/codebase/rest/custom/domain/<Domain\_Identifier>/<Domain\_Version>/complexType.

6\. Configure entities and entity relations at <Windchill>/codebase/rest/custom/domain/<Domain\_Identifier>/<Domain\_Version>/entity.

After these files are setup, the domain is available at the REST root URL and can be accessed by OData URLs.

These are generic instructions to create a domain. You have to create and configure files depending on the entities of the domain. In this User’s Guide, we have provided an example, that shows how to create a domain. The example helps you understand which files to create while configuring a domain.
