from config.routes import ROUTES

from flask import Blueprint, render_template
import json

# debug
from pprint import pprint

class Router:
    ''' Module allowing route specification as a list of dictionaries in config/routes.py'''

    routes = ROUTES  # Internal Reference

    @staticmethod
    def register_routes(app):   
        ''' Register all routes in config/routes.py '''

        for route in ROUTES:
            blueprint = Router.dict_to_blueprint(route, ROUTES[route])
            Router.configure_blueprint(route, ROUTES[route], blueprint)
            app.register_blueprint(blueprint)


    @staticmethod
    def dict_to_blueprint(route_name: str, route_dict: dict) -> Blueprint:
        ''' Converts routes specified in dictionary form to Flask Blueprints '''
        
        return Blueprint(route_name, __name__, template_folder=route_dict.get('template'))
        

    @staticmethod
    def configure_blueprint(route_name: str, route_dict: dict, blueprint: Blueprint):
        ''' Adds configurations to the route Blueprint based on the dictionary specification '''
        
        blueprint.add_url_rule(route_dict['path'], route_name, view_func=route_dict['logic'], methods=route_dict['methods'], **({'defaults': route_dict['defaults']} if route_dict.get('defaults') else {}))
