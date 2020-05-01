from apps import db
from flask_restful import fields


class Coupons(db.Model):
    """Class for storing information about informations of coupon table

    Attributes:
        __tablename__: a string of table name
        id: an integer of coupon's id
        name: a string that indicate of the coupon name.
        rate: an integer that indicates the rate of the discount.
        type: a string that indicates the type of coupon (percentage or nominal).
        expired_date: a string that indicates the expired date of coupon.
        active_status: an integer that indicate the status of coupon.
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "coupons"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=True)
    rate = db.Column(db.Integer, nullable=True)
    type = db.Column(db.String(30), nullable=False)
    expired_date = db.Column(db.String(30), nullable=False)
    active_status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'rate': fields.Integer,
        'type': fields.String,
        'expired_date': fields.String,
        'active_status': fields.Boolean,
    }

    def __init__(self, data):
        """Inits Coupons with data that user inputted

        The data already validated on the resources function

        Args:
                name: a string that indicate of the coupon name.
                rate: an integer that indicates the rate of the discount.
                type: a string that indicates the type of coupon (percentage or nominal).
                expired_date: a string that indicates the expired date of coupon.
                active_status: an integer that indicate the status of coupon.
        """
        self.name = data['name']
        self.rate = data['rate']
        self.type = data['type']
        self.expired_date = data['expired_date']
        self.active_status = data['active_status']
