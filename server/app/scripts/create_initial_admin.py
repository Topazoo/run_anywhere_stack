#!/usr/bin/env python
''' Create an initial admin user '''

# Utils
from dead_simple_framework.database import Database
from dead_simple_framework.api.utils import insert_data

# Settings
from dead_simple_framework.config import MongoDB_Settings

# Password hashing
from passlib.hash import pbkdf2_sha256 as sha256


def create_admin_user(email:str='admin@application.org', password:str='Password', name:str='Peter Swanson'):
    ''' Create an initial admin user with the passed email + password + name'''

    # Invoke settings
    MongoDB_Settings()

    # Insert user
    with Database(collection='users') as users_db:
        inserted_id = insert_data({
            "email_address": email,
            "username": email,
            "password": sha256.hash(password),
            "name": name,
            "permissions": ["ADMIN"],
        }, users_db)

    # Print confirmation
    print(f'Admin user created :) | ID: [{inserted_id}]')

if __name__ == "__main__":
    create_admin_user()
