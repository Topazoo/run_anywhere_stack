from routes.index import serve_index

ROUTES = {
    'index': {
        'path': '/',
        'methods': ['GET'],
        'template': None,
        'defaults': None,
        'logic': serve_index
    }
}