''' Schemas for password reset route '''

PASSWORD_RESET_ROUTE_SCHEMA = {

    # Sent a password reset email containing a reset token
    'POST': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            # The username of the user to send the email for
            'username': {'type': 'string', "minLength": 1},
        },
        'required': ['username']
    },

    # Check if a reset token is valid
    'GET': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            # The username of the user to check for a valid reset token 
            'username': {'type': 'string', "minLength": 1},
            # The reset token sent in an email to the user to validate
            'reset_token': {'type': 'string', "minLength": 36, "maxLength": 36},
        },
        'required': ['username', 'reset_token']
    }, 

    # Set a user's password with a valid reset token
    'PUT': {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            # The username of the user to check for a valid reset token 
            'username': {'type': 'string', "minLength": 1},
            # The reset token sent in an email to the user
            'reset_token': {'type': 'string', "minLength": 36, "maxLength": 36},
            # The user's new password
            'password': {'type': 'string', "minLength": 5}, 
        },
        'required': ['username', 'reset_token', 'password']
    }, 
}
