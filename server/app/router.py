# Framework
from dead_simple_framework import Route, RouteHandler
from dead_simple_framework.handlers import UserRouteHandler, LoginRouteHandler, \
    DefaultPermissionsRouteHandler, Permissions, PermissionsRouteHandler

# Schemas
from schemas import USER_ROUTE_SCHEMA, AUTH_ROUTE_SCHEMA, CONFIG_ROUTE_SCHEMA, PASSWORD_RESET_ROUTE_SCHEMA

# Login Route Logic
from routes import login

# User Route Logic
from routes import users

# Password Reset Route Logic
from routes import password_reset

ROUTES = \
{
    # Healthcheck for AWS
    'healthcheck': Route(url='/', handler=RouteHandler(GET=lambda request, payload: "It's alive!")),

    # Authentication (Login/Logout)
    'authentication': Route(
        url='/api/authenticate', 
        handler=LoginRouteHandler(
            POST=login.POST
        ),
        collection='users',
        schema=AUTH_ROUTE_SCHEMA
    ),

    # User Management (Create, Update, Delete)
    'users': Route(
        url='/api/users',
        handler=DefaultPermissionsRouteHandler(
            POST=users.POST,
            PUT=UserRouteHandler.PUT,
            DELETE=UserRouteHandler.DELETE,
            verifier=UserRouteHandler.verifier,
            permissions=Permissions(PUT='USER', PATCH='USER', GET='USER', DELETE='USER')
        ), 
        collection='users',
        schema=USER_ROUTE_SCHEMA
    ),

    # Password Reset (Send Email, Check Token, Update Password)
    # Requires Gmail configuration in environment
    # 'password_reset': Route(
    #     url='/api/password_reset',
    #     handler=RouteHandler(
    #         verifier=password_reset.verifier,
    #         GET=password_reset.GET,
    #         POST=password_reset.POST,
    #         PUT=password_reset.PUT
    #     ),
    #     collection='reset_tokens',
    #     schema=PASSWORD_RESET_ROUTE_SCHEMA
    # ),

    # API-Modifiable Config
    'config': Route(
        url='/api/config',
        handler=DefaultPermissionsRouteHandler(permissions=Permissions(POST=['ADMIN'], PUT=['ADMIN'], DELETE=['ADMIN'], GET=['ADMIN'])),
        collection='config',
        schema=CONFIG_ROUTE_SCHEMA
    ),
}
