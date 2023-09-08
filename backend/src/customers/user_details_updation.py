import json

from flask import jsonify
import requests
from src.exception import InvalidCustomerData
from src.models import customers, db
from src.tokens_and_roles import get_access_token


def update_user_details(user_details):
    user_id = user_details.get('user_id')
    user = customers.query.get(user_id)
    if user is None:
        return jsonify({"message": "User does not exists"}), 403
    
    url = "https://dev-d6pchdbvs0cq84vq.us.auth0.com/api/v2/users/{user.login_id}"
    access_token = get_access_token()
    payload = json.dumps({
        "email": user_details.get('email'),
        "name": user_details.get('name')
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization":f"Bearer {access_token}"
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    if (response.json()['statusCode'] != 200) :
        raise InvalidCustomerData(response.json()['message'], status_code = response.json()['statusCode'])
    
    #update local database
    user.email = user_details.get('email')
    user.name = user_details.get('name')
    user.phone_number = user_details.get('phone_number')
    db.session.commit()