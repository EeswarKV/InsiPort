
from flask import json, jsonify
import requests
from src.exception import InvalidCustomerData, UserRightsException
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
    if (response.json()['statusCode'] != 200) :
        raise InvalidCustomerData(response.json()['message'], status_code = response.json()['statusCode'])
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
    if (response.json()['statusCode'] != 200) :
        raise UserRightsException(response.json()['message'], status_code = response.json()['statusCode'])
    return response

def delete_customer_information(customer_id):
    customer = customers.query.get(customer_id)
    id = customer.login_id
    url = f"https://dev-d6pchdbvs0cq84vq.us.auth0.com/api/v2/users/{id}"
    access_token = get_access_token()
    headers = {
        "Authorization":f"Bearer {access_token}"
    }
    response = requests.request("DELETE", url, headers=headers)
    if (response.json()['statusCode'] != 200) :
        raise InvalidCustomerData(response.json()['message'], status_code = response.json()['statusCode'])
    
    db.session.delete(customer)
    db.session.commit()
    return("Recored sucessfully deleted")

def get_customers_info_under_advisor(advisor_id):
    customers_list = customers.query.filter_by(advisor_id = advisor_id).all()
    customers_info = []

    for customer in customers_list:
        customer_dict = {
            'id' : customer.id,
            'advisor_id' : customer.advisor_id,
            'name': customer.name,
            'email': customer.email,
            'age': customer.age,
            'phone_number': customer.phone_number
        }
        customers_info.append(customer_dict)
    return customers_info

def get_customer_info(customer_id):
    customer = customers.query.get(customer_id)

    if customer is None:
        raise InvalidCustomerData("customer details invalid", status_code = 404)

    customer_dict = {
        'id' : customer.id,
        'advisor_id' : customer.advisor_id,
        'name': customer.name,
        'email': customer.email,
        'age': customer.age,
        'phone_number': customer.phone_number
    }
    return customer_dict



def create_customer_in_local_db(customer_info, customer_id, advisor_id):

    customer = customers(login_id = customer_id, advisor_id = advisor_id, 
                         name = customer_info.get('name'), email = customer_info.get('email'), 
                         age = customer_info.get('age'), phone_number = customer_info.get('phone_number'))
    db.session.add(customer)
    db.session.commit()

    
