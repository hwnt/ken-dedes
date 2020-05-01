from flask import Blueprint, Response, json
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Categories
from apps import app, db, adminRequired, nonAdminRequired
from flask_jwt_extended import jwt_required, get_jwt_claims
from ..commons import cors_value, cors_status, content_type_json

bp_categories = Blueprint('categories', __name__)
api = Api(bp_categories)


class CategoriesResource(Resource):
    """Class for storing HTTP request method for users table that can be accessed by user"""

    def __init__(self):
        pass

    def options(self, id=None):
        """Flask-CORS function to make Flask allowing our apps to support cross origin resource sharing (CORS)"""
        return cors_value, cors_status

    def post(self):
        """Post new data to categories table.

        Retrieve data from user input located in JSON, validate the data, then post the data to users tables.

        Args (located in JSON):
            name: a string of a name.
            details: a string that explain details.

        Returns:
            A dict mapping keys to the corresponding value, for example:

            {
                "id": 1,
                "name": "Pijat Bayi",
                "details": "Pijat Bayi untuk Umur 2 Tahun",
            }

        Raises: 
            Bad Request (400): An error that occured when some of the field is missing, or if the data is not valid (email and mobile phone inputted is wrong formatted)        
        """

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('details', location='json', required=False)
        args = parser.parse_args()

        new_category = {
            'name': args['name'],
            'details': args['details'],
        }
        category = Categories(new_category)
        db.session.add(category)
        db.session.commit()

        app.logger.debug('DEBUG : %s', category)

        return marshal(category, Categories.response_fields), 200, content_type_json


class CategoriesList(Resource):
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

        qry = Categories.query

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Categories.id)) 
                else:
                    qry = qry.order_by((Categories.id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Categories.response_fields))

        return rows, 200, {'Content-Type': 'application/json'}

api.add_resource(CategoriesResource, '', '/<id>')
api.add_resource(CategoriesList, '/list')
