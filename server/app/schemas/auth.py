''' Schemas for authentication routes '''

AUTH_ROUTE_SCHEMA = {

    # Login
    'POST': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
        },
        'required': ['username', 'password']
    },

    # Logout
    'DELETE': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            '_id': {'type': 'string', "minLength": 24, "maxLength": 24}
        },
        'required': ['_id']
    }
}