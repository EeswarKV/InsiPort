from flask import app, Flask, request, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector
from src.customers.user_details_updation import update_user_details
from src.exception import InvalidCustomerData, MissingUserDetails, UserRightsException
from src.general_settings import get_general_settings
from src.customers.customer_operations import delete_customer_information, get_customer_info, get_customers_info_under_advisor, new_customer_creation
from src.validator import Auth0JWTBearerTokenValidator, ValidateAddCustomerRequest, ValidateUpdateUserInfoSchema, authenticate_user_role
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

@app.errorhandler(InvalidCustomerData)
def invalid_customer_data(e):
    return jsonify(e.to_dict()), e.status_code

@app.errorhandler(UserRightsException)
def user_rights_exception(e):
    return jsonify(e.to_dict()), e.status_code

@app.errorhandler(MissingUserDetails)
def missing_user_Details(e):
    return jsonify(e.to_dict()), e.status_code

@app.route('/general_setting', methods = ['GET'])
@require_auth()
def general_settings():
    try:
        user_id = request.headers['user']
    except:
        raise MissingUserDetails("Invalid user details", status_code= 403)
    response = get_general_settings(user_id)
    return jsonify(response)

@app.route('/create_customer', methods = ['POST'])
@require_auth()
@authenticate_user_role(role="Fund_Manager")
@ValidateAddCustomerRequest()
def create_customer():
    customer_info = request.get_json()
    try:
        advisor_id = request.headers['user']
    except:
        raise MissingUserDetails("Invalid user details", status_code= 403)
    response = new_customer_creation(customer_info, advisor_id)
    return jsonify(response), 201

@app.route('/update_user', methods = ['PUT'])
@require_auth()
@ValidateUpdateUserInfoSchema()
def update_user():
    user_info = request.get_json()
    update_user_details(user_info)
    return jsonify(), 200
        
@app.route('/customers', methods = ['GET'])
@require_auth()
@authenticate_user_role(role="Fund_Manager")
def get_customers():
    try:
        advisor_id = request.headers['user']
    except:
        raise MissingUserDetails("Invalid user details", status_code= 403)
    response = get_customers_info_under_advisor(advisor_id);
    return jsonify(response)

@app.route('/customer/<id>', methods = ['GET'])
@require_auth()
def get_customer(id):
    response = get_customer_info(id);
    return jsonify(response)

@app.route('/delete_customer', methods = ['DELETE'])
@require_auth()
@authenticate_user_role(role="Fund_Manager")
def delete_customer():
    try:
        customer_id = request.headers['Customer']
    except:
        raise MissingUserDetails("Invalid customer details", status_code= 403)
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
    app.run()