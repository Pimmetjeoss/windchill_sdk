# Configuration Paths and Files


The configuration home of Windchill REST Services is <Windchill>/codebase/rest folder. Windchill REST Services searches for the configuration files in a set of subfolders which is called the configuration path set. These subfolders are available in the configuration home.

A configuration path set is specific to a domain provider who provides domain configurations for Windchill. PTC is the primary domain provider. However, PTC partners and PTC Customer Success organization, can act as domain providers, if they create and publish domain configurations independent of the release of Windchill REST Services.

The configuration path set for a provider has two types of folders:

• Configuration path folder

• Custom configuration path folder

The configuration path folder for a given provider contains configurations files provided by the domain provider. The custom configuration path folder contains configuration files created by customers which extends the entity definitions available in the configuration path folder. The configuration files available in the configuration path folder of a domain provider must not be modified. You can create new configuration files under the custom configuration path folder of the domain provider.

![](https://support.ptc.com/help/windchill_rest_services/r1.6/en/windchill_rest_services/images/wrs_helpcenter.1.022.1.jpg)

Windchill REST Services reads all the configuration path sets in the configuration home to provide a unified view of the domains available in a Windchill installation. For each configuration path set, Windchill REST Services consolidates the configuration files from both configuration path and custom configuration path folders to create a unified list of domains and their EDM available for a provider.

For domains provided by PTC, the configuration path and the custom configuration path folders are:

• PTC Configuration Path—<Windchill>/codebase/rest/ptc/domain/, where <Windchill> is the Windchill installation directory.

◦ This path is reserved for domain configurations that are provided by PTC. The domains and entities are installed at this path.

◦ Do not modify the files at this path.

◦ You must not create any new configuration files at this location as future updates from PTC will delete and recreate files in this path.

• PTC Custom Configuration Path—<Windchill>/codebase/rest/custom/domain/, where <Windchill> is the Windchill installation directory.

◦ This path is provided for custom configuration files.

◦ By creating custom configuration files at this location, customizers can extend PTC-provided domains, or create new custom domains.

|     |     |
| --- | --- |
| ![*](https://support.ptc.com/help/windchill_rest_services/r1.6/en/windchill_rest_services/note_16x16.png) | The configuration details and examples in this guide have been explained with PTC as the domain provider. The details explained for PTC domain provider can be applied to domain configurations created by PTC partners and customers in their own configuration path sets. |
