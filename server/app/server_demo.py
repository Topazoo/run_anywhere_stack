from dead_simple_framework import Application, Task_Manager, Database, API

sample_config = {
    'routes': {
        '/insert': { # Another route with automatic CRUD support
            'name': 'insert',
            'methods': ['GET', 'POST', 'DELETE', 'PUT'],
            'template': None,
            'defaults': None,
            'logic': None,
            'collection': 'insert'
        },
        '/api/refresh': {  # Route that runs an async task (API call)
            'name': 'call',
            'methods': ['GET'],
            'template': None,
            'defaults': None,
            'logic': lambda: str(Task_Manager.run_task('scheduled_call')),
        },
        '/': {  # Route that fetches the last result of an async task (API call)
            'name': 'call_cached',
            'methods': ['GET'],
            'template': None,
            'defaults': None,
            'logic': lambda: str(Task_Manager.get_result('scheduled_call'))
        },
        '/add': {  # Route that fetches the last result of an async task (API call)
            'name': 'add',
            'methods': ['GET'],
            'template': None,
            'defaults': None,
            'logic': lambda: str(Task_Manager.run_task('add'))
        },
    },
    'tasks': { # Async tasks available to the Task_Manager [celery] to schedule or run
        'add': {        # Simple Addition Task (with default arguments) 
            'logic': lambda x,y: x + y,
            'schedule': None,
            'timeframe': None,
            'args': (2,2)
        },
        'insert': {     # Periodic Database Insert Task 
            'logic': lambda res: Database(collection='insert').connect().insert_one({'test': 'doc', 'result': res}),
            'schedule': {}, # Default - every minute
            'timeframe': None,
            'depends_on': 'add' # Return value substituted for `res`
        },
        'call_api': {   # API Call Task
            'logic': lambda url, params=None: API.get_json(url, params, ignore_errors=True, retry_ms=1000, num_retries=5),
        },
        'scheduled_call': {
            'logic': lambda: Task_Manager.parallelize([['call_api', [f'http://dummy.restapiexample.com/api/v1/employee/{x}']] for x in range(1,33)]),
            'schedule': {'hour': 1}
        }
    }
}

app = Application(sample_config)
if __name__ == '__main__':
    app.run()