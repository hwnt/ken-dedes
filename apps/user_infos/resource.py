from flask import Blueprint, Response, json
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import UserInfos
from apps.users.model import Users
from apps import app, db, adminRequired, nonAdminRequired, jwtRequired
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..commons import cors_value, cors_status, content_type_json

bp_user_infos = Blueprint('user_infos', __name__)
api = Api(bp_user_infos)


class UserInfosResource(Resource):
    """Class for storing HTTP request method for users table that can be accessed by user"""

    def __init__(self):
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    @jwtRequired
    def post(self):
        """Post new data to user_infos table.

        Retrieve data from user input located in JSON, validate the data, then post the data to users tables.

        Args (located in JSON):
                id: an integer of user's id
                address: a string of user's address.
                photo: a string of URL of user's profile photo.
                birthdate: a string that indicate the user birthdate.
                weight: an integer that explain the user's weight in kg(s).
                height: an integer that explain the user's height in cm(s).

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "id": 1,
                "address": "Banyumas",
                "photo": "https://blabla.com",
                "birthdate": "24051998",
                "weight": 50,
                "height": 60
            }

        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid (email and mobile phone inputted is wrong formatted)        
        """

        parser = reqparse.RequestParser()
        parser.add_argument('address', location='json', required=False)
        parser.add_argument('photo', location='json', required=False)
        parser.add_argument('birthdate', location='json', required=False)
        parser.add_argument('weight', location='json', required=False)
        parser.add_argument('height', location='json', required=False)
        args = parser.parse_args()

        claims = get_jwt_claims()

        new_user_infos = {
            'id': claims['id'],
            'address': args['address'],
            'photo': args['photo'],
            'birthdate': args['birthdate'],
            'weight': args['weight'],
            'height': args['height'],
        }

        user_info = UserInfos(new_user_infos)

        # Save in DB
        db.session.add(user_info)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user_info)

        return marshal(user_info, UserInfos.response_fields), 200, content_type_json

    @jwtRequired
    def get(self):
        """ Gets category by id from providers  table
        Returns:
            A dict consist of providers data.

            For example:
            {
                "id": 1,
                "address": "Banyumas",
                "photo": "https://blabla.com",
                "birthdate": "24051998",
                "weight": 50,
                "height": 60
            }

        """
        claims = get_jwt_claims()
        user_info = UserInfos.query.get(claims['id'])

        if user_info is not None:
            return marshal(user_info, UserInfos.response_fields), 200, content_type_json

        return {'status':'NOT_FOUND'}, 400, content_type_json

    @jwtRequired
    def put(self):
        """ Edits informations from a single record in user infos table specified by id 
        Args:
                id: an integer of user's id
                address: a string of user's address.
                photo: a string of URL of user's profile photo.
                birthdate: a string that indicate the user birthdate.
                weight: an integer that explain the user's weight in kg(s).
                height: an integer that explain the user's height in cm(s).

        Returns:
            A dictionary that contains the updated data from the record edited. For example:
            
            {
                "id": 1,
                "address": "Banyumas",
                "photo": "https://blabla.com",
                "birthdate": "24051998",
                "weight": 50,
                "height": 60
            }

            Not Found(404): An error occured when the id inputted is not found in the table
            Bad Request(400): An error occured when the data inputted is null
        """
        parser = reqparse.RequestParser()
        parser.add_argument('address', location='json', required=False)
        parser.add_argument('photo', location='json', required=False)
        parser.add_argument('birthdate', location='json', required=False)
        parser.add_argument('weight', location='json', required=False)
        parser.add_argument('height', location='json', required=False)
        args = parser.parse_args()

        claims = get_jwt_claims()

        user_info = UserInfos.query.get(claims['id'])

        if user_info is None:
            return {'status': 'NOT_FOUND'}, 400, {'Content_Type': 'application/json'}

        if args['address'] is not None:
            user_info.address = args['address']

        if args['photo'] is not None:
            user_info.photo = args['photo']

        if args['birthdate'] is not None:
            user_info.birthdate = args['birthdate']

        if args['weight'] is not None:
            user_info.weight = args['weight'].title()

        if args['height'] is not None:
            user_info.height = args['height']

        db.session.commit()

        return marshal(user_info, UserInfos.response_fields), 200, {'Content_Type': 'application/json'}

api.add_resource(UserInfosResource, '', '/<id>')
