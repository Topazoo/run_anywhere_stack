''' Schemas for user management routes '''

USER_ROUTE_SCHEMA = {

    # Get user details
    'GET': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            # ID of the user to fetch
            '_id': {'type': 'string', "minLength": 24, "maxLength": 24},
            # ID to fetch users after
            'after_id': {'type': 'string', "minLength": 24, "maxLength": 24},
            # ID to fetch users after
            'before_id': {'type': 'string', "minLength": 24, "maxLength": 24},
            # Number of results to fetch
            'limit': { "type": "string", "pattern": "^\d+$"},
            # Field and order to sort by
            'sort': {"type": "object"}
        },
        'redact': ['data.permissions', 'data.password'],
        'required': ['_id']
    },

    # Create user
    'POST': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'username': {'type': 'string', "minLength": 4},
            'password': {'type': 'string', "minLength": 5},
            'first_name': {'type': 'string', "minLength": 1},
            'last_name': {'type': 'string', "minLength": 1},
            'email_address': {
                'type': 'string',
                'pattern': '^([a-zA-Z0-9_\-\.\+]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
            },
            'permissions': {'type': 'array', "minItems": 1, "items": {"type": "string"}}
        },
        'required': ['username', 'first_name', 'last_name', 'password', 'email_address']
    },

    # Update user
    'PUT': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            '_id': {'type': 'string'},
            'password': {'type': 'string', "minLength": 5},
            'first_name': {'type': 'string', "minLength": 1},
            'last_name': {'type': 'string', "minLength": 1},
            'email_address': {
                'type': 'string',
                'pattern': '^([a-zA-Z0-9_\-\.\+]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
            },
            'permissions': {'type': 'array', "minItems": 1, "items": {"type": "string"}}
        },
    },

    # Delete user
    'DELETE': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            '_id': {'type': 'string', "minLength": 24, "maxLength": 24}
        },
        'required': ['_id']
    }
}
