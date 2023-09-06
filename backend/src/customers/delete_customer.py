
import requests
from src.tokens_and_roles import get_access_token
from src.models import customers, db


def delete_customer_information(customer_id):
    customer = customers.query.get(customer_id)
    id = customer.login_id
    url = f"https://dev-d6pchdbvs0cq84vq.us.auth0.com/api/v2/users/{id}"
    access_token = get_access_token()
    headers = {
        "Authorization":f"Bearer {access_token}"
    }
    response = requests.request("DELETE", url, headers=headers)
    
    db.session.delete(customer)
    db.session.commit()
    return("Recored sucessfully deleted")