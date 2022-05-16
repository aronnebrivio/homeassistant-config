# EXEMPLE 1
#   - service: python_script.state_change
#     data_template:
#       entity_id: person.one, person.two
#       state: 'not_home'

# EXEMPLE 2
#   - service: python_script.state_change
#     data_template:
#       entity_id:
#         - person.one
#         - person.two
#       state: 'not_home'

# EXEMPLE 3
#   - service: python_script.state_change
#     data_template:
#       entity_id: >
#         {% set entities = state_attr('group.family_persons', 'entity_id') %}
#         {{ states.person | selectattr('entity_id', 'in', entities)
#                          | selectattr('state', 'eq', 'home')
#                          | map(attribute='entity_id')
#                          | join(', ') }}
#       state: 'not_home'

if isinstance(data.get('entity_id'), str):
    EntityList = data.get('entity_id').split(', ')
else:
    EntityList = data.get('entity_id')
for item in EntityList:
    inputEntity = item
    if inputEntity is None:
        logger.warning("===== entity_id is required if you want to set something.")
    else:
        inputStateObject = hass.states.get(inputEntity)
        inputState = inputStateObject.state
        inputAttributesObject = inputStateObject.attributes.copy()

        for item in data:
            newAttribute = data.get(item)
            logger.debug("===== item = {0}; value = {1}".format(item,newAttribute))
            if item == 'entity_id':
                continue            # already handled
            elif item == 'state':
                inputState = newAttribute
                logger.info(inputEntity + ': ' 'state' + '> ' + inputState)
            else:
                inputAttributesObject[item] = newAttribute
        hass.states.set(inputEntity, inputState, inputAttributesObject)
