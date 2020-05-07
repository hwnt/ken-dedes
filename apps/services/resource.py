from flask import Blueprint, Response, json
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Services
from apps import app, db, adminRequired, nonAdminRequired, jwtRequired
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..commons import cors_value, cors_status, content_type_json

from apps.providers.model import Providers
from apps.categories.model import Categories

bp_services = Blueprint('services', __name__)
api = Api(bp_services)


class ServicesResource(Resource):
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
            provider_id: an integer of a provider's id.
            category_id: an integer that category's id.
            price: an integer that shows the price of a service.
            transport_price: an integer that shows the transport price of a service.

        Returns:
            A dict mapping keys to the corresponding value, for example:

        {
            "id": 1,
            "provider_id": 1,
            "category_id": 1,
            "price": 50000,
            "transport_price": 20000,
        }

        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid (email and mobile phone inputted is wrong formatted)        
        """

        parser = reqparse.RequestParser()
        parser.add_argument('provider_id', location='json', required=True)
        parser.add_argument('category_id', location='json', required=True)
        parser.add_argument('price', location='json', required=True)
        parser.add_argument('transport_price', location='json', required=True)
        args = parser.parse_args()

        new_service = {
            'provider_id': args['provider_id'],
            'category_id': args['category_id'],
            'price': args['price'],
            'transport_price': args['transport_price'],
        }

        # Check the provider is exist or not
        provider = Providers.query.get(args['provider_id'])
        if provider is None:
            return {'msg': 'Provider is not found'}, 400, {'Content_Type': 'application/json'}

        # Check the category is exist or not
        provider = Categories.query.get(args['category_id'])
        if provider is None:
            return {'msg': 'Category is not found'}, 400, {'Content_Type': 'application/json'}

        app.logger.debug(new_service)

        # Save in DB
        service = Services(new_service)
        db.session.add(service)
        db.session.commit()

        app.logger.debug('DEBUG : %s', service)

        return marshal(service, Services.response_fields), 200, content_type_json

    # @jwt_required
    def get(self, id):
        """ Gets category by id from services  table
        Returns:
            A dict consist of services data.

            For example:
            {
                "id": 1,
                "provider_id": 1,
                "category_id": 1,
                "price": 50000,
                "transport_price": 20000,
            }

        """
        service = Services.query.get(id)

        return marshal(service, Services.response_fields), 200, {'Content_Type': 'application/json'}

    # @adminRequired
    def put(self, id):
        """ Edits informations from a single record in services table specified by id 
        Args:
            provider_id: an integer of a provider's id.
            category_id: an integer that category's id.
            price: an integer that shows the price of a service.
            transport_price: an integer that shows the transport price of a service.

        Returns:
            A dictionary that contains the updated data from the record edited. For example:
            
            {
                "id": 1,
                "provider_id": 1,
                "category_id": 1,
                "price": 50000,
                "transport_price": 20000,
            }

            Not Found(404): An error occured when the id inputted is not found in the table
            Bad Request(400): An error occured when the data inputted is null
        """
        parser = reqparse.RequestParser()
        parser.add_argument('provider_id', location='json', required=False)
        parser.add_argument('category_id', location='json', required=False)
        parser.add_argument('price', location='json', required=False)
        parser.add_argument('transport_price', location='json', required=False)

        args = parser.parse_args()

        service = Services.query.get(id)
        # admin = get_jwt_claims()

        if service is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        if args['provider_id'] is not None:
            service.provider_id = args['provider_id']

        if args['category_id'] is not None:
            service.category_id = args['category_id']

        if args['price'] is not None:
            service.price = args['price']

        if args['transport_price'] is not None:
            service.transport_price = args['transport_price'].title()

        db.session.commit()

        return marshal(service, Services.response_fields), 200, {'Content_Type': 'application/json'}

    # @adminRequired
    def delete(self, id):
        """Hard delete a single record from services table 
        Args (located in function's parameter): 
            id: An integer of provider's id which want to be deleted
        Returns:
            A dictionary of key 'status' which have value of sucess message. For example:
            {"Status": "The data with id 3 is deleted"}
        Raise:
            Not Found(404): An error occured when the id inputted is not found in the table
        """
        service = Services.query.get(id)
        # admin = get_jwt_claims()
        if service is None:
            return {'status': 'Not Found'}, 404, {'Content_Type': 'application/json'}

        db.session.delete(service)
        db.session.commit()
        return {"Status": "The data with id {} is deleted".format(id)}, 200, {'Content_Type': 'application/json'}


class ServicesList(Resource):
    """Class for storing HTTP request method for users tabel, accessed by admin"""

    def __init__(self):
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    def get(self):
        """Get all category's data from services table

            Returns : An array of dictionary contains all data from users. Example :
            [
                {
                    "id": 1,
                    "provider_id": 1,
                    "category_id": 1,
                    "price": 50000,
                    "transport_price": 20000,
                },
                {
                    "id": 2,
                    "provider_id": 1,
                    "category_id": 2,
                    "price": 30000,
                    "transport_price": 20000,
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

        qry = Services.query

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Services.id)) 
                else:
                    qry = qry.order_by((Services.id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Services.response_fields))

        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(ServicesResource, '', '/<id>')
api.add_resource(ServicesList, '/list')
