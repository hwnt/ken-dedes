from apps import db
from flask_restful import fields


class Orders(db.Model):
    """Class for storing information about informations of order table

    Attributes:
        __tablename__: a string of table name
        id: an integer of order's id
        user_id: an integer of user's id.
        total_price: an integer that shows the total price of an order.
        address: a string that shows order address.
        status: an integer that indicate the status of order (like: ordered, paid, done, etc).
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    total_price = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'total_price': fields.Integer,
        'address': fields.String,
        'status': fields.Integer,
    }

    def __init__(self, data):
        """Inits Orders with data that user inputted

        The data already validated on the resources function

        Args:
                user_id: an integer of user's id.
                total_price: an integer that shows the total price of an order.
                address: a string that shows order address.
                status: an integer that indicate the status of order (like: ordered, paid, done, etc).
        """
        self.user_id = data['user_id']
        self.total_price = data['total_price']
        self.address = data['address']
        self.status = data['status']
