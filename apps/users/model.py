from apps import db
from flask_restful import fields
import re


class Users(db.Model):
    """Class for storing information about users table

    Attributes:
        __tablename__: a string of table name
        id: an integer of user's id
        name: a string of user's name
        email: a string of user's email
        phone_number: a string of user's phone_number
        password: a string of user's password
        role: a boolean that indicates user role. True for admin and False for user
        created_at: a datetime that indicates when the account created
        updated_at: a datetime that indicates when the account last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    phone_number = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'phone_number': fields.String,
        'role': fields.Integer
    }

    login_response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'phone_number': fields.String,
        'password': fields.String,
        'role': fields.Integer
    }

    def __init__(self, name, email, phone_number, password, role):
        """Inits Users with data that user inputted

        The data already validated on the resources function

        Args:
            name: a string of user's name
            email: a string of user's email
            phone_number: a string of user's phone_number
            password: a string of user's password
            role: a boolean that indicates user role. True for admin and False for user
        """
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.role = role

    def isEmailAddressValid(self, email):
        """Validate the email address using a regex."""
        if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return False
        return True

    def isPhoneNumberValid(self, phone_number):
        """Validate the mobile phone using a regex."""
        if not re.match("^0[0-9]{9,}$", phone_number):
            return False
        return True

    @classmethod
    def isEmailExist(cls, email):
        """Check whether email already listed in database"""
        all_data = cls.query.all()

        # Make a list of email listed in database

        existing_email = [item.email for item in all_data]

        if email in existing_email:
            return True

        return False

    @classmethod
    def isPhoneNumberExist(cls, phone_number):
        """Check whether mobile number already listed in database"""
        all_data = cls.query.all()

        # Make a list of email listed in database

        existing_phone_number = [item.phone_number for item in all_data]

        if phone_number in existing_phone_number:
            return True

        return False
