# App driver
from dead_simple_framework import Application

# App routes (URLs and Logic)
from router import ROUTES

# Database Indices
from indices import INDICES

# Fixtures
from fixtures import FIXTURES

application = Application({'routes': ROUTES, 'indices': INDICES, 'fixtures': FIXTURES})
gunicorn = application.app # Hook for gunicorn

if __name__ == '__main__': application.run()
