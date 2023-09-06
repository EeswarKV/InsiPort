
from flask import json
import requests
from src.tokens_and_roles import get_access_token
from src.models import advisors, customers, db


def new_customer_creation(customer_info, advisor_id):
    customer_id = create_customer_id(customer_info)
    assign_customer_role(customer_id)
    response = create_customer_in_local_db(customer_info, customer_id, advisor_id)
    return response

def create_customer_id(customer_info):
    url = "https://dev-d6pchdbvs0cq84vq.us.auth0.com/api/v2/users"
    access_token = get_access_token()
    payload = json.dumps({
        "email": customer_info.get('email'),
        "blocked": False,
        "email_verified": False,
        "given_name": customer_info.get('given_name'),
        "family_name": customer_info.get('family_name'),
        "name": customer_info.get('name'),
        "nickname": customer_info.get('nickname'),
        "connection": "Username-Password-Authentication",
        "password": customer_info.get('password'),
        "verify_email": False,
        "username": customer_info.get('username')
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization":f"Bearer {access_token}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    user_id = response.json()['user_id']
    return user_id

def assign_customer_role(user_id):
    url = f"https://dev-d6pchdbvs0cq84vq.us.auth0.com/api/v2/roles/rol_8z06qPwi66JC5Kk2/users"
    access_token = get_access_token()
    payload = json.dumps({
        "users": [
            user_id
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        "Authorization":f"Bearer {access_token}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def create_customer_in_local_db(customer_info, customer_id, advisor_id):

    customer = customers(login_id = customer_id, advisor_id = advisor_id, 
                         name = customer_info.get('name'), email = customer_info.get('email'), 
                         age = customer_info.get('age'), phone_number = customer_info.get('phone_number'))
    db.session.add(customer)
    db.session.commit()
    return "Record added sucessfully"

def add_advisor_data(advisor_id):
    advisor = advisors(login_id = advisor_id, name = 'Eshwar', email = 'eshwar4299@gmail.com', age = 34, phone_number = 9441553934)
    db.session.add(advisor)
    db.session.commit()

    
