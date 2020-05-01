from apps import db
from flask_restful import fields


class OrderDetails(db.Model):
    """Class for storing information about informations of order detail table

    Attributes:
        __tablename__: a string of table name
        id: an integer of order's id
        order_id: an integer of user's id.
        service_id: an integer of service's id.
        provider_id: an integer of provider's id.
        coupon_id: an integer of coupon's id.
        date: a string that shows the date that order will be held.
        time_start: an integer that indicates the time of the order start.
        time_end: an integer that indicates the time of the order end.
        address: a string that shows order address.
        status: an integer that indicate the status of order (like: ordered, paid, done, etc).
        price: an integer that shows the price of the order detail.
        transport_price: an integer that shows the transport price of the order detail.
        total_price_after_discount: an integer that shows the total price after discount of the order detail.
        info: a string that indicate any info of order detail.
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "order_details"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable = False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable = False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable = False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable = True)
    date = db.Column(db.String(30), nullable=False)
    time_start = db.Column(db.String(30), nullable=False)
    time_end = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    transport_price = db.Column(db.Integer, nullable=False)
    total_price_after_discount = db.Column(db.Integer, nullable=False)
    info = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'service_id': fields.Integer,
        'provider_id': fields.Integer,
        'coupon_id': fields.Integer,
        'date': fields.String,
        'time_start': fields.String,
        'time_end': fields.String,
        'address': fields.String,
        'status': fields.Integer,
        'price': fields.Integer,
        'transport_price': fields.Integer,
        'total_price_after_discount': fields.Integer,
        'info': fields.String,
    }

    def __init__(self, data):
        """Inits Order Details with data that user inputted

        The data already validated on the resources function

        Args:
                order_id: an integer of user's id.
                service_id: an integer of service's id.
                provider_id: an integer of provider's id.
                coupon_id: an integer of coupon's id.
                date: a string that shows the date that order will be held.
                time_start: an integer that indicates the time of the order start.
                time_end: an integer that indicates the time of the order end.
                address: a string that shows order address.
                status: an integer that indicate the status of order (like: ordered, paid, done, etc).
                price: an integer that shows the price of the order detail.
                transport_price: an integer that shows the transport price of the order detail.
                total_price_after_discount: an integer that shows the total price after discount of the order detail.
                info: a string that indicate any info of order detail.
        """
        self.user_id = data['user_id']
        self.service_id = data['service_id']
        self.provider_id = data['provider_id']
        self.coupon_id = data['coupon_id']
        self.date = data['date']
        self.time_start = data['time_start']
        self.time_end = data['time_end']
        self.address = data['address']
        self.status = data['status']
        self.price = data['price']
        self.transport_price = data['transport_price']
        self.total_price_after_discount = data['total_price_after_discount']
        self.info = data['info']
