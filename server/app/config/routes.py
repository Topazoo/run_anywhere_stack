from routes.index import serve_index

ROUTES = {
    '/': {
        'name': 'index',
        'methods': ['GET', 'POST'],
        'template': None,
        'defaults': None,
        'logic': serve_index,
        'collection': 'test'
    },
    '/demo': {
        'name': 'demo',
        'methods': ['GET', 'POST', 'DELETE', 'PUT'],
        'template': None,
        'defaults': None,
        'logic': None,
        'collection': 'demo'
    }
}