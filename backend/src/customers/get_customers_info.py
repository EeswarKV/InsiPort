from src.models import customers

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

