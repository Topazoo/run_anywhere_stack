
from flask import Flask 
from router import Router
  
class Application:
    ''' Main application driver '''

    def __init__(self, debug=True):
        ''' Initialize the server '''

        # Create Flask application
        self.app = Flask(__name__) 

        self.app.config['TESTING'] = debug

        # Register routes from config/routes.py
        Router.register_routes(self.app) 


    def run(self):
        ''' Run the server '''

        self.app.run()


if __name__ == '__main__': 
    app = Application()
    app.run()