''' Indices for the application '''

from dead_simple_framework.database import Indices

INDICES = Indices({
    'users': {
        'password': {
            'order': -1,
        },
        'email_address': {
            'order': -1,
            'properties': {
                'unique': True
            }
        },
        'username': {
            'order': -1,
            'properties': {
                'unique': True
            }
        }
    },

    'config': {
        'name': {
            'order': 1,
            'properties': {
                'unique': True
            }
        },
    },

    'reset_tokens': {
        'created_on': {
            'order': 1,
            'properties': {
                'expireAfterSeconds': 600
            }
        },
    }
})