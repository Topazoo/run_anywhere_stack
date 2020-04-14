from api.main import API

from flask import Blueprint, render_template
import json

# debug
from pprint import pprint

class Router:
    ''' Module allowing route specification as a list of dictionaries in config/routes.py'''

    @staticmethod
    def register_routes(app, routes:dict):   
        ''' Register all routes in config/routes.py '''

        API.ROUTES = routes
        for route in routes:
            blueprint = Router.dict_to_blueprint(routes[route]['name'], routes[route])
            Router.configure_blueprint(route, routes[route]['name'], routes[route], blueprint)
            app.register_blueprint(blueprint)


    @staticmethod
    def dict_to_blueprint(route_name: str, route_dict: dict) -> Blueprint:
        ''' Converts routes specified in dictionary form to Flask Blueprints '''
        
        return Blueprint(route_name, __name__, template_folder=route_dict.get('template'))
        

    @staticmethod
    def configure_blueprint(route_path:str, route_name: str, route_dict: dict, blueprint: Blueprint):
        ''' Adds configurations to the route Blueprint based on the dictionary specification '''

        view_func = API.main if route_dict.get('collection') else route_dict['logic']
        blueprint.add_url_rule(route_path, route_name, view_func=view_func, methods=route_dict['methods'], **({'defaults': route_dict['defaults']} if route_dict.get('defaults') else {}))
