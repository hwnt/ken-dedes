from flask import Blueprint, Response, json
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import UserConditions
from apps import app, db, adminRequired, nonAdminRequired, jwtRequired
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..commons import cors_value, cors_status, content_type_json

from apps.conditions.model import Conditions
from apps.users.model import Users

bp_user_conditions = Blueprint('user_conditions', __name__)
api = Api(bp_user_conditions)


class UserConditionsResource(Resource):
    """Class for storing HTTP request method for users table that can be accessed by user"""

    def __init__(self):
        pass

    def options(self):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    @jwtRequired
    def post(self):
        """Post new data to providers table.

        Retrieve data from user input located in JSON, validate the data, then post the data to users tables.

        Args (located in JSON):
            user_id: an integer of a user's id.
            user_answer: a string that explain the user answer of a condition.

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "id": 1,
                "user_id": 2,
                "condition_id": 3,
                "condition": "Apakah sudah makan",
                "condition_detail": "Makan besar",
                "user_answer": "sudah",
            }

        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid (email and mobile phone inputted is wrong formatted)        
        """

        parser = reqparse.RequestParser()
        parser.add_argument('condition_id', location='json', required=True)
        parser.add_argument('user_answer', location='json', required=True)
        args = parser.parse_args()

        # Check the condition is exist or not
        condition = Conditions.query.get(args['condition_id'])
        if condition is None:
            return {'msg': 'Condition is not found'}, 400, {'Content_Type': 'application/json'}
        
        claims = get_jwt_claims()

        new_user_condition = {
            'user_id': claims['id'],
            'condition_id': condition.id,
            'condition': condition.condition,
            'condition_details': condition.details,
            'user_answer': args['user_answer'],
        }

        app.logger.debug(new_user_condition)

        # Save in DB
        user_condition = UserConditions(new_user_condition)
        db.session.add(user_condition)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user_condition)

        return marshal(user_condition, UserConditions.response_fields), 200, content_type_json

    @jwtRequired
    def get(self):
        """ Gets category by id from services  table
        Returns:
            A dict consist of services data.

            For example:
            [
                {
                    "id": 4,
                    "user_id": 4,
                    "condition_id": 3,
                    "condition": "Yakin sudah minum berat?",
                    "condition_details": "Minum air",
                    "user_answer": "Ya belom"
                },
                {
                    "id": 2,
                    "user_id": 4,
                    "condition_id": 1,
                    "condition": "Apakah sudah makan berat kah?",
                    "condition_details": "Makan berat",
                    "user_answer": "Sudah dong"
                }
            ]

        """
        claims = get_jwt_claims()

        user_conditions = UserConditions.query.filter(UserConditions.user_id==claims['id']).order_by(desc(UserConditions.id))

        # Loop for getting the latest answer for the latest condition_id
        rows = []
        for user_condition in user_conditions:
            if not any(user_condition.condition_id == row['condition_id'] for row in rows):
                rows.append(marshal(user_condition, UserConditions.response_fields))

        return rows, 200, content_type_json

api.add_resource(UserConditionsResource, '')
