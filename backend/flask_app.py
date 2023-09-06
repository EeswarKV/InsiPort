from flask import app, Flask, request, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector
from src.general_settings import get_general_settings
from src.customers.get_customers_info import get_customers_info_under_advisor
from src.customers.delete_customer import delete_customer_information
from src.tokens_and_roles import get_access_token
from src.customers.create_customer import new_customer_creation
from src.validator import Auth0JWTBearerTokenValidator, authenticate_user_role
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
from src.models import advisors, db

app = Flask(__name__)
app.config.from_object('config.Config')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app) 

# Create the tables
with app.app_context():
    db.create_all()

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "dev-d6pchdbvs0cq84vq.us.auth0.com",
    "https://insightfullportfolios/"
)
require_auth.register_token_validator(validator)

@app.route('/general_setting', methods = ['GET'])
@require_auth()
def general_settings():
    user_id = request.headers['user']
    response = get_general_settings(user_id)
    return jsonify(response)

@app.route('/create_customer', methods = ['POST'])
@require_auth()
@authenticate_user_role(role="Fund_Manager")
def create_customer():
    customer_info = request.get_json()
    advisor_id = request.headers['user']
    response = new_customer_creation(customer_info, advisor_id)
    return jsonify(response)

@app.route('/customers', methods = ['GET'])
@require_auth()
@authenticate_user_role(role="Fund_Manager")
def get_customers():
    advisor_id = request.headers['user']
    response = get_customers_info_under_advisor(advisor_id);
    return jsonify(response)

@app.route('/add_stock', methods = ['POST'])
@require_auth()
@authenticate_user_role(role="Fund_Manager")
def add_stock():
    customer_info = request.get_json()
    # advisor_id = request.headers['user']
    print("Hellooo",request.get_json().get('exchange'))
    # response = get_customers_info_under_advisor(advisor_id);
    return jsonify(customer_info)

@app.route('/delete_customer', methods = ['DELETE'])
@require_auth()
@authenticate_user_role(role="Fund_Manager")
def delete_customer():
    customer_id = request.headers['Customer']
    response = delete_customer_information(customer_id)
    return jsonify(response)

@app.route('/add_advisor', methods = ['POST'])
@require_auth()
def add_advisor():
    advisorDetails = advisors.query.filter_by(login_id = request.get_json().get('id')).first()

    if advisorDetails is None :
        advisor = advisors(login_id = request.get_json().get('id'), 
                        name = request.get_json().get('name'), 
                        email = request.get_json().get('email'), 
                        age = request.get_json().get('age'), 
                        phone_number = request.get_json().get('phone_number'))
        db.session.add(advisor)
        db.session.commit()
    response = advisors.query.filter_by(login_id = request.get_json().get('id')).first()
    return jsonify(response.id)

if __name__ == "__main__":
    app.run(port=8000)