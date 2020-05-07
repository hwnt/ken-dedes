from flask import Blueprint, Response, json
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Providers
from apps.users.model import Users
from apps import app, db, adminRequired, nonAdminRequired, jwtRequired
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..commons import cors_value, cors_status, content_type_json

bp_providers = Blueprint('providers', __name__)
api = Api(bp_providers)


class ProvidersResource(Resource):
    """Class for storing HTTP request method for users table that can be accessed by user"""

    def __init__(self):
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    # @adminRequired
    def post(self):
        """Post new data to providers table.

        Retrieve data from user input located in JSON, validate the data, then post the data to users tables.

        Args (located in JSON):
            user_id: a string of provider's user id
            name: a string of provider's name
            birthday: a date of provider's birthday
            experience: a string of provider's experience year
            almamater: a string of provider's almamater.
            details: a string that explain details.
            role: a string that indicates user role. such as: doctor, midwife, etc.
            permit_number: a string that shows the provider's legality of permission.

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "id": 1,
                "user_id": 3,
                "name": "Ratna Sarumpaet",
                "birthday": "23041993",
                "experience": "1 Year",
                "almamater": "Universitas Brawijaya",
                "details": "-",
                "role": "midwife",
                "permit_number": "123-456-789",
            }

        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid (email and mobile phone inputted is wrong formatted)        
        """

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json', required=False)
        parser.add_argument('name', location='json', required=False)
        parser.add_argument('birthday', location='json', required=False)
        parser.add_argument('experience', location='json', required=False)
        parser.add_argument('almamater', location='json', required=False)
        parser.add_argument('details', location='json', required=False)
        parser.add_argument('role', location='json', required=False)
        parser.add_argument('permit_number', location='json', required=False)
        args = parser.parse_args()

        new_provider = {
            'user_id': args['user_id'],
            'name': args['name'].title(),
            'birthday': args['birthday'],
            'experience': args['experience'],
            'almamater': args['almamater'].title(),
            'details': args['details'],
            'role': args['role'],
            'permit_number': args['permit_number'],
        }

        provider = Providers(new_provider)

        # Check the Role of User
        user = Users.query.get(args['user_id'])
        if user.role != 1:
            return {'msg': 'Sorry this user ROLE is not eligible to be registered as Provider'}, 400, content_type_json

        app.logger.debug(new_provider)

        # Save in DB
        db.session.add(provider)
        db.session.commit()

        app.logger.debug('DEBUG : %s', provider)

        return marshal(provider, Providers.response_fields), 200, content_type_json

    # @jwt_required
    def get(self, id):
        """ Gets category by id from providers  table
        Returns:
            A dict consist of providers data.

            For example:
            {
                "id": 1,
                "user_id": 3,
                "name": "Ratna Sarumpaet",
                "birthday": "23041993",
                "experience": "1 Year",
                "almamater": "Universitas Brawijaya",
                "details": "-",
                "role": "midwife",
                "permit_number": "123-456-789",
            }

        """
        provider = Providers.query.get(id)

        return marshal(provider, Providers.response_fields), 200, {'Content_Type': 'application/json'}

    # @adminRequired
    def put(self, id):
        """ Edits informations from a single record in providers table specified by id 
        Args:
            name: a string of provider's name
            birthday: a string of provider's birthday
            experience: a string of provider's experience year/
            almamater: a string of provider's almamater.
            details: a string that explain details.
            role: a string that indicates user role. such as: doctor, midwife, etc.
            permit_number: a string that shows the provider's legality of permission.

        Returns:
            A dictionary that contains the updated data from the record edited. For example:
            
            {
                "id": 1,
                "user_id": 3,
                "name": "Ratna Sarumpaet",
                "birthday": "23041993",
                "experience": "1 Year",
                "almamater": "Universitas Brawijaya",
                "details": "-",
                "role": "midwife",
                "permit_number": "123-456-789",
            }

            Not Found(404): An error occured when the id inputted is not found in the table
            Bad Request(400): An error occured when the data inputted is null
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=False)
        parser.add_argument('birthday', location='json', required=False)
        parser.add_argument('experience', location='json', required=False)
        parser.add_argument('almamater', location='json', required=False)
        parser.add_argument('details', location='json', required=False)
        parser.add_argument('role', location='json', required=False)
        parser.add_argument('permit_number', location='json', required=False)
        args = parser.parse_args()

        provider = Providers.query.get(id)
        # admin = get_jwt_claims()

        if provider is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        if args['name'] is not None:
            provider.name = args['name'].title()

        if args['birthday'] is not None:
            provider.birthday = args['birthday']

        if args['experience'] is not None:
            provider.experience = args['experience']

        if args['almamater'] is not None:
            provider.almamater = args['almamater'].title()

        if args['details'] is not None:
            provider.details = args['details']

        if args['role'] is not None:
            provider.role = args['role']

        if args['permit_number'] is not None:
            provider.permit_number = args['permit_number']


        db.session.commit()

        return marshal(provider, Providers.response_fields), 200, {'Content_Type': 'application/json'}

    # @adminRequired
    def delete(self, id):
        """Hard delete a single record from categories table 
        Args (located in function's parameter): 
            id: An integer of provider's id which want to be deleted
        Returns:
            A dictionary of key 'status' which have value of sucess message. For example:
            {"Status": "The data with id 3 is deleted"}
        Raise:
            Not Found(404): An error occured when the id inputted is not found in the table
        """
        provider = Providers.query.get(id)
        # admin = get_jwt_claims()
        if provider is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        db.session.delete(provider)
        db.session.commit()
        return {"Status": "The data with id {} is deleted".format(id)}, 200, {'Content_Type': 'application/json'}


class ProvidersList(Resource):
    """Class for storing HTTP request method for users tabel, accessed by admin"""

    def __init__(self):
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    def get(self):
        """Get all category's data from categories table

            Returns : An array of dictionary contains all data from users. Example :
            [
                {   
                    "id" : 1,
                    "name": "Pijat Bayi",
                    "details": "Pijat Bayi untuk Umur 2 Tahun",
                },
                {
                    "id": 2,
                    "name": "Baby Spa",
                    "details": "",
                }
            ]

            Raise:
              Forbidden(403): An error occured when standard user try to access this method.  
        """
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', choices=('id'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Providers.query

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Providers.id)) 
                else:
                    qry = qry.order_by((Providers.id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Providers.response_fields))

        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(ProvidersResource, '', '/<id>')
api.add_resource(ProvidersList, '/list')
