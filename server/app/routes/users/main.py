''' Main route logic for handling users '''

# Core logic
from dead_simple_framework.handlers import UserRouteHandler

# Typing
from flask import Request
from pymongo.collection import Collection
from datetime import datetime


def POST(request:Request, payload:dict, collection:Collection):
    ''' Logic for handling POST requests for users '''

    payload['createdOn'] = datetime.now()
    return UserRouteHandler.POST(request, payload, collection)
