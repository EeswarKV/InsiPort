from src.models import advisors, customers
from src.tokens_and_roles import get_roles

def get_user_details(user_roles, id):
    user_info = {}
    for user_role in user_roles.json():
        if "Fund_Manager" in user_role['name'] :
            advisor = advisors.query.filter_by(login_id = id).first()
            user_info = {
                'id' : advisor.id,
                'name': advisor.name,
                'email': advisor.email,
                'age': advisor.age,
                'phone_number': advisor.phone_number,
                'role': 'Fund_Manager'
            }
        elif "Customer" in user_role['name'] :
            customer = customers.query.filter_by(login_id = id).first()
            user_info = {
                'id' : customer.id,
                'advisor_id' : customer.advisor_id,
                'name': customer.name,
                'email': customer.email,
                'age': customer.age,
                'phone_number': customer.phone_number,
                'role': 'customer'
            }
    return user_info

def get_general_settings(id):
    user_roles = get_roles(id)
    response = get_user_details(user_roles, id)
    return response
