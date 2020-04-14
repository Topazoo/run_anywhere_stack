#!/usr/bin/env python3.7

from main import Application

ROUTES = {
    '/demo': {
        'name': 'demo',
        'methods': ['GET', 'POST', 'DELETE', 'PUT'],
        'template': None,
        'defaults': None,
        'logic': None,
        'collection': 'demo'
    }
}

if __name__ == '__main__': 
    application = Application(ROUTES)
    application.run()