
from flask import Flask 
from router import Router
from encoder import JSON_Encoder
import os
  
class Application:
    ''' Main application driver '''

    def __init__(self, config:dict, debug=True):
        ''' Initialize the server '''

        # Create Flask application
        self.app = Flask(__name__) 
        self.app.json_encoder = JSON_Encoder

        # Register routes from config/routes.py
        Router.register_routes(self.app, config) 


    def run(self):
        ''' Run the server '''

        self.app.run(host=os.environ.get('FLASK_RUN_HOST', '0.0.0.0'), debug=(os.environ.get('APP_DEBUG') == 'True'))