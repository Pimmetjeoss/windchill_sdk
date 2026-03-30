# Overview


Windchill REST Services has a framework that provides capabilities to create OData services based on the OData V4 protocol.

The framework enables domain authors to create a set of configuration files that define the OData entities available in a service. You can map the OData entities to Windchill types.

The framework provides default processing logic for GET, POST, PUT, PATCH, and DELETE requests. The domain authors can override or enhance the processing logic with code hooks.

The framework supports inheritance. Domain entities can derive properties, actions, or functions from the framework without defining them explicitly. For example, consider a Windchill capability Workable. Domain entities that inherit the framework capability Workable also inherit the properties of the capability. The properties to display version, iteration, actions to check out, check in, undo check out, and revise the entity are inherited.
