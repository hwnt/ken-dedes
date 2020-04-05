from flask import Blueprint, Response, json
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Users
from sqlalchemy import desc
from apps import app, db, adminRequired, nonAdminRequired
from flask_jwt_extended import jwt_required, get_jwt_claims
from passlib.hash import sha256_crypt
from ..commons import cors_value, cors_status, content_type_json

bp_users = Blueprint('users', __name__)
api = Api(bp_users)


class UsersResource(Resource):
    """Class for storing HTTP request method for users table that can be accessed by user"""

    def __init__(self):
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    def post(self):
        """Post new data to users table and user attributes table

        Retrieve data from user input located in JSON, validate the data, then post the data to users tables.

        Args (located in JSON):
            name: A string of user's name
            email: A string of user's email
            phone_number: A string of user's phone_number
            password: A string of user's password

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "name": "user",
                "email": "user@mail.com",
                "phone_number": "08111111111",
            }

        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid (email and mobile phone inputted is wrong formatted)        
        """

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        # We use isEmailAddressValid function to check whether email inputted is valid or not
        users = Users(args['name'], args['email'],
                      args['phone_number'], args['password'], False)
        if not users.isEmailAddressValid(args['email']):
            return {'message': 'Invalid email format!'}, 400, content_type_json

        # We use isPhoneNumberValid function to check whether mobile number inputted is valid or not
        if not users.isPhoneNumberValid(args['phone_number']):
            return {'message': 'Invalid mobile number format!'}, 400, content_type_json

        # Check whether email is already exist in database
        check_email = users.isEmailExist(args['email'])
        if check_email is True:
            return {'message': 'Email already listed!'}, 400, content_type_json

        # Check whether phone_number is already exist in database
        check_phone_number = users.isPhoneNumberExist(args['phone_number'])
        if check_phone_number is True:
            return {'message': 'Mobile number already listed!'}, 400, content_type_json

        # Encrypt password using sha256
        password_encrypted = sha256_crypt.hash(args['password'])

        # Input data to users table
        user = Users(args['name'], args['email'],
                     args['phone_number'], password_encrypted, False)
        db.session.add(user)
        db.session.commit()

        # get user id
        user_contain = marshal(user, Users.response_fields)
        user_id = user_contain['id']

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, content_type_json

    @nonAdminRequired
    def get(self, id):
        """Get a user's detail by id. A user can not access another user's data

        Args (retrieved from function's parameter):
            id: user's id whose detail want to be shown

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "id":1,
                "name": "user",
                "email": "user@mail.com",
                "phone_number": "08111111111",
                "role": 0,
                "point": 10
                "total_trash": 10
                "onboarding_status": true
            }

        Raise :
            Forbidden(403) : Occured when user try to access another user's data
            Not Found(404) : Occured when the data is not found in the table
        """

        user = get_jwt_claims()
        user_requested = Users.query.get(id)

        if user_requested is None:
            return {'Status': 'Not Found'}, 404, content_type_json

        requested = marshal(user_requested, Users.response_fields)

        if user['id'] != requested['id']:
            return {'Warning': 'You are not allowed to access others credentials'}, 403, content_type_json

        return requested, 200, content_type_json

    @nonAdminRequired
    def put(self):
        """Edit data in users table

        Retrieve data from user input located in JSON, validate the data, then edit the data in users tables.

        Args (located in JSON):
            name: A string of user's name
            email: A string of user's email
            phone_number: A string of user's phone_number
            password: A string of user's password

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "id": 1,
                "name": "user",
                "email": "user@mail.com",
                "phone_number": "08111111111",
                "role": 0 
            }

        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid (email and mobile phone inputted is wrong formatted)        
        """

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('phone_number', location='json')
        parser.add_argument('password', location='json')
        args = parser.parse_args()

        claims = get_jwt_claims()
        user_edited = Users.query.get(claims['id'])

        users = Users("dummy", "dummy", "dummy", "dummy", False)

        # Cheks if user input a name
        if args['name'] is not None:
            user_edited.name = args['name']

        # checks email and edit it
        if args['email'] is not None:

            if not users.isEmailAddressValid(args['email']):
                return {'message': 'Invalid email format!'}, 400, content_type_json

            if user_edited.email == args['email']:
                pass
            else:
                check_email = users.isEmailExist(args['email'])
                if check_email is True:
                    return {'message': 'Email already listed!'}, 400, content_type_json

            user_edited.email = args['email']

        # checks the number phone and edit it
        if args['phone_number'] is not None:

            if not users.isPhoneNumberValid(args['phone_number']):
                return {'message': 'Invalid mobile number format!'}, 400, content_type_json

            if user_edited.phone_number == args['phone_number']:
                pass
            else:
                check_phone_number = users.isPhoneNumberExist(
                    args['phone_number'])
                if check_phone_number is True:
                    return {'message': 'Mobile number already listed!'}, 400, content_type_json

            user_edited.phone_number = args['phone_number']

        # checks if user input a new password
        if args['password'] is not None:
            password_encrypted = sha256_crypt.hash(args['password'])
            user_edited.password = password_encrypted

        db.session.commit()

        return marshal(user_edited, Users.response_fields), 200, content_type_json


class UsersForAdminResource(Resource):
    """Class for storing HTTP request method for users table that can be accessed by admin"""

    def __init__(self):
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    @adminRequired
    def get(self, id):
        """get user's data  by id

        Args (retrieved from function's parameter):
            id: An integer of user's id whose data is going to be shown.

        Returns: 
            A dict contains all profile data from a specific user. For example :
                {
                    "id" : 1,
                    "name" : "user",
                    "email" : "exp@exp.com",
                    "mobile_number" : "0898787878",
                    "role": false
                }

        Raise:
            Not Found(404): An error occured when user with id inputted is not found in the table.
        """
        # find user's data in table
        user = Users.query.get(id)

        if user is None:
            return {'Status': 'Not Found'}, 404
        user_dict = marshal(user, Users.response_fields)

        return user_dict, 200, {'Content-Type': 'application/json'}


class AllUserResource(Resource):
    """Class for storing HTTP request method for users tabel, accessed by admin"""

    def __init__(self):
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    @adminRequired
    def get(self):
        """Get all user's data from users table

            Returns : An array of dictionary contains all data from users. Example :
            [
                {
                    "id" : 1,
                    "name" : "user",
                    "email" : "exp@exp.com"
                    "phone_number" : "0898787878",
                    "role": 0
                },
                {
                    "id" : 2,
                    "name" : "user2",
                    "email" : "exp2@exp.com"
                    "phone_number" : "08298989898",
                    "role": 0
                }
            ]

            Raise:
              Forbidden(403): An error occured when standard user try to access this method.  
        """
        users = Users.query
        result = []
        for user in users:
            user = marshal(user, Users.response_fields)
            attr = UserAttributes.query.filter_by(user_id=user['id'])
            attr = marshal(attr, UserAttributes.response_fields)
            attr.pop('user_id')
            data = user.update(attr)
            result.append(user)

        return result, 200, content_type_json


api.add_resource(UsersResource, '', '/<id>')
api.add_resource(UsersForAdminResource, '/admin', '/admin/<id>')
api.add_resource(AllUserResource, '/all')
