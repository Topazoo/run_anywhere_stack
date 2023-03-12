''' Handler for login route '''

# Password hashing
from passlib.hash import pbkdf2_sha256 as sha256

# JWT
from flask_jwt_extended import set_access_cookies, set_refresh_cookies

# JWT Settings
from dead_simple_framework.config import JWT_Settings

# Utils
from dead_simple_framework.api import JsonError, JsonResponse
from dead_simple_framework.handlers import LoginRouteHandler
from datetime import datetime, timedelta

# Flask HTTP
from flask import Request, Response

# Typing
from pymongo.collection import Collection


def POST(request:Request, payload, collection:Collection) -> Response:
    ''' Attempt to log in for a specified user '''

    user = collection.find_one({'username': payload.get('username')})
    if not user:
        return JsonError(f"User '{payload.get('username')}' not found", 404)

    if not sha256.verify(payload.get('password'), user['password']):
        return JsonError("Incorrect Password", 400)

    permissions = user.get('permissions')
    if isinstance(permissions, str): permissions = [permissions]

    try:
        identity = {'username': user['username'], '_id': str(user['_id']), 'permissions': permissions}
        access_token, refresh_token = LoginRouteHandler.update_stored_token(identity)
    except Exception:
        return JsonError("Failed to create session, please try again", 500)

    response = JsonResponse({
        '_id': str(user['_id']),
        'permissions': permissions,
        'session_expires': datetime.now() + timedelta(seconds=int(JWT_Settings.APP_JWT_LIFESPAN))
    })

    try:
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
    except Exception:
        return JsonError("Failed to set session cookies, please try again", 500)

    return response