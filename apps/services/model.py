from apps import db
from flask_restful import fields


class Services(db.Model):
    """Class for storing information about services table

    Attributes:
        __tablename__: a string of table name
        id: an integer of certifications of provider's id
        provider_id: an integer of a provider's id.
        category_id: an integer that category's id.
        price: an integer that shows the price of a service.
        transport_price: an integer that shows the transport price of a service.
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    price = db.Column(db.Integer, nullable=True)
    transport_price = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'provider_id': fields.Integer,
        'condition_id': fields.Integer,
        'price': fields.Integer,
        'transport_price': fields.Integer,
    }

    def __init__(self, data):
        """Inits Providers with data that user inputted

        The data already validated on the resources function

        Args:
                provider_id: an integer of a provider's id.
                category_id: an integer that category's id.
                price: an integer that shows the price of a service.
                transport_price: an integer that shows the transport price of a service.
        """
        self.provider_id = data['provider_id']
        self.category_id = data['category_id']
        self.price = data['price']
        self.transport_price = data['transport_price']
