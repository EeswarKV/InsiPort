from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class advisors(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    login_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=True)
    phone_number = db.Column(db.Integer, unique=True, nullable=True)
    customers = db.relationship('customers', backref='advisors', lazy=True)

class customers(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    login_id = db.Column(db.String, unique=True, nullable=False)
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisors.id'), nullable=False)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=True)
    phone_number = db.Column(db.Integer, unique=True, nullable=True)

class customers_portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customers_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
