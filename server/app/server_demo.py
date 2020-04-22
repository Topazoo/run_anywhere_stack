#!/usr/bin/env python3.7
from dead_simple_framework import Application

sample_config = {
    'routes': {
        '/demo': {
            'name': 'demo',
            'methods': ['GET', 'POST', 'DELETE', 'PUT'],
            'template': None,
            'defaults': None,
            'logic': None,
            'collection': 'demo'
        },
        '/': {
            'name': 'index',
            'methods': ['GET'],
            'template': None,
            'defaults': None,
            'logic': lambda: str('Index'),
        },
        '/celery': {
            'name': 'celery',
            'methods': ['GET'],
            'template': None,
            'defaults': None,
            'logic': lambda: str(Application.run_task('add', [5, 8], kwargs={}).get()),
        }
    },
    'tasks': {
        'add': {
            'logic': lambda x,y: x + y,
            'schedule': None,
            'timeframe': None
        }
    }
}

app = Application(sample_config)
if __name__ == '__main__':
    app.run()
