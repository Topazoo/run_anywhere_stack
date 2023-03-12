# Clients
from dead_simple_framework.database import Database
from ..route_clients import GmailClient

# Utils
from uuid import uuid4
from dead_simple_framework.api import JsonResponse, JsonError
from datetime import datetime
import os

# Typing
from pymongo.collection import Collection
from flask import Request


def POST(request:Request, payload:dict, collection:Collection):
    ''' Send a password reset email. Link expires after 5 mins '''

    # Generate a reset token
    reset_token = str(uuid4())

    collection.insert_one({
        "username": payload["username"],
        "reset_token": reset_token,
        "created_on": datetime.now()
    })

    with Database(collection='users') as users_db:
        user = dict(users_db.find_one({"username": payload["username"]}) or {})

    if user:
        GmailClient().send_email(
            recipient_email_address=user['email_address'],
            subject="Application Password Reset",
            template_name="password_reset",
            template_values= {
                "name": user['first_name'],
                "username": payload["username"],
                "domain": os.environ.get('APP_DOMAIN'),
                "reset_token": reset_token
            }
        )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False}, 404)


def GET(request:Request, payload:dict, collection:Collection):
    ''' Checks if a password reset token for a user is valid '''

    if collection.count_documents({
        "username": payload["username"],
        "reset_token": payload["reset_token"]
    }) > 0:
        return JsonResponse({'valid': True})

    return JsonResponse({'valid': False}, 404)


def PUT(request:Request, payload:dict, collection:Collection):
    ''' Change a user's password '''

    # If the link is still valid
    if GET(request, payload, collection).status == "200 OK":
        with Database(collection='users') as users_db:
            # Set the new password
            users_db.update_one(
                {'username': payload["username"]}, {'$set': {
                    "password": payload.get('password')
                }}
            )

            # Delete the reset token
            collection.delete_one({
                "username": payload["username"],
                "reset_token": payload["reset_token"]
            })

            return JsonResponse({'success': True})
    else:
        return JsonError("No valid reset token found!", 404) 
