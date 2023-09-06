
from functools import wraps
import json
from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from flask import request
import requests

from src.tokens_and_roles import get_access_token, get_roles
from src.models import advisors


class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        issuer = "https://dev-d6pchdbvs0cq84vq.us.auth0.com/"
        jsonurl = urlopen("https://dev-d6pchdbvs0cq84vq.us.auth0.com/.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }

def authenticate_user_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = request.headers['user']
            advisor = advisors.query.get(user_id)
            id = advisor.login_id
            user_roles = get_roles(id)
            for user_role in user_roles.json():
                if role in user_role['name'] :
                    return func(*args, **kwargs)
            return "Invalid role"
        return wrapper
    return decorator