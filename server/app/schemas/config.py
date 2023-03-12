''' Schemas for application config management routes '''

CONFIG_ROUTE_SCHEMA = {

    # Get one or more configs
    'GET': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            # The ID of the config to get - if not set, get all configs 
            '_id': {'type': 'string', "minLength": 24, "maxLength": 24},
            # Number of results to fetch
            'name': { "type": "string"},
            # Field and order to sort by
            'sort': {"type": "object"}
        },
    },

    # Create a config
    'POST': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            # The name of the config
            'name': {"type": 'string', "minLength": 1},
            # The value of the config
            'value': {}
        },
        'required': ['name', 'value']
    },

    # Update a config
    'PUT': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            # The ID of the config to update
            '_id': {'type': 'string', "minLength": 24, "maxLength": 24},
            # The name of the config
            'name': {"type": 'string', "minLength": 1},
            # The value to update the config with
            'value': {}
        },
        'required': ['value', '_id']
    },

    # Delete a config
    'DELETE': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            '_id': {'type': 'string', "minLength": 24, "maxLength": 24},
        },
        'required': ['_id']
    }
}