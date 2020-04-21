from apps import db
from flask_restful import fields


class UserInfos(db.Model):
    """Class for storing information about informations of user infos table

    Attributes:
        __tablename__: a string of table name
        id: an integer of user's id
        address: a string of user's address.
        photo: a string of URL of user's profile photo.
        birthdate: a string that indicate the user birthdate.
        weight: an integer that explain the user's weight in kg(s).
        height: an integer that explain the user's height in cm(s).
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "user_infos"
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=True)
    address = db.Column(db.String(100), nullable = True)
    photo = db.Column(db.String(100), nullable = False)
    birthdate = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'address': fields.String,
        'photo': fields.String,
        'birthdate': fields.String,
        'weight': fields.Integer,
        'height': fields.Integer,
    }

    def __init__(self, data):
        """Inits Users with data that user inputted

        The data already validated on the resources function

        Args:
                id: an integer of user's id
                address: a string of user's address.
                photo: a string of URL of user's profile photo.
                birthdate: a string that indicate the user birthdate.
                weight: an integer that explain the user's weight in kg(s).
                height: an integer that explain the user's height in cm(s).
        """
        self.id = data['id']
        self.address = data['address']
        self.photo = data['photo']
        self.birthdate = data['birthdate']
        self.weight = data['weight']
        self.height = data['height']
