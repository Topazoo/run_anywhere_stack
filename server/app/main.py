
from flask import Flask 
from router import Router
import os
  
class Application:
    ''' Main application driver '''

    def __init__(self, debug=True):
        ''' Initialize the server '''

        # Create Flask application
        self.app = Flask(__name__) 

        # Register routes from config/routes.py
        Router.register_routes(self.app) 


    def run(self):
        ''' Run the server '''

        self.app.run(host=os.environ.get('FLASK_RUN_HOST', '0.0.0.0'), debug=(os.environ.get('APP_DEBUG') == 'True'))


if __name__ == '__main__': 
    app = Application()
    app.run()