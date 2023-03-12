# Settings
from dead_simple_framework.config import JWT_Settings

# Utils
from passlib.hash import pbkdf2_sha256 as sha256

def verifier(method, payload, identity):
    ''' Ensure passwords are hashed '''

    if 'password' in payload: payload['password'] = sha256.hash(payload.get('password'))

    return True
