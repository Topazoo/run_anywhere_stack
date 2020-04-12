def hello_world(): # TODO - Refactor to views
    return 'Hello World'

ROUTES = {
    'index': {
        'path': '/',
        'methods': ['GET'],
        'template': None,
        'defaults': None,
        'logic': hello_world
    }
}