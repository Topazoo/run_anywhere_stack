from dead_simple_framework import Application, Task_Manager, Database, API, Route
from dead_simple_framework.handlers import Permissions, RouteHandler, DefaultPermissionsRouteHandler
from random import randint, sample

sample_config = {
    'routes': {
        'insert': Route( # Another route with automatic CRUD support
            url = '/insert',
            handler = DefaultPermissionsRouteHandler(
                permissions=Permissions(GET=['USER'], POST=['USER'], PUT=['USER'], PATCH=['USER'], DELETE=['USER'])
            ),
            collection = 'insert'
        ),
        'call': Route(  # Route that runs an async task (API call)
            url = '/refresh',
            handler = RouteHandler(
                GET=lambda request,payload: str(Task_Manager.run_task('scheduled_call')),
            ),
        ),
        'call_cached': Route(  # Route that fetches the last cached of an async task (API call)
            url = "/",
            handler = RouteHandler(
                GET=lambda request, payload: str(Task_Manager.get_result('scheduled_call')),
            ),
        ),
        'add': Route(  # Route that runs a task to add two numbers together
            url = '/add', # The route must be sent x and y like /add?x=5&y=2
            handler = RouteHandler(
                GET=lambda request, payload: str(Task_Manager.run_task('add', args=(int(payload.get("x", 1)), int(payload.get("y", 5))))),
            )
        ),
    },
    'tasks': { # Async tasks available to the Task_Manager [celery] to schedule or run
        'add': {        # Simple Addition Task (with default arguments) 
            'logic': lambda x=2,y=2: x + y,
            'schedule': None
        },
        'insert': {     # Periodic Database Insert Task 
            'logic': lambda res: Database(collection='insert').connect().insert_one({'test': 'doc', 'result': res}),
            'schedule': {}, # Default - every minute
            'depends_on': 'add' # Return value substituted for `res`
        },
        'call_api': {   # API Call Task
            'logic': lambda url, params=None: API.get_json(url, params, ignore_errors=True, retry_ms=1000, num_retries=5),
        },
        'scheduled_call': { # Call an API every hour (or when this task is run)
            'logic': lambda: Task_Manager.parallelize([['call_api', [f'http://api.zippopotam.us/us/{x}']] for x in sample(["94941", "94942", "94943", "94901", "94902", "94109"], 3)]),
            'schedule': {'hour': 1}
        }
    }
}

app = Application(sample_config)
if __name__ == '__main__':
    app.run()