
from functools import wraps
import json
from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from flask import jsonify, request
from src.exception import MissingUserDetails
from src.schema import AddCustomerSchema, UpdateUserInfoSchema, UpdateUserPasswordSchema

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
            try:
                user_id = request.headers['user']
            except:
                raise MissingUserDetails("Invalid user details", status_code= 403)
            advisor = advisors.query.get(user_id)
            if advisor is None:
                return jsonify({"message": "User does not exists"}), 403
            id = advisor.login_id
            user_roles = get_roles(id)
            for user_role in user_roles.json():
                if role in user_role['name'] :
                    return func(*args, **kwargs)
            return jsonify({"message": "User does not have enough rights"}), 403
        return wrapper
    return decorator

def ValidateAddCustomerRequest():
    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            add_customer = AddCustomerSchema()
            errors = add_customer.validate(request.get_json())
            print(errors)
            if errors:
                if errors['phone_number']:
                    return jsonify({"message": "Invalid phone number"}), 400
                if errors['email']:
                    return jsonify({"message": "Invalid email"}), 400
                if errors['given_name']:
                    return jsonify({"message": "Invalid given name"}), 400
                if errors['family_name']:
                    return jsonify({"message": "Invalid family name"}), 400
                if errors['nickname']:
                    return jsonify({"message": "Invalid nick name"}), 400
                if errors['username']:
                    return jsonify({"message": "Invalid user name"}), 400
                if errors['password']:
                    return jsonify({"message": "Invalid password"}), 400
                if errors['age']:
                    return jsonify({"message": "Invalid age"}), 400
            return fun(*args, **kwargs)
        return wrapper
    return decorator

def ValidateUpdateUserInfoSchema():
    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            add_customer = UpdateUserInfoSchema()
            errors = add_customer.validate(request.get_json())
            if errors:
                if errors['phone_number']:
                    return jsonify({"message": "Invalid phone number"}), 400
                if errors['email']:
                    return jsonify({"message": "Invalid email"}), 400
                if errors['name']:
                    return jsonify({"message": "Invalid name"}), 400
                if errors['user_id']:
                    return jsonify({"message": "Invalid user id"}), 400
            return fun(*args, **kwargs)
        return wrapper
    return decorator

def ValidateUpdateUserPassword():
    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            add_customer = UpdateUserPasswordSchema()
            errors = add_customer.validate(request.get_json())
            if errors:
                if errors['old_password']:
                    return jsonify({"message": "Invalid old password"}), 400
                if errors['new_password']:
                    return jsonify({"message": "Invalid new password"}), 400
                if errors['confirm_password']:
                    return jsonify({"message": "Invalid confirm password"}), 400
            if request.get_json.get['new_password'] != request.get_json.get['confirm_password']:
                return jsonify({"message": "Dosen't match new password and confirmation password"}), 400

            return fun(*args, **kwargs)
        return wrapper
    return decorator