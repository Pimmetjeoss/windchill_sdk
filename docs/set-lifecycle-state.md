# Set the Life Cycle State of an Entity


An entity can transition through different life cycle states. If an entity is associated with a life cycle template, then the transition states depend on the unique set of life cycle states defined in the template.

Use the action SetState() to set a valid life cycle state for an entity. The action accepts the life cycle state as input parameter in the display-value pair format. The valid value for the life cycle state is of type PTC.EnumType.

For example, if you want to change the life cycle state of an entity to INWORK, pass the input parameter as:

{ "Display": "In Work" "Value": "INWORK" }

You must specify the value for both the parameters. They cannot be blank or null. You can specify any value for the Display parameter. In the Value parameter, specify the internal name of life cycle state. When the action succeeds, the life cycle state of the entity is changed to the value specified in the parameter Value.

If an invalid life cycle state is specified, then the action returns a bad request error. Use the function GetValidStateTransitions(), to get the list of valid life cycle states that the entity can transition. Refer to the section [Getting Information About Windchill Life Cycle States](https://support.ptc.com/help/windchill_rest_services/r1.6/en/windchill_rest_services/wccg_restapi_lifecycle_state.html#wwID0ELGGM "Getting Information About Windchill Life Cycle States"), for more information.

If the URL used to execute the action is not formed correctly, the action throws the URL malformed exception.
